import logging

def calculate_secondhalf_scores(df):
    """
    Calculate the second half scores for both home and away teams.
    Adds 'Secondhalf Home Score' and 'Secondhalf Away Score' columns to the DataFrame.
    
    :param df: DataFrame containing fixture data.
    :return: DataFrame with new second half score columns.
    """
    logging.info("İkinci yarı skor hesaplama işlemi başlıyor...")

    try:
        df['Secondhalf Home Score'] = df['Fulltime Home Score'] - df['Halftime Home Score']
        df['Secondhalf Away Score'] = df['Fulltime Away Score'] - df['Halftime Away Score']
        logging.info("İkinci yarı skor sütunları başarıyla eklendi: 'Secondhalf Home Score', 'Secondhalf Away Score'.")
    except KeyError as e:
        logging.error(f"İkinci yarı skor hesaplanırken eksik sütun hatası: {e}")
    except Exception as e:
        logging.error(f"İkinci yarı skor hesaplanırken bir hata oluştu: {e}")

    return df