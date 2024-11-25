import requests
import logging
import os

# Loglama yapılandırması
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Config:
    # Çevre değişkenlerinden API URL'sini yükler veya varsayılan değeri kullanır
    api_url = os.getenv('API_URL', "https://v3.football.api-sports.io")
    
    # Çevre değişkenlerinden API anahtarını yükler; geliştirme için varsayılan bir anahtar sağlar
    api_key = os.getenv('API_KEY', 'your_test_api_key')

class APIClient:
    def __init__(self):
        """
        Config sınıfından alınan API detayları ile APIClient'ı başlatır.
        """
        # API URL ve anahtarını al
        self.base_url = Config.api_url
        self.api_key = Config.api_key
        self.timezone = "Europe/Istanbul"  # Sabit zaman dilimi ayarı

        # API Anahtarını doğrula
        if not self.api_key:
            logging.critical("API Anahtarı bulunamadı. Lütfen geçerli bir anahtar sağlayın.")
            raise ValueError("API Anahtarı bulunamadı.")
        else:
            logging.info(f"API Anahtarı başarıyla alındı: {self.api_key[:4]}****")

        # Header bilgilerini ayarla
        self.headers = {
            "x-apisports-key": self.api_key
        }

    def test_connection(self):
        """
        API bağlantısını test eder.
        """
        try:
            response = requests.get(self.base_url, headers=self.headers, timeout=10)
            response.raise_for_status()  # Hata durumunda istisna fırlatır
            logging.info("API bağlantısı testi tamamlandı ve başarılı.")
            return True
        except requests.exceptions.RequestException as req_err:
            logging.error(f"API bağlantısı başarısız! Hata: {req_err}")
            return False

    def send_request(self, endpoint, **kwargs):
        """
        Genel bir API isteği yapar.
        :param endpoint: Erişim sağlanacak API uç noktası.
        :param kwargs: İsteğe gönderilecek isteğe bağlı parametreler.
        """
        # Uç nokta için tam URL'yi oluştur
        url = f"{self.base_url}/{endpoint}"

        try:
            # Parametrelerle birlikte GET isteği gönder
            response = requests.get(url, headers=self.headers, params=kwargs, timeout=10)
            response.raise_for_status()  # HTTP hatalarını kontrol et

            # Tüm URL'yi ve parametreleri logla
            logging.info(f"Tam URL ve parametreler: {response.url}")
            logging.info("API isteği başarılı!")

            return response.json()  # Yanıtı JSON formatında döndür
        except requests.exceptions.HTTPError as http_err:
            logging.error(f"HTTP hatası oluştu: {http_err}")
        except requests.exceptions.RequestException as req_err:
            logging.error(f"API isteği sırasında bir hata oluştu: {req_err}")
            return {"error": f"API isteği başarısız oldu. Detay: {req_err}"}