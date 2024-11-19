import logging
from modules.correlation_analysis import run_correlation_analysis
from modules.distribution_analysis import run_distribution_analysis
from modules.missing_value_analysis import run_missing_value_analysis
from modules.class_imbalance_analysis import run_class_imbalance_analysis

def run_all_analyses(ml_df):
    """
    ML için hazırlanmış veriler üzerinde tüm analizleri sırayla çalıştırır.
    :param ml_df: ML için hazırlanmış DataFrame.
    """
    logging.info("=== ANALİZ BAŞLIYOR ===")
    
    # 1. Korelasyon Analizi
    logging.info("Korelasyon analizi başlatılıyor...")
    try:
        run_correlation_analysis(ml_df)
        logging.info("Korelasyon analizi başarıyla tamamlandı.")
    except Exception as e:
        logging.error(f"Korelasyon analizi sırasında hata oluştu: {e}")
    
    # 2. Veri Dağılımı Analizi
    logging.info("Veri dağılımı analizi başlatılıyor...")
    try:
        run_distribution_analysis(ml_df)
        logging.info("Veri dağılımı analizi başarıyla tamamlandı.")
    except Exception as e:
        logging.error(f"Veri dağılımı analizi sırasında hata oluştu: {e}")
    
    # 3. Eksik Veri Analizi
    logging.info("Eksik veri analizi başlatılıyor...")
    try:
        run_missing_value_analysis(ml_df)
        logging.info("Eksik veri analizi başarıyla tamamlandı.")
    except Exception as e:
        logging.error(f"Eksik veri analizi sırasında hata oluştu: {e}")
    
    # 4. Sınıf Dengesizliği Analizi
    logging.info("Sınıf dengesizliği analizi başlatılıyor...")
    labels = [
        "Halftime Total Goals", "Secondhalf Total Goals", "Fulltime Total Goals", "Goal Range", "Both Team Score",
        "Fulltime Home Over 0.5", "Fulltime Home Over 1.5", "Fulltime Home Over 2.5", "Fulltime Home Over 3.5",
        "Fulltime Away Over 0.5", "Fulltime Away Over 1.5", "Fulltime Away Over 2.5", "Fulltime Away Over 3.5",
        "Fulltime Over 0.5", "Fulltime Over 1.5", "Fulltime Over 2.5", "Fulltime Over 3.5",
        "Halftime Home Clean Sheet", "Halftime Away Clean Sheet", "Secondhalf Home Clean Sheet", "Secondhalf Away Clean Sheet",
        "Fulltime Home Clean Sheet", "Fulltime Away Clean Sheet", "Halftime Home Fail to Score", "Halftime Away Fail to Score",
        "Secondhalf Home Fail to Score", "Secondhalf Away Fail to Score", "Fulltime Home Fail to Score", "Fulltime Away Fail to Score",
        "Fulltime Result", "Halftime Result", "Secondhalf Result"
    ]
    try:
        run_class_imbalance_analysis(ml_df, labels)
        logging.info("Sınıf dengesizliği analizi başarıyla tamamlandı.")
    except Exception as e:
        logging.error(f"Sınıf dengesizliği analizi sırasında hata oluştu: {e}")
    
    logging.info("=== ANALİZ TAMAMLANDI ===")