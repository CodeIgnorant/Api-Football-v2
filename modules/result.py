import logging

def calculate_match_result(df):
    """
    Fulltime, halftime ve ikinci yarı skorlarına dayalı maç sonuçlarını hesaplar.
    Aşağıdaki sütunlar DataFrame'e eklenir:
    - 'Fulltime Result', 'Halftime Result', 'Secondhalf Result'
    Değerler:
    - 1: Ev sahibi kazandı
    - 2: Deplasman kazandı
    - 0: Beraberlik
    
    :param df: DataFrame containing fixture data.
    :return: DataFrame with new 'Fulltime Result', 'Halftime Result', and 'Secondhalf Result' columns.
    """
    logging.info("Fulltime sonuçlarının hesaplanması başlatılıyor...")
    # Calculate Match Result (Fulltime Result)
    df['Fulltime Result'] = df.apply(
        lambda row: 1 if row['Fulltime Home Score'] > row['Fulltime Away Score'] 
        else 2 if row['Fulltime Away Score'] > row['Fulltime Home Score']
        else 0, axis=1
    )
    logging.info("Fulltime sonuçları hesaplandı.")
    
    logging.info("Halftime sonuçlarının hesaplanması başlatılıyor...")
    # Calculate Halftime Result
    df['Halftime Result'] = df.apply(
        lambda row: 1 if row['Halftime Home Score'] > row['Halftime Away Score'] 
        else 2 if row['Halftime Away Score'] > row['Halftime Home Score']
        else 0, axis=1
    )
    logging.info("Halftime sonuçları hesaplandı.")
    
    logging.info("Secondhalf sonuçlarının hesaplanması başlatılıyor...")
    # Calculate Secondhalf Result
    df['Secondhalf Result'] = df.apply(
        lambda row: 1 if row['Secondhalf Home Score'] > row['Secondhalf Away Score'] 
        else 2 if row['Secondhalf Away Score'] > row['Secondhalf Home Score']
        else 0, axis=1
    )
    logging.info("Secondhalf sonuçları hesaplandı.")
    
    logging.info("Tüm maç sonuçları hesaplandı.")
    return df