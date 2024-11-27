import logging

def calculate_result_win_rates(df):
    """
    Her bir takım için Fulltime, Halftime ve Secondhalf sonuçlarına dayalı kazanma, kaybetme ve beraberlik oranlarını hesaplar.
    Aşağıdaki sütunlar oluşturulur:
    - Home Fulltime Result Home Win
    - Home Fulltime Result Away Win
    - Home Fulltime Result Draw
    - Away Fulltime Result Home Win
    - Away Fulltime Result Away Win
    - Away Fulltime Result Draw
    - (Halftime ve Secondhalf sonuçları için de benzer sütunlar)

    :param df: ML için hazırlanmakta olan DataFrame.
    :return: Güncellenmiş df.
    """
    def calculate_rate(row, team_id_column, result_value, result_column):
        """
        Belirli bir takımın belirli bir sonuç oranını hesaplar.
        :param row: ML DataFrame'deki bir satır.
        :param team_id_column: Takım ID'sini belirten sütun (ör. 'Home Team ID').
        :param result_value: Hedef sonuç (1: kazanma, 0: beraberlik, 2: kaybetme).
        :param result_column: Hedef sonuç sütunu (ör. 'Fulltime Result').
        :return: Belirtilen sonucun oranı.
        """
        team_id = row[team_id_column]
        past_matches = df[
            (df[team_id_column] == team_id) & (df["Round"] < row["Round"])
        ]
        total_matches = past_matches.shape[0]
        if total_matches == 0:
            return 0
        return past_matches[past_matches[result_column] == result_value].shape[0] / total_matches

    # Fulltime Result oranları
    df["Home Fulltime Result Home Win"] = df.apply(
        lambda row: calculate_rate(row, "Home Team ID", 1, "Fulltime Result"), axis=1
    )
    df["Home Fulltime Result Away Win"] = df.apply(
        lambda row: calculate_rate(row, "Home Team ID", 2, "Fulltime Result"), axis=1
    )
    df["Home Fulltime Result Draw"] = df.apply(
        lambda row: calculate_rate(row, "Home Team ID", 0, "Fulltime Result"), axis=1
    )
    df["Away Fulltime Result Home Win"] = df.apply(
        lambda row: calculate_rate(row, "Away Team ID", 1, "Fulltime Result"), axis=1
    )
    df["Away Fulltime Result Away Win"] = df.apply(
        lambda row: calculate_rate(row, "Away Team ID", 2, "Fulltime Result"), axis=1
    )
    df["Away Fulltime Result Draw"] = df.apply(
        lambda row: calculate_rate(row, "Away Team ID", 0, "Fulltime Result"), axis=1
    )
    logging.info("Fulltime sonuç oranları başarıyla hesaplandı.")

    # Halftime Result oranları
    df["Home Halftime Result Home Win"] = df.apply(
        lambda row: calculate_rate(row, "Home Team ID", 1, "Halftime Result"), axis=1
    )
    df["Home Halftime Result Away Win"] = df.apply(
        lambda row: calculate_rate(row, "Home Team ID", 2, "Halftime Result"), axis=1
    )
    df["Home Halftime Result Draw"] = df.apply(
        lambda row: calculate_rate(row, "Home Team ID", 0, "Halftime Result"), axis=1
    )
    df["Away Halftime Result Home Win"] = df.apply(
        lambda row: calculate_rate(row, "Away Team ID", 1, "Halftime Result"), axis=1
    )
    df["Away Halftime Result Away Win"] = df.apply(
        lambda row: calculate_rate(row, "Away Team ID", 2, "Halftime Result"), axis=1
    )
    df["Away Halftime Result Draw"] = df.apply(
        lambda row: calculate_rate(row, "Away Team ID", 0, "Halftime Result"), axis=1
    )
    logging.info("Halftime sonuç oranları başarıyla hesaplandı.")

    # Secondhalf Result oranları
    df["Home Secondhalf Result Home Win"] = df.apply(
        lambda row: calculate_rate(row, "Home Team ID", 1, "Secondhalf Result"), axis=1
    )
    df["Home Secondhalf Result Away Win"] = df.apply(
        lambda row: calculate_rate(row, "Home Team ID", 2, "Secondhalf Result"), axis=1
    )
    df["Home Secondhalf Result Draw"] = df.apply(
        lambda row: calculate_rate(row, "Home Team ID", 0, "Secondhalf Result"), axis=1
    )
    df["Away Secondhalf Result Home Win"] = df.apply(
        lambda row: calculate_rate(row, "Away Team ID", 1, "Secondhalf Result"), axis=1
    )
    df["Away Secondhalf Result Away Win"] = df.apply(
        lambda row: calculate_rate(row, "Away Team ID", 2, "Secondhalf Result"), axis=1
    )
    df["Away Secondhalf Result Draw"] = df.apply(
        lambda row: calculate_rate(row, "Away Team ID", 0, "Secondhalf Result"), axis=1
    )
    logging.info("Secondhalf sonuç oranları başarıyla hesaplandı.")

    logging.info("Sonuç oranları hesaplama işlemi tamamlandı.")
    return df