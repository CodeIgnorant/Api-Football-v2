from modules.ml_halftime_metrics import calculate_halftime_metrics
from modules.ml_secondhalf_metrics import calculate_secondhalf_metrics
from modules.ml_fulltime_metrics import calculate_fulltime_metrics
from modules.ml_result_win_rates import calculate_result_win_rates

def process_ml_data(df_finished):
    """
    Verilen DataFrame'i ML için hazır hale getirir.
    :param df_finished: İşlenmiş ve oynanmış maçları içeren DataFrame.
    :return: ML için hazırlanmış yeni bir DataFrame (ml_df).
    """
    # 1. Başlangıçta df_finished'deki tüm sütunları ml_df'ye kopyala
    ml_df = df_finished.copy()

    # 2. Gereksiz sütunları kaldır
    columns_to_drop = [
        "Fixture ID", "Timestamp", "Status Long", "Status Short",
        "League ID", "League Name", "League Country", "League Season",
        "Home Team Name", "Away Team Name"  # Eklenen sütunlar
    ]
    ml_df = ml_df.drop(columns=columns_to_drop, errors='ignore')

    # 3. Round sütununu sayısal bir değere dönüştür
    ml_df['Round'] = ml_df['Round'].apply(
        lambda x: int(x.split("-")[-1].strip()) if "-" in x else None
    )

    # 4. Round sütununa göre veriyi sıralama
    ml_df = ml_df.sort_values(by='Round').reset_index(drop=True)

    # 5. Halftime metrics hesaplama
    ml_df = calculate_halftime_metrics(ml_df)

    # 6. Second half metrics hesaplama
    ml_df = calculate_secondhalf_metrics(ml_df)

    # 7. Fulltime metrics hesaplama
    ml_df = calculate_fulltime_metrics(ml_df)

    # 8. Result-based win rates hesaplama
    ml_df = calculate_result_win_rates(ml_df)

    # 9. Sütunları sıralama
    columns_order = [
        # Features
        "Round", "Home Team ID", "Away Team ID", 
        "Halftime Cumulative Goals - Home", "Halftime Average Goals - Home", "Halftime Scoring Rate - Home",
        "Halftime Cumulative Goals - Away", "Halftime Average Goals - Away", "Halftime Scoring Rate - Away",
        "Second Half Cumulative Goals - Home", "Second Half Average Goals - Home", "Second Half Scoring Rate - Home",
        "Second Half Cumulative Goals - Away", "Second Half Average Goals - Away", "Second Half Scoring Rate - Away",
        "Fulltime Cumulative Goals - Home", "Fulltime Average Goals - Home", "Fulltime Scoring Rate - Home",
        "Fulltime Cumulative Goals - Away", "Fulltime Average Goals - Away", "Fulltime Scoring Rate - Away",
        "Home Fulltime Result Home Win", "Home Fulltime Result Away Win", "Home Fulltime Result Draw",
        "Away Fulltime Result Home Win", "Away Fulltime Result Away Win", "Away Fulltime Result Draw",
        "Home Halftime Result Home Win", "Home Halftime Result Away Win", "Home Halftime Result Draw",
        "Away Halftime Result Home Win", "Away Halftime Result Away Win", "Away Halftime Result Draw",
        "Home Secondhalf Result Home Win", "Home Secondhalf Result Away Win", "Home Secondhalf Result Draw",
        "Away Secondhalf Result Home Win", "Away Secondhalf Result Away Win", "Away Secondhalf Result Draw",
        # Labels
        "Halftime Total Goals", "Secondhalf Total Goals", "Fulltime Total Goals", "Goal Range", "Both Team Score",
        "Fulltime Home Over 0.5", "Fulltime Home Over 1.5", "Fulltime Home Over 2.5", "Fulltime Home Over 3.5",
        "Fulltime Away Over 0.5", "Fulltime Away Over 1.5", "Fulltime Away Over 2.5", "Fulltime Away Over 3.5",
        "Fulltime Over 0.5", "Fulltime Over 1.5", "Fulltime Over 2.5", "Fulltime Over 3.5",
        "Halftime Home Clean Sheet", "Halftime Away Clean Sheet", "Secondhalf Home Clean Sheet", "Secondhalf Away Clean Sheet",
        "Fulltime Home Clean Sheet", "Fulltime Away Clean Sheet", "Halftime Home Fail to Score", "Halftime Away Fail to Score",
        "Secondhalf Home Fail to Score", "Secondhalf Away Fail to Score", "Fulltime Home Fail to Score", "Fulltime Away Fail to Score",
        "Fulltime Result", "Halftime Result", "Secondhalf Result"
    ]

    # Sütun sırasını düzenle
    ml_df = ml_df[columns_order]

    return ml_df