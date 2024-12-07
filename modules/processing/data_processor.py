import pandas as pd
from modules.processing.secondhalf_score import calculate_secondhalf_scores
from modules.processing.result import calculate_match_result
from modules.processing.total_goals import calculate_total_goals
from modules.processing.over_under import calculate_over_under
from modules.processing.goal_range import calculate_goal_range
from modules.processing.both_team_score import calculate_both_team_score
from modules.processing.cs_fail_score import calculate_clean_sheets_and_fail_to_score
from modules.processing.ml_halftime_metrics import calculate_halftime_metrics
from modules.processing.ml_secondhalf_metrics import calculate_secondhalf_metrics
from modules.processing.ml_fulltime_metrics import calculate_fulltime_metrics
from modules.processing.ml_result_win_rates import calculate_result_win_rates
from modules.processing.binary_win import calculate_binary_win
from modules.processing.point_calculator import calculate_points
from datetime import datetime, timedelta

def process_all_data(df, season_year):
    """
    Verilen tüm maçlar üzerinde işlem yapar.
    Gereksiz maçları filtreler, Round sütununu sayısallaştırır ve hesaplamaları yapar.
    Eksik verileri yalnızca tamamlanmış maçlar için doldurur ve ardından tüm maçlar için ML metriklerini hesaplar.
    :param df: İşlenecek tüm maçları içeren DataFrame.
    :param season_year: Sezon yılı.
    :return: İşlenmiş DataFrame.
    """

    # Timestamp sütununu datetime formatına dönüştür
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], format='%Y-%m-%d %H:%M:%S')

    # 1. Status Short ve Timestamp'e göre gereksiz maçları çıkar
    today = datetime.now()
    tomorrow = today + timedelta(days=1)
    day_after_tomorrow = today + timedelta(days=2)

    df = df[
        (df["Status Short"] == "FT") | 
        ((df["Timestamp"] >= today) & (df["Timestamp"] < day_after_tomorrow + timedelta(days=1)))
    ]
    print(f"Kalan maç sayısı: {len(df)}")

    # 2. Round sütununu sayısal bir değere dönüştür
    try:
        df['Round'] = df['Round'].apply(
            lambda x: int(x.split("-")[-1].strip()) if "-" in x else None
        )
        print("Round sütunu başarıyla sayısal değerlere dönüştürüldü.")
    except Exception as e:
        print(f"Round sütunu dönüştürülürken bir hata oluştu: {e}")

    # 3. Status Short ve Round sütunlarına göre veriyi sıralama
    df = df.sort_values(by=['Status Short', 'Round'], ascending=[True, True]).reset_index(drop=True)
    print("DataFrame, Status Short ve Round sütunlarına göre sıralandı.")

    # 4. Eksik verileri doldurma
    columns_to_fill = [
        "Halftime Home Score", "Halftime Away Score",
        "Fulltime Home Score", "Fulltime Away Score"
    ]

    missing_counts = df.loc[df["Status Short"] == "FT", columns_to_fill].isnull().sum()

    for column, missing_count in missing_counts.items():
        if missing_count > 0:
            print(f"{column} sütununda {missing_count} eksik değer bulundu ve '0' ile dolduruldu.")
        else:
            print(f"{column} sütununda eksik değer bulunamadı.")

    # Eksik değerleri doldur
    df.loc[df["Status Short"] == "FT", columns_to_fill] = df.loc[df["Status Short"] == "FT", columns_to_fill].fillna(0)

    # 5. Tamamlanmış maçlar için hesaplamalar
    df = calculate_secondhalf_scores(df)
    df = calculate_match_result(df)
    df = calculate_binary_win(df)
    df = calculate_total_goals(df)
    df = calculate_over_under(df)
    df = calculate_goal_range(df)
    df = calculate_both_team_score(df)
    df = calculate_clean_sheets_and_fail_to_score(df)
    df = calculate_points(df)
    print("Tamamlanmış maçlar için hesaplamalar tamamlandı.")

    # 6. Tüm maçlar için ML metriklerini hesaplama
    df = calculate_halftime_metrics(df)
    df = calculate_secondhalf_metrics(df)
    df = calculate_fulltime_metrics(df)
    df = calculate_result_win_rates(df)
    print("Tüm maçlar için ML metrikleri hesaplandı.")

    return df