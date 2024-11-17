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

    return ml_df