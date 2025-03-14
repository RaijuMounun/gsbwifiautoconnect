"""Contains the necessary classes for the user interface."""
from tkinter import messagebox
import json
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

    def __init__(self, connect_callback, disconnect_callback):
        self.root = ctk.CTk()
        self.root.title("GSB Wifi Auto Connect")
        self.root.geometry("600x400")

        self.connect_callback = connect_callback
        self.disconnect_callback = disconnect_callback
        self.is_connected = False

        self.image_login_info_button_path = "icons/wrench.png"
        self.image_connect_button_path = ("icons/connected.png" if self.is_connected
                                          else "icons/disconnected.png")

        self.setup_ui()

    def setup_ui(self):
        """Sets up the user interface."""
        self.image_connect_button = ctk.CTkImage(
            light_image=Image.open(self.image_connect_button_path),
            dark_image=Image.open(self.image_connect_button_path),
            size=(200, 200)
        )

        self.button_connect = ctk.CTkButton(
            self.root,
            text="",
            image=self.image_connect_button,
            corner_radius=100,
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
            command=self.connect)
=======
            command=self.toggle_connection)
>>>>>>> Stashed changes
=======
            command=self.toggle_connection)
>>>>>>> Stashed changes
=======
            command=self.toggle_connection)
>>>>>>> Stashed changes

        self.button_connect.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        self.image_login_info = ctk.CTkImage(
            light_image=Image.open(self.image_login_info_button_path),
            dark_image=Image.open(self.image_login_info_button_path),
            size=(20, 20)
        )

        self.button_login_info = ctk.CTkButton(
            self.root,
            text="",
            image=self.image_login_info,
            width=30,
            height=30,
            command=self.open_login_info_window)

        self.button_login_info.place(relx=0.95, rely=0.05, anchor=ctk.NE)

    def toggle_connection(self):
        """Toggles the Wi-Fi connection."""
        if not self.is_connected:
            self.connect_callback()
            self.update_button_image("icons/connected.png")
            self.is_connected = True
        else:
            self.disconnect_callback()
            self.update_button_image("icons/disconnected.png")
            self.is_connected = False

    def update_button_image(self, image_path):
        """Updates the connect button image."""
        self.image_connect_button.configure(
            light_image=Image.open(image_path),
            dark_image=Image.open(image_path))
        self.button_connect.configure(image=self.image_connect_button)

    def open_login_info_window(self):
        """Opens the login information window."""
        WindowLoginInfo(self.root)

    def run(self):
        """Starts the application by calling the mainloop for the window."""
        self.root.mainloop()

    def destroy(self):
        """Closes the window."""
        self.root.destroy()


class WindowLoginInfo(WindowBase):
    """Creates a window to save login information."""
    def __init__(self, parent):
        self.parent = parent
        self.window = ctk.CTkToplevel(self.parent)
        self.window.title("Login Information")
        self.window.geometry("300x200")
        self.window.attributes("-topmost", True)

        self.setup_ui()

    def setup_ui(self):
        """Sets up the user interface."""
        self.entry_username = ctk.CTkEntry(
            self.window,
            placeholder_text="Enter your username")
        self.entry_username.pack(pady=10)

        self.entry_password = ctk.CTkEntry(
            self.window,
            show="*",
            placeholder_text="Enter your password")
        self.entry_password.pack(pady=10)

        self.load_login_info()

        button_save = ctk.CTkButton(self.window, text="Save and Close", command=self.save_and_exit)
        button_save.pack(pady=10)

    def load_login_info(self):
        """Loads saved username and password."""
        try:
            with open("login_info.json", "r", encoding="utf-8") as file:
                login_info = json.load(file)
                self.entry_username.insert(0, login_info.get("username", ""))
                self.entry_password.insert(0, login_info.get("password", ""))
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def save_and_exit(self):
        """Saves the username and password and closes the window."""
        username = self.entry_username.get()
        password = self.entry_password.get()
        login_info = {
            "username": username,
            "password": password
        }

        with open("login_info.json", "w", encoding="utf-8") as file:
            json.dump(login_info, file)

        messagebox.showinfo("Info", "Username and password saved!")
        self.destroy()

    def run(self):
        """Starts the window."""
        self.window.mainloop()

    def destroy(self):
        """Closes the window."""
        self.window.destroy()
