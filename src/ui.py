"""
Kullanıcı arayüzü modülü.
Backend'den fırlatılan hataları yakalar ve kullanıcıya gösterir.
"""
#region Import'lar
import json
import os
import sys
import webbrowser
from typing import Callable, Optional
from pathlib import Path
from PIL import Image

# UI Kütüphaneleri
import customtkinter as ctk
from tkinter import messagebox

import requests

# Backend bağlantısı
from connection import connect_to_wifi, WifiConnectionError, AuthenticationError, NetworkTimeoutError
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
        
        # Görsel yolları
        self.image_connect_button_path = resource_path("icons/disconnected.png")
        self.github_icon_path = resource_path("icons/github.png")
        self.instagram_icon_path = resource_path("icons/instagram.png")
        
        # Linkler
        self.github_url = "https://github.com/RaijuMounun"
        self.instagram_url = "https://www.instagram.com/erenzapkinus"
        
        self.setup_ui()
        
        # Başlangıçta verileri yükle
        self._load_creds_to_ui()

    #region UI Kurulumu
    def setup_ui(self) -> None:
        """Kullanıcı arayüzü bileşenlerini ve düzenini ayarlar."""
        # Giriş bilgileri için çerçeve
        frame_login = ctk.CTkFrame(self.root)
        frame_login.pack(pady=20, padx=20, fill="x")
        
        # Kullanıcı adı label ve giriş alanı
        username_label = ctk.CTkLabel(frame_login, text="Kullanıcı Adı:")
        username_label.pack(anchor="w", pady=(10, 0), padx=10)
        
        self.entry_username = ctk.CTkEntry(
            frame_login,
            placeholder_text="Kullanıcı adın",
            width=300)
        self.entry_username.pack(pady=(0, 10), padx=10, fill="x")
        
        # Parola label ve giriş alanı
        password_label = ctk.CTkLabel(frame_login, text="Parola:")
        password_label.pack(anchor="w", pady=(10, 0), padx=10)
        
        self.entry_password = ctk.CTkEntry(
            frame_login,
            show="*",
            placeholder_text="Parolan",
            width=300)
        self.entry_password.pack(pady=(0, 10), padx=10, fill="x")
        
        # Kaydet düğmesi
        button_save = ctk.CTkButton(
            frame_login, 
            text="Kaydet", 
            command=self.save_creds_from_ui) # Artık sınıf içindeki yeni metoda gidiyor
        button_save.pack(pady=(10, 20), padx=10)
        
        # Bağlantı düğmesi
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

    #region Sosyal Medya Kısmı Kurulumu
    def _setup_social_media(self) -> None:
        """Sosyal medya düğmeleri bölümünü ayarlar."""
        social_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        social_frame.pack(pady=(5, 10), padx=20, fill="x")
        
        # Sosyal medya ikonlarını oluştur
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
        
        # Sosyal butonlar için frame
        buttons_frame = ctk.CTkFrame(social_frame, fg_color="transparent")
        buttons_frame.pack(pady=(0, 10), fill="x")
        
        center_frame = ctk.CTkFrame(buttons_frame, fg_color="transparent")
        center_frame.pack(expand=True, fill="x")
        
        ctk.CTkLabel(center_frame, text="", fg_color="transparent").pack(side="left", expand=True)
        
        # GitHub butonu
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
        
        # Instagram butonu
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
        
        ctk.CTkLabel(center_frame, text="", fg_color="transparent").pack(side="left", expand=True)
    #endregion

    #region Yardımcı Metodlar
    def open_social_media(self, url: str) -> None:
        webbrowser.open(url)

    def update_button_image(self, image_path: str) -> None:
        """Bağlantı düğmesinin görüntüsünü günceller."""
        self.image_connect_button = ctk.CTkImage(
            light_image=Image.open(image_path),
            dark_image=Image.open(image_path),
            size=(100, 100)
        )
        self.button_connect.configure(image=self.image_connect_button)
    #endregion

    #region Veri Yönetimi (Geçici - Phase 2'de Keyring olacak)
    def _load_creds_to_ui(self):
        """Başlangıçta JSON'dan veriyi okuyup kutucuklara yazar."""
        try:
            with open("login_info.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                self.entry_username.delete(0, 'end')
                self.entry_password.delete(0, 'end')
                self.entry_username.insert(0, data.get("username", ""))
                self.entry_password.insert(0, data.get("password", ""))
        except (FileNotFoundError, json.JSONDecodeError):
            pass 

    def save_creds_from_ui(self, show_msg=True) -> bool:
        """Kutucuklardaki veriyi JSON dosyasına yazar."""
        u = self.entry_username.get()
        p = self.entry_password.get()
        
        if not u or not p:
            if show_msg: messagebox.showwarning("Eksik Bilgi", "Kullanıcı adı ve parola gerekli.")
            return False
            
        try:
            with open("login_info.json", "w", encoding="utf-8") as f:
                json.dump({"username": u, "password": p}, f)
            if show_msg:
                messagebox.showinfo("Başarılı", "Bilgiler kaydedildi.")
            return True
        except Exception as e:
            messagebox.showerror("Hata", f"Kaydedilemedi: {e}")
            return False
    #endregion

    #region WiFi Bağlantı İşlemleri
    def connect(self) -> None:
        """Yeni nesil bağlantı fonksiyonu."""
        # 1. UI'dan veriyi al
        username = self.entry_username.get()
        password = self.entry_password.get()
        
        # 2. Önce kaydetmeyi dene 
        if not self.save_creds_from_ui(show_msg=False):
            return

        # 3. Backend'i çağır ve hataları dinle
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

    #region Pencere Yönetimi
    def run(self) -> None:
        self.root.mainloop()

    def destroy(self) -> None:
        self.root.destroy()
    #endregion