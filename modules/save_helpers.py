import os

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
        print(f"'{folder_name}' klasörü oluşturuldu.")

    # Dosya yolunu oluştur
    file_path = os.path.join(folder_name, file_name)

    # DataFrame'i Excel'e kaydet
    df.to_excel(file_path, index=False)
    print(f"DataFrame '{file_path}' olarak kaydedildi.")


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
        return f"{country_name}_{league_name}_{season_year}_{data_type}.xlsx"
    else:
        return f"unknown_{season_year}_{data_type}.xlsx"