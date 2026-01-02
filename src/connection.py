"""WiFi connection and portal scraping module.

This module handles authentication with the GSB WiFi captive portal
and extracts session information (quota, dates) from the dashboard HTML.
"""

import requests
from bs4 import BeautifulSoup
import urllib3

from models import SessionInfo
from config import (
    PORTAL_BASE_URL,
    LOGIN_URL,
    URL_INDEX,
    INITIAL_REQUEST_TIMEOUT,
    LOGIN_REQUEST_TIMEOUT,
    SKIP_SSL_VERIFICATION,
    LABEL_REMAINING_QUOTA,
    LABEL_TOTAL_QUOTA,
    LABEL_NEXT_REFRESH,
    LABEL_LAST_LOGIN,
)

# Suppress SSL warnings if verification is disabled
if SKIP_SSL_VERIFICATION:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# --- Custom Exceptions ---

class WifiConnectionError(Exception):
    """Base exception for WiFi connection failures."""
    pass


class AuthenticationError(WifiConnectionError):
    """Raised when login credentials are invalid."""
    pass


class NetworkTimeoutError(WifiConnectionError):
    """Raised when the server does not respond in time."""
    pass


# --- HTML Parsing ---

def _parse_dashboard(html_content: str) -> dict:
    """Extract quota and date information from the dashboard HTML.
    
    The GSB portal uses dynamically generated element IDs (JSF framework),
    so we search by label text instead. This is more fragile but necessary.
    
    Args:
        html_content: Raw HTML string from the dashboard page.
        
    Returns:
        Dictionary with keys: 'quota', 'total_quota', 'date', 'last_login'.
        Values default to "Not Found" if parsing fails.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    data = {
        "quota": "Not Found",
        "total_quota": "Not Found",
        "date": "Not Found",
        "last_login": "Not Found"
    }

    try:
        # 1. Find Remaining Quota
        quota_label = soup.find('label', string=lambda t: t and LABEL_REMAINING_QUOTA in t)
        if quota_label:
            parent_td = quota_label.find_parent('td')
            if parent_td:
                sibling_td = parent_td.find_next_sibling('td')
                if sibling_td:
                    value_label = sibling_td.find('label')
                    if value_label:
                        data["quota"] = f"{value_label.text.strip()} MB"

        # 2. Find Total Quota (New)
        total_label = soup.find('label', string=lambda t: t and LABEL_TOTAL_QUOTA in t)
        if total_label:
            parent_td = total_label.find_parent('td')
            if parent_td:
                sibling_td = parent_td.find_next_sibling('td')
                if sibling_td:
                    value_label = sibling_td.find('label')
                    if value_label:
                        data["total_quota"] = f"{value_label.text.strip()} MB"

        # 3. Find Next Refresh Date
        date_label = soup.find('label', string=lambda t: t and LABEL_NEXT_REFRESH in t)
        if date_label:
            parent_td = date_label.find_parent('td')
            if parent_td:
                sibling_td = parent_td.find_next_sibling('td')
                if sibling_td:
                    value_label = sibling_td.find('label')
                    if value_label:
                        full_date = value_label.text.strip()
                        # Extract just the date part (e.g., "01/02/2026" from "01/02/2026 00:00:00")
                        data["date"] = full_date.split(" ")[0] if " " in full_date else full_date

        # 4. Find Last Login (in page header)
        login_label = soup.find('label', string=lambda t: t and LABEL_LAST_LOGIN in t)
        if login_label:
            text = login_label.text.replace(f"{LABEL_LAST_LOGIN}:", "").strip()
            data["last_login"] = text

    except Exception as e:
        # TODO: Replace with proper logging
        print(f"Parse error: {e}")
    
    return data


# --- Main Connection Logic ---

def check_connection_status() -> SessionInfo:
    """Check if we are already connected to GSB WiFi.
    
    Attempts to access the dashboard page. If redirected to login,
    we are not connected. If we see dashboard content, we are connected.
    
    Returns:
        SessionInfo object with success=True if connected, False otherwise.
    """
    session = requests.Session()
    verify_ssl = not SKIP_SSL_VERIFICATION
    
    try:
        response = session.get(URL_INDEX, verify=verify_ssl, timeout=INITIAL_REQUEST_TIMEOUT)
        
        # If we see "Quota" or "Welcome", we are logged in
        if "Quota" in response.text or "Hoşgeldiniz" in response.text:
            parsed_data = _parse_dashboard(response.text)
            return SessionInfo(
                success=True,
                message="Already Connected",
                remaining_quota=parsed_data["quota"],
                total_quota=parsed_data["total_quota"],
                quota_renewal_date=parsed_data["date"],
                last_login=parsed_data["last_login"]
            )
        else:
            return SessionInfo(success=False, message="Not Connected")
            
    except Exception:
        return SessionInfo(success=False, message="Connection Error")


def logout() -> bool:
    """Terminate the current session.
    
    Scrapes the dashboard for the view state and submit button ID,
    then posts to trigger the logout action.
    """
    session = requests.Session()
    verify_ssl = not SKIP_SSL_VERIFICATION
    
    try:
        # 1. Get the dashboard page to find the ViewState and Button ID
        response = session.get(URL_INDEX, verify=verify_ssl, timeout=INITIAL_REQUEST_TIMEOUT)
        
        if response.status_code != 200:
            return False
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find ViewState
        view_state_input = soup.find('input', {'name': 'javax.faces.ViewState'})
        if not view_state_input:
            return False
        view_state = view_state_input.get('value')
        
        # Find Logout Button (End Session)
        # Based on HTML: <button ...>End Session</button>
        # We look for a button containing "End Session" or "Oturumu Sonlandır"
        logout_btn = soup.find('button', string=lambda t: t and ("End Session" in t or "Oturumu Sonlandır" in t))
        
        if not logout_btn:
            # Fallback: try finding by common GSB ID 'servisUpdateForm:j_idt159'
            # (This is risky as IDs change, but serves as fallback)
            logout_btn = soup.find('button', id=lambda i: i and 'j_idt159' in i)
            
        if not logout_btn:
            return False
            
        btn_name = logout_btn.get('name')
        
        # 2. Post the logout request
        post_data = {
            'javax.faces.ViewState': view_state,
            btn_name: btn_name, # The button clicked
            'servisUpdateForm': 'servisUpdateForm' # The form name
        }
        
        res = session.post(URL_INDEX, data=post_data, verify=verify_ssl, timeout=LOGIN_REQUEST_TIMEOUT)
        return res.status_code == 200

    except Exception:
        return False


def connect_to_wifi(username: str, password: str) -> SessionInfo:
    """Authenticate with the GSB WiFi portal and return session info."""
    if not username or not password:
        raise ValueError("Username and password cannot be empty.")

    session = requests.Session()
    verify_ssl = not SKIP_SSL_VERIFICATION
    
    # Step 1: Initial request
    try:
        session.get(PORTAL_BASE_URL, verify=verify_ssl, timeout=INITIAL_REQUEST_TIMEOUT)
    except Exception:
        pass

    # Step 2: Login
    form_data = {"j_username": username, "j_password": password}

    try:
        response = session.post(
            LOGIN_URL, 
            data=form_data, 
            verify=verify_ssl, 
            timeout=LOGIN_REQUEST_TIMEOUT
        )
        
        if response.status_code == 200:
            if "Quota" in response.text or "Hoşgeldiniz" in response.text:
                parsed_data = _parse_dashboard(response.text)
                return SessionInfo(
                    success=True,
                    message="Login Successful",
                    remaining_quota=parsed_data["quota"],
                    total_quota=parsed_data["total_quota"], # New field
                    quota_renewal_date=parsed_data["date"],
                    last_login=parsed_data["last_login"]
                )
            else:
                raise AuthenticationError("Login failed. Username or password may be incorrect.")
            
        elif response.status_code in (401, 403):
            raise AuthenticationError("Invalid username or password.")
        else:
            raise WifiConnectionError(f"Server error: {response.status_code}")

    except requests.exceptions.Timeout:
        raise NetworkTimeoutError("Request timed out. Are you connected to the GSB network?")
    except requests.exceptions.ConnectionError:
        raise WifiConnectionError("Cannot reach server. Check your WiFi connection.")
    except (AuthenticationError, NetworkTimeoutError, WifiConnectionError):
        raise
    except Exception as e:
        raise WifiConnectionError(f"Unexpected error: {str(e)}")