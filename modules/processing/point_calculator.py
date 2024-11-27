import logging
import numpy as np

def calculate_points(df):
    """
    Fulltime Result sütununa dayalı olarak aşağıdaki sütunları hesaplar:
    1. Home Point: Ev sahibinin puanı (Tamamlanmış maçlarda)
    2. Away Point: Deplasman takımının puanı (Tamamlanmış maçlarda)
    3. Home Point Cumulative: Ev sahibinin sadece evinde oynadığı maçlardan aldığı toplam puan
    4. Away Point Cumulative: Deplasman takımının sadece deplasmanda oynadığı maçlardan aldığı toplam puan

    Notlar:
    - Home Point ve Away Point sütunları yalnızca tamamlanmış maçlar için doldurulur, diğer maçlarda NaN kalır.
    - Cumulative sütunlar, tüm maçlar için hesaplanır.

    :param df: DataFrame containing fixture data.
    :return: DataFrame with new 'Home Point', 'Away Point', 'Home Point Cumulative', and 'Away Point Cumulative' columns.
    """
    logging.info("Puan hesaplama işlemi başlatılıyor...")

    try:
        # Tamamlanmış maçları filtrele
        completed_matches = df[df["Status Short"] == "FT"]

        # Home Point ve Away Point hesapla (Tamamlanmış maçlar için)
        df['Home Point'] = np.nan
        df['Away Point'] = np.nan
        df.loc[completed_matches.index, 'Home Point'] = completed_matches['Fulltime Result'].apply(
            lambda result: 3 if result == 1 else 1 if result == 0 else 0
        )
        df.loc[completed_matches.index, 'Away Point'] = completed_matches['Fulltime Result'].apply(
            lambda result: 3 if result == 2 else 1 if result == 0 else 0
        )
        logging.info("Home Point ve Away Point sütunları tamamlanmış maçlar için hesaplandı.")

        # Home Point Cumulative ve Away Point Cumulative hesapla (Tüm maçlar için)
        df['Home Point Cumulative'] = 0
        df['Away Point Cumulative'] = 0

        for index, row in df.iterrows():
            # Round'dan önceki maçları filtrele
            previous_matches = df[
                (df['Round'] < row['Round']) &  # Daha önceki maçlar
                ((df['Home Team ID'] == row['Home Team ID']) | (df['Away Team ID'] == row['Away Team ID']))
            ]

            # Home için birikimli puan (sadece ev sahibi maçlar)
            home_matches = previous_matches[previous_matches['Home Team ID'] == row['Home Team ID']]
            home_cumulative = home_matches['Home Point'].sum()

            # Away için birikimli puan (sadece deplasman maçlar)
            away_matches = previous_matches[previous_matches['Away Team ID'] == row['Away Team ID']]
            away_cumulative = away_matches['Away Point'].sum()

            # Cumulative sütunlara ekle
            df.at[index, 'Home Point Cumulative'] = home_cumulative
            df.at[index, 'Away Point Cumulative'] = away_cumulative

        logging.info("Home Point Cumulative ve Away Point Cumulative sütunları tüm maçlar için hesaplandı.")

    except KeyError as e:
        logging.error(f"Sütun eksik: {e}")
    except Exception as e:
        logging.error(f"Puan hesaplama sırasında bir hata oluştu: {e}")

    logging.info("Puan hesaplama işlemi tamamlandı.")
    return df