import pandas as pd
from modules.fixture_processor import process_fixture_data
from modules.secondhalf_score import calculate_secondhalf_scores
from modules.result import calculate_match_result
from modules.total_goals import calculate_total_goals
from modules.over_under import calculate_over_under
from modules.goal_range import calculate_goal_range
from modules.both_team_score import calculate_both_team_score
from modules.cs_fail_score import calculate_clean_sheets_and_fail_to_score
from datetime import datetime, timedelta

def process_all_data(fixtures, season_year):
    """
    Process all data for fixtures by applying various calculations.
    :param fixtures: List of fixture data.
    :param season_year: Season year for fixtures.
    :return: Processed DataFrame with all calculations and upcoming matches.
    """
    # Ham veriyi işlenmiş DataFrame'e dönüştür
    df = process_fixture_data(fixtures, season_year)

    # Tarihleri datetime formatına dönüştür
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], format='%Y-%m-%d %H:%M:%S')

    # Sadece 'FT' olan maçları filtrele
    df_finished = df[df["Status Short"] == "FT"].copy()
    print(f"Toplam oynanmış maç sayısı: {len(df_finished)}")

    # Eksik verileri kontrol et ve "0" ile doldur
    columns_to_fill = [
        "Halftime Home Score", "Halftime Away Score",
        "Fulltime Home Score", "Fulltime Away Score"
    ]
    missing_counts = df_finished[columns_to_fill].isnull().sum()

    for column, missing_count in missing_counts.items():
        if missing_count > 0:
            print(f"{column} sütununda {missing_count} eksik değer bulundu ve '0' ile dolduruldu.")
        else:
            print(f"{column} sütununda eksik değer bulunamadı.")

    # Eksik değerleri "0" ile doldur
    df_finished[columns_to_fill] = df_finished[columns_to_fill].fillna(0)

    # Ek hesaplamaları sırayla uygula
    df_finished = calculate_secondhalf_scores(df_finished)
    df_finished = calculate_match_result(df_finished)
    df_finished = calculate_total_goals(df_finished)
    df_finished = calculate_over_under(df_finished)
    df_finished = calculate_goal_range(df_finished)
    df_finished = calculate_both_team_score(df_finished)
    df_finished = calculate_clean_sheets_and_fail_to_score(df_finished)

    # Bugün, yarın ve ertesi günün tarihlerini belirle
    today = datetime.now()
    tomorrow = today + timedelta(days=1)
    day_after_tomorrow = today + timedelta(days=2)

    # Tarih aralığındaki maçları filtrele
    upcoming_matches = df[
        (df["Timestamp"] >= today) &
        (df["Timestamp"] < day_after_tomorrow + timedelta(days=1))  # 3 günlük aralığı kapsar
    ].copy()

    print(f"Sıradaki üç gün içinde toplam {len(upcoming_matches)} maç bulundu.")

    return df_finished, upcoming_matches