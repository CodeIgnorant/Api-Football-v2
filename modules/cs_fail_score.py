import logging

def calculate_clean_sheets_and_fail_to_score(df):
    """
    Calculate clean sheet and fail to score values for halftime, secondhalf, and fulltime for home and away teams.
    Adds related columns for each case.

    :param df: DataFrame containing fixture data.
    :return: DataFrame with new columns.
    """
    logging.info("Clean Sheet ve Fail to Score hesaplamaları başlatıldı.")

    # Halftime Clean Sheet hesaplama
    df['Halftime Home Clean Sheet'] = df['Halftime Away Score'].apply(lambda x: 1 if x == 0 else 0)
    df['Halftime Away Clean Sheet'] = df['Halftime Home Score'].apply(lambda x: 1 if x == 0 else 0)
    logging.info("Halftime Clean Sheet hesaplamaları tamamlandı.")

    # Secondhalf Clean Sheet hesaplama
    df['Secondhalf Home Clean Sheet'] = df['Secondhalf Away Score'].apply(lambda x: 1 if x == 0 else 0)
    df['Secondhalf Away Clean Sheet'] = df['Secondhalf Home Score'].apply(lambda x: 1 if x == 0 else 0)
    logging.info("Secondhalf Clean Sheet hesaplamaları tamamlandı.")

    # Fulltime Clean Sheet hesaplama
    df['Fulltime Home Clean Sheet'] = df['Fulltime Away Score'].apply(lambda x: 1 if x == 0 else 0)
    df['Fulltime Away Clean Sheet'] = df['Fulltime Home Score'].apply(lambda x: 1 if x == 0 else 0)
    logging.info("Fulltime Clean Sheet hesaplamaları tamamlandı.")

    # Halftime Fail to Score hesaplama
    df['Halftime Home Fail to Score'] = df['Halftime Home Score'].apply(lambda x: 1 if x == 0 else 0)
    df['Halftime Away Fail to Score'] = df['Halftime Away Score'].apply(lambda x: 1 if x == 0 else 0)
    logging.info("Halftime Fail to Score hesaplamaları tamamlandı.")

    # Secondhalf Fail to Score hesaplama
    df['Secondhalf Home Fail to Score'] = df['Secondhalf Home Score'].apply(lambda x: 1 if x == 0 else 0)
    df['Secondhalf Away Fail to Score'] = df['Secondhalf Away Score'].apply(lambda x: 1 if x == 0 else 0)
    logging.info("Secondhalf Fail to Score hesaplamaları tamamlandı.")

    # Fulltime Fail to Score hesaplama
    df['Fulltime Home Fail to Score'] = df['Fulltime Home Score'].apply(lambda x: 1 if x == 0 else 0)
    df['Fulltime Away Fail to Score'] = df['Fulltime Away Score'].apply(lambda x: 1 if x == 0 else 0)
    logging.info("Fulltime Fail to Score hesaplamaları tamamlandı.")

    logging.info("Clean Sheet ve Fail to Score hesaplamaları başarıyla tamamlandı.")
    return df