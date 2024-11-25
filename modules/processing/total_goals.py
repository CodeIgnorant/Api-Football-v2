import logging

def calculate_total_goals(df):
    """
    Calculate the total goals for halftime, second half, and fulltime.
    Adds 'Halftime Total Goals', 'Secondhalf Total Goals', and 'Fulltime Total Goals' columns to the DataFrame.
    
    :param df: DataFrame containing fixture data.
    :return: DataFrame with new total goals columns.
    """
    logging.info("Toplam gol hesaplama işlemi başlıyor...")

    try:
        # Sadece tamamlanmış maçlar için işlem yap
        completed_matches = df[df["Status Short"] == "FT"]

        # Calculate Halftime Total Goals
        df.loc[completed_matches.index, 'Halftime Total Goals'] = completed_matches['Halftime Home Score'] + completed_matches['Halftime Away Score']
        logging.info("'Halftime Total Goals' sütunu başarıyla eklendi.")

        # Calculate Secondhalf Total Goals
        df.loc[completed_matches.index, 'Secondhalf Total Goals'] = completed_matches['Secondhalf Home Score'] + completed_matches['Secondhalf Away Score']
        logging.info("'Secondhalf Total Goals' sütunu başarıyla eklendi.")

        # Calculate Fulltime Total Goals
        df.loc[completed_matches.index, 'Fulltime Total Goals'] = completed_matches['Fulltime Home Score'] + completed_matches['Fulltime Away Score']
        logging.info("'Fulltime Total Goals' sütunu başarıyla eklendi.")

    except KeyError as e:
        logging.error(f"Toplam gol hesaplanırken eksik sütun hatası: {e}")
    except Exception as e:
        logging.error(f"Toplam gol hesaplanırken bir hata oluştu: {e}")

    logging.info("Toplam gol hesaplama işlemi tamamlandı.")
    return df