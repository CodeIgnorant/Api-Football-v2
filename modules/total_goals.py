# total_goals.py

def calculate_total_goals(df):
    """
    Calculate the total goals for halftime, second half, and fulltime.
    Adds 'Halftime Total Goals', 'Secondhalf Total Goals', and 'Fulltime Total Goals' columns to the DataFrame.
    
    :param df: DataFrame containing fixture data.
    :return: DataFrame with new total goals columns.
    """
    # Calculate Halftime Total Goals
    df['Halftime Total Goals'] = df['Halftime Home Score'] + df['Halftime Away Score']
    
    # Calculate Secondhalf Total Goals
    df['Secondhalf Total Goals'] = df['Secondhalf Home Score'] + df['Secondhalf Away Score']
    
    # Calculate Fulltime Total Goals
    df['Fulltime Total Goals'] = df['Fulltime Home Score'] + df['Fulltime Away Score']
    
    return df
