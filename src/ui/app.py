"""Main App Controller handling View switching."""

import threading
import customtkinter as ctk
from config import *
from credentials import CredentialManager
from connection import check_connection_status, connect_to_wifi
from ui.frames import LoginFrame, DashboardFrame

class WindowMain:
    def __init__(self, connect_callback=None):
        self.root = ctk.CTk()
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_GEOMETRY)
        self.root.configure(fg_color=COLOR_BG_MAIN)
        
        self.creds = CredentialManager()
        self.container = ctk.CTkFrame(self.root, fg_color="transparent")
        self.container.pack(fill="both", expand=True)

        # Loading Indicator
        self.lbl_loading = ctk.CTkLabel(
            self.container, text="Checking Status...", 
            font=("Outfit", 16), text_color=COLOR_TEXT_ACCENT
        )
        self.lbl_loading.place(relx=0.5, rely=0.5, anchor="center")
        
        self.root.after(200, self._check_init)

    def _check_init(self):
        threading.Thread(target=self._bg_check, daemon=True).start()

    def _bg_check(self):
        # 1. Connected?
        sess = check_connection_status()
        if sess.success:
            self.root.after(0, lambda: self.show_dash(sess))
            return

        # 2. Auto-Connect?
        u, p = self.creds.get_last_credentials()
        if u and p:
            self.root.after(0, lambda: self.lbl_loading.configure(text=f"Connecting {u}..."))
            try:
                ns = connect_to_wifi(u, p)
                if ns.success:
                    self.root.after(0, lambda: self.show_dash(ns))
                    return
            except Exception: pass
        
        self.root.after(0, self.show_login)

    def show_login(self):
        self._clear()
        LoginFrame(self.container, self.creds, self.show_dash).pack(fill="both", expand=True)

    def show_dash(self, session):
        self._clear()
        # on_switch calls show_dash recursively
        DashboardFrame(self.container, session, self.creds, self.show_login, self.show_dash).pack(fill="both", expand=True)

    def _clear(self):
        for w in self.container.winfo_children(): w.destroy()

    def run(self): self.root.mainloop()
