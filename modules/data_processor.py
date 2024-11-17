from modules.fixture_processor import process_fixture_data
from modules.secondhalf_score import calculate_secondhalf_scores
from modules.result import calculate_match_result
from modules.total_goals import calculate_total_goals
from modules.over_under import calculate_over_under
from modules.goal_range import calculate_goal_range
from modules.both_team_score import calculate_both_team_score
from modules.cs_fail_score import calculate_clean_sheets_and_fail_to_score

def process_all_data(fixtures, season_year):
    """
    Process all data for fixtures by applying various calculations.
    :param fixtures: List of fixture data.
    :param season_year: Season year for fixtures.
    :return: Processed DataFrame with all calculations.
    """
    # Ham veriyi işlenmiş DataFrame'e dönüştür
    df = process_fixture_data(fixtures, season_year)

    # Sadece 'FT' olan maçları filtrele
    df_finished = df[df["Status Short"] == "FT"].copy()
    print(f"Toplam oynanmış maç sayısı: {len(df_finished)}")

    # Ek hesaplamaları sırayla uygula
    df_finished = calculate_secondhalf_scores(df_finished)
    df_finished = calculate_match_result(df_finished)
    df_finished = calculate_total_goals(df_finished)
    df_finished = calculate_over_under(df_finished)
    df_finished = calculate_goal_range(df_finished)
    df_finished = calculate_both_team_score(df_finished)
    df_finished = calculate_clean_sheets_and_fail_to_score(df_finished)

    return df_finished