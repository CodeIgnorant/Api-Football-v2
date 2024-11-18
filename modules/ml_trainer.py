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
    algorithms = {
        "XGBoost": run_xgboost,
        "RandomForest": run_randomforest
    }
    
    results = {}
    for algo_name, algo_function in algorithms.items():
        print(f"\n{algo_name} modeli çalıştırılıyor...")
        metrics = algo_function(ml_df, features, label)
        results[algo_name] = metrics
    
    return results

def train_and_evaluate(ml_df, label_configs):
    """
    Belirtilen label'lar için ML modellerini eğitir ve değerlendirir.
    
    :param ml_df: ML için hazırlanmış DataFrame.
    :param label_configs: Label ve features yapılandırmalarını içeren liste.
    :return: Tüm label'lar için sonuçları içeren bir sözlük.
    """
    all_results = {}
    for config in label_configs:
        label = config["label"]
        features = config["features"]
        
        print(f"\n=== '{label}' için ML modelleri eğitiliyor ===")
        results = run_ml_for_label(ml_df, features, label)
        all_results[label] = results
    
    return all_results
