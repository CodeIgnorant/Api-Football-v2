import xgboost as xgb
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import GridSearchCV
import logging
import numpy as np

# Logging yapılandırması
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)

def train_xgboost(X_train, X_test, y_train, y_test):
    """
    XGBoost modeli ile çok sınıflı sınıflandırma eğitimi ve değerlendirme işlemlerini yapar.
    Hiperparametre optimizasyonu içerir.

    Args:
        X_train (ndarray): Eğitim özellikleri.
        X_test (ndarray): Test özellikleri.
        y_train (ndarray): Eğitim etiketleri.
        y_test (ndarray): Test etiketleri.

    Returns:
        model: Eğitimli XGBoost modeli.
        predictions: Test seti üzerindeki tahminler.
    """
    logging.info("XGBoost modeli eğitilmeye başlanıyor...")

    # Sınıf sayısını belirle
    num_classes = len(np.unique(y_train))
    logging.info(f"Toplam sınıf sayısı: {num_classes}")

    # Hiperparametre optimizasyonu için Grid Search
    logging.info("Hiperparametre optimizasyonu başlatılıyor...")
    param_grid = {
        "max_depth": [3, 5, 7],         # Maksimum derinlik
        "eta": [0.01, 0.1, 0.2],       # Öğrenme oranı
        "num_boost_round": [50, 100]   # Boosting iterasyon sayısı
    }

    # Grid Search için XGBClassifier kullanıyoruz
    xgb_model = xgb.XGBClassifier(
        objective="multi:softprob",
        num_class=num_classes,
        eval_metric="mlogloss",
        random_state=42,
        use_label_encoder=False  # Sklearn API için gerekli
    )

    grid_search = GridSearchCV(
        estimator=xgb_model,
        param_grid=param_grid,
        scoring="accuracy",
        cv=5,  # Çapraz doğrulama katman sayısı
        verbose=1
    )

    # Grid Search ile en iyi parametreleri bul
    grid_search.fit(X_train, y_train)
    best_params = grid_search.best_params_
    logging.info(f"En iyi hiperparametreler: {best_params}")

    # En iyi parametrelerle modeli yeniden eğit
    logging.info("En iyi parametrelerle model yeniden eğitiliyor...")
    final_model = xgb.train(
        params={
            "objective": "multi:softprob",
            "num_class": num_classes,
            "eval_metric": "mlogloss",
            "eta": best_params["eta"],
            "max_depth": best_params["max_depth"],
            "random_state": 42
        },
        dtrain=xgb.DMatrix(X_train, label=y_train),
        num_boost_round=best_params["num_boost_round"]
    )

    # Test seti üzerinde tahminler
    logging.info("XGBoost tahminleri yapılıyor...")
    predictions_prob = final_model.predict(xgb.DMatrix(X_test))  # Olasılık tahmini
    predictions = np.argmax(predictions_prob, axis=1)  # Maksimum olasılığa sahip sınıfı seç

    # Model performansı
    accuracy = accuracy_score(y_test, predictions)
    logging.info(f"Model Accuracy: {accuracy}")

    logging.info("Classification Report:")
    report = classification_report(y_test, predictions, target_names=["Draw (0)", "Home Win (1)", "Away Win (2)"])
    print(report)

    logging.info("Confusion Matrix:")
    print(confusion_matrix(y_test, predictions))

    return final_model, predictions