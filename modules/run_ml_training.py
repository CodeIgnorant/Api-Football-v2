import os
import logging
from modules.ml_trainer import train_and_evaluate
import warnings

# Uyarıları temizlemek için ayarlama
warnings.filterwarnings("ignore", category=UserWarning, module="xgboost")

def run_ml_training(ml_df):
    """
    ML modellerini eğitmek ve değerlendirmek için ana fonksiyon.
    :param ml_df: ML için hazırlanmış DataFrame.
    """
    logging.info("ML Eğitimi ve Değerlendirme Başlıyor.")

    # Precision ve Recall açıklaması
    logging.info("""
    === Precision ve Recall Açıklaması ===

    - Precision (Kesinlik): Modelin "kendi dediği şey" konusunda ne kadar doğru olduğunu ölçer.
      Örneğin, model bir maçı "Ev sahibi kazanır" (1) diye tahmin ettiğinde, bu tahminlerin kaçının gerçekten doğru olduğunu gösterir.

    - Recall (Duyarlılık): Modelin "olayları kaçırma oranını" ölçer.
      Örneğin, toplamda 10 maçta ev sahibi kazanmışsa ve model bu maçların sadece 6'sını doğru tahmin etmişse, recall düşük olacaktır.
    """)

    # Label ve features yapılandırması
    label_configs = [
        {
            "label": "Fulltime Result",
            "features": [
                "Halftime Cumulative Goals - Home", "Halftime Average Goals - Home", "Halftime Scoring Rate - Home",
                "Halftime Cumulative Goals - Away", "Halftime Average Goals - Away", "Halftime Scoring Rate - Away",
                "Second Half Cumulative Goals - Home", "Second Half Average Goals - Home", "Second Half Scoring Rate - Home",
                "Second Half Cumulative Goals - Away", "Second Half Average Goals - Away", "Second Half Scoring Rate - Away",
                "Fulltime Cumulative Goals - Home", "Fulltime Average Goals - Home", "Fulltime Scoring Rate - Home",
                "Fulltime Cumulative Goals - Away", "Fulltime Average Goals - Away", "Fulltime Scoring Rate - Away",
                "Home Fulltime Result Home Win", "Home Fulltime Result Away Win", "Home Fulltime Result Draw",
                "Away Fulltime Result Home Win", "Away Fulltime Result Away Win", "Away Fulltime Result Draw",
                "Home Halftime Result Home Win", "Home Halftime Result Away Win", "Home Halftime Result Draw",
                "Away Halftime Result Home Win", "Away Halftime Result Away Win", "Away Halftime Result Draw",
                "Home Secondhalf Result Home Win", "Home Secondhalf Result Away Win", "Home Secondhalf Result Draw",
                "Away Secondhalf Result Home Win", "Away Secondhalf Result Away Win", "Away Secondhalf Result Draw"
            ]
        }
    ]

    # Eğitim ve değerlendirme
    try:
        model_results = train_and_evaluate(ml_df, label_configs)
        logging.info("ML eğitim ve değerlendirme başarıyla tamamlandı.")
    except Exception as e:
        logging.error(f"ML eğitim ve değerlendirme sırasında hata oluştu: {e}")
        return None

    # Her sınıf için en iyi algoritmayı bul ve yazdır
    logging.info("Sınıf bazlı F1 skorları inceleniyor.")
    class_best_results = {}
    numbered_algorithms = []
    algorithm_number = 1

    for label, results in model_results.items():
        logging.info(f"{label} için algoritmalar değerlendirilirken.")
        for model_name, metrics in results.items():
            class_reports = metrics.get("classification_report", {})
            for class_name, class_metrics in class_reports.items():
                if isinstance(class_metrics, dict):  # Sadece sınıf metriklerini al
                    f1_score = class_metrics.get("f1-score", 0)
                    logging.info(f"{model_name} modeli, Sınıf '{class_name}' için F1-Score: {f1_score:.4f}")
                    
                    # En iyi algoritmayı kaydet
                    if class_name not in class_best_results or f1_score > class_best_results[class_name][1]:
                        class_best_results[class_name] = (model_name, f1_score)
            
            # Algoritmaları numaralandırarak listele
            numbered_algorithms.append((algorithm_number, model_name, label))
            algorithm_number += 1

    # Kullanıcıdan seçim yapmasını isteme
    logging.info("Algoritma önerisi ve kullanıcı seçimi aşamasına geçiliyor.")
    for idx, model_name, label in numbered_algorithms:
        logging.info(f"{idx}: {model_name} modeli ({label})")
    
    selected_number = int(input("\nHangi algoritma ile devam etmek istiyorsunuz? Numara giriniz: ").strip())
    selected_algorithm = next((algo for algo in numbered_algorithms if algo[0] == selected_number), None)

    if selected_algorithm:
        logging.info(f"Seçilen algoritma: {selected_algorithm[1]} modeli, {selected_algorithm[2]} etiketi ile.")
    else:
        logging.warning("Geçerli bir seçim yapılmadı.")
    
    logging.info("ML Eğitimi ve Değerlendirme Tamamlandı.")
    return model_results