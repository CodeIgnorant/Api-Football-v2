import xgboost as xgb
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report

def run_xgboost(ml_df, features, label):
    """
    XGBoost modelini çalıştırır ve sonuçları döndürür.
    
    :param ml_df: ML için hazırlanmış DataFrame.
    :param features: Kullanılacak features listesi.
    :param label: Hedef label.
    :return: Performans metriklerini ve classification report'u içeren bir sözlük.
    """
    # Veriyi ayırma
    X = ml_df[features]
    y = ml_df[label]
    
    # Eğitim ve test setlerini ayırma (%80 eğitim, %20 test)
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Modeli oluşturma ve eğitme
    model = xgb.XGBClassifier(eval_metric="logloss", use_label_encoder=False)  # "use_label_encoder" kaldırıldı
    model.fit(X_train, y_train)
    
    # Tahmin yapma
    y_pred = model.predict(X_test)
    
    # Performans metriklerini hesaplama
    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred, average="weighted"),
        "recall": recall_score(y_test, y_pred, average="weighted"),
        "f1": f1_score(y_test, y_pred, average="weighted"),
        "classification_report": classification_report(y_test, y_pred, output_dict=True)
    }
    
    # Classification Report'u konsola yazdırma
    print(f"\nXGBoost Classification Report for '{label}':")
    print(classification_report(y_test, y_pred))
    
    return metrics