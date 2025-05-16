"""GSB WiFi Auto Connect Uygulaması.

Bu uygulama, GSB yurt WiFi ağına otomatik olarak bağlanmak için basit bir
kullanıcı arayüzü sağlar. Giriş bilgilerini otomatik olarak kaydeder ve
kullanarak sorunsuz bağlantı sunar.

Örnek:
    Sadece script'i çalıştırarak uygulamayı başlatabilirsiniz (exe kullanmıyorsanız):
        $ python main.py
"""

from src.ui import WindowMain
from src.connection import connect_to_wifi

if __name__ == "__main__":
    ui = WindowMain(connect_to_wifi)
    ui.run()
