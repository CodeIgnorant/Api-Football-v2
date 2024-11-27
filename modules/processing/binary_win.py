import logging

def calculate_binary_win(df):
    """
    Fulltime Result sütununa dayalı olarak iki yeni sütun hesaplar:
    - 'Binary Home Win': Ev sahibi kazandıysa 1, aksi halde 0
    - 'Binary Away Win': Deplasman kazandıysa 1, aksi halde 0
    
    :param df: DataFrame containing fixture data.
    :return: DataFrame with new 'Binary Home Win' and 'Binary Away Win' columns.
    """
    logging.info("Binary Win sütunları hesaplama işlemi başlatılıyor...")

    try:
        # Sadece tamamlanmış maçları işlemek için filtre
        completed_matches = df[df["Status Short"] == "FT"]

        # Binary Home Win hesaplama
        df.loc[completed_matches.index, 'Binary Home Win'] = completed_matches['Fulltime Result'].apply(
            lambda result: 1 if result == 1 else 0
        )
        logging.info("Binary Home Win sütunu hesaplandı.")

        # Binary Away Win hesaplama
        df.loc[completed_matches.index, 'Binary Away Win'] = completed_matches['Fulltime Result'].apply(
            lambda result: 1 if result == 2 else 0
        )
        logging.info("Binary Away Win sütunu hesaplandı.")

    except KeyError as e:
        logging.error(f"Binary Win sütunları hesaplanırken eksik sütun hatası: {e}")
    except Exception as e:
        logging.error(f"Binary Win sütunları hesaplanırken bir hata oluştu: {e}")

    logging.info("Binary Win sütunları hesaplama işlemi tamamlandı.")
    return df