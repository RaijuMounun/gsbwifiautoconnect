"""This module allows logging in to wifi.gsb.gov.tr.

This module provides functionality to authenticate with the GSB WiFi portal
through its login endpoint.
"""
import json
from tkinter import messagebox
import requests
from typing import Dict, Optional, Union


def print_status(statuscode: int) -> None:
    """Prints a user-friendly message based on the HTTP status code.
    
    Args:
        statuscode: The HTTP status code returned by the server
        
    Returns:
        None
    """
    statuscodes: Dict[int, str] = {
        200: "Success",
        302: "Redirect",
        401: "Unauthorized",
        403: "Forbidden",
        404: "Not Found",
        500: "Server Error",
        503: "Service Unavailable"
    }
    messagebox.showinfo("Info", statuscodes.get(statuscode, f"Unknown Status: {statuscode}"))


def connect_to_wifi() -> Optional[requests.Response]:
    """Attempts to log in to the wifi.gsb.gov.tr portal using stored credentials.
    
    This function reads the login credentials from login_info.json and sends
    a POST request to the GSB WiFi login endpoint.
    
    Returns:
        Optional[requests.Response]: The server response if successful, None otherwise
    """
    # Read username and password from login_info.json
    try:
        with open("login_info.json", "r", encoding="utf-8") as file:
            login_info: Dict[str, str] = json.load(file)
            username = login_info.get("username", "")
            password = login_info.get("password", "")
            
            if not username or not password:
                messagebox.showerror("Error", "Username or password is empty")
                return None
                
    except FileNotFoundError:
        messagebox.showerror("Error", "Login information file not found")
        return None
    except json.JSONDecodeError:
        messagebox.showerror("Error", "Login information file is invalid")
        return None

    # Create session and login form data
    session = requests.Session()
    url = "https://wifi.gsb.gov.tr/login/j_spring_security_check"
    form = {
        "j_username": username,
        "j_password": password
    }

    # Send login request
    try:
        response = session.post(url, data=form, timeout=10)
        print_status(response.status_code)
        return response
    except requests.exceptions.Timeout:
        messagebox.showerror("Error", "Connection timed out")
        return None
    except requests.exceptions.ConnectionError:
        messagebox.showerror("Error", "Could not connect to server")
        return None
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Connection error: {e}")
        return None
