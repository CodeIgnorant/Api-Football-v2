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

    # Fulltime Cumulative Goals - Home
    ml_df["Fulltime Cumulative Goals - Home"] = ml_df.apply(
        lambda row: ml_df[
            (ml_df["Home Team ID"] == row["Home Team ID"]) & (ml_df["Round"] < row["Round"])
        ]["Fulltime Home Score"].sum() if not ml_df[
            (ml_df["Home Team ID"] == row["Home Team ID"]) & (ml_df["Round"] < row["Round"])
        ]["Fulltime Home Score"].empty else 0,
        axis=1
    )

    # Fulltime Average Goals - Home
    ml_df["Fulltime Average Goals - Home"] = ml_df.apply(
        lambda row: ml_df[
            (ml_df["Home Team ID"] == row["Home Team ID"]) & (ml_df["Round"] < row["Round"])
        ]["Fulltime Home Score"].mean() if not ml_df[
            (ml_df["Home Team ID"] == row["Home Team ID"]) & (ml_df["Round"] < row["Round"])
        ]["Fulltime Home Score"].empty else 0,
        axis=1
    )

    # Fulltime Scoring Rate - Home
    ml_df["Fulltime Scoring Rate - Home"] = ml_df.apply(
        lambda row: ml_df[
            (ml_df["Home Team ID"] == row["Home Team ID"]) & (ml_df["Round"] < row["Round"])
        ]["Fulltime Home Score"].apply(lambda x: 1 if x > 0 else 0).mean() if not ml_df[
            (ml_df["Home Team ID"] == row["Home Team ID"]) & (ml_df["Round"] < row["Round"])
        ]["Fulltime Home Score"].empty else 0,
        axis=1
    )

    # Fulltime Cumulative Goals - Away
    ml_df["Fulltime Cumulative Goals - Away"] = ml_df.apply(
        lambda row: ml_df[
            (ml_df["Away Team ID"] == row["Away Team ID"]) & (ml_df["Round"] < row["Round"])
        ]["Fulltime Away Score"].sum() if not ml_df[
            (ml_df["Away Team ID"] == row["Away Team ID"]) & (ml_df["Round"] < row["Round"])
        ]["Fulltime Away Score"].empty else 0,
        axis=1
    )

    # Fulltime Average Goals - Away
    ml_df["Fulltime Average Goals - Away"] = ml_df.apply(
        lambda row: ml_df[
            (ml_df["Away Team ID"] == row["Away Team ID"]) & (ml_df["Round"] < row["Round"])
        ]["Fulltime Away Score"].mean() if not ml_df[
            (ml_df["Away Team ID"] == row["Away Team ID"]) & (ml_df["Round"] < row["Round"])
        ]["Fulltime Away Score"].empty else 0,
        axis=1
    )

    # Fulltime Scoring Rate - Away
    ml_df["Fulltime Scoring Rate - Away"] = ml_df.apply(
        lambda row: ml_df[
            (ml_df["Away Team ID"] == row["Away Team ID"]) & (ml_df["Round"] < row["Round"])
        ]["Fulltime Away Score"].apply(lambda x: 1 if x > 0 else 0).mean() if not ml_df[
            (ml_df["Away Team ID"] == row["Away Team ID"]) & (ml_df["Round"] < row["Round"])
        ]["Fulltime Away Score"].empty else 0,
        axis=1
    )

    return ml_df