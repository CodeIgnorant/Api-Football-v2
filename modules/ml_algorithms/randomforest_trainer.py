from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from modules.ml_metrics_calculator import calculate_metrics

def run_randomforest(ml_df, features, label):
    """
    Verilen label ve features ile Random Forest modelini çalıştırır.
    
    :param ml_df: ML için hazırlanmış DataFrame.
    :param features: Kullanılacak features listesi.
    :param label: Hedef label.
    :return: Performans metriklerini ve classification report'u içeren bir sözlük.
    """
    X = ml_df[features]
    y = ml_df[label]
    
    # Veriyi train-test olarak ayır
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Modeli eğit
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    
    # Tahmin yap
    predictions = model.predict(X_test)
    
    # Metrikleri hesapla
    metrics = calculate_metrics(y_test, predictions)
    metrics["classification_report"] = classification_report(y_test, predictions, output_dict=True)
    
    # Classification Report'u konsola yazdır
    print(f"\nRandom Forest Classification Report for '{label}':")
    print(classification_report(y_test, predictions))
    
    return metrics