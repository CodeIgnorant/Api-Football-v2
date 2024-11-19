import logging

# Loglama yapılandırması
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def calculate_both_team_score(df):
    """
    Calculate if both teams scored at least one goal.
    Adds a 'Both Team Score' column to the DataFrame with values '1' if both teams scored, otherwise '0'.
    
    :param df: DataFrame containing fixture data.
    :return: DataFrame with new 'Both Team Score' column.
    """
    logging.info("Both Team Score hesaplanıyor...")
    
    df['Both Team Score'] = df.apply(
        lambda row: 1 if row['Fulltime Home Score'] > 0 and row['Fulltime Away Score'] > 0 else 0, axis=1
    )
    
    logging.info("Both Team Score sütunu başarıyla eklendi.")
    return df