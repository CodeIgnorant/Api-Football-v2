import os
import shutil
import logging

# Loglama yapılandırması
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def initialize_data_folder(folder_name="data"):
    """
    Verilen klasörü temizler ve yeniden oluşturur.
    :param folder_name: Temizlenecek ve yeniden oluşturulacak klasör adı.
    """
    if os.path.exists(folder_name):
        logging.info(f"'{folder_name}' klasörü mevcut. İçerik temizleniyor...")
        shutil.rmtree(folder_name)  # Mevcut klasörü ve içindekileri sil
        logging.info(f"'{folder_name}' klasörü silindi.")
    else:
        logging.info(f"'{folder_name}' klasörü mevcut değil. Yeni oluşturulacak.")
        
    os.makedirs(folder_name)  # Yeni ve temiz bir klasör oluştur
    logging.info(f"'{folder_name}' klasörü temizlendi ve yeniden oluşturuldu.")