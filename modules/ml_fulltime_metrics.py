import logging

def calculate_fulltime_metrics(ml_df):
    """
    Fulltime metriklerini hesaplar:
    - Fulltime Average Goals - Home
    - Fulltime Scoring Rate - Home
    - Fulltime Cumulative Goals - Home
    - Fulltime Average Goals - Away
    - Fulltime Scoring Rate - Away
    - Fulltime Cumulative Goals - Away

    :param ml_df: ML için hazırlanmakta olan DataFrame.
    :return: Güncellenmiş ml_df.
    """

    logging.info("Fulltime metrikleri hesaplanmaya başlıyor...")

    # Fulltime Cumulative Goals - Home
    ml_df["Fulltime Cumulative Goals - Home"] = ml_df.apply(
        lambda row: ml_df[
            (ml_df["Home Team ID"] == row["Home Team ID"]) & (ml_df["Round"] < row["Round"])
        ]["Fulltime Home Score"].sum() if not ml_df[
            (ml_df["Home Team ID"] == row["Home Team ID"]) & (ml_df["Round"] < row["Round"])
        ]["Fulltime Home Score"].empty else 0,
        axis=1
    )
    logging.info("Fulltime Cumulative Goals - Home sütunu hesaplandı.")

    # Fulltime Average Goals - Home
    ml_df["Fulltime Average Goals - Home"] = ml_df.apply(
        lambda row: ml_df[
            (ml_df["Home Team ID"] == row["Home Team ID"]) & (ml_df["Round"] < row["Round"])
        ]["Fulltime Home Score"].mean() if not ml_df[
            (ml_df["Home Team ID"] == row["Home Team ID"]) & (ml_df["Round"] < row["Round"])
        ]["Fulltime Home Score"].empty else 0,
        axis=1
    )
    logging.info("Fulltime Average Goals - Home sütunu hesaplandı.")

    # Fulltime Scoring Rate - Home
    ml_df["Fulltime Scoring Rate - Home"] = ml_df.apply(
        lambda row: ml_df[
            (ml_df["Home Team ID"] == row["Home Team ID"]) & (ml_df["Round"] < row["Round"])
        ]["Fulltime Home Score"].apply(lambda x: 1 if x > 0 else 0).mean() if not ml_df[
            (ml_df["Home Team ID"] == row["Home Team ID"]) & (ml_df["Round"] < row["Round"])
        ]["Fulltime Home Score"].empty else 0,
        axis=1
    )
    logging.info("Fulltime Scoring Rate - Home sütunu hesaplandı.")

    # Fulltime Cumulative Goals - Away
    ml_df["Fulltime Cumulative Goals - Away"] = ml_df.apply(
        lambda row: ml_df[
            (ml_df["Away Team ID"] == row["Away Team ID"]) & (ml_df["Round"] < row["Round"])
        ]["Fulltime Away Score"].sum() if not ml_df[
            (ml_df["Away Team ID"] == row["Away Team ID"]) & (ml_df["Round"] < row["Round"])
        ]["Fulltime Away Score"].empty else 0,
        axis=1
    )
    logging.info("Fulltime Cumulative Goals - Away sütunu hesaplandı.")

    # Fulltime Average Goals - Away
    ml_df["Fulltime Average Goals - Away"] = ml_df.apply(
        lambda row: ml_df[
            (ml_df["Away Team ID"] == row["Away Team ID"]) & (ml_df["Round"] < row["Round"])
        ]["Fulltime Away Score"].mean() if not ml_df[
            (ml_df["Away Team ID"] == row["Away Team ID"]) & (ml_df["Round"] < row["Round"])
        ]["Fulltime Away Score"].empty else 0,
        axis=1
    )
    logging.info("Fulltime Average Goals - Away sütunu hesaplandı.")

    # Fulltime Scoring Rate - Away
    ml_df["Fulltime Scoring Rate - Away"] = ml_df.apply(
        lambda row: ml_df[
            (ml_df["Away Team ID"] == row["Away Team ID"]) & (ml_df["Round"] < row["Round"])
        ]["Fulltime Away Score"].apply(lambda x: 1 if x > 0 else 0).mean() if not ml_df[
            (ml_df["Away Team ID"] == row["Away Team ID"]) & (ml_df["Round"] < row["Round"])
        ]["Fulltime Away Score"].empty else 0,
        axis=1
    )
    logging.info("Fulltime Scoring Rate - Away sütunu hesaplandı.")

    logging.info("Fulltime metrikleri başarıyla hesaplandı.")
    return ml_df