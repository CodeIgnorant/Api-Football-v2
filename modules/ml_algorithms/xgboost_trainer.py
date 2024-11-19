import logging
import xgboost as xgb
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
from sklearn.model_selection import train_test_split

def run_xgboost(ml_df, features, label):
    """
    XGBoost modelini çalıştırır ve sonuçları döndürür.
    
    :param ml_df: ML için hazırlanmış DataFrame.
    :param features: Kullanılacak features listesi.
    :param label: Hedef label.
    :return: Performans metriklerini ve classification report'u içeren bir sözlük.
    """
    logging.info(f"XGBoost modeli '{label}' için başlatılıyor...")

    try:
        # Veriyi ayırma
        logging.info("Veri train-test setlerine bölünüyor...")
        X = ml_df[features]
        y = ml_df[label]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Modeli oluşturma ve eğitme
        logging.info("XGBoost modeli oluşturuluyor ve eğitiliyor...")
        model = xgb.XGBClassifier(eval_metric="logloss", use_label_encoder=False)  # "use_label_encoder" kaldırıldı
        model.fit(X_train, y_train)
        logging.info("Model eğitimi tamamlandı.")

        # Tahmin yapma
        logging.info("Tahmin yapılıyor...")
        y_pred = model.predict(X_test)

        # Performans metriklerini hesaplama
        logging.info("Model performans metrikleri hesaplanıyor...")
        metrics = {
            "accuracy": accuracy_score(y_test, y_pred),
            "precision": precision_score(y_test, y_pred, average="weighted", zero_division=0),
            "recall": recall_score(y_test, y_pred, average="weighted", zero_division=0),
            "f1": f1_score(y_test, y_pred, average="weighted", zero_division=0),
            "classification_report": classification_report(y_test, y_pred, output_dict=True)
        }

        # Classification Report'u konsola yazdırma
        logging.info(f"XGBoost modeli için sınıflandırma raporu oluşturuldu: {label}")
        print(f"\nXGBoost Classification Report for '{label}':")
        print(classification_report(y_test, y_pred))

    except KeyError as e:
        logging.error(f"XGBoost çalıştırılırken eksik sütun hatası: {e}")
        return {"error": f"Missing column: {e}"}
    except Exception as e:
        logging.error(f"XGBoost çalıştırılırken bir hata oluştu: {e}")
        return {"error": f"Unexpected error: {e}"}

    return metrics