import logging

def calculate_total_goals(df):
    """
    Calculate the total goals for halftime, second half, and fulltime.
    Adds 'Halftime Total Goals', 'Secondhalf Total Goals', and 'Fulltime Total Goals' columns to the DataFrame.
    
    :param df: DataFrame containing fixture data.
    :return: DataFrame with new total goals columns.
    """
    logging.info("Toplam gol hesaplama işlemi başlıyor...")

    try:
        # Calculate Halftime Total Goals
        df['Halftime Total Goals'] = df['Halftime Home Score'] + df['Halftime Away Score']
        logging.info("'Halftime Total Goals' sütunu başarıyla eklendi.")

        # Calculate Secondhalf Total Goals
        df['Secondhalf Total Goals'] = df['Secondhalf Home Score'] + df['Secondhalf Away Score']
        logging.info("'Secondhalf Total Goals' sütunu başarıyla eklendi.")

        # Calculate Fulltime Total Goals
        df['Fulltime Total Goals'] = df['Fulltime Home Score'] + df['Fulltime Away Score']
        logging.info("'Fulltime Total Goals' sütunu başarıyla eklendi.")

    except KeyError as e:
        logging.error(f"Toplam gol hesaplanırken eksik sütun hatası: {e}")
    except Exception as e:
        logging.error(f"Toplam gol hesaplanırken bir hata oluştu: {e}")

    return df