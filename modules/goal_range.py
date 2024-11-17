# goal_range.py

def calculate_goal_range(df):
    """
    Calculate the goal range based on the fulltime total goals.
    Adds a 'Goal Range' column to the DataFrame with values '0-1', '2-3', '4-5', or '6+'.
    
    :param df: DataFrame containing fixture data.
    :return: DataFrame with new 'Goal Range' column.
    """
    def goal_range_value(total_goals):
        if total_goals <= 1:
            return "0-1"
        elif 2 <= total_goals <= 3:
            return "2-3"
        elif 4 <= total_goals <= 5:
            return "4-5"
        else:
            return "6+"
    
    df['Goal Range'] = df['Fulltime Total Goals'].apply(goal_range_value)
    
    return df
