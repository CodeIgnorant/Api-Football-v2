import pandas as pd
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
from imblearn.over_sampling import SMOTE  # SMOTE kullanımı
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

# Özellikleri ölçeklendirme
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# SMOTE uygulama
smote = SMOTE(random_state=42)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train_scaled, y_train)
print(f"SMOTE sonrası sınıf dağılımı: {Counter(y_train_resampled)}")

# Logistic Regression için RandomizedSearch parametreleri
param_distributions = {
    'penalty': ['l2'],  # Çok sınıflı için 'l2' kullanıyoruz
    'C': [0.01, 0.1, 1, 10, 100],  # Düzenleme parametresi
    'solver': ['lbfgs', 'saga', 'newton-cg'],  # Çok sınıflı için uygun çözücüler
    'max_iter': [1000, 2000, 3000],  # Maksimum iterasyon artırıldı
    'random_state': [42]
}

# Randomized Search ile Logistic Regression optimizasyonu
random_search = RandomizedSearchCV(
    estimator=LogisticRegression(),  # Çok sınıflı destek için multinomial kullanılıyor
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
y_pred = best_model.predict(X_test_scaled)

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

# Özellikleri ölçeklendirme
prediction_features_scaled = scaler.transform(prediction_features)  # Tahmin verilerini ölçeklendirme

# Tahmin yap
predictions = best_model.predict(prediction_features_scaled)  # Ölçeklendirilmiş verilerle tahmin

# Tahmin sonuçlarını dataframe'e ekle
prediction_data['Prediction'] = predictions

# Tahmin sonuçlarını görüntüleme
print("\nTahmin Sonuçları:")
print(prediction_data[['Home Team Name', 'Away Team Name', 'Prediction']])
