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
    try:
        # Sadece tamamlanmış maçları işlemek için filtre
        completed_matches = df[df["Status Short"] == "FT"]
        
        # Fulltime Result hesaplama
        df.loc[completed_matches.index, 'Fulltime Result'] = completed_matches.apply(
            lambda row: 1 if row['Fulltime Home Score'] > row['Fulltime Away Score']
            else 2 if row['Fulltime Away Score'] > row['Fulltime Home Score']
            else 0, axis=1
        )
        logging.info("Fulltime sonuçları hesaplandı.")

        # Halftime Result hesaplama
        df.loc[completed_matches.index, 'Halftime Result'] = completed_matches.apply(
            lambda row: 1 if row['Halftime Home Score'] > row['Halftime Away Score']
            else 2 if row['Halftime Away Score'] > row['Halftime Home Score']
            else 0, axis=1
        )
        logging.info("Halftime sonuçları hesaplandı.")

        # Secondhalf Result hesaplama
        df.loc[completed_matches.index, 'Secondhalf Result'] = completed_matches.apply(
            lambda row: 1 if row['Secondhalf Home Score'] > row['Secondhalf Away Score']
            else 2 if row['Secondhalf Away Score'] > row['Secondhalf Home Score']
            else 0, axis=1
        )
        logging.info("Secondhalf sonuçları hesaplandı.")
        
    except KeyError as e:
        logging.error(f"Maç sonuçları hesaplanırken eksik sütun hatası: {e}")
    except Exception as e:
        logging.error(f"Maç sonuçları hesaplanırken bir hata oluştu: {e}")

    logging.info("Tüm maç sonuçları hesaplama işlemi tamamlandı.")
    return df
