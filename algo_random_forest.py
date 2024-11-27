import pandas as pd
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from imblearn.over_sampling import SMOTE
from collections import Counter

# 1. Data klasöründeki ml.csv dosyasını oku
file_path = "data/ml.csv"
ml_data = pd.read_csv(file_path)

# 2. Hedef (target) sütunu ve özellik (features) sütunlarını belirleme
target_column = 'Fulltime Result'  # Hedef sütun
feature_columns = [  # Özellik olarak kullanılacak sütunlar
    'Home Team ID',
    'Away Team ID',
    'Fulltime Cumulative Goals - Home',
    'Fulltime Average Goals - Home',
    'Fulltime Scoring Rate - Home',
    'Fulltime Cumulative Goals - Away',
    'Fulltime Average Goals - Away',
    'Fulltime Scoring Rate - Away',
    'Home Fulltime Result Home Win',
    'Home Fulltime Result Away Win',
    'Home Fulltime Result Draw',
    'Away Fulltime Result Home Win',
    'Away Fulltime Result Away Win',
    'Away Fulltime Result Draw',
]

# 3. Özellikler (X) ve hedef (y) ayrımı
X = ml_data[feature_columns]
y = ml_data[target_column]

# Veriyi eğitim ve test setine böl
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# SMOTE uygulama
smote = SMOTE(random_state=42)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)
print(f"SMOTE sonrası sınıf dağılımı: {Counter(y_train_resampled)}")

# Sınıf ağırlıklarını hesapla
class_counts = Counter(y_train_resampled)
total_samples = sum(class_counts.values())
class_weights = {cls: total_samples / (len(class_counts) * count) for cls, count in class_counts.items()}
print("Hesaplanan Class Ağırlıkları:", class_weights)

# Randomized Search için hiperparametre grid'i
param_distributions = {
    'n_estimators': [3, 9, 27, 54, 108],  # Ağaç sayısını artırmak
    'max_depth': [5, 6, 8, 10],  # Derinliği sınırlamak
    'min_samples_split': [10, 15, 20],  # Dallanma için daha yüksek eşik
    'min_samples_leaf': [3, 4, 5],  # Yaprak düğümde daha fazla örnek
    'max_features': ['sqrt', 'log2'],  # Özelliklerin her birini kullanarak en iyi sonucu bulmaya çalışın
    'criterion': ['gini', 'entropy'],  # Bölme kriteri
    'class_weight': ['balanced'],  # Sınıf ağırlıklarını dengeleme
    'bootstrap': [True],  # Bootstrap kullanma
    'oob_score': [True],  # OOB (out-of-bag) skorunu kullanma
    'random_state': [42],  # Sabit random state değeri
    'warm_start': [False],  # Yeni ağaçlar eklenmeden her seferinde baştan başlayın
    'n_jobs': [-1]  # Tüm işlemci çekirdeklerini kullanmak
}

# Randomized Search ile Random Forest optimizasyonu
random_search = RandomizedSearchCV(
    estimator=RandomForestClassifier(random_state=42),
    param_distributions=param_distributions,
    n_iter=50,  # Daha az kombinasyon
    cv=5,  # Çapraz doğrulama
    scoring='accuracy',  # Doğruluğa göre değerlendirme
    n_jobs=-1,
    random_state=42,
    verbose=1
)

# Randomized Search'ü uygulama
random_search.fit(X_train_resampled, y_train_resampled)

# En iyi parametreleri ve doğruluğu yazdır
print("En iyi parametreler:", random_search.best_params_)
print("En iyi model doğruluğu (cross-validation):", random_search.best_score_)

# En iyi modeli seçme
best_model = random_search.best_estimator_

# Test verisi ile tahmin yap
y_pred = best_model.predict(X_test)

# Doğruluk
accuracy = accuracy_score(y_test, y_pred)
print(f"Test Doğruluğu: {accuracy:.2f}")

# Daha detaylı performans raporu
print("\nSınıflandırma Raporu:")
print(classification_report(y_test, y_pred))

# Prediction verisini oku
prediction_file_path = "data/prediction.csv"
prediction_data = pd.read_csv(prediction_file_path)

# Modelin ihtiyaç duyduğu feature sütunlarını seç
prediction_features = prediction_data[feature_columns]

# Tahmin yap
predictions = best_model.predict(prediction_features)

# Tahmin sonuçlarını dataframe'e ekle
prediction_data['Prediction'] = predictions

# Tahmin sonuçlarını görüntüleme
print("\nTahmin Sonuçları:")
print(prediction_data[['Home Team Name', 'Away Team Name', 'Prediction']])