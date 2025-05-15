"""Contains the necessary classes for the user interface.

This module implements the graphical user interface for the GSB WiFi Auto Connect
application using customtkinter. It includes classes for the main window.
"""
#region Imports
from tkinter import messagebox
import json
import os
import sys
import webbrowser
from typing import Callable, Dict, Optional, Any, Union
from pathlib import Path
from PIL import Image
import customtkinter as ctk
import requests
from connection import connect_to_wifi, save_login_info, load_login_info
#endregion


class WindowMain:
    """Creates the main application window with WiFi login functionality.
    
    This class implements the main user interface with login fields and 
    a connect button for authenticating with the GSB WiFi portal.
    """

    #region Initialization
    def __init__(self, connect_callback: Callable[[], Optional[requests.Response]]):
        """Initializes the main window with the given connection callback.
        
        Args:
            connect_callback: Function to call when attempting to connect to WiFi
        """
        self.root = ctk.CTk()
        self.root.title("GSB Wifi Auto Connect")
        self.root.geometry("400x550")

        self.connect_callback = connect_callback
        
        self.image_connect_button_path = "icons/disconnected.png"
        
        # Social media profiles
        self.github_url = "https://github.com/RaijuMounun"
        self.instagram_url = "https://www.instagram.com/erenzapkinus"
        
        # Load social media icons
        self.github_icon_path = "icons/github.png"
        self.instagram_icon_path = "icons/instagram.png"
        
        self.setup_ui()
        self.load_login_info()
    #endregion

    #region UI Setup
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
            command=self.save_login_info_to_file)
        button_save.pack(pady=(10, 20), padx=10)
        
        # Connection button - Icon only, moderate size with padding for better visibility
        self.image_connect_button = ctk.CTkImage(
            light_image=Image.open(self.image_connect_button_path),
            dark_image=Image.open(self.image_connect_button_path),
            size=(100, 100)
        )

        self.button_connect = ctk.CTkButton(
            self.root,
            text="",
            image=self.image_connect_button,
            width=140,
            height=140,
            corner_radius=70,
            hover=True,
            fg_color="#1f538d",
            compound="top",
            command=self.connect)
        
        self.button_connect.pack(pady=30)
        
        self._setup_social_media()
    #endregion

    #region Social Media Setup
    def _setup_social_media(self) -> None:
        """Sets up the social media buttons section."""
        social_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        social_frame.pack(pady=(5, 10), padx=20, fill="x")
        
        # Create the social media icons
        github_image = ctk.CTkImage(
            light_image=Image.open(self.github_icon_path),
            dark_image=Image.open(self.github_icon_path),
            size=(24, 24)
        )
        
        instagram_image = ctk.CTkImage(
            light_image=Image.open(self.instagram_icon_path),
            dark_image=Image.open(self.instagram_icon_path),
            size=(24, 24)
        )
        
        # Social buttons frame (for horizontal layout) - Center aligned
        buttons_frame = ctk.CTkFrame(social_frame, fg_color="transparent")
        buttons_frame.pack(pady=(0, 10), fill="x")
        
        # Create a container frame for button centering
        center_frame = ctk.CTkFrame(buttons_frame, fg_color="transparent")
        center_frame.pack(expand=True, fill="x")
        
        # Center the buttons using a label
        center_label = ctk.CTkLabel(center_frame, text="", fg_color="transparent")
        center_label.pack(side="left", expand=True)
        
        # GitHub button with icon
        github_button = ctk.CTkButton(
            center_frame,
            text="",
            image=github_image,
            width=40,
            height=40,
            corner_radius=8,
            hover_color="#2D333B",
            fg_color="#24292E",
            command=lambda: self.open_social_media(self.github_url))
        github_button.pack(side="left", padx=5)
        
        # Instagram button with icon
        instagram_button = ctk.CTkButton(
            center_frame,
            text="",
            image=instagram_image,
            width=40,
            height=40,
            corner_radius=8,
            hover_color="#C13584",
            fg_color="#E1306C",
            command=lambda: self.open_social_media(self.instagram_url))
        instagram_button.pack(side="left", padx=5)
        
        # Spacer for centering
        center_label2 = ctk.CTkLabel(center_frame, text="", fg_color="transparent")
        center_label2.pack(side="left", expand=True)
    #endregion

    #region Social Media Actions
    def open_social_media(self, url: str) -> None:
        """Opens the developer's social profiles in the default browser."""
        webbrowser.open(url)
    #endregion

    #region Login Information Handling
    def load_login_info(self) -> None:
        """Loads saved username and password from the JSON file."""
        login_info = load_login_info()
        self.entry_username.delete(0, 'end')
        self.entry_password.delete(0, 'end')
        self.entry_username.insert(0, login_info.get("username", ""))
        self.entry_password.insert(0, login_info.get("password", ""))

    def save_login_info_to_file(self) -> None:
        """Saves the username and password with a confirmation message."""
        username = self.entry_username.get()
        password = self.entry_password.get()
        save_login_info(username, password, show_message=True)
    #endregion

    #region WiFi Connection Handling
    def connect(self) -> None:
        """Connects to the Wi-Fi network using the provided credentials."""
        username = self.entry_username.get()
        password = self.entry_password.get()
        
        if save_login_info(username, password, show_message=False):
            response = self.connect_callback()
            if response and response.status_code == 200:
                self.image_connect_button_path = "icons/connected.png"
                self.update_button_image(self.image_connect_button_path)
                self.root.quit()

    def update_button_image(self, image_path: str) -> None:
        """Updates the connect button image.
        
        Args:
            image_path: Path to the image file
        """
        self.image_connect_button = ctk.CTkImage(
        light_image=Image.open(image_path),
        dark_image=Image.open(image_path),
        size=(100, 100)
        )
        self.button_connect.configure(image=self.image_connect_button)
    #endregion

    #region Window Management
    def run(self) -> None:
        """Starts the application by calling the mainloop for the window."""
        self.root.mainloop()

    def destroy(self) -> None:
        """Closes the window and releases resources."""
        self.root.destroy()
    #endregion
