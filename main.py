from modules.api_manager import get_api_client
from modules.country_league_selector import select_country_and_league
from modules.fixture_fetcher import fetch_fixtures
from modules.fixture_processor import process_fixture_data
from modules.data_processor import process_all_data
from modules.save_helpers import save_to_excel, generate_file_name
from modules.ml_processor import process_ml_data
from modules.folder_manager import initialize_data_folder
from modules.run_analysis import run_all_analyses
from modules.run_ml_training import run_ml_training

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

    # Tüm maç verilerini işleyerek DataFrame oluştur
    fixtures_df = process_fixture_data(fixtures, season_year)
    
    # Tüm maçları içeren DataFrame'i kaydet
    fixtures_file_name = generate_file_name(fixtures, season_year, "all_fixtures")
    save_to_excel(fixtures_df, fixtures_file_name)

    # 5. Tüm veriyi işleyerek genişletilmiş DataFrame ve sıradaki maçları oluştur
    df_finished, upcoming_matches = process_all_data(fixtures, season_year)

    # 6. Tüm maçları içeren genişletilmiş DataFrame'i Excel'e kaydet
    processed_file_name = generate_file_name(fixtures, season_year, "finished_fixtures")
    save_to_excel(df_finished, processed_file_name)

    # 7. Sıradaki maçları içeren DataFrame'i Excel'e kaydet
    upcoming_matches_file_name = generate_file_name(fixtures, season_year, "upcoming_matches")
    save_to_excel(upcoming_matches, upcoming_matches_file_name)

    # 8. ML için gerekli DataFrame'i hazırla
    ml_df = process_ml_data(df_finished)

    # 9. ML için hazırlanmış veriyi kaydet
    ml_file_name = generate_file_name(fixtures, season_year, "ml_ready")
    save_to_excel(ml_df, ml_file_name)

    # 10. ML verisi üzerinde analizleri çalıştır
    run_all_analyses(ml_df)

    # 11. ML modellerini eğit ve değerlendir
    run_ml_training(ml_df)

if __name__ == "__main__":
    main()