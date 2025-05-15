"""This module allows logging in to wifi.gsb.gov.tr.

This module provides functionality to authenticate with the GSB WiFi portal
through its login endpoint.
"""
#region Imports
import json
from tkinter import messagebox
import requests
from typing import Dict, Optional, Union, Tuple, Callable
from PIL import Image
#endregion


#region Status Handling
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
#endregion


#region Login Info Management
def load_login_info() -> Dict[str, str]:
    """Loads saved username and password from the JSON file.
    
    Returns:
        Dict[str, str]: Dictionary containing username and password
    """
    try:
        with open("login_info.json", "r", encoding="utf-8") as file:
            login_info: Dict[str, str] = json.load(file)
            return login_info
    except (FileNotFoundError, json.JSONDecodeError):
        return {"username": "", "password": ""}


def save_login_info(username: str, password: str, show_message: bool = True) -> bool:
    """Saves the username and password to the JSON file.
    
    Args:
        username: The username to save
        password: The password to save
        show_message: Whether to show a success message
        
    Returns:
        bool: True if credentials were saved successfully, False otherwise
    """
    if not username or not password:
        messagebox.showwarning("Warning", "Please enter both username and password!")
        return False
        
    login_info = {
        "username": username,
        "password": password
    }

    try:
        with open("login_info.json", "w", encoding="utf-8") as file:
            json.dump(login_info, file)
        if show_message:
            messagebox.showinfo("Info", "Username and password saved!")
        return True
    except IOError as e:
        error_msg = f"Could not save credentials: {e}" if show_message else "Could not save credentials"
        messagebox.showerror("Error", error_msg)
        return False
#endregion


#region WiFi Connection
def connect_to_wifi() -> Optional[requests.Response]:
    """Attempts to log in to the wifi.gsb.gov.tr portal using stored credentials.
    
    This function reads the login credentials from login_info.json and sends
    a POST request to the GSB WiFi login endpoint.
    
    Returns:
        Optional[requests.Response]: The server response if successful, None otherwise
    """
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
#endregion
