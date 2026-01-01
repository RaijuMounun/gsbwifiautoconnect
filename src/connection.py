"""
Bu modül GSB WiFi portalına bağlantı mantığını (Business Logic) içerir.
"""
import requests
from typing import Optional

# Custom Exceptions
class WifiConnectionError(Exception):
    """Genel bağlantı hataları için temel sınıf."""
    pass

class AuthenticationError(WifiConnectionError):
    """Kullanıcı adı veya şifre hatalıysa fırlatılır."""
    pass

class NetworkTimeoutError(WifiConnectionError):
    """Sunucuya ulaşılamadığında fırlatılır."""
    pass


def connect_to_wifi(username: str, password: str) -> requests.Response:
    """
    Verilen kimlik bilgileriyle GSB WiFi portalına bağlanır.
    
    Argümanlar:
        username (str): Kullanıcı adı
        password (str): Parola
        
    Döndürür:
        requests.Response: Başarılı sunucu yanıtı
        
    Hata Fırlatır (Raises):
        AuthenticationError: Giriş başarısızsa (401, 403 vb.)
        NetworkTimeoutError: Zaman aşımı olursa
        WifiConnectionError: Diğer bağlantı hataları
    """
    
    # Validation (Doğrulama) Logic Katmanında yapılır
    if not username or not password:
        raise ValueError("Kullanıcı adı veya parola boş olamaz.")

    session = requests.Session()
    # TODO: URL sabitleri normalde bir config dosyasında durmalı ama şimdilik burada kalsın.
    url = "https://wifi.gsb.gov.tr/login/j_spring_security_check"
    
    form_data = {
        "j_username": username,
        "j_password": password
    }

    try:
        # verify=False, bazen yurt ağlarında SSL sertifika sorunları olabildiği için eklenebilir
        # ama güvenlik için True olması iyidir. Şimdilik standart bırakıyoruz.
        response = session.post(url, data=form_data, timeout=10)
        
        # HTTP Hata kodlarını kontrol et ve Yorumla
        if response.status_code == 200:
            # GSB portalı bazen başarısız girişte de 200 dönebilir, 
            # içeriği kontrol etmek gerekebilir ama şimdilik status koda güveniyoruz.
            return response
            
        elif response.status_code in (401, 403):
            raise AuthenticationError("Kullanıcı adı veya şifre hatalı.")
            
        else:
            raise WifiConnectionError(f"Sunucu beklenmeyen bir kod döndürdü: {response.status_code}")

    except requests.exceptions.Timeout:
        raise NetworkTimeoutError("Bağlantı zaman aşımına uğradı. WiFi'a bağlı mısın?")
        
    except requests.exceptions.ConnectionError:
        raise WifiConnectionError("Sunucuya bağlanılamadı. İnternet bağlantını kontrol et.")
        
    except requests.exceptions.RequestException as e:
        raise WifiConnectionError(f"Beklenmeyen bir hata oluştu: {str(e)}")