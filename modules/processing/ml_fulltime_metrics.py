import logging

def calculate_fulltime_metrics(df):
    """
    Fulltime metriklerini hesaplar:
    - Fulltime Average Goals - Home
    - Fulltime Scoring Rate - Home
    - Fulltime Cumulative Goals - Home
    - Fulltime Average Goals - Away
    - Fulltime Scoring Rate - Away
    - Fulltime Cumulative Goals - Away

    :param df: ML için hazırlanmakta olan DataFrame.
    :return: Güncellenmiş df.
    """

    logging.info("Fulltime metrikleri hesaplanmaya başlıyor...")

    # Fulltime Cumulative Goals - Home
    df["Fulltime Cumulative Goals - Home"] = df.apply(
        lambda row: df[
            (df["Home Team ID"] == row["Home Team ID"]) & (df["Round"] < row["Round"])
        ]["Fulltime Home Score"].sum(), axis=1
    )
    logging.info("Fulltime Cumulative Goals - Home sütunu hesaplandı.")

    # Fulltime Average Goals - Home
    df["Fulltime Average Goals - Home"] = df.apply(
        lambda row: df[
            (df["Home Team ID"] == row["Home Team ID"]) & (df["Round"] < row["Round"])
        ]["Fulltime Home Score"].mean(), axis=1
    ).fillna(0)  # NaN değerlerini 0 ile doldur
    logging.info("Fulltime Average Goals - Home sütunu hesaplandı.")

    # Fulltime Scoring Rate - Home
    df["Fulltime Scoring Rate - Home"] = df.apply(
        lambda row: df[
            (df["Home Team ID"] == row["Home Team ID"]) & (df["Round"] < row["Round"])
        ]["Fulltime Home Score"].apply(lambda x: 1 if x > 0 else 0).mean(), axis=1
    ).fillna(0)  # NaN değerlerini 0 ile doldur
    logging.info("Fulltime Scoring Rate - Home sütunu hesaplandı.")

    # Fulltime Cumulative Goals - Away
    df["Fulltime Cumulative Goals - Away"] = df.apply(
        lambda row: df[
            (df["Away Team ID"] == row["Away Team ID"]) & (df["Round"] < row["Round"])
        ]["Fulltime Away Score"].sum(), axis=1
    )
    logging.info("Fulltime Cumulative Goals - Away sütunu hesaplandı.")

    # Fulltime Average Goals - Away
    df["Fulltime Average Goals - Away"] = df.apply(
        lambda row: df[
            (df["Away Team ID"] == row["Away Team ID"]) & (df["Round"] < row["Round"])
        ]["Fulltime Away Score"].mean(), axis=1
    ).fillna(0)  # NaN değerlerini 0 ile doldur
    logging.info("Fulltime Average Goals - Away sütunu hesaplandı.")

    # Fulltime Scoring Rate - Away
    df["Fulltime Scoring Rate - Away"] = df.apply(
        lambda row: df[
            (df["Away Team ID"] == row["Away Team ID"]) & (df["Round"] < row["Round"])
        ]["Fulltime Away Score"].apply(lambda x: 1 if x > 0 else 0).mean(), axis=1
    ).fillna(0)  # NaN değerlerini 0 ile doldur
    logging.info("Fulltime Scoring Rate - Away sütunu hesaplandı.")

    logging.info("Fulltime metrikleri başarıyla hesaplandı.")
    return df