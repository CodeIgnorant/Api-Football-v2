from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import GridSearchCV, StratifiedKFold
import logging
import numpy as np

# Logging yapılandırması
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)

def train_logistic_regression(X_train, X_test, y_train, y_test):
    """
    Logistic Regression modeli ile hiperparametre optimizasyonu, eğitim ve değerlendirme işlemlerini yapar.

    Args:
        X_train (ndarray): Eğitim özellikleri.
        X_test (ndarray): Test özellikleri.
        y_train (ndarray): Eğitim etiketleri.
        y_test (ndarray): Test etiketleri.

    Returns:
        model: En iyi Logistic Regression modeli.
        predictions: Test seti üzerindeki tahminler.
    """
    logging.info("Logistic Regression hiperparametre optimizasyonu başlatılıyor...")

    # Hiperparametre ızgarası
    param_grid = {
        "solver": ["lbfgs", "liblinear", "sag"],
        "class_weight": ["balanced", None],
        "C": [0.01, 0.1, 1, 10, 100],  # Regularizasyon parametresi
        "max_iter": [100, 200, 300]
    }

    # Logistic Regression modeli
    base_model = LogisticRegression(multi_class="multinomial", random_state=42)

    # GridSearchCV ile hiperparametre optimizasyonu
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    grid_search = GridSearchCV(
        estimator=base_model,
        param_grid=param_grid,
        scoring="accuracy",
        cv=skf,
        verbose=1,
        n_jobs=-1
    )

    # Optimizasyonu gerçekleştir
    grid_search.fit(X_train, y_train)
    best_params = grid_search.best_params_
    logging.info(f"En iyi hiperparametreler: {best_params}")

    # En iyi modelle eğitimi tamamla
    best_model = grid_search.best_estimator_

    # Test seti üzerinde tahminler yap
    logging.info("Logistic Regression modeli test seti üzerinde tahmin yapıyor...")
    predictions = best_model.predict(X_test)

    # Model performansını değerlendirme
    accuracy = accuracy_score(y_test, predictions)
    logging.info(f"Test seti doğruluğu: {accuracy}")

    logging.info("Classification Report:")
    report = classification_report(y_test, predictions, target_names=["Draw (0)", "Home Win (1)", "Away Win (2)"])
    print(report)

    logging.info("Confusion Matrix:")
    print(confusion_matrix(y_test, predictions))

    return best_model, predictions
