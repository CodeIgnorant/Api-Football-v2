from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
import logging

def calculate_metrics(y_true, y_pred):
    """
    Verilen gerçek (y_true) ve tahmin edilen (y_pred) değerler için sınıflandırma metriklerini hesaplar.
    :param y_true: Gerçek etiketler (ground truth).
    :param y_pred: Tahmin edilen etiketler.
    :return: Sınıflandırma metriklerini içeren bir sözlük.
    """
    logging.info("Sınıflandırma metrikleri hesaplanmaya başlıyor...")

    metrics = {
        "Accuracy": accuracy_score(y_true, y_pred),
        "Precision": precision_score(y_true, y_pred, average='weighted', zero_division=0),
        "Recall": recall_score(y_true, y_pred, average='weighted', zero_division=0),
        "F1 Score": f1_score(y_true, y_pred, average='weighted', zero_division=0),
        "Classification Report": classification_report(y_true, y_pred, zero_division=0)
    }

    # Loglama
    logging.info(f"Accuracy: {metrics['Accuracy']:.4f}")
    logging.info(f"Precision: {metrics['Precision']:.4f}")
    logging.info(f"Recall: {metrics['Recall']:.4f}")
    logging.info(f"F1 Score: {metrics['F1 Score']:.4f}")
    logging.info("Classification Report:")
    logging.info(metrics["Classification Report"])

    logging.info("Sınıflandırma metrikleri başarıyla hesaplandı.")
    return metrics