"""
Kullanıcı arayüzü modülü.
Backend'den fırlatılan hataları yakalar ve kullanıcıya gösterir.
"""
#region Import'lar
import sys
import os
import webbrowser
from typing import Callable
from pathlib import Path
from PIL import Image

# UI Kütüphaneleri
import customtkinter as ctk
from tkinter import messagebox

import requests

# Backend ve Güvenlik
from connection import connect_to_wifi, WifiConnectionError, AuthenticationError, NetworkTimeoutError
from credentials import CredentialManager
#endregion


def resource_path(relative_path):
    """PyInstaller için kaynak yolunu bulur."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class WindowMain:
    def __init__(self, connect_callback: Callable[[str, str], requests.Response]):
        self.root = ctk.CTk()
        self.root.title("GSB Wifi Auto Connect")
        self.root.geometry("400x550")

        self.connect_callback = connect_callback
        
        # YENİ: Credential Manager'ı başlat
        self.creds_manager = CredentialManager()
        
        # Görsel yolları
        self.image_connect_button_path = resource_path("icons/disconnected.png")
        self.github_icon_path = resource_path("icons/github.png")
        self.instagram_icon_path = resource_path("icons/instagram.png")
        
        # Linkler
        self.github_url = "https://github.com/RaijuMounun"
        self.instagram_url = "https://www.instagram.com/erenzapkinus"
        
        self.setup_ui()
        
        # Başlangıçta verileri güvenli alandan yükle
        self._load_creds_to_ui()

    #region UI Kurulumu
    def setup_ui(self) -> None:
        """Kullanıcı arayüzü bileşenlerini ve düzenini ayarlar."""
        # Giriş bilgileri için çerçeve
        frame_login = ctk.CTkFrame(self.root)
        frame_login.pack(pady=20, padx=20, fill="x")
        
        # Kullanıcı adı
        ctk.CTkLabel(frame_login, text="Kullanıcı Adı:").pack(anchor="w", pady=(10, 0), padx=10)
        
        self.entry_username = ctk.CTkEntry(frame_login, placeholder_text="Kullanıcı adın", width=300)
        self.entry_username.pack(pady=(0, 10), padx=10, fill="x")
        
        # Parola
        ctk.CTkLabel(frame_login, text="Parola:").pack(anchor="w", pady=(10, 0), padx=10)
        
        self.entry_password = ctk.CTkEntry(frame_login, show="*", placeholder_text="Parolan", width=300)
        self.entry_password.pack(pady=(0, 10), padx=10, fill="x")
        
        # Kaydet düğmesi
        button_save = ctk.CTkButton(
            frame_login, 
            text="Kaydet", 
            command=self.save_creds_from_ui) 
        button_save.pack(pady=(10, 20), padx=10)
        
        # Bağlantı düğmesi
        self.image_connect_button = ctk.CTkImage(
            light_image=Image.open(self.image_connect_button_path),
            dark_image=Image.open(self.image_connect_button_path),
            size=(100, 100)
        )

        self.button_connect = ctk.CTkButton(
            self.root, text="", image=self.image_connect_button,
            width=140, height=140, corner_radius=70, hover=True,
            fg_color="#1f538d", compound="top",
            command=self.connect)
        
        self.button_connect.pack(pady=30)
        
        self._setup_social_media()
    #endregion

    #region Sosyal Medya
    def _setup_social_media(self) -> None:
        # (Burası aynı, yer kaplamaması için kısalttım ama senin kodunda aynı kalsın)
        social_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        social_frame.pack(pady=(5, 10), padx=20, fill="x")
        
        github_image = ctk.CTkImage(light_image=Image.open(self.github_icon_path), size=(24, 24))
        instagram_image = ctk.CTkImage(light_image=Image.open(self.instagram_icon_path), size=(24, 24))
        
        buttons_frame = ctk.CTkFrame(social_frame, fg_color="transparent")
        buttons_frame.pack(pady=(0, 10), fill="x")
        center_frame = ctk.CTkFrame(buttons_frame, fg_color="transparent")
        center_frame.pack(expand=True, fill="x")
        ctk.CTkLabel(center_frame, text="", fg_color="transparent").pack(side="left", expand=True)
        
        ctk.CTkButton(center_frame, text="", image=github_image, width=40, height=40, corner_radius=8,
            hover_color="#2D333B", fg_color="#24292E",
            command=lambda: self.open_social_media(self.github_url)).pack(side="left", padx=5)
            
        ctk.CTkButton(center_frame, text="", image=instagram_image, width=40, height=40, corner_radius=8,
            hover_color="#C13584", fg_color="#E1306C",
            command=lambda: self.open_social_media(self.instagram_url)).pack(side="left", padx=5)
            
        ctk.CTkLabel(center_frame, text="", fg_color="transparent").pack(side="left", expand=True)

    def open_social_media(self, url: str) -> None:
        webbrowser.open(url)
    
    def update_button_image(self, image_path: str) -> None:
        self.image_connect_button = ctk.CTkImage(light_image=Image.open(image_path), size=(100, 100))
        self.button_connect.configure(image=self.image_connect_button)
    #endregion

    #region Veri Yönetimi
    def _load_creds_to_ui(self):
        """Credential Manager'dan verileri çeker ve arayüze basar."""
        username, password = self.creds_manager.get_last_credentials()
        
        self.entry_username.delete(0, 'end')
        self.entry_password.delete(0, 'end')
        
        if username:
            self.entry_username.insert(0, username)
        if password:
            self.entry_password.insert(0, password)

    def save_creds_from_ui(self, show_msg=True) -> bool:
        """Arayüzdeki verileri Credential Manager'a gönderir."""
        u = self.entry_username.get()
        p = self.entry_password.get()
        
        if not u or not p:
            if show_msg: messagebox.showwarning("Eksik Bilgi", "Kullanıcı adı ve parola gerekli.")
            return False
            
        try:
            self.creds_manager.save_credentials(u, p)
            
            if show_msg:
                messagebox.showinfo("Güvenli Kayıt", "Bilgileriniz güvenli kasaya kaydedildi.")
            return True
        except Exception as e:
            messagebox.showerror("Kayıt Hatası", f"Kaydedilemedi: {e}")
            return False
    #endregion

    #region WiFi Bağlantı
    def connect(self) -> None:
        username = self.entry_username.get()
        password = self.entry_password.get()
        
        if not self.save_creds_from_ui(show_msg=False):
            return

        try:
            response = self.connect_callback(username, password)
            if response:
                self.image_connect_button_path = resource_path("icons/connected.png")
                self.update_button_image(self.image_connect_button_path) 
                messagebox.showinfo("Başarılı", "GSB WiFi ağına giriş yapıldı!")
                self.root.quit()

        except AuthenticationError:
            messagebox.showerror("Giriş Başarısız", "Şifre veya kullanıcı adı hatalı.")
        except NetworkTimeoutError:
            messagebox.showwarning("Bağlantı Sorunu", "Sunucu cevap vermiyor. WiFi'a bağlı mısın?")
        except WifiConnectionError as e:
            messagebox.showerror("Hata", f"Beklenmeyen bir sorun: {str(e)}")
        except Exception as e:
            messagebox.showerror("Kritik Hata", f"Kod hatası: {str(e)}")
    #endregion

    def run(self):
        self.root.mainloop()

    def destroy(self):
        self.root.destroy()