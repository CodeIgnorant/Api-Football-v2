def calculate_over_under(df):
    """
    Calculate over/under metrics for fulltime home, away, and total goals.
    Adds the following columns to the DataFrame:
    - 'Fulltime Home Over 0.5', 'Fulltime Home Over 1.5', 'Fulltime Home Over 2.5', 'Fulltime Home Over 3.5'
    - 'Fulltime Away Over 0.5', 'Fulltime Away Over 1.5', 'Fulltime Away Over 2.5', 'Fulltime Away Over 3.5'
    - 'Fulltime Over 0.5', 'Fulltime Over 1.5', 'Fulltime Over 2.5', 'Fulltime Over 3.5'
    
    :param df: DataFrame containing fixture data.
    :return: DataFrame with new over/under columns.
    """
    # Calculate Fulltime Home Over X.5
    df['Fulltime Home Over 0.5'] = df['Fulltime Home Score'].apply(lambda x: 1 if x > 0.5 else 0)
    df['Fulltime Home Over 1.5'] = df['Fulltime Home Score'].apply(lambda x: 1 if x > 1.5 else 0)
    df['Fulltime Home Over 2.5'] = df['Fulltime Home Score'].apply(lambda x: 1 if x > 2.5 else 0)
    df['Fulltime Home Over 3.5'] = df['Fulltime Home Score'].apply(lambda x: 1 if x > 3.5 else 0)
    
    # Calculate Fulltime Away Over X.5
    df['Fulltime Away Over 0.5'] = df['Fulltime Away Score'].apply(lambda x: 1 if x > 0.5 else 0)
    df['Fulltime Away Over 1.5'] = df['Fulltime Away Score'].apply(lambda x: 1 if x > 1.5 else 0)
    df['Fulltime Away Over 2.5'] = df['Fulltime Away Score'].apply(lambda x: 1 if x > 2.5 else 0)
    df['Fulltime Away Over 3.5'] = df['Fulltime Away Score'].apply(lambda x: 1 if x > 3.5 else 0)
    
    # Calculate Fulltime Total Over X.5
    df['Fulltime Over 0.5'] = df['Fulltime Total Goals'].apply(lambda x: 1 if x > 0.5 else 0)
    df['Fulltime Over 1.5'] = df['Fulltime Total Goals'].apply(lambda x: 1 if x > 1.5 else 0)
    df['Fulltime Over 2.5'] = df['Fulltime Total Goals'].apply(lambda x: 1 if x > 2.5 else 0)
    df['Fulltime Over 3.5'] = df['Fulltime Total Goals'].apply(lambda x: 1 if x > 3.5 else 0)
    
    return df