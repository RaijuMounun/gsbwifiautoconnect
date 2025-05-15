"""Kullanıcı arayüzü için gerekli sınıfları içerir.

Bu modül, GSB WiFi Auto Connect uygulaması için customtkinter kullanarak
kullanıcı arayüzünü oluşturur. Ana pencere için sınıfları içerir.
"""
#region Import'lar
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
    """GSB WiFi giriş işlevselliği ile ana uygulama penceresini oluşturur.
    
    Bu sınıf, GSB WiFi portalında kimlik doğrulama için giriş alanları ve
    bir bağlantı düğmesi içeren ana kullanıcı arayüzünü oluşturur.
    """

    #region Başlatma
    def __init__(self, connect_callback: Callable[[], Optional[requests.Response]]):
        """Ana pencereyi verilen bağlantı geri çağırma işleviyle başlatır.
        
        Argümanlar:
            connect_callback: WiFi'a bağlanmaya çalışırken çağrılacak işlev
        """
        self.root = ctk.CTk()
        self.root.title("GSB Wifi Auto Connect")
        self.root.geometry("400x550")

        self.connect_callback = connect_callback
        
        self.image_connect_button_path = "icons/disconnected.png"
        
        # Sosyal medya profilleri
        self.github_url = "https://github.com/RaijuMounun"
        self.instagram_url = "https://www.instagram.com/erenzapkinus"
        
        # Sosyal medya ikonları
        self.github_icon_path = "icons/github.png"
        self.instagram_icon_path = "icons/instagram.png"
        
        self.setup_ui()
        self.load_login_info()
    #endregion

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
            command=self.save_login_info_to_file)
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
        
        # Sosyal butonlar için frame (yatay düzen için) - Merkeze hizalı
        buttons_frame = ctk.CTkFrame(social_frame, fg_color="transparent")
        buttons_frame.pack(pady=(0, 10), fill="x")
        
        # Butonları merkezlemek için container frame oluştur
        center_frame = ctk.CTkFrame(buttons_frame, fg_color="transparent")
        center_frame.pack(expand=True, fill="x")
        
        # Butonları merkezlemek için label kullan
        center_label = ctk.CTkLabel(center_frame, text="", fg_color="transparent")
        center_label.pack(side="left", expand=True)
        
        # GitHub butonu ve ikonu
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
        
        # Instagram butonu ve ikonu
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
        
        # Merkezleme için spacer
        center_label2 = ctk.CTkLabel(center_frame, text="", fg_color="transparent")
        center_label2.pack(side="left", expand=True)
    #endregion

    #region Sosyal Medya İşlemleri
    def open_social_media(self, url: str) -> None:
        """Geliştiricinin sosyal medya profillerini varsayılan tarayıcıda açar."""
        webbrowser.open(url)
    #endregion

    #region Giriş Bilgileri İşleme
    def load_login_info(self) -> None:
        """JSON dosyasından kaydedilmiş kullanıcı adı ve parolayı yükler."""
        login_info = load_login_info()
        self.entry_username.delete(0, 'end')
        self.entry_password.delete(0, 'end')
        self.entry_username.insert(0, login_info.get("username", ""))
        self.entry_password.insert(0, login_info.get("password", ""))

    def save_login_info_to_file(self) -> None:
        """Kullanıcı adı ve parolayı onay mesajıyla kaydeder."""
        username = self.entry_username.get()
        password = self.entry_password.get()
        save_login_info(username, password, show_message=True)
    #endregion

    #region WiFi Bağlantı İşlemleri
    def connect(self) -> None:
        """Girilen kullanıcı bilgileriyle WiFi ağına bağlanır."""
        username = self.entry_username.get()
        password = self.entry_password.get()
        
        if save_login_info(username, password, show_message=False):
            response = self.connect_callback()
            if response and response.status_code == 200:
                self.image_connect_button_path = "icons/connected.png"
                self.update_button_image(self.image_connect_button_path)
                self.root.quit()

    def update_button_image(self, image_path: str) -> None:
        """Bağlantı düğmesinin görüntüsünü günceller.
        
        Argümanlar:
            image_path: Görüntü dosyasının yolu
        """
        self.image_connect_button = ctk.CTkImage(
        light_image=Image.open(image_path),
        dark_image=Image.open(image_path),
        size=(100, 100)
        )
        self.button_connect.configure(image=self.image_connect_button)
    #endregion

    #region Pencere Yönetimi
    def run(self) -> None:
        """Pencere ana döngüsünü çağırarak uygulamayı başlatır."""
        self.root.mainloop()

    def destroy(self) -> None:
        """Pencereyi kapatır ve kaynakları serbest bırakır."""
        self.root.destroy()
    #endregion
