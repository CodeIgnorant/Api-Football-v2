import os
from modules.api.api_manager import get_api_client
from modules.api.country_league_selector import select_country_and_league
from modules.api.fixture_fetcher import fetch_fixtures
from modules.api.fixture_processor import process_fixture_data
from modules.processing.data_processor import process_all_data
from modules.io.folder_manager import initialize_data_folder
from modules.analysis.run_analysis import run_all_analyses
from modules.processing.data_splitter import split_processed_data

def main():
    """
    Programın ana fonksiyonu.
    """
    # 1. 'data' klasörünü temizle ve yeniden oluştur
    initialize_data_folder()

    # 2. API Bağlantısını Test Et ve Al
    api_client = get_api_client()

    # 3. Kullanıcıdan ülke ve lig seçimini al
    league_id, season_year = select_country_and_league(api_client)

    # 4. Seçilen lig ve sezonun maçlarını indir
    fixtures = fetch_fixtures(api_client, league_id, season_year)

    # 5. Maç verilerini işleyerek DataFrame'e dönüştür
    fixtures_df = process_fixture_data(fixtures, season_year)

    # 6. Ham verileri CSV'ye kaydet
    raw_file_name = os.path.join("data", "raw.csv")
    fixtures_df.to_csv(raw_file_name, index=False, float_format="%.2f", decimal=".")
    print(f"Ham veriler CSV dosyasına kaydedildi: {raw_file_name}")

    # 7. İşlenmiş verileri daha fazla işlem yapmak için 'process_all_data' fonksiyonuna aktar
    processed_df = process_all_data(fixtures_df, season_year)

    # 8. İşlenmiş verileri CSV'ye kaydet
    processed_file_name = os.path.join("data", "data.csv")
    processed_df.to_csv(processed_file_name, index=False, float_format="%.2f", decimal=".")
    print(f"İşlenmiş veriler CSV dosyasına kaydedildi: {processed_file_name}")

    # 9. İşlenmiş veriyi ayır
    print("Veri bölünüyor...")
    ml_df, prediction_df = split_processed_data(processed_df)
    print(f"ML için veri (ml_df) ve tahminler için veri (prediction_df) ayrıldı.")

    # ML verisi için CSV kaydetme
    ml_file_name = os.path.join("data", "ml.csv")
    ml_df.to_csv(ml_file_name, index=False, float_format="%.2f", decimal=".")
    print(f"ML için veri CSV dosyasına kaydedildi: {ml_file_name}")

    # Prediction verisi için CSV kaydetme
    prediction_file_name = os.path.join("data", "prediction.csv")
    prediction_df.to_csv(prediction_file_name, index=False, float_format="%.2f", decimal=".")
    print(f"Tahmin için veri CSV dosyasına kaydedildi: {prediction_file_name}")

    # 10. Analizlerin çalıştırılıp çalıştırılmayacağını sor
    run_analysis = input("Analizler uygulansın mı? (e/h): ").strip().lower()
    if run_analysis == "e":
        print("Analizler başlatılıyor...")
        run_all_analyses(ml_df)
        print("Analizler tamamlandı.")
    else:
        print("Analizler atlandı.")

if __name__ == "__main__":
    main()