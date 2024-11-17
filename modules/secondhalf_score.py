def calculate_secondhalf_scores(df):
    """
    Calculate the second half scores for both home and away teams.
    Adds 'Secondhalf Home Score' and 'Secondhalf Away Score' columns to the DataFrame.
    
    :param df: DataFrame containing fixture data.
    :return: DataFrame with new second half score columns.
    """
    df['Secondhalf Home Score'] = df['Fulltime Home Score'] - df['Halftime Home Score']
    df['Secondhalf Away Score'] = df['Fulltime Away Score'] - df['Halftime Away Score']
    
    return df