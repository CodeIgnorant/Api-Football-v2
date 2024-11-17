from modules.api_client import APIClient

def get_api_client():
    """
    API bağlantısını test eder ve geçerli bir APIClient örneği döner.
    Bağlantı başarısızsa None döner.
    """
    print("API bağlantısı test ediliyor...")
    api_client = APIClient()
    if api_client.test_connection():
        print("API bağlantısı başarılı!")
        return api_client
    else:
        print("API bağlantısı başarısız. Lütfen API anahtarını kontrol edin.")
        return None