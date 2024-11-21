from modules.api_manager import get_api_client
from modules.country_league_selector import select_country_and_league
from modules.fixture_fetcher import fetch_fixtures
from modules.fixture_processor import process_fixture_data
from modules.data_processor import process_all_data
from modules.save_helpers import save_to_excel, generate_file_name
from modules.folder_manager import initialize_data_folder
from modules.run_analysis import run_all_analyses
from modules.data_splitter import split_processed_data
from modules.columns_selector import select_columns
from modules.ml_preparation import prepare_ml_data
from modules.ml_algorithms.logistic_regression_trainer import train_logistic_regression
from modules.ml_predictions import make_predictions

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

    # 6. Ham verileri Excel'e kaydet
    raw_file_name = generate_file_name(fixtures, season_year, "raw_fixtures")
    save_to_excel(fixtures_df, raw_file_name)
    print(f"Ham veriler Excel dosyasına kaydedildi: {raw_file_name}")

    # 7. İşlenmiş verileri daha fazla işlem yapmak için 'process_all_data' fonksiyonuna aktar
    processed_df = process_all_data(fixtures_df, season_year)

    # 8. İşlenmiş verileri Excel'e kaydet
    processed_file_name = generate_file_name(fixtures, season_year, "processed_fixtures")
    save_to_excel(processed_df, processed_file_name)
    print(f"İşlenmiş veriler Excel dosyasına kaydedildi: {processed_file_name}")

    # 9. İşlenmiş veriyi ayır
    print("Veri bölünüyor...")
    ml_df, prediction_df = split_processed_data(processed_df)
    print(f"ML için veri (ml_df) ve tahminler için veri (prediction_df) ayrıldı.")

    # 10. Analizlerin çalıştırılıp çalıştırılmayacağını sor
    run_analysis = input("Analizler uygulansın mı? (e/h): ").strip().lower()
    if run_analysis == "e":
        print("Analizler başlatılıyor...")
        run_all_analyses(ml_df)
        print("Analizler tamamlandı.")
    else:
        print("Analizler atlandı.")

    # 11. Kullanıcıdan sütun seçimlerini al
    print("\nML için sütun seçim aşamasına geçiliyor...")
    labels, features, selected_labels, selected_features = select_columns(ml_df)
    print(f"Labels ve features sütunları ayrıldı.")
    print(f"Labels sütunları: {selected_labels}")
    print(f"Features sütunları: {selected_features}")

    # 12. Seçilen sütunları ML veri hazırlık fonksiyonuna gönder
    print("\nML veri hazırlık aşamasına geçiliyor...")
    X_train_scaled, X_test_scaled, y_train_resampled, y_test = prepare_ml_data(
        ml_df, selected_features, selected_labels
    )
    print("ML veri hazırlık işlemi tamamlandı.")

    # 13. Logistic Regression ile model eğitimi ve değerlendirme
    print("\nLogistic Regression model eğitimi başlatılıyor...")
    model, predictions = train_logistic_regression(X_train_scaled, X_test_scaled, y_train_resampled, y_test)
    print("Logistic Regression modeli eğitimi ve değerlendirmesi tamamlandı.")

    # 14. Prediction işlemi
    print("\nPrediction işlemi başlatılıyor...")
    predicted_df = make_predictions(model, prediction_df, selected_features)
    if predicted_df is not None:
        print("Tahminler başarıyla tamamlandı. Sonuçlar aşağıda listeleniyor:\n")
        
        # Terminalde anlamlı bir şekilde tahmin sonuçlarını göster
        for _, row in predicted_df.iterrows():
            home_team = row.get("Home Team Name", "Unknown")
            away_team = row.get("Away Team Name", "Unknown")
            prediction = row.get("Prediction", "Unknown")
            print(f"{home_team} vs {away_team} - Tahmin: {prediction}")
    else:
        print("Prediction işlemi sırasında bir hata oluştu.")

if __name__ == "__main__":
    main()
