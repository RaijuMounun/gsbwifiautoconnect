"""This module allows logging in to wifi.gsb.gov.tr."""
import json
from tkinter import messagebox
import requests


def print_status(statuscode):
    """Prints the status based on the status code."""
    statuscodes = {
        200: "Success",
        302: "Redirect",
        401: "Unauthorized",
        403: "Forbidden",
        404: "Not Found",
        500: "Server Error",
        503: "Service Unavailable"
    }
    messagebox.showinfo("Info", statuscodes.get(statuscode, "Unknown Status"))


def connect_to_wifi():
    """Attempts to log in to wifi.gsb.gov.tr."""
    try:  # Read username and password from login_info.json
        with open("login_info.json", "r", encoding="utf-8") as file:
            login_info = json.load(file)
            username = login_info.get("username", "")
            password = login_info.get("password", "")
    except (FileNotFoundError, json.JSONDecodeError):
        messagebox.showerror("Error", "Login information not found or invalid.")
        return

    session = requests.Session()
    url = "https://wifi.gsb.gov.tr/login/j_spring_security_check"
    form = {
        "j_username": username,
        "j_password": password
    }

    try:
        response = session.post(url, data=form)
        print_status(response.status_code)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Connection error: {e}")


def disconnect_from_wifi():
    """Logs out from wifi.gsb.gov.tr."""
    try:
        with open("login_info.json", "r", encoding="utf-8") as file:
            login_info = json.load(file)
            username = login_info.get("username", "")
            password = login_info.get("password", "")
    except (FileNotFoundError, json.JSONDecodeError):
        messagebox.showerror("Error", "Login information not found or invalid.")
        return

    session = requests.Session()
    login_url = "https://wifi.gsb.gov.tr/login/j_spring_security_check"
    logout_url = "https://wifi.gsb.gov.tr/logout"

    try:
        form = {
            "j_username": username,
            "j_password": password
        }
        session.post(login_url, data=form)

        # Log out
        response = session.get(logout_url)
        print_status(response.status_code)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Connection error: {e}")
