import os
import logging
from modules.ml_trainer import run_ml_for_label

def run_all_ml(ml_df, labels_features_mapping, output_folder="ml_results"):
    """
    Verilen label'lar için belirtilen features kullanılarak tüm ML algoritmalarını çalıştırır.
    
    :param ml_df: ML için hazırlanmış DataFrame.
    :param labels_features_mapping: Hedef label ve ona uygun features'ların eşleştirildiği bir sözlük.
                                    Örnek: {"Fulltime Result": ["Feature1", "Feature2"], ...}
    :param output_folder: Sonuçların kaydedileceği ana klasör.
    """
    os.makedirs(output_folder, exist_ok=True)

    logging.info("=== ML Süreci Başlıyor ===")
    
    for label, features in labels_features_mapping.items():
        logging.info(f"'{label}' için ML eğitimi başlıyor...")
        
        # Hedef klasörü oluştur
        label_folder = os.path.join(output_folder, label.replace(" ", "_").lower())
        os.makedirs(label_folder, exist_ok=True)
        
        # ML algoritmalarını çalıştır
        results = run_ml_for_label(ml_df, features, label)
        
        # Sonuçları kaydet
        for algo_name, metrics in results.items():
            file_path = os.path.join(label_folder, f"{algo_name}_results.xlsx")
            metrics.to_excel(file_path, index=False)
            logging.info(f"{algo_name} sonuçları kaydedildi: {file_path}")
    
    logging.info("=== Tüm ML Süreci Tamamlandı ===")