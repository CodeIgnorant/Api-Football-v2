import os
import shutil

def initialize_data_folder(folder_name="data"):
    """
    Verilen klasörü temizler ve yeniden oluşturur.
    :param folder_name: Temizlenecek ve yeniden oluşturulacak klasör adı.
    """
    if os.path.exists(folder_name):
        shutil.rmtree(folder_name)  # Mevcut klasörü ve içindekileri sil
    os.makedirs(folder_name)  # Yeni ve temiz bir klasör oluştur
    print(f"'{folder_name}' klasörü temizlendi ve yeniden oluşturuldu.")