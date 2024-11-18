from modules.correlation_analysis import run_correlation_analysis
from modules.distribution_analysis import run_distribution_analysis
from modules.missing_value_analysis import run_missing_value_analysis
from modules.class_imbalance_analysis import run_class_imbalance_analysis

def run_all_analyses(ml_df):
    """
    ML için hazırlanmış veriler üzerinde tüm analizleri sırayla çalıştırır.
    :param ml_df: ML için hazırlanmış DataFrame.
    """
    print("=== ANALİZ BAŞLIYOR ===")
    
    # 1. Korelasyon Analizi
    print("\n--- Korelasyon Analizi ---")
    run_correlation_analysis(ml_df)
    
    # 2. Veri Dağılımı Analizi
    print("\n--- Veri Dağılımı Analizi ---")
    run_distribution_analysis(ml_df)
    
    # 3. Eksik Veri Analizi
    print("\n--- Eksik Veri Analizi ---")
    run_missing_value_analysis(ml_df)
    
    # 4. Sınıf Dengesizliği Analizi
    print("\n--- Sınıf Dengesizliği Analizi ---")
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
    run_class_imbalance_analysis(ml_df, labels)
    
    print("\n=== ANALİZ TAMAMLANDI ===")