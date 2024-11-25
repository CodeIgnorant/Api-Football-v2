import logging

def calculate_secondhalf_scores(df):
    """
    Calculate the second half scores for both home and away teams.
    Adds 'Secondhalf Home Score' and 'Secondhalf Away Score' columns to the DataFrame.
    This calculation is only applied to rows where 'Status Short' is 'FT'.
    
    :param df: DataFrame containing fixture data.
    :return: DataFrame with new second half score columns.
    """
    logging.info("İkinci yarı skor hesaplama işlemi başlıyor...")

    try:
        # Sadece tamamlanmış maçları işlemek için filtre
        completed_matches = df[df["Status Short"] == "FT"]
        
        # Hesaplamaları yap ve orijinal DataFrame'e ekle
        df.loc[completed_matches.index, 'Secondhalf Home Score'] = (
            completed_matches['Fulltime Home Score'] - completed_matches['Halftime Home Score']
        )
        df.loc[completed_matches.index, 'Secondhalf Away Score'] = (
            completed_matches['Fulltime Away Score'] - completed_matches['Halftime Away Score']
        )
        logging.info("İkinci yarı skor sütunları başarıyla eklendi: 'Secondhalf Home Score', 'Secondhalf Away Score'.")
    except KeyError as e:
        logging.error(f"İkinci yarı skor hesaplanırken eksik sütun hatası: {e}")
    except Exception as e:
        logging.error(f"İkinci yarı skor hesaplanırken bir hata oluştu: {e}")

    return df
