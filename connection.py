"""Bu modül wifi.gsb.gov.tr'ye giriş yapmayı sağlar.

Bu modül, GSB WiFi portalına giriş endpoint'i aracılığıyla kimlik doğrulama 
işlevselliğini sağlar.
"""
#region Import'lar
import json
from tkinter import messagebox
import requests
from typing import Dict, Optional, Union, Tuple, Callable
from PIL import Image
#endregion


#region Durum İşleme
def print_status(statuscode: int) -> None:
    """HTTP durum koduna göre kullanıcı dostu bir mesaj yazdırır.
    
    Argümanlar:
        statuscode: Sunucudan dönen HTTP durum kodu
        
    Döndürür:
        None
    """
    statuscodes: Dict[int, str] = {
        200: "Başarılı",
        302: "Yönlendirme",
        401: "Yetkisiz Erişim",
        403: "Erişim Engellendi",
        404: "Sayfa Bulunamadı",
        500: "Sunucu Hatası",
        503: "Hizmet Kullanılamıyor"
    }
    messagebox.showinfo("Bilgi", statuscodes.get(statuscode, f"Bilinmeyen Durum: {statuscode}"))
#endregion


#region Giriş Bilgileri Yönetimi
def load_login_info() -> Dict[str, str]:
    """JSON dosyasından kaydedilmiş kullanıcı adı ve parolayı yükler.
    
    Döndürür:
        Dict[str, str]: Kullanıcı adı ve parola içeren dictionary
    """
    try:
        with open("login_info.json", "r", encoding="utf-8") as file:
            login_info: Dict[str, str] = json.load(file)
            return login_info
    except (FileNotFoundError, json.JSONDecodeError):
        return {"username": "", "password": ""}


def save_login_info(username: str, password: str, show_message: bool = True) -> bool:
    """Kullanıcı adı ve parolayı JSON dosyasına kaydeder.
    
    Argümanlar:
        username: Kaydedilecek kullanıcı adı
        password: Kaydedilecek parola
        show_message: Başarı mesajı gösterilip gösterilmeyeceği
        
    Döndürür:
        bool: Kimlik bilgileri başarıyla kaydedildiyse True, aksi halde False
    """
    if not username or not password:
        messagebox.showwarning("Uyarı", "Lütfen kullanıcı adını ve parolanı gir.")
        return False
        
    login_info = {
        "username": username,
        "password": password
    }

    try:
        with open("login_info.json", "w", encoding="utf-8") as file:
            json.dump(login_info, file)
        if show_message:
            messagebox.showinfo("Bilgi", "Kullanıcı adı ve parola kaydedildi.")
        return True
    except IOError as e:
        error_msg = f"Kullanıcı bilgileri kaydedilemedi: {e}" if show_message else "Kullanıcı bilgileri kaydedilemedi."
        messagebox.showerror("Hata", error_msg)
        return False
#endregion


#region WiFi Bağlantısı
def connect_to_wifi() -> Optional[requests.Response]:
    """Kaydedilmiş kimlik bilgilerini kullanarak wifi.gsb.gov.tr portalına giriş yapmayı dener.
    
    Bu işlev, login_info.json'dan giriş bilgilerini okur ve GSB WiFi giriş endpoint'ine
    bir POST isteği gönderir.
    
    Döndürür:
        Optional[requests.Response]: Başarılı olursa sunucu yanıtı, aksi halde None
    """
    try:
        with open("login_info.json", "r", encoding="utf-8") as file:
            login_info: Dict[str, str] = json.load(file)
            username = login_info.get("username", "")
            password = login_info.get("password", "")
            
            if not username or not password:
                messagebox.showerror("Hata", "Kullanıcı adı veya parola boş")
                return None
                
    except FileNotFoundError:
        messagebox.showerror("Hata", "Giriş bilgileri dosyası bulunamadı")
        return None
    except json.JSONDecodeError:
        messagebox.showerror("Hata", "Giriş bilgileri dosyası geçersiz")
        return None

    session = requests.Session()
    url = "https://wifi.gsb.gov.tr/login/j_spring_security_check"
    form = {
        "j_username": username,
        "j_password": password
    }

    # Login isteği gönder
    try:
        response = session.post(url, data=form, timeout=10)
        print_status(response.status_code)
        return response
    except requests.exceptions.Timeout:
        messagebox.showerror("Hata", "Bağlantı zaman aşımına uğradı")
        return None
    except requests.exceptions.ConnectionError:
        messagebox.showerror("Hata", "Sunucuya bağlanılamadı")
        return None
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Hata", f"Bağlantı hatası: {e}")
        return None
#endregion
