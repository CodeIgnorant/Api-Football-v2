import logging

def calculate_over_under(df):
    """
    Fulltime home, away, and total goals için over/under metriklerini hesaplar.
    Aşağıdaki sütunlar DataFrame'e eklenir:
    - 'Fulltime Home Over 0.5', 'Fulltime Home Over 1.5', 'Fulltime Home Over 2.5', 'Fulltime Home Over 3.5'
    - 'Fulltime Away Over 0.5', 'Fulltime Away Over 1.5', 'Fulltime Away Over 2.5', 'Fulltime Away Over 3.5'
    - 'Fulltime Over 0.5', 'Fulltime Over 1.5', 'Fulltime Over 2.5', 'Fulltime Over 3.5'
    
    :param df: DataFrame containing fixture data.
    :return: DataFrame with new over/under columns.
    """

    try:
        # Sadece tamamlanmış maçlar için işlem yap
        completed_matches = df[df["Status Short"] == "FT"]

        # Fulltime Home Over X.5
        df.loc[completed_matches.index, 'Fulltime Home Over 0.5'] = completed_matches['Fulltime Home Score'].apply(lambda x: 1 if x > 0.5 else 0)
        df.loc[completed_matches.index, 'Fulltime Home Over 1.5'] = completed_matches['Fulltime Home Score'].apply(lambda x: 1 if x > 1.5 else 0)
        df.loc[completed_matches.index, 'Fulltime Home Over 2.5'] = completed_matches['Fulltime Home Score'].apply(lambda x: 1 if x > 2.5 else 0)
        df.loc[completed_matches.index, 'Fulltime Home Over 3.5'] = completed_matches['Fulltime Home Score'].apply(lambda x: 1 if x > 3.5 else 0)
        logging.info("Fulltime Home Over/Under hesaplamaları tamamlandı.")

        # Fulltime Away Over X.5
        df.loc[completed_matches.index, 'Fulltime Away Over 0.5'] = completed_matches['Fulltime Away Score'].apply(lambda x: 1 if x > 0.5 else 0)
        df.loc[completed_matches.index, 'Fulltime Away Over 1.5'] = completed_matches['Fulltime Away Score'].apply(lambda x: 1 if x > 1.5 else 0)
        df.loc[completed_matches.index, 'Fulltime Away Over 2.5'] = completed_matches['Fulltime Away Score'].apply(lambda x: 1 if x > 2.5 else 0)
        df.loc[completed_matches.index, 'Fulltime Away Over 3.5'] = completed_matches['Fulltime Away Score'].apply(lambda x: 1 if x > 3.5 else 0)
        logging.info("Fulltime Away Over/Under hesaplamaları tamamlandı.")

        # Fulltime Total Over X.5
        df.loc[completed_matches.index, 'Fulltime Over 0.5'] = completed_matches['Fulltime Total Goals'].apply(lambda x: 1 if x > 0.5 else 0)
        df.loc[completed_matches.index, 'Fulltime Over 1.5'] = completed_matches['Fulltime Total Goals'].apply(lambda x: 1 if x > 1.5 else 0)
        df.loc[completed_matches.index, 'Fulltime Over 2.5'] = completed_matches['Fulltime Total Goals'].apply(lambda x: 1 if x > 2.5 else 0)
        df.loc[completed_matches.index, 'Fulltime Over 3.5'] = completed_matches['Fulltime Total Goals'].apply(lambda x: 1 if x > 3.5 else 0)
        logging.info("Fulltime Total Over/Under hesaplamaları tamamlandı.")

    except KeyError as e:
        logging.error(f"Over/Under hesaplanırken eksik sütun hatası: {e}")
    except Exception as e:
        logging.error(f"Over/Under hesaplanırken bir hata oluştu: {e}")

    logging.info("Tüm Over/Under hesaplamaları başarıyla tamamlandı.")
    return df
