"""Contains the necessary classes for the user interface.

This module implements the graphical user interface for the GSB WiFi Auto Connect
application using customtkinter. It includes classes for the main window and
utility functions for resource path handling.
"""
from tkinter import messagebox
import json
import os
import sys
from abc import ABC, abstractmethod
from typing import Callable, Dict, Optional, Any, Union
from pathlib import Path
from PIL import Image
import customtkinter as ctk
import requests


class WindowBase(ABC):
    """Base abstract class for all windows in the application.
    
    This class defines the interface that all window classes must implement.
    """

    @abstractmethod
    def run(self) -> None:
        """Starts the window main loop."""
        pass

    @abstractmethod
    def destroy(self) -> None:
        """Closes the window and releases resources."""
        pass


class WindowMain(WindowBase):
    """Creates the main application window with WiFi login functionality.
    
    This class implements the main user interface with login fields and 
    a connect button for authenticating with the GSB WiFi portal.
    """

    def __init__(self, connect_callback: Callable[[], Optional[requests.Response]]):
        """Initializes the main window with the given connection callback.
        
        Args:
            connect_callback: Function to call when attempting to connect to WiFi
        """
        self.root = ctk.CTk()
        self.root.title("GSB Wifi Auto Connect")
        self.root.geometry("400x500")

        self.connect_callback = connect_callback
        
        self.image_connect_button_path = resource_path("icons/disconnected.png")
        
        self.setup_ui()
        self.load_login_info()

    def setup_ui(self) -> None:
        """Sets up the user interface components and layout."""
        # Frame for login credentials
        frame_login = ctk.CTkFrame(self.root)
        frame_login.pack(pady=20, padx=20, fill="x")
        
        # Username label and entry
        username_label = ctk.CTkLabel(frame_login, text="Username:")
        username_label.pack(anchor="w", pady=(10, 0), padx=10)
        
        self.entry_username = ctk.CTkEntry(
            frame_login,
            placeholder_text="Enter your username",
            width=300)
        self.entry_username.pack(pady=(0, 10), padx=10, fill="x")
        
        # Password label and entry
        password_label = ctk.CTkLabel(frame_login, text="Password:")
        password_label.pack(anchor="w", pady=(10, 0), padx=10)
        
        self.entry_password = ctk.CTkEntry(
            frame_login,
            show="*",
            placeholder_text="Enter your password",
            width=300)
        self.entry_password.pack(pady=(0, 10), padx=10, fill="x")
        
        # Save button
        button_save = ctk.CTkButton(
            frame_login, 
            text="Save", 
            command=self.save_login_info)
        button_save.pack(pady=(10, 20), padx=10)
        
        # Connection button
        self.image_connect_button = ctk.CTkImage(
            light_image=Image.open(self.image_connect_button_path),
            dark_image=Image.open(self.image_connect_button_path),
            size=(200, 200)
        )

        self.button_connect = ctk.CTkButton(
            self.root,
            text="Connect",
            image=self.image_connect_button,
            compound="top",
            width=250,
            height=250,
            corner_radius=100,
            command=self.connect)
        
        self.button_connect.pack(pady=20)

    def load_login_info(self) -> None:
        """Loads saved username and password from the JSON file."""
        try:
            with open("login_info.json", "r", encoding="utf-8") as file:
                login_info: Dict[str, str] = json.load(file)
                self.entry_username.delete(0, 'end')
                self.entry_password.delete(0, 'end')
                self.entry_username.insert(0, login_info.get("username", ""))
                self.entry_password.insert(0, login_info.get("password", ""))
        except (FileNotFoundError, json.JSONDecodeError):
            # No need to show error, just start with empty fields
            pass

    def save_login_info(self) -> None:
        """Saves the username and password to the JSON file and shows confirmation."""
        username = self.entry_username.get()
        password = self.entry_password.get()
        
        if not username or not password:
            messagebox.showwarning("Warning", "Please enter both username and password!")
            return
            
        login_info = {
            "username": username,
            "password": password
        }

        try:
            with open("login_info.json", "w", encoding="utf-8") as file:
                json.dump(login_info, file)
            messagebox.showinfo("Info", "Username and password saved!")
        except IOError as e:
            messagebox.showerror("Error", f"Could not save credentials: {e}")

    def save_login_info_silently(self) -> bool:
        """Saves the username and password without showing a message.
        
        Returns:
            bool: True if credentials were saved successfully, False otherwise
        """
        username = self.entry_username.get()
        password = self.entry_password.get()
        
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
            return True
        except IOError:
            messagebox.showerror("Error", "Could not save credentials")
            return False

    def connect(self) -> None:
        """Connects to the Wi-Fi network using the provided credentials."""
        # Save credentials silently before connecting
        if self.save_login_info_silently():
            # Connect to WiFi
            response = self.connect_callback()
            if response and response.status_code == 200:
                self.update_button_image(resource_path("icons/connected.png"))

    def update_button_image(self, image_path: str) -> None:
        """Updates the connect button image.
        
        Args:
            image_path: Path to the image file
        """
        self.image_connect_button.configure(
            light_image=Image.open(image_path),
            dark_image=Image.open(image_path))
        self.button_connect.configure(image=self.image_connect_button)

    def run(self) -> None:
        """Starts the application by calling the mainloop for the window."""
        self.root.mainloop()

    def destroy(self) -> None:
        """Closes the window and releases resources."""
        self.root.destroy()


def resource_path(relative_path: str) -> str:
    """Get the absolute path to the resource.
    
    This function is used to access resources both when running as a Python script 
    and when bundled as an executable with PyInstaller.
    
    Args:
        relative_path: The relative path to the resource
        
    Returns:
        str: The absolute path to the resource
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
