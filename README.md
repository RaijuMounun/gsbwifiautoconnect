# GSB WiFi Auto Connect

Bu uygulama, GSB (Gençlik ve Spor Bakanlığı) yurdu internet ağına **otomatik ve hızlı bir şekilde** bağlanmak için geliştirilmiş basit bir arayüz sunar.

## Neden Bu Uygulama?

Normal şartlarda GSB WiFi'ına bağlanmak oldukça zahmetli bir süreç:
1. Önce cihazı WiFi'a bağlamanız
2. Otomatik açılan GSB internet sitesinde kullanıcı adı ve şifre girmeniz 
3. Açılan sayfada bağlan tuşuna basmanız gerekiyor

Bu süreç genellikle çok yavaş ilerliyor çünkü:
- GSB internet altyapısı yavaş çalışıyor
- Tarayıcılar güvenlik uyarıları göstererek işlemi zorlaştırıyor
- Her defasında kimlik bilgilerini manuel girmek zaman alıyor

**Bu uygulama ile tüm bu süreci otomatikleştirdim.** 

## Özellikler

- Tamamen Türkçe kullanıcı arayüzü
- Basit ve kullanıcı dostu arayüz
- Giriş bilgilerini kaydetme
- Tek tıkla WiFi bağlantısı (tarayıcı açmadan)
- Bağlantı durumu görsel geri bildirimi
- Hızlı ve otomatik bağlantı süreci

## Kullanım Kılavuzu

### Exe Dosyası İle Kullanım (Önerilen)

1. [Releases](https://github.com/RaijuMounun/gsbwifiautoconnect/releases) sayfasından v0.2 sürümünü indirin
2. İndirdiğiniz .exe dosyasını çalıştırın (Herhangi bir kurulum gerekmez)
3. Kullanıcı adınızı ve parolanızı girin
4. Bilgileri kaydetmek için "Kaydet" düğmesine tıklayın
5. WiFi'a bağlanmak için bağlantı düğmesine tıklayın

**Not**: Exe dosyası tüm gerekli bileşenleri içerir, ayrıca Python veya başka bir program yüklemeniz gerekmez. Programı çalıştırdığınızda uyarı verebilir. Bu tarz programların imza süreçleri falan çok sorunlu. "Yine de çalıştır" diyerek programı çalıştırabilirsiniz.

### Kaynak Kod İle Geliştirme (Geliştiriciler İçin)

Eğer uygulamayı kendiniz geliştirmek veya değiştirmek istiyorsanız:

#### Gereksinimler

- Python 3.6 veya üstü
- Aşağıdaki Python paketleri (requirements.txt dosyasında listelenmiştir):
  - customtkinter>=5.2.0
  - pillow>=9.0.0
  - requests>=2.28.0

#### Kurulum Adımları

1. Projeyi bilgisayarınıza indirin:
   ```bash
   git clone https://github.com/RaijuMounun/gsbwifiautoconnect.git
   ```

2. Gerekli paketleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```
   
3. Uygulamayı çalıştırın:
   ```bash
   python main.py
   ```

## Proje kodları ve arayüzü Türkçe

- **Türkçe Arayüz**: Önceki sürümde Ingilizce olan uygulama arayüzünü Türkçe'ye çevirdim.
- **Türkçe Kod Yorumları**: Önceki sürümde Ingilizce olan tüm kod yorumlarını ve dokümantasyonu Türkçe'ye çevirdim.
- **Bölge İşaretçileri**: Kodun anlaşılması daha kolay olsun diye içerisinde `#region` ve `#endregion` etiketleri ile bölümler oluşturdum.

Bu sayede anadili Türkçe olanlar için kod daha anlaşılır ve bakımı daha kolay hale geldi. 

## Nasıl Çalışır?

1. Uygulama, GSB WiFi portalıyla doğrudan iletişim kurar, tarayıcı açmaya gerek kalmaz
2. Kullanıcı bilgileriniz yerel bir JSON dosyasında *şifrelenmeden* saklanır (login_info.json). Giriş bilgileriniz sadece sizin bilgisayarınızda saklanır. Başka herhangi bir yere gönderilmez.
   2,5. Kullanıcı bilgilerinizi tutan JSON dosyası .exe dosyasının bulunduğu konuma oluşturuluyor. O yüzden tavsiyem programlarınızı tuttuğunuz klasöre, GsbWifiAutoConnect için de bir klasör oluşturup .exe dosyasını orada tutmanız. Masaüstü kısayolu oluşturmak için: 
   1- .exe dosyasına sağ tıklayın
   2- Açılan pencerede en altta "Daha fazla seçenek göster" tuşuna tıklayın.
   3- Açılan pencerede 'Gönder' kısmına gelin.
   4- Açılan küçük pencerede "Masaüstü (kısayol oluştur)" seçeneğini seçin.
3. Bağlan düğmesine bastığınızda, uygulama otomatik olarak GSB WiFi portalına giriş yapar
4. Bağlantı başarılı olduğunda, program otomatik olarak kendini kapatır.

## Lisans

Bu proje açık kaynak olarak paylaşılmıştır.

## Geliştirici

Eren Keskinoğlu

[Instagram](https://www.instagram.com/erenzapkinus) [@erenzapkinus]


