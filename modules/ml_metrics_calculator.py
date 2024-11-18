from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report

def calculate_metrics(y_true, y_pred):
    """
    Verilen gerçek (y_true) ve tahmin edilen (y_pred) değerler için sınıflandırma metriklerini hesaplar.
    :param y_true: Gerçek etiketler (ground truth).
    :param y_pred: Tahmin edilen etiketler.
    :return: Sınıflandırma metriklerini içeren bir sözlük.
    """
    metrics = {
        "Accuracy": accuracy_score(y_true, y_pred),
        "Precision": precision_score(y_true, y_pred, average='weighted', zero_division=0),
        "Recall": recall_score(y_true, y_pred, average='weighted', zero_division=0),
        "F1 Score": f1_score(y_true, y_pred, average='weighted', zero_division=0),
        "Classification Report": classification_report(y_true, y_pred, zero_division=0)
    }
    return metrics