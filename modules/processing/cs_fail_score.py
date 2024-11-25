import logging

def calculate_clean_sheets_and_fail_to_score(df):
    """
    Calculate clean sheet and fail to score values for halftime, secondhalf, and fulltime for home and away teams.
    Adds related columns for each case, only for completed matches (Status Short == "FT").

    :param df: DataFrame containing fixture data.
    :return: DataFrame with new columns.
    """
    logging.info("Clean Sheet ve Fail to Score hesaplamaları başlatıldı.")

    try:
        # Sadece tamamlanmış maçları işle
        completed_matches = df[df["Status Short"] == "FT"]

        # Halftime Clean Sheet hesaplama
        df.loc[completed_matches.index, 'Halftime Home Clean Sheet'] = completed_matches['Halftime Away Score'].apply(
            lambda x: 1 if x == 0 else 0)
        df.loc[completed_matches.index, 'Halftime Away Clean Sheet'] = completed_matches['Halftime Home Score'].apply(
            lambda x: 1 if x == 0 else 0)
        logging.info("Halftime Clean Sheet hesaplamaları tamamlandı.")

        # Secondhalf Clean Sheet hesaplama
        df.loc[completed_matches.index, 'Secondhalf Home Clean Sheet'] = completed_matches['Secondhalf Away Score'].apply(
            lambda x: 1 if x == 0 else 0)
        df.loc[completed_matches.index, 'Secondhalf Away Clean Sheet'] = completed_matches['Secondhalf Home Score'].apply(
            lambda x: 1 if x == 0 else 0)
        logging.info("Secondhalf Clean Sheet hesaplamaları tamamlandı.")

        # Fulltime Clean Sheet hesaplama
        df.loc[completed_matches.index, 'Fulltime Home Clean Sheet'] = completed_matches['Fulltime Away Score'].apply(
            lambda x: 1 if x == 0 else 0)
        df.loc[completed_matches.index, 'Fulltime Away Clean Sheet'] = completed_matches['Fulltime Home Score'].apply(
            lambda x: 1 if x == 0 else 0)
        logging.info("Fulltime Clean Sheet hesaplamaları tamamlandı.")

        # Halftime Fail to Score hesaplama
        df.loc[completed_matches.index, 'Halftime Home Fail to Score'] = completed_matches['Halftime Home Score'].apply(
            lambda x: 1 if x == 0 else 0)
        df.loc[completed_matches.index, 'Halftime Away Fail to Score'] = completed_matches['Halftime Away Score'].apply(
            lambda x: 1 if x == 0 else 0)
        logging.info("Halftime Fail to Score hesaplamaları tamamlandı.")

        # Secondhalf Fail to Score hesaplama
        df.loc[completed_matches.index, 'Secondhalf Home Fail to Score'] = completed_matches['Secondhalf Home Score'].apply(
            lambda x: 1 if x == 0 else 0)
        df.loc[completed_matches.index, 'Secondhalf Away Fail to Score'] = completed_matches['Secondhalf Away Score'].apply(
            lambda x: 1 if x == 0 else 0)
        logging.info("Secondhalf Fail to Score hesaplamaları tamamlandı.")

        # Fulltime Fail to Score hesaplama
        df.loc[completed_matches.index, 'Fulltime Home Fail to Score'] = completed_matches['Fulltime Home Score'].apply(
            lambda x: 1 if x == 0 else 0)
        df.loc[completed_matches.index, 'Fulltime Away Fail to Score'] = completed_matches['Fulltime Away Score'].apply(
            lambda x: 1 if x == 0 else 0)
        logging.info("Fulltime Fail to Score hesaplamaları tamamlandı.")

    except KeyError as e:
        logging.error(f"Clean Sheet ve Fail to Score hesaplanırken eksik sütun hatası: {e}")
    except Exception as e:
        logging.error(f"Clean Sheet ve Fail to Score hesaplanırken bir hata oluştu: {e}")

    logging.info("Clean Sheet ve Fail to Score hesaplamaları başarıyla tamamlandı.")
    return df
