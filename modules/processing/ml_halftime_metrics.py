import logging

def calculate_halftime_metrics(df):
    """
    Halftime metriklerini hesaplar:
    - Halftime Average Goals - Home
    - Halftime Scoring Rate - Home
    - Halftime Cumulative Goals - Home
    - Halftime Average Goals - Away
    - Halftime Scoring Rate - Away
    - Halftime Cumulative Goals - Away

    :param df: İşlenmekte olan DataFrame.
    :return: Güncellenmiş df.
    """

    # Halftime Cumulative Goals - Home
    df["Halftime Cumulative Goals - Home"] = df.apply(
        lambda row: df[
            (df["Home Team ID"] == row["Home Team ID"]) & (df["Round"] < row["Round"])
        ]["Halftime Home Score"].sum() if not df[
            (df["Home Team ID"] == row["Home Team ID"]) & (df["Round"] < row["Round"])
        ].empty else 0, axis=1
    )
    logging.info("Halftime Cumulative Goals - Home sütunu hesaplandı.")

    # Halftime Average Goals - Home
    df["Halftime Average Goals - Home"] = df.apply(
        lambda row: df[
            (df["Home Team ID"] == row["Home Team ID"]) & (df["Round"] < row["Round"])
        ]["Halftime Home Score"].mean() if not df[
            (df["Home Team ID"] == row["Home Team ID"]) & (df["Round"] < row["Round"])
        ].empty else 0, axis=1
    )
    logging.info("Halftime Average Goals - Home sütunu hesaplandı.")

    # Halftime Scoring Rate - Home
    df["Halftime Scoring Rate - Home"] = df.apply(
        lambda row: df[
            (df["Home Team ID"] == row["Home Team ID"]) & (df["Round"] < row["Round"])
        ]["Halftime Home Score"].apply(lambda x: 1 if x > 0 else 0).mean() if not df[
            (df["Home Team ID"] == row["Home Team ID"]) & (df["Round"] < row["Round"])
        ].empty else 0, axis=1
    )
    logging.info("Halftime Scoring Rate - Home sütunu hesaplandı.")

    # Halftime Cumulative Goals - Away
    df["Halftime Cumulative Goals - Away"] = df.apply(
        lambda row: df[
            (df["Away Team ID"] == row["Away Team ID"]) & (df["Round"] < row["Round"])
        ]["Halftime Away Score"].sum() if not df[
            (df["Away Team ID"] == row["Away Team ID"]) & (df["Round"] < row["Round"])
        ].empty else 0, axis=1
    )
    logging.info("Halftime Cumulative Goals - Away sütunu hesaplandı.")

    # Halftime Average Goals - Away
    df["Halftime Average Goals - Away"] = df.apply(
        lambda row: df[
            (df["Away Team ID"] == row["Away Team ID"]) & (df["Round"] < row["Round"])
        ]["Halftime Away Score"].mean() if not df[
            (df["Away Team ID"] == row["Away Team ID"]) & (df["Round"] < row["Round"])
        ].empty else 0, axis=1
    )
    logging.info("Halftime Average Goals - Away sütunu hesaplandı.")

    # Halftime Scoring Rate - Away
    df["Halftime Scoring Rate - Away"] = df.apply(
        lambda row: df[
            (df["Away Team ID"] == row["Away Team ID"]) & (df["Round"] < row["Round"])
        ]["Halftime Away Score"].apply(lambda x: 1 if x > 0 else 0).mean() if not df[
            (df["Away Team ID"] == row["Away Team ID"]) & (df["Round"] < row["Round"])
        ].empty else 0, axis=1
    )
    logging.info("Halftime Scoring Rate - Away sütunu hesaplandı.")

    logging.info("Halftime metrikleri başarıyla hesaplandı.")
    return df
