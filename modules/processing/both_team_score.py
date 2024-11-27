import logging

# Loglama yapılandırması
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def calculate_both_team_score(df):
    """
    Calculate if both teams scored at least one goal.
    Adds a 'Both Team Score' column to the DataFrame with values '1' if both teams scored, otherwise '0'.
    Only processes matches where 'Status Short' is 'FT'.
    
    :param df: DataFrame containing fixture data.
    :return: DataFrame with new 'Both Team Score' column.
    """

    try:
        # Sadece tamamlanmış maçları işle
        completed_matches = df[df["Status Short"] == "FT"]
        
        # Sütunu tamamlanmış maçlar için hesapla
        df.loc[completed_matches.index, 'Both Team Score'] = completed_matches.apply(
            lambda row: 1 if row['Fulltime Home Score'] > 0 and row['Fulltime Away Score'] > 0 else 0, axis=1
        )
        
        logging.info("Both Team Score sütunu başarıyla eklendi.")
    except KeyError as e:
        logging.error(f"Both Team Score hesaplanırken eksik sütun hatası: {e}")
    except Exception as e:
        logging.error(f"Both Team Score hesaplanırken bir hata oluştu: {e}")
    
    return df
