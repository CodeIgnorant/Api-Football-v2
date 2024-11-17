def calculate_result_win_rates(ml_df):
    """
    Fulltime, Halftime ve Secondhalf sonuçları için kazanma, beraberlik ve kaybetme oranlarını hesaplar.
    ML için hazırlanmakta olan DataFrame'e aşağıdaki sütunları ekler:
    - Fulltime Result Home Win - Home
    - Fulltime Result Away Win - Home
    - Fulltime Result Draw - Home
    - Fulltime Result Home Win - Away
    - Fulltime Result Away Win - Away
    - Fulltime Result Draw - Away
    - (Halftime ve Secondhalf sonuçları için de benzer oranlar)

    :param ml_df: ML için hazırlanmakta olan DataFrame.
    :return: Güncellenmiş ml_df.
    """

    def calculate_rate(row, team_id_column, is_home, result_value, result_column):
        """
        Belirli bir takımın belirli bir sonuç (1: kazanma, 0: beraberlik, 2: kaybetme) oranını hesaplar.
        :param row: ML DataFrame'deki bir satır.
        :param team_id_column: Takım ID'sini belirten sütun (ör. 'Home Team ID').
        :param is_home: Ev sahibi mi (True) yoksa deplasman mı (False).
        :param result_value: Hedef sonuç (1, 0, 2).
        :param result_column: Hedef sonuç sütunu (ör. 'Fulltime Result').
        :return: Belirtilen sonucun oranı.
        """
        team_id = row[team_id_column]
        if is_home:
            matches = ml_df[
                (ml_df["Home Team ID"] == team_id) & (ml_df["Round"] < row["Round"])
            ]
        else:
            matches = ml_df[
                (ml_df["Away Team ID"] == team_id) & (ml_df["Round"] < row["Round"])
            ]

        total_matches = matches.shape[0]
        if total_matches == 0:
            return 0
        return matches[matches[result_column] == result_value].shape[0] / total_matches

    # Fulltime Result oranları
    ml_df["Fulltime Result Home Win - Home"] = ml_df.apply(
        lambda row: calculate_rate(row, "Home Team ID", True, 1, "Fulltime Result"), axis=1
    )
    ml_df["Fulltime Result Away Win - Home"] = ml_df.apply(
        lambda row: calculate_rate(row, "Home Team ID", True, 2, "Fulltime Result"), axis=1
    )
    ml_df["Fulltime Result Draw - Home"] = ml_df.apply(
        lambda row: calculate_rate(row, "Home Team ID", True, 0, "Fulltime Result"), axis=1
    )
    ml_df["Fulltime Result Home Win - Away"] = ml_df.apply(
        lambda row: calculate_rate(row, "Away Team ID", False, 1, "Fulltime Result"), axis=1
    )
    ml_df["Fulltime Result Away Win - Away"] = ml_df.apply(
        lambda row: calculate_rate(row, "Away Team ID", False, 2, "Fulltime Result"), axis=1
    )
    ml_df["Fulltime Result Draw - Away"] = ml_df.apply(
        lambda row: calculate_rate(row, "Away Team ID", False, 0, "Fulltime Result"), axis=1
    )

    # Halftime Result oranları
    ml_df["Halftime Result Home Win - Home"] = ml_df.apply(
        lambda row: calculate_rate(row, "Home Team ID", True, 1, "Halftime Result"), axis=1
    )
    ml_df["Halftime Result Away Win - Home"] = ml_df.apply(
        lambda row: calculate_rate(row, "Home Team ID", True, 2, "Halftime Result"), axis=1
    )
    ml_df["Halftime Result Draw - Home"] = ml_df.apply(
        lambda row: calculate_rate(row, "Home Team ID", True, 0, "Halftime Result"), axis=1
    )
    ml_df["Halftime Result Home Win - Away"] = ml_df.apply(
        lambda row: calculate_rate(row, "Away Team ID", False, 1, "Halftime Result"), axis=1
    )
    ml_df["Halftime Result Away Win - Away"] = ml_df.apply(
        lambda row: calculate_rate(row, "Away Team ID", False, 2, "Halftime Result"), axis=1
    )
    ml_df["Halftime Result Draw - Away"] = ml_df.apply(
        lambda row: calculate_rate(row, "Away Team ID", False, 0, "Halftime Result"), axis=1
    )

    # Secondhalf Result oranları
    ml_df["Secondhalf Result Home Win - Home"] = ml_df.apply(
        lambda row: calculate_rate(row, "Home Team ID", True, 1, "Secondhalf Result"), axis=1
    )
    ml_df["Secondhalf Result Away Win - Home"] = ml_df.apply(
        lambda row: calculate_rate(row, "Home Team ID", True, 2, "Secondhalf Result"), axis=1
    )
    ml_df["Secondhalf Result Draw - Home"] = ml_df.apply(
        lambda row: calculate_rate(row, "Home Team ID", True, 0, "Secondhalf Result"), axis=1
    )
    ml_df["Secondhalf Result Home Win - Away"] = ml_df.apply(
        lambda row: calculate_rate(row, "Away Team ID", False, 1, "Secondhalf Result"), axis=1
    )
    ml_df["Secondhalf Result Away Win - Away"] = ml_df.apply(
        lambda row: calculate_rate(row, "Away Team ID", False, 2, "Secondhalf Result"), axis=1
    )
    ml_df["Secondhalf Result Draw - Away"] = ml_df.apply(
        lambda row: calculate_rate(row, "Away Team ID", False, 0, "Secondhalf Result"), axis=1
    )

    return ml_df