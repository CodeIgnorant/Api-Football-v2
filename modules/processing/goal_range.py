import logging

def calculate_goal_range(df):
    """
    Calculate the goal range based on the fulltime total goals.
    Adds a 'Goal Range' column to the DataFrame with numeric mid-range values:
    - 0.5 for '0-1'
    - 2.5 for '2-3'
    - 4.5 for '4-5'
    - 6.5 for '6+'
    
    :param df: DataFrame containing fixture data.
    :return: DataFrame with new 'Goal Range' column.
    """
    def goal_range_value(total_goals):
        if total_goals <= 1:
            return 0.5
        elif 2 <= total_goals <= 3:
            return 2.5
        elif 4 <= total_goals <= 5:
            return 4.5
        else:
            return 6.5
   
    try:
        # Sadece tamamlanmış maçları işle
        completed_matches = df[df["Status Short"] == "FT"]

        # Goal Range sütununu hesapla ve ekle
        df.loc[completed_matches.index, 'Goal Range'] = completed_matches['Fulltime Total Goals'].apply(goal_range_value)

        logging.info("Goal Range sütunu başarıyla eklendi.")
    except KeyError as e:
        logging.error(f"Goal Range hesaplanırken eksik sütun hatası: {e}")
    except Exception as e:
        logging.error(f"Goal Range hesaplanırken bir hata oluştu: {e}")

    return df
