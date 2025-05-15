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
        200: "Başarılı",
        302: "Yönlendirme",
        401: "Yetkisiz Erişim",
        403: "Erişim Engellendi",
        404: "Sayfa Bulunamadı",
        500: "Sunucu Hatası",
        503: "Hizmet Kullanılamıyor"
    }
    messagebox.showinfo("Bilgi", statuscodes.get(statuscode, f"Bilinmeyen Durum: {statuscode}"))
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
        messagebox.showwarning("Uyarı", "Lütfen kullanıcı adını ve parolanı gir.")
        return False
        
    login_info = {
        "username": username,
        "password": password
    }

    try:
        with open("login_info.json", "w", encoding="utf-8") as file:
            json.dump(login_info, file)
        if show_message:
            messagebox.showinfo("Bilgi", "Kullanıcı adı ve parola kaydedildi.")
        return True
    except IOError as e:
        error_msg = f"Kullanıcı bilgileri kaydedilemedi: {e}" if show_message else "Kullanıcı bilgileri kaydedilemedi."
        messagebox.showerror("Hata", error_msg)
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
                messagebox.showerror("Hata", "Kullanıcı adı veya parola boş")
                return None
                
    except FileNotFoundError:
        messagebox.showerror("Hata", "Giriş bilgileri dosyası bulunamadı")
        return None
    except json.JSONDecodeError:
        messagebox.showerror("Hata", "Giriş bilgileri dosyası geçersiz")
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
        messagebox.showerror("Hata", "Bağlantı zaman aşımına uğradı")
        return None
    except requests.exceptions.ConnectionError:
        messagebox.showerror("Hata", "Sunucuya bağlanılamadı")
        return None
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Hata", f"Bağlantı hatası: {e}")
        return None
#endregion
