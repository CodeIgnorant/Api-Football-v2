# both_team_score.py

def calculate_both_team_score(df):
    """
    Calculate if both teams scored at least one goal.
    Adds a 'Both Team Score' column to the DataFrame with values '1' if both teams scored, otherwise '0'.
    
    :param df: DataFrame containing fixture data.
    :return: DataFrame with new 'Both Team Score' column.
    """
    df['Both Team Score'] = df.apply(lambda row: 1 if row['Fulltime Home Score'] > 0 and row['Fulltime Away Score'] > 0 else 0, axis=1)
    return df