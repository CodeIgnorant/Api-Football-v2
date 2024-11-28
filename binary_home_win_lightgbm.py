import pandas as pd
import optuna
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report
from lightgbm import LGBMClassifier
from imblearn.over_sampling import SMOTE
from collections import Counter

# 1. Data klasöründeki ml.csv dosyasını oku
file_path = "data/ml.csv"
ml_data = pd.read_csv(file_path)

# 2. Hedef (target) sütunu ve özellik (features) sütunlarını belirleme
target_column = 'Binary Home Win'  # Hedef sütun
feature_columns = [
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
    'Away Fulltime Result Draw'
]

# 3. Özellikler (X) ve hedef (y) ayrımı
X = ml_data[feature_columns]
y = ml_data[target_column]

# Veriyi eğitim ve test setine böl
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

# SMOTE uygulama
smote = SMOTE(random_state=42)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)
print(f"\n--------------------------\nSMOTE sonrası eğitim seti boyutları: {X_train_resampled.shape}, {y_train_resampled.shape}")
print(f"SMOTE sonrası sınıf dağılımı: {Counter(y_train_resampled)}\n--------------------------")

# Optuna ile hiperparametre optimizasyonu
def objective(trial):
    param = {
        'n_estimators': trial.suggest_int('n_estimators', 50, 200),
        'max_depth': trial.suggest_categorical('max_depth', [3, 5, 7, None]),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.1),
        'num_leaves': trial.suggest_int('num_leaves', 31, 127),
        'min_child_samples': trial.suggest_int('min_child_samples', 5, 20),
        'min_split_gain': trial.suggest_float('min_split_gain', 0.0, 0.5),
        'subsample': trial.suggest_float('subsample', 0.7, 1.0),
        'subsample_freq': trial.suggest_int('subsample_freq', 1, 5),
        'colsample_bytree': trial.suggest_float('colsample_bytree', 0.7, 1.0),
        'reg_alpha': trial.suggest_float('reg_alpha', 0.0, 0.5),
        'reg_lambda': trial.suggest_float('reg_lambda', 0.0, 0.5),
        'class_weight': 'balanced',
        'objective': 'binary',  # İkili sınıflandırma için ayarlanmış
        'random_state': 42,
        'boosting_type': 'gbdt',
    }

    model = LGBMClassifier(**param)
    scores = cross_val_score(model, X_train_resampled, y_train_resampled, cv=5, scoring='accuracy')
    return scores.mean()

# Optuna çalışmasını başlat
study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=50)

# En iyi modeli eğit ve değerlendirme yap
best_params = study.best_params
best_model = LGBMClassifier(**best_params)
best_model.fit(X_train_resampled, y_train_resampled)

y_pred = best_model.predict(X_test)

# En iyi parametreler ve doğruluğu yazdır
print("\n--------------------------")
print("En iyi parametreler:", study.best_params)
print("En iyi model doğruluğu (Cross-Validation):", study.best_value)
print("--------------------------")

# Test doğruluğunu yazdır
accuracy = accuracy_score(y_test, y_pred)
print(f"\n--------------------------\nTest Doğruluğu: {accuracy:.2f}")
print("\nSınıflandırma Raporu:\n", classification_report(y_test, y_pred))
print("--------------------------")

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
print("\n--------------------------\nTahmin Sonuçları:")
print(prediction_data[['Home Team Name', 'Away Team Name', 'Prediction']])
print("--------------------------")