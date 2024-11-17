def calculate_match_result(df):
    """
    Calculate the match results based on the fulltime, halftime, and second half scores.
    Adds 'Fulltime Result', 'Halftime Result', and 'Secondhalf Result' columns to the DataFrame with values 1, 0, or 2.
    
    :param df: DataFrame containing fixture data.
    :return: DataFrame with new 'Fulltime Result', 'Halftime Result', and 'Secondhalf Result' columns.
    """
    # Calculate Match Result (Fulltime Result)
    df['Fulltime Result'] = df.apply(lambda row: 1 if row['Fulltime Home Score'] > row['Fulltime Away Score'] 
                                             else 2 if row['Fulltime Away Score'] > row['Fulltime Home Score']
                                             else 0, axis=1)
    
    # Calculate Halftime Result
    df['Halftime Result'] = df.apply(lambda row: 1 if row['Halftime Home Score'] > row['Halftime Away Score'] 
                                               else 2 if row['Halftime Away Score'] > row['Halftime Home Score']
                                               else 0, axis=1)
    
    # Calculate Secondhalf Result
    df['Secondhalf Result'] = df.apply(lambda row: 1 if row['Secondhalf Home Score'] > row['Secondhalf Away Score'] 
                                                 else 2 if row['Secondhalf Away Score'] > row['Secondhalf Home Score']
                                                 else 0, axis=1)
    
    return df