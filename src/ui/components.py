"""Reusable UI components for the Midnight Zen theme (Sharp Edition)."""

import customtkinter as ctk
from config import *

class CustomDialog(ctk.CTkToplevel):
    """A custom, dark-themed dialog window (Sharp Edition)."""
    
    def __init__(self, master, title, message, is_password=False, is_confirmation=False):
        super().__init__(master)
        
        self.title(title)
        self.geometry("340x220") # Slightly wider for sharp text
        self.resizable(False, False)
        self.configure(fg_color=COLOR_BG_MAIN)
        
        # Center the dialog
        self.transient(master)
        self.grab_set()
        
        # Value holder
        self.user_input = None
        
        # UI Elements
        self.frame = ctk.CTkFrame(self, fg_color="transparent")
        self.frame.pack(expand=True, fill="both", padx=25, pady=25)
        
        # Title/Message
        ctk.CTkLabel(
            self.frame, text=title.upper(), # Uppercase for industrial feel
            font=("Outfit", 16, "bold"), text_color=COLOR_TEXT_MAIN
        ).pack(pady=(0, 10), anchor="w")
        
        ctk.CTkLabel(
            self.frame, text=message, 
            font=("Outfit", 13), text_color=COLOR_TEXT_MUTED,
            wraplength=280, justify="left"
        ).pack(pady=(0, 20), anchor="w")
        
        # Input Field (if not confirmation)
        if not is_confirmation:
            self.entry = ctk.CTkEntry(
                self.frame, show="*" if is_password else "",
                fg_color=COLOR_BG_SECONDARY, border_width=1, border_color=COLOR_BG_SECONDARY,
                text_color=COLOR_TEXT_MAIN, height=35, corner_radius=0
            )
            self.entry.pack(fill="x", pady=(0, 20))
            self.entry.bind("<Return>", self._on_confirm)
            self.entry.focus_set()
        
        # Buttons
        btn_row = ctk.CTkFrame(self.frame, fg_color="transparent")
        btn_row.pack(fill="x")
        
        confirm_color = COLOR_DANGER if is_confirmation else COLOR_ACCENT_PRIMARY
        confirm_text = "CONFIRM" if is_confirmation else "OK"
        
        ctk.CTkButton(
            btn_row, text="CANCEL", width=100, height=35,
            fg_color="transparent", hover_color=COLOR_BG_SECONDARY,
            text_color=COLOR_TEXT_MUTED, border_width=1, border_color=COLOR_BG_SECONDARY,
            corner_radius=2,
            command=self._on_cancel
        ).pack(side="right", padx=(10, 0))
        
        ctk.CTkButton(
            btn_row, text=confirm_text, width=100, height=35,
            fg_color=confirm_color, hover_color=COLOR_ACCENT_HOVER if not is_confirmation else COLOR_DANGER,
            text_color="#FFFFFF",
            corner_radius=2,
            command=self._on_confirm
        ).pack(side="right") # Right aligned buttons for industrial feel

        self.protocol("WM_DELETE_WINDOW", self._on_cancel)
        self.wait_window()

    def _on_confirm(self, event=None):
        if hasattr(self, 'entry'):
            self.user_input = self.entry.get()
        else:
            self.user_input = True # Confirmation
        self.destroy()

    def _on_cancel(self):
        self.user_input = None
        self.destroy()

    @classmethod
    def ask_string(cls, master, title, message, is_password=False):
        dialog = cls(master, title, message, is_password)
        return dialog.user_input

    @classmethod
    def ask_confirm(cls, master, title, message):
        dialog = cls(master, title, message, is_confirmation=True)
        return dialog.user_input is True

class SocialButton(ctk.CTkButton):
    """Button for social media links."""
    def __init__(self, master, image, color, hover_color, command):
        super().__init__(
            master, text="", image=image, 
            width=40, height=40, corner_radius=2, # Sharp
            fg_color=color, hover_color=hover_color,
            command=command
        )
