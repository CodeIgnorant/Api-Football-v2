import logging

def split_processed_data(processed_df):
    """
    İşlenmiş DataFrame'i ML eğitimi ve prediction için kullanılacak şekilde böler.
    
    :param processed_df: İşlenmiş DataFrame.
    :return: ml_df (ML eğitimi için kullanılacak tamamlanmış maçlar), 
             prediction_df (Tamamlanmamış maçlar).
    """
    logging.info("DataFrame'in bölünme işlemi başlatılıyor...")
    
    try:
        # Status Short = FT olanları ayırarak ml_df oluştur
        ml_df = processed_df[processed_df["Status Short"] == "FT"].copy()
        logging.info(f"ML için kullanılacak maçlar (ml_df): {len(ml_df)} adet tamamlanmış maç bulundu.")

        # Status Short != FT olanları ayırarak prediction_df oluştur
        prediction_df = processed_df[processed_df["Status Short"] != "FT"].copy()
        logging.info(f"Prediction için kullanılacak maçlar (prediction_df): {len(prediction_df)} adet tamamlanmamış maç bulundu.")

    except KeyError as e:
        logging.error(f"Gerekli sütun bulunamadı: {e}")
        raise
    except Exception as e:
        logging.error(f"DataFrame'in bölünmesi sırasında bir hata oluştu: {e}")
        raise

    logging.info("DataFrame'in bölünme işlemi başarıyla tamamlandı.")
    return ml_df, prediction_df