"""Contains the necessary classes for the user interface."""
from tkinter import messagebox
import json
from PIL import Image
import customtkinter as ctk
from connection import connect_to_wifi, disconnect_from_wifi


class WindowMain:
    """Creates the main application window."""
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("GSB Wifi Auto Connect")
        self.root.geometry("600x400")

        self.image_login_info_button_path = "icons/wrench.png"
        self.is_connected = False
        self.image_connect_button_path = ("icons/connected.png" if self.is_connected
                                          else "icons/disconnected.png")

        #region Connect Button
        self.image_connect_button = ctk.CTkImage(
            light_image=Image.open(self.image_connect_button_path),
            dark_image=Image.open(self.image_connect_button_path),
            size=(200, 200)
        )

        self.button_connect = ctk.CTkButton(
            self.root,
            text="",  # Placeholder for an icon
            image=self.image_connect_button,
            font=("Arial", 100),
            corner_radius=500,
            command=self.connect)

        self.button_connect.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        #endregion

        #region Login Info Button
        self.image_login_info = ctk.CTkImage(
            light_image=Image.open(self.image_login_info_button_path),
            dark_image=Image.open(self.image_login_info_button_path),
            size=(20, 20)
        )

        self.button_login_info = ctk.CTkButton(
            self.root,
            text="",  # Placeholder for an icon
            image=self.image_login_info,
            width=30,
            height=30,
            command=self.open_login_info_window)

        self.button_login_info.place(relx=0.95, rely=0.05, anchor=ctk.NE)
        #endregion

    def connect(self):
        """Connects to the Wi-Fi network."""
        if not self.is_connected:
            connect_to_wifi()  # Attempt to connect
            self.image_connect_button.configure(light_image=Image.open("icons/connected.png"),
                                                dark_image=Image.open("icons/connected.png"))
            self.button_connect.configure(image=self.image_connect_button)
            self.is_connected = True
        else:
            disconnect_from_wifi()  # Disconnect
            self.image_connect_button.configure(light_image=Image.open("icons/disconnected.png"),
                                                dark_image=Image.open("icons/disconnected.png"))
            self.button_connect.configure(image=self.image_connect_button)
            self.is_connected = False

    def open_login_info_window(self):
        """Opens the login information window."""
        WindowLoginInfo(self.root)

    def run(self):
        """Starts the application by calling the mainloop for the window."""
        self.root.mainloop()


class WindowLoginInfo:
    """Creates a window to save login information.
    The window consists of username and password entry fields and a save-and-close button."""

    def __init__(self, parent):
        self.parent = parent
        self.window = ctk.CTkToplevel(self.parent)
        self.window.title("Login Information")
        self.window.geometry("300x200")
        self.window.attributes("-topmost", True)

        #region Login Info Entries
        self.entry_username = ctk.CTkEntry(
            self.window,
            placeholder_text="Enter your username")
        self.entry_username.pack(pady=10)

        self.entry_password = ctk.CTkEntry(
            self.window,
            show="*",
            placeholder_text="Enter your password")
        self.entry_password.pack(pady=10)
        #endregion

        self.load_login_info()

        button_save = ctk.CTkButton(self.window, text="Save and Close", command=self.save_and_exit)
        button_save.pack(pady=10)

    def load_login_info(self):
        """Loads saved username and password and populates the entry fields."""
        try:
            with open("login_info.json", "r", encoding="utf-8") as file:
                login_info = json.load(file)
                self.entry_username.insert(0, login_info.get("username", ""))
                self.entry_password.insert(0, login_info.get("password", ""))
        except FileNotFoundError:
            pass
        except json.JSONDecodeError:
            pass

    def save_and_exit(self):
        """Saves the username and password and closes the window.
        Takes no parameters and returns no value."""

        username = self.entry_username.get()
        password = self.entry_password.get()
        login_info = {
            "username": username,
            "password": password
        }

        with open("login_info.json", "w", encoding="utf-8") as file:
            json.dump(login_info, file)

        messagebox.showinfo("Info", "Username and password saved!")
        self.destroy_window()

    def destroy_window(self):
        """Closes the window."""
        self.window.destroy()
