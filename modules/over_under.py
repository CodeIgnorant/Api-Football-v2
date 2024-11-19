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
    logging.info("Fulltime Home Over/Under hesaplamaları başlatılıyor...")
    # Calculate Fulltime Home Over X.5
    df['Fulltime Home Over 0.5'] = df['Fulltime Home Score'].apply(lambda x: 1 if x > 0.5 else 0)
    df['Fulltime Home Over 1.5'] = df['Fulltime Home Score'].apply(lambda x: 1 if x > 1.5 else 0)
    df['Fulltime Home Over 2.5'] = df['Fulltime Home Score'].apply(lambda x: 1 if x > 2.5 else 0)
    df['Fulltime Home Over 3.5'] = df['Fulltime Home Score'].apply(lambda x: 1 if x > 3.5 else 0)
    logging.info("Fulltime Home Over/Under hesaplamaları tamamlandı.")
    
    logging.info("Fulltime Away Over/Under hesaplamaları başlatılıyor...")
    # Calculate Fulltime Away Over X.5
    df['Fulltime Away Over 0.5'] = df['Fulltime Away Score'].apply(lambda x: 1 if x > 0.5 else 0)
    df['Fulltime Away Over 1.5'] = df['Fulltime Away Score'].apply(lambda x: 1 if x > 1.5 else 0)
    df['Fulltime Away Over 2.5'] = df['Fulltime Away Score'].apply(lambda x: 1 if x > 2.5 else 0)
    df['Fulltime Away Over 3.5'] = df['Fulltime Away Score'].apply(lambda x: 1 if x > 3.5 else 0)
    logging.info("Fulltime Away Over/Under hesaplamaları tamamlandı.")
    
    logging.info("Fulltime Total Over/Under hesaplamaları başlatılıyor...")
    # Calculate Fulltime Total Over X.5
    df['Fulltime Over 0.5'] = df['Fulltime Total Goals'].apply(lambda x: 1 if x > 0.5 else 0)
    df['Fulltime Over 1.5'] = df['Fulltime Total Goals'].apply(lambda x: 1 if x > 1.5 else 0)
    df['Fulltime Over 2.5'] = df['Fulltime Total Goals'].apply(lambda x: 1 if x > 2.5 else 0)
    df['Fulltime Over 3.5'] = df['Fulltime Total Goals'].apply(lambda x: 1 if x > 3.5 else 0)
    logging.info("Fulltime Total Over/Under hesaplamaları tamamlandı.")
    
    logging.info("Tüm Over/Under hesaplamaları tamamlandı.")
    return df