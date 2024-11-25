import os
import logging

def save_to_excel(df, file_name, folder_name="data"):
    """
    Verilen DataFrame'i belirtilen klasöre Excel dosyası olarak kaydeder.
    :param df: Kaydedilecek DataFrame.
    :param file_name: Dosya adı (ör. 'processed_data.xlsx').
    :param folder_name: Klasör adı (varsayılan: 'data').
    """
    # Klasör kontrolü ve oluşturma
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        logging.info(f"'{folder_name}' klasörü oluşturuldu.")

    # Dosya yolunu oluştur
    file_path = os.path.join(folder_name, file_name)

    # DataFrame'i Excel'e kaydet
    try:
        df.to_excel(file_path, index=False)
        logging.info(f"DataFrame '{file_path}' olarak başarıyla kaydedildi.")
    except Exception as e:
        logging.error(f"DataFrame '{file_path}' olarak kaydedilirken hata oluştu: {e}")


def generate_file_name(fixtures, season_year, data_type):
    """
    Dosya adı oluşturmak için ülke ve lig bilgilerini fixtures verisinden alır.
    Eğer fixtures boşsa varsayılan bir dosya adı döndürür.
    :param fixtures: Maç bilgilerini içeren liste.
    :param season_year: Sezon yılı.
    :param data_type: DataFrame türünü belirtir (ör. 'finished_fixtures').
    :return: Dosya adı.
    """
    if fixtures and len(fixtures) > 0:
        country_name = fixtures[0].get("league", {}).get("country", "unknown_country").replace(" ", "_")
        league_name = fixtures[0].get("league", {}).get("name", "unknown_league").replace(" ", "_")
        file_name = f"{country_name}_{league_name}_{season_year}_{data_type}.xlsx"
        logging.info(f"Dosya adı oluşturuldu: {file_name}")
        return file_name
    else:
        file_name = f"unknown_{season_year}_{data_type}.xlsx"
        logging.warning(f"Fixtures boş, varsayılan dosya adı oluşturuldu: {file_name}")
        return file_name