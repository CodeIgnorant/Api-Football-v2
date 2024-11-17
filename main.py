from modules.api_manager import get_api_client
from modules.country_league_selector import select_country_and_league
from modules.fixture_fetcher import fetch_fixtures
from modules.data_processor import process_all_data
from modules.save_helpers import save_to_excel, generate_file_name
from modules.ml_processor import process_ml_data

def main():
    """
    Programın ana fonksiyonu.
    """
    # 1. API Bağlantısını Test Et ve Al
    api_client = get_api_client()

    # 2. Kullanıcıdan ülke ve lig seçimini al
    league_id, season_year = select_country_and_league(api_client)

    # 3. Seçilen lig ve sezonun maçlarını indir
    fixtures = fetch_fixtures(api_client, league_id, season_year)

    # 4. Tüm veriyi işleyerek genişletilmiş DataFrame oluştur
    df_finished = process_all_data(fixtures, season_year)

    # 5. DataFrame'i Excel'e kaydet
    processed_file_name = generate_file_name(fixtures, season_year, "finished_fixtures")
    save_to_excel(df_finished, processed_file_name)

    # 6. ML için gerekli DataFrame'i hazırla
    ml_df = process_ml_data(df_finished)

    # 7. ML için hazırlanmış veriyi kaydet
    ml_file_name = generate_file_name(fixtures, season_year, "ml_ready")
    save_to_excel(ml_df, ml_file_name)

if __name__ == "__main__":
    main()