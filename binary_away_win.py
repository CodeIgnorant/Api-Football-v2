import pandas as pd
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import accuracy_score, classification_report
from lightgbm import LGBMClassifier
from imblearn.over_sampling import SMOTE  # SMOTE kullanımı
from collections import Counter

# 1. Data klasöründeki ml.csv dosyasını oku
file_path = "data/ml.csv"
ml_data = pd.read_csv(file_path)

# 2. Hedef (target) sütunu ve özellik (features) sütunlarını belirleme
target_column = 'Binary Away Win'  # Hedef sütun
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
print(f"SMOTE sonrası eğitim seti boyutları: {X_train_resampled.shape}, {y_train_resampled.shape}")
print(f"SMOTE sonrası sınıf dağılımı: {Counter(y_train_resampled)}")

# Class ağırlıkları hesaplama
class_counts = Counter(y_train_resampled)
total_samples = sum(class_counts.values())
class_weights = {cls: total_samples / (len(class_counts) * count) for cls, count in class_counts.items()}
print("Sınıf Ağırlıkları:", class_weights)

# LightGBM modeli için Randomized Search parametreleri
param_distributions = {
    'n_estimators': [3, 6, 12],  # Ağaç sayısı
    'max_depth': [3, 5, 7],  # Maksimum derinlik
    'learning_rate': [0.01, 0.05, 0.1],  # Öğrenme oranı
    'num_leaves': [31, 63],  # Maksimum yaprak sayısı
    'min_child_samples': [5, 10, 20],  # Dallanma için minimum örnek
    'subsample': [0.8, 1.0],  # Alt örnekleme oranı
    'colsample_bytree': [0.8, 1.0],  # Ağaç başına sütun örnekleme
    'reg_alpha': [0.1, 0.5],  # L1 düzenleme
    'reg_lambda': [0.5, 1.0],  # L2 düzenleme
    'class_weight': [class_weights]  # Hesaplanan sınıf ağırlıkları
}

# Randomized Search ile LightGBM optimizasyonu
random_search = RandomizedSearchCV(
    estimator=LGBMClassifier(random_state=42),
    param_distributions=param_distributions,
    n_iter=50,  # Daha az kombinasyon
    cv=5,  # 5 katlı çapraz doğrulama
    scoring='accuracy',  # Doğruluğa göre değerlendirme
    n_jobs=-1,
    random_state=42,
    verbose=1
)

# Modeli eğit ve en iyi parametreleri bul
random_search.fit(X_train_resampled, y_train_resampled)

# En iyi parametreleri ve çapraz doğrulama doğruluğunu yazdır
print("En iyi parametreler:", random_search.best_params_)
print("En iyi model doğruluğu (cross-validation):", random_search.best_score_)

# En iyi modeli seç
best_model = random_search.best_estimator_

# Test verisi ile tahmin yap
y_pred = best_model.predict(X_test)

# Test doğruluğunu yazdır
accuracy = accuracy_score(y_test, y_pred)
print(f"Test Doğruluğu: {accuracy:.2f}")

# Daha detaylı sınıflandırma raporu
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