"""
Bu modül, hassas verilerin (parola) güvenli bir şekilde saklanmasını yönetir.
Parolalar 'Keyring'de, ayarlar ise AppData klasöründe tutulur.
"""
import keyring
import json
import os
from pathlib import Path
from typing import Tuple

# Sabitler
SERVICE_ID = "GSB_Wifi_Auto_Connect"
APP_FOLDER_NAME = "GSB_Wifi_Connect_App" # Klasör adı net olsun
CONFIG_FILENAME = "user_preferences.json" # Dosya adı net olsun

class CredentialManager:
    """Kimlik bilgilerini ve ayarları yöneten sınıf."""

    def __init__(self):
        # Sınıf başlatıldığında config dosyasının yolunu hesapla
        self.config_path = self._get_config_path()

    def _get_config_path(self) -> Path:
        """
        İşletim sistemine uygun veri saklama yolunu bulur ve oluşturur.
        Windows: %LOCALAPPDATA%/GSB_Wifi_Connect_App/user_preferences.json
        Linux/Mac: ~/.config/GSB_Wifi_Connect_App/user_preferences.json
        """
        if os.name == 'nt':  # Windows
            base_path = os.getenv('LOCALAPPDATA')
            if not base_path:
                base_path = os.path.expanduser("~") # Fallback
            base_dir = Path(base_path)
        else:  # Linux / Mac
            base_dir = Path.home() / ".config"

        # Klasör yolunu oluştur
        app_dir = base_dir / APP_FOLDER_NAME
        
        # Eğer klasör yoksa oluştur (Sessizce)
        app_dir.mkdir(parents=True, exist_ok=True)
        
        return app_dir / CONFIG_FILENAME

    def save_credentials(self, username: str, password: str) -> None:
        """Kullanıcı adını AppData'ya, parolayı Keyring'e kaydeder."""
        if not username or not password:
            raise ValueError("Kullanıcı adı ve parola boş olamaz.")

        # 1. Parolayı Güvenli Kasaya at
        try:
            keyring.set_password(SERVICE_ID, username, password)
        except Exception as e:
            print(f"Keyring hatası: {e}")
            raise e

        # 2. Kullanıcı adını gizli config dosyasına yaz
        config_data = {"last_username": username}
        
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(config_data, f)
        except IOError as e:
            print(f"Config dosyası yazılamadı: {e}")

    def get_last_credentials(self) -> Tuple[str, str]:
        """Kayıtlı bilgileri getirir."""
        username = ""
        
        # 1. Dosyadan kullanıcı adını oku
        if self.config_path.exists():
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    username = data.get("last_username", "")
            except (json.JSONDecodeError, IOError):
                pass # Dosya bozuksa veya okunamıyorsa dert etme

        if not username:
            return "", ""

        # 2. Şifreyi kasadan çek
        try:
            password = keyring.get_password(SERVICE_ID, username)
            if password is None:
                return username, ""
            return username, password
        except Exception:
            return username, ""

    def delete_credentials(self, username: str) -> None:
        """Şifreyi kasadan siler."""
        try:
            keyring.delete_password(SERVICE_ID, username)
            # İstersen config dosyasını da silebilirsin ama gerek yok, overwite ediliyor zaten.
        except Exception:
            pass