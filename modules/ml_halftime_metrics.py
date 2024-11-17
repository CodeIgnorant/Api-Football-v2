def calculate_halftime_metrics(ml_df):
    """
    Halftime metriklerini hesaplar:
    - Halftime Average Goals - Home
    - Halftime Scoring Rate - Home
    - Halftime Cumulative Goals - Home
    - Halftime Average Goals - Away
    - Halftime Scoring Rate - Away
    - Halftime Cumulative Goals - Away

    :param ml_df: ML için hazırlanmakta olan DataFrame.
    :return: Güncellenmiş ml_df.
    """

    # Halftime Cumulative Goals - Home
    ml_df["Halftime Cumulative Goals - Home"] = ml_df.apply(
        lambda row: ml_df[
            (ml_df["Home Team ID"] == row["Home Team ID"]) & (ml_df["Round"] < row["Round"])
        ]["Halftime Home Score"].sum(), axis=1
    )

    # Halftime Average Goals - Home
    ml_df["Halftime Average Goals - Home"] = ml_df.apply(
        lambda row: ml_df[
            (ml_df["Home Team ID"] == row["Home Team ID"]) & (ml_df["Round"] < row["Round"])
        ]["Halftime Home Score"].mean() if not ml_df[
            (ml_df["Home Team ID"] == row["Home Team ID"]) & (ml_df["Round"] < row["Round"])
        ]["Halftime Home Score"].empty else 0, axis=1
    )

    # Halftime Scoring Rate - Home
    ml_df["Halftime Scoring Rate - Home"] = ml_df.apply(
        lambda row: ml_df[
            (ml_df["Home Team ID"] == row["Home Team ID"]) & (ml_df["Round"] < row["Round"])
        ]["Halftime Home Score"].apply(lambda x: 1 if x > 0 else 0).mean() if not ml_df[
            (ml_df["Home Team ID"] == row["Home Team ID"]) & (ml_df["Round"] < row["Round"])
        ]["Halftime Home Score"].empty else 0, axis=1
    )

    # Halftime Cumulative Goals - Away
    ml_df["Halftime Cumulative Goals - Away"] = ml_df.apply(
        lambda row: ml_df[
            (ml_df["Away Team ID"] == row["Away Team ID"]) & (ml_df["Round"] < row["Round"])
        ]["Halftime Away Score"].sum(), axis=1
    )

    # Halftime Average Goals - Away
    ml_df["Halftime Average Goals - Away"] = ml_df.apply(
        lambda row: ml_df[
            (ml_df["Away Team ID"] == row["Away Team ID"]) & (ml_df["Round"] < row["Round"])
        ]["Halftime Away Score"].mean() if not ml_df[
            (ml_df["Away Team ID"] == row["Away Team ID"]) & (ml_df["Round"] < row["Round"])
        ]["Halftime Away Score"].empty else 0, axis=1
    )

    # Halftime Scoring Rate - Away
    ml_df["Halftime Scoring Rate - Away"] = ml_df.apply(
        lambda row: ml_df[
            (ml_df["Away Team ID"] == row["Away Team ID"]) & (ml_df["Round"] < row["Round"])
        ]["Halftime Away Score"].apply(lambda x: 1 if x > 0 else 0).mean() if not ml_df[
            (ml_df["Away Team ID"] == row["Away Team ID"]) & (ml_df["Round"] < row["Round"])
        ]["Halftime Away Score"].empty else 0, axis=1
    )

    return ml_df