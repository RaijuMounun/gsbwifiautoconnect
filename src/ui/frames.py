"""Application frames for Login and Dashboard views (Zen Mode - Sharp Edition)."""

import webbrowser
import threading
from PIL import Image
import customtkinter as ctk
from tkinter import messagebox

from config import *
from connection import connect_to_wifi, logout, WifiConnectionError, AuthenticationError, NetworkTimeoutError
from ui.components import CustomDialog, SocialButton

def resource_path(relative_path: str) -> str:
    """Helper to get resource path."""
    import sys, os
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class LoginFrame(ctk.CTkFrame):
    """Minimalist Zen Login Screen."""
    
    def __init__(self, master, creds_manager, on_connect_success):
        super().__init__(master, fg_color="transparent")
        self.creds_manager = creds_manager
        self.on_connect_success = on_connect_success
        
        self._load_icons()
        self._setup_ui()
        self._load_accounts()

    def _load_icons(self):
        self.icons = {
            "github": ctk.CTkImage(light_image=Image.open(resource_path(ICON_GITHUB)), size=(20, 20)),
            "insta": ctk.CTkImage(light_image=Image.open(resource_path(ICON_INSTAGRAM)), size=(20, 20)),
            "linkedin": ctk.CTkImage(light_image=Image.open(resource_path(ICON_LINKEDIN)), size=(20, 20))
        }

    def _setup_ui(self):
        # Center Container
        self.center = ctk.CTkFrame(self, fg_color="transparent")
        self.center.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9)

        # Title (Minimal)
        ctk.CTkLabel(
            self.center, text="GSB WiFi", 
            font=("Outfit", 36, "bold"), text_color=COLOR_TEXT_MAIN
        ).pack(pady=(0, 40))

        # Account Dropdown (Wider, Sharp)
        self.account_var = ctk.StringVar()
        self.combo_acc = ctk.CTkComboBox(
            self.center, variable=self.account_var, width=320, height=45,
            fg_color=COLOR_BG_SECONDARY, border_width=1, border_color=COLOR_BG_SECONDARY,
            text_color=COLOR_TEXT_MAIN, dropdown_fg_color=COLOR_BG_CARD,
            font=("Outfit", 14), corner_radius=2, # Sharp
            command=self._on_account_selected
        )
        self.combo_acc.pack(pady=10)

        # Password (Wider, Sharp)
        self.entry_pwd = ctk.CTkEntry(
            self.center, show="*", width=320, height=45,
            placeholder_text="Password",
            fg_color=COLOR_BG_SECONDARY, border_width=1, border_color=COLOR_BG_SECONDARY,
            text_color=COLOR_TEXT_MAIN, corner_radius=2, # Sharp
            font=("Outfit", 14)
        )
        self.entry_pwd.pack(pady=10)

        # Connect Button (Sharp, Glowing)
        self.btn_connect = ctk.CTkButton(
            self.center, text="CONNECT", width=320, height=55,
            corner_radius=2, # Sharp
            fg_color=COLOR_ACCENT_PRIMARY, hover_color=COLOR_ACCENT_HOVER,
            font=("Outfit", 15, "bold"),
            command=self._on_connect
        )
        self.btn_connect.pack(pady=30)

        # Actions Row
        actions = ctk.CTkFrame(self.center, fg_color="transparent")
        actions.pack(pady=10)
        
        ctk.CTkButton(
            actions, text="+ New Account", width=120, fg_color="transparent",
            text_color=COLOR_TEXT_ACCENT, hover_color=COLOR_BG_SECONDARY,
            corner_radius=2,
            command=self._on_add
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            actions, text="Remove", width=100, fg_color="transparent",
            text_color=COLOR_TEXT_MUTED, hover_color=COLOR_BG_SECONDARY,
            corner_radius=2,
            command=self._on_remove
        ).pack(side="left", padx=10)

        # Footer
        footer = ctk.CTkFrame(self, fg_color="transparent")
        footer.pack(side="bottom", pady=40)
        
        SocialButton(footer, self.icons["github"], COLOR_GITHUB, COLOR_GITHUB_HOVER, lambda: webbrowser.open(GITHUB_URL)).pack(side="left", padx=5)
        SocialButton(footer, self.icons["insta"], COLOR_INSTAGRAM, COLOR_INSTAGRAM_HOVER, lambda: webbrowser.open(INSTAGRAM_URL)).pack(side="left", padx=5)
        SocialButton(footer, self.icons["linkedin"], COLOR_LINKEDIN, COLOR_LINKEDIN_HOVER, lambda: webbrowser.open(LINKEDIN_URL)).pack(side="left", padx=5)

    def _load_accounts(self):
        accounts = self.creds_manager.get_all_accounts()
        last_used = self.creds_manager.get_last_used()
        
        display_list = []
        self.map_label_to_user = {}
        
        for u in accounts:
            meta = self.creds_manager.get_account_metadata(u)
            quota = meta.get("quota", "---")
            label = f"{u}  |  {quota}" if quota != "---" else u # Pipe separator for sharp look
            display_list.append(label)
            self.map_label_to_user[label] = u
            
        self.combo_acc.configure(values=display_list)
        
        # Select last used
        target = None
        if last_used:
            for lbl, usr in self.map_label_to_user.items():
                if usr == last_used:
                    target = lbl; break
        
        if target:
            self.account_var.set(target)
            self._on_account_selected(target)
        elif display_list:
            self.account_var.set(display_list[0])
            self._on_account_selected(display_list[0])

    def _on_account_selected(self, selection):
        username = self.map_label_to_user.get(selection, selection)
        pwd = self.creds_manager.get_password(username)
        self.entry_pwd.delete(0, 'end')
        if pwd: self.entry_pwd.insert(0, pwd)
        self.creds_manager.set_last_used(username)

    def _on_add(self):
        u = CustomDialog.ask_string(self, "New Account", "Username:")
        if not u: return
        p = CustomDialog.ask_string(self, "New Account", f"Password for {u}:", is_password=True)
        if not p: return
        self.creds_manager.add_account(u, p)
        self._load_accounts()

    def _on_remove(self):
        sel = self.account_var.get()
        user = self.map_label_to_user.get(sel, sel)
        if user and CustomDialog.ask_confirm(self, "Remove Account", f"Remove '{user}'?"):
            self.creds_manager.remove_account(user)
            self._load_accounts()

    def _on_connect(self):
        sel = self.account_var.get()
        user = self.map_label_to_user.get(sel, sel)
        pwd = self.entry_pwd.get()
        
        if not user or not pwd: return

        self.creds_manager.add_account(user, pwd)
        self.btn_connect.configure(state="disabled", text="CONNECTING...")
        threading.Thread(target=self._connect_thread, args=(user, pwd), daemon=True).start()

    def _connect_thread(self, user, pwd):
        try:
            session = connect_to_wifi(user, pwd)
            self.after(0, lambda: self.on_connect_success(session))
        except Exception as e:
            self.after(0, lambda: self._handle_error(e))

    def _handle_error(self, e):
        self.btn_connect.configure(state="normal", text="CONNECT")
        CustomDialog(self, "Connection Failed", str(e))


class DashboardFrame(ctk.CTkFrame):
    """Zen Mode Dashboard - Sharp Edition"""
    
    def __init__(self, master, session, creds_manager, on_logout, on_switch):
        super().__init__(master, fg_color="transparent")
        self.session = session
        self.creds_manager = creds_manager
        self.on_logout = on_logout
        self.on_switch = on_switch
        
        self.current_user = creds_manager.get_last_used()
        if self.current_user:
            creds_manager.update_account_metadata(self.current_user, session.remaining_quota)
            
        self._setup_ui()

    def _setup_ui(self):
        # Top Bar (Account Switcher - Minimal)
        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", padx=30, pady=30)
        
        self._setup_dropdown(top)

        # Hero Ring
        hero = ctk.CTkFrame(self, fg_color="transparent")
        hero.place(relx=0.5, rely=0.5, anchor="center")
        
        percent = int(self.session.quota_percent * 100)
        ring_color = COLOR_ACCENT_PRIMARY if percent > 20 else COLOR_DANGER
        
        # Simulated Ring
        self.ring = ctk.CTkButton(
            hero, text=f"{percent}%",
            font=("Outfit", 54, "bold"), text_color="#FFFFFF",
            width=220, height=220, corner_radius=110, # Keep circular for ring
            fg_color="transparent", border_width=4, border_color=ring_color,
            hover=False
        )
        self.ring.pack()
        
        ctk.CTkLabel(hero, text=self.session.remaining_quota, font=("Outfit", 28), text_color=COLOR_TEXT_MAIN).pack(pady=(20, 0))
        ctk.CTkLabel(hero, text="REMAINING", font=("Outfit", 12, "bold"), text_color=COLOR_TEXT_MUTED).pack()

        # Bottom details
        self.lbl_renewal = ctk.CTkLabel(
            self, text=f"RENEWS {self.session.quota_renewal_date}",
            font=("Outfit", 13, "bold"), text_color=COLOR_TEXT_MUTED
        )
        self.lbl_renewal.place(relx=0.5, rely=0.85, anchor="center")

        # Discrete Disconnect - INSTANT ACTION
        ctk.CTkButton(
            self, text="DISCONNECT", width=140, height=35,
            fg_color="transparent", hover_color=COLOR_BG_SECONDARY,
            text_color=COLOR_DANGER, font=("Outfit", 12, "bold"),
            corner_radius=2, # Sharp
            command=self._on_logout_click
        ).place(relx=0.5, rely=0.93, anchor="center")

    def _setup_dropdown(self, parent):
        accounts = self.creds_manager.get_all_accounts()
        display_list = []
        self.map_label = {}
        current_disp = self.current_user
        
        for u in accounts:
            meta = self.creds_manager.get_account_metadata(u)
            quota = meta.get("quota", "---")
            label = f"{u} | {quota}" if quota != "---" else u
            display_list.append(label)
            self.map_label[label] = u
            if u == self.current_user: current_disp = label

        self.acc_var = ctk.StringVar(value=current_disp)
        self.cmb = ctk.CTkComboBox(
            parent, variable=self.acc_var, values=display_list,
            width=220, height=32,
            fg_color=COLOR_BG_SECONDARY, border_width=0, corner_radius=2, # Sharp
            dropdown_fg_color=COLOR_BG_CARD,
            command=self._on_switch
        )
        self.cmb.pack(side="right")
        
        ctk.CTkLabel(parent, text="ACTIVE", font=("Outfit", 14, "bold"), text_color=COLOR_TEXT_MUTED).pack(side="left")

    def _on_switch(self, sel):
        user = self.map_label.get(sel, sel)
        if user == self.current_user: return
        
        self.cmb.configure(state="disabled")
        threading.Thread(target=self._switch_thread, args=(user,), daemon=True).start()

    def _switch_thread(self, user):
        logout()
        pwd = self.creds_manager.get_password(user)
        try:
            sess = connect_to_wifi(user, pwd)
            self.creds_manager.set_last_used(user)
            self.after(0, lambda: self.on_switch(sess))
        except Exception:
            self.after(0, lambda: self.on_logout())

    def _on_logout_click(self):
        # NO CONFIRMATION - Instant disconnect
        threading.Thread(target=lambda: [logout(), self.after(0, self.on_logout)], daemon=True).start()
