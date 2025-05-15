"""Contains the necessary classes for the user interface."""
from tkinter import messagebox
import json
import os
import sys
from abc import ABC, abstractmethod
from PIL import Image
import customtkinter as ctk


class WindowBase(ABC):
    """Base class for all windows in the application."""

    @abstractmethod
    def run(self):
        """Starts the window."""

    @abstractmethod
    def destroy(self):
        """Closes the window."""


class WindowMain(WindowBase):
    """Creates the main application window."""

    def __init__(self, connect_callback):
        self.root = ctk.CTk()
        self.root.title("GSB Wifi Auto Connect")
        self.root.geometry("400x500")

        self.connect_callback = connect_callback
        
        self.image_connect_button_path = resource_path("icons/disconnected.png")
        
        self.setup_ui()
        self.load_login_info()

    def setup_ui(self):
        """Sets up the user interface."""
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
            text="Save Credentials", 
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

    def load_login_info(self):
        """Loads saved username and password."""
        try:
            with open("login_info.json", "r", encoding="utf-8") as file:
                login_info = json.load(file)
                self.entry_username.insert(0, login_info.get("username", ""))
                self.entry_password.insert(0, login_info.get("password", ""))
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def save_login_info(self):
        """Saves the username and password."""
        username = self.entry_username.get()
        password = self.entry_password.get()
        
        if not username or not password:
            messagebox.showwarning("Warning", "Please enter both username and password!")
            return
            
        login_info = {
            "username": username,
            "password": password
        }

        with open("login_info.json", "w", encoding="utf-8") as file:
            json.dump(login_info, file)

        messagebox.showinfo("Info", "Username and password saved!")

    def save_login_info_silently(self):
        """Saves the username and password without showing a message."""
        username = self.entry_username.get()
        password = self.entry_password.get()
        
        if not username or not password:
            messagebox.showwarning("Warning", "Please enter both username and password!")
            return False
            
        login_info = {
            "username": username,
            "password": password
        }

        with open("login_info.json", "w", encoding="utf-8") as file:
            json.dump(login_info, file)
            
        return True

    def connect(self):
        """Connects to the Wi-Fi."""
        # Save credentials silently before connecting
        if self.save_login_info_silently():
            # Connect to WiFi
            response = self.connect_callback()
            if response and response.status_code == 200:
                self.update_button_image(resource_path("icons/connected.png"))

    def update_button_image(self, image_path):
        """Updates the connect button image."""
        self.image_connect_button.configure(
            light_image=Image.open(image_path),
            dark_image=Image.open(image_path))
        self.button_connect.configure(image=self.image_connect_button)

    def run(self):
        """Starts the application by calling the mainloop for the window."""
        self.root.mainloop()

    def destroy(self):
        """Closes the window."""
        self.root.destroy()


def resource_path(relative_path):
    """Get the absolute path to the resource."""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
