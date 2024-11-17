def calculate_secondhalf_metrics(ml_df):
    """
    İkinci yarı metriklerini hesaplar:
    - Second Half Average Goals - Home
    - Second Half Scoring Rate - Home
    - Second Half Cumulative Goals - Home
    - Second Half Average Goals - Away
    - Second Half Scoring Rate - Away
    - Second Half Cumulative Goals - Away

    :param ml_df: ML için hazırlanmakta olan DataFrame.
    :return: Güncellenmiş ml_df.
    """

    # Second Half Cumulative Goals - Home
    ml_df["Second Half Cumulative Goals - Home"] = ml_df.apply(
        lambda row: ml_df[
            (ml_df["Home Team ID"] == row["Home Team ID"]) & (ml_df["Round"] < row["Round"])
        ]["Secondhalf Home Score"].sum(), axis=1
    )

    # Second Half Average Goals - Home
    ml_df["Second Half Average Goals - Home"] = ml_df.apply(
        lambda row: ml_df[
            (ml_df["Home Team ID"] == row["Home Team ID"]) & (ml_df["Round"] < row["Round"])
        ]["Secondhalf Home Score"].mean() if not ml_df[
            (ml_df["Home Team ID"] == row["Home Team ID"]) & (ml_df["Round"] < row["Round"])
        ]["Secondhalf Home Score"].empty else 0, axis=1
    )

    # Second Half Scoring Rate - Home
    ml_df["Second Half Scoring Rate - Home"] = ml_df.apply(
        lambda row: ml_df[
            (ml_df["Home Team ID"] == row["Home Team ID"]) & (ml_df["Round"] < row["Round"])
        ]["Secondhalf Home Score"].apply(lambda x: 1 if x > 0 else 0).mean() if not ml_df[
            (ml_df["Home Team ID"] == row["Home Team ID"]) & (ml_df["Round"] < row["Round"])
        ]["Secondhalf Home Score"].empty else 0, axis=1
    )

    # Second Half Cumulative Goals - Away
    ml_df["Second Half Cumulative Goals - Away"] = ml_df.apply(
        lambda row: ml_df[
            (ml_df["Away Team ID"] == row["Away Team ID"]) & (ml_df["Round"] < row["Round"])
        ]["Secondhalf Away Score"].sum(), axis=1
    )

    # Second Half Average Goals - Away
    ml_df["Second Half Average Goals - Away"] = ml_df.apply(
        lambda row: ml_df[
            (ml_df["Away Team ID"] == row["Away Team ID"]) & (ml_df["Round"] < row["Round"])
        ]["Secondhalf Away Score"].mean() if not ml_df[
            (ml_df["Away Team ID"] == row["Away Team ID"]) & (ml_df["Round"] < row["Round"])
        ]["Secondhalf Away Score"].empty else 0, axis=1
    )

    # Second Half Scoring Rate - Away
    ml_df["Second Half Scoring Rate - Away"] = ml_df.apply(
        lambda row: ml_df[
            (ml_df["Away Team ID"] == row["Away Team ID"]) & (ml_df["Round"] < row["Round"])
        ]["Secondhalf Away Score"].apply(lambda x: 1 if x > 0 else 0).mean() if not ml_df[
            (ml_df["Away Team ID"] == row["Away Team ID"]) & (ml_df["Round"] < row["Round"])
        ]["Secondhalf Away Score"].empty else 0, axis=1
    )

    return ml_df
