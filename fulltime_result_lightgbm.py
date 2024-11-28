import pandas as pd
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder  # Label Encoder ekledik
from lightgbm import LGBMClassifier
from imblearn.over_sampling import SMOTE  # SMOTE kullanımı
from collections import Counter

# 1. Data klasöründeki ml.csv dosyasını oku
file_path = "data/ml.csv"
ml_data = pd.read_csv(file_path)

# Label Encoding işlemi
label_encoder_home = LabelEncoder()
label_encoder_away = LabelEncoder()

ml_data['Home Team ID'] = label_encoder_home.fit_transform(ml_data['Home Team ID'])
ml_data['Away Team ID'] = label_encoder_away.fit_transform(ml_data['Away Team ID'])

# 2. Hedef (target) sütunu ve özellik (features) sütunlarını belirleme
target_column = 'Fulltime Result'  # Hedef sütun
feature_columns = [  # Özellik olarak kullanılacak sütunlar
    'Home Team ID',
    'Away Team ID',
    # 'Halftime Home Score',
    # 'Halftime Away Score',
    # 'Fulltime Home Score',
    # 'Fulltime Away Score',
    # 'Secondhalf Home Score',
    # 'Secondhalf Away Score',
    # 'Fulltime Result',
    # 'Halftime Result',
    # 'Secondhalf Result',
    # 'Binary Home Win',
    # 'Binary Away Win',
    # 'Halftime Total Goals',
    # 'Secondhalf Total Goals',
    # 'Fulltime Total Goals',
    # 'Fulltime Home Over 0.5',
    # 'Fulltime Home Over 1.5',
    # 'Fulltime Home Over 2.5',
    # 'Fulltime Home Over 3.5',
    # 'Fulltime Away Over 0.5',
    # 'Fulltime Away Over 1.5',
    # 'Fulltime Away Over 2.5',
    # 'Fulltime Away Over 3.5',
    # 'Fulltime Over 0.5',
    # 'Fulltime Over 1.5',
    # 'Fulltime Over 2.5',
    # 'Fulltime Over 3.5',
    # 'Goal Range',
    # 'Both Team Score',
    # 'Halftime Home Clean Sheet',
    # 'Halftime Away Clean Sheet',
    # 'Secondhalf Home Clean Sheet',
    # 'Secondhalf Away Clean Sheet',
    # 'Fulltime Home Clean Sheet',
    # 'Fulltime Away Clean Sheet',
    # 'Halftime Home Fail to Score',
    # 'Halftime Away Fail to Score',
    # 'Secondhalf Home Fail to Score',
    # 'Secondhalf Away Fail to Score',
    # 'Fulltime Home Fail to Score',
    # 'Fulltime Away Fail to Score',
    # 'Home Point',
    # 'Away Point',
    'Home Point Cumulative',
    'Away Point Cumulative',
    # 'Halftime Cumulative Goals - Home',
    # 'Halftime Average Goals - Home',
    # 'Halftime Scoring Rate - Home',
    # 'Halftime Cumulative Goals - Away',
    # 'Halftime Average Goals - Away',
    # 'Halftime Scoring Rate - Away',
    # 'Second Half Cumulative Goals - Home',
    # 'Second Half Average Goals - Home',
    # 'Second Half Scoring Rate - Home',
    # 'Second Half Cumulative Goals - Away',
    # 'Second Half Average Goals - Away',
    # 'Second Half Scoring Rate - Away',
    # 'Fulltime Cumulative Goals - Home',
    'Fulltime Average Goals - Home',
    # 'Fulltime Scoring Rate - Home',
    # 'Fulltime Cumulative Goals - Away',
    'Fulltime Average Goals - Away',
    # 'Fulltime Scoring Rate - Away',
    # 'Home Fulltime Result Home Win',
    # 'Home Fulltime Result Away Win',
    # 'Home Fulltime Result Draw',
    # 'Away Fulltime Result Home Win',
    # 'Away Fulltime Result Away Win',
    # 'Away Fulltime Result Draw',
    # 'Home Halftime Result Home Win',
    # 'Home Halftime Result Away Win',
    # 'Home Halftime Result Draw',
    # 'Away Halftime Result Home Win',
    # 'Away Halftime Result Away Win',
    # 'Away Halftime Result Draw',
    # 'Home Secondhalf Result Home Win',
    # 'Home Secondhalf Result Away Win',
    # 'Home Secondhalf Result Draw',
    # 'Away Secondhalf Result Home Win',
    # 'Away Secondhalf Result Away Win',
    # 'Away Secondhalf Result Draw',
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
    'n_estimators': [50, 100, 200],  # Ağaç sayısı
    'max_depth': [3, 7, None],  # Maksimum derinlik (None: sınırsız)
    'learning_rate': [0.01, 0.05, 0.1],  # Öğrenme oranı
    'num_leaves': [31, 63, 127],  # Maksimum yaprak sayısı
    'min_child_samples': [5, 10, 20],  # Minimum dallanma örneği
    'min_split_gain': [0, 0.1, 0.2],  # Bölünme için minimum kazanç
    # 'subsample': [0.7, 0.8, 0.9],  # Alt örnekleme oranı
    'bagging_fraction': [0.7, 0.8, 0.9],  # Alternatif olarak subsample yerine kullanılabilir
    'bagging_freq': [1, 5],  # Eğer bagging_fraction kullanılıyorsa aktif edilebilir
    'colsample_bytree': [0.7, 0.8, 1.0],  # Ağaç başına sütun örnekleme oranı
    'reg_alpha': [0.0, 0.1, 0.5],  # L1 düzenleme
    'reg_lambda': [0.0, 0.1, 0.5],  # L2 düzenleme
    'class_weight': [class_weights],  # Sınıf ağırlıkları
    'scale_pos_weight': [0.5, 1.0, 2.0],  # Pozitif sınıf ağırlığı
    'random_state': [42]
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
prediction_data['Home Team ID'] = label_encoder_home.transform(prediction_data['Home Team ID'])
prediction_data['Away Team ID'] = label_encoder_away.transform(prediction_data['Away Team ID'])
prediction_features = prediction_data[feature_columns]

# Tahmin yap
predictions = best_model.predict(prediction_features)

# Tahmin sonuçlarını dataframe'e ekle
prediction_data['Prediction'] = predictions

# Tahmin sonuçlarını görüntüleme
print("\nTahmin Sonuçları:")
print(prediction_data[['Home Team Name', 'Away Team Name', 'Prediction']])