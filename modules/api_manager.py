from modules.api_client import APIClient
import logging

# Loglama yapılandırması
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_api_client():
    """
    API bağlantısını test eder ve geçerli bir APIClient örneği döner.
    Bağlantı başarısızsa None döner.
    """
    logging.info("API bağlantısı test ediliyor...")
    api_client = APIClient()
    
    if api_client.test_connection():
        logging.info("API bağlantısı başarılı!")
        return api_client
    else:
        logging.error("API bağlantısı başarısız. Lütfen API anahtarını kontrol edin.")
        return None