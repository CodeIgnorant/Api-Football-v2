import logging
from modules.ml_algorithms.xgboost_trainer import run_xgboost
from modules.ml_algorithms.randomforest_trainer import run_randomforest

def run_ml_for_label(ml_df, features, label):
    """
    Verilen label için farklı ML algoritmalarını çalıştırır.
    
    :param ml_df: ML için hazırlanmış DataFrame.
    :param features: Kullanılacak features listesi.
    :param label: Hedef label.
    :return: Her algoritma için sonuçları içeren bir sözlük.
    """
    logging.info(f"'{label}' için ML algoritmaları çalıştırılıyor...")
    
    algorithms = {
        "XGBoost": run_xgboost,
        "RandomForest": run_randomforest
    }
    
    results = {}
    for algo_name, algo_function in algorithms.items():
        logging.info(f"{algo_name} modeli başlatılıyor...")
        metrics = algo_function(ml_df, features, label)
        results[algo_name] = metrics
        logging.info(f"{algo_name} modeli tamamlandı.")
    
    logging.info(f"'{label}' için tüm ML algoritmaları başarıyla çalıştırıldı.")
    return results

def train_and_evaluate(ml_df, label_configs):
    """
    Belirtilen label'lar için ML modellerini eğitir ve değerlendirir.
    
    :param ml_df: ML için hazırlanmış DataFrame.
    :param label_configs: Label ve features yapılandırmalarını içeren liste.
    :return: Tüm label'lar için sonuçları içeren bir sözlük.
    """
    logging.info("ML modelleri eğitme ve değerlendirme süreci başlatılıyor...")
    
    all_results = {}
    for config in label_configs:
        label = config["label"]
        features = config["features"]
        
        logging.info(f"'{label}' için ML modelleri eğitiliyor...")
        results = run_ml_for_label(ml_df, features, label)
        all_results[label] = results
        logging.info(f"'{label}' için ML modelleri başarıyla tamamlandı.")
    
    logging.info("Tüm ML modelleri eğitme ve değerlendirme süreci tamamlandı.")
    return all_results