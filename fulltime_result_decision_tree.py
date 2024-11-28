import pandas as pd
import optuna
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE

# 1. Data klasöründeki ml.csv dosyasını oku
file_path = "data/ml.csv"
ml_data = pd.read_csv(file_path)

# 2. Label Encoding for Home Team ID and Away Team ID
label_encoder_home = LabelEncoder()
label_encoder_away = LabelEncoder()

ml_data['Home Team ID'] = label_encoder_home.fit_transform(ml_data['Home Team ID'])
ml_data['Away Team ID'] = label_encoder_away.fit_transform(ml_data['Away Team ID'])

print("Home Team ID ve Away Team ID sütunları için Label Encoding tamamlandı.")

# 3. Hedef (target) sütunu ve özellik (features) sütunlarını belirleme
target_column = 'Fulltime Result'  # Hedef sütun
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
    'Away Fulltime Result Draw',
]

# 4. Özellikler (X) ve hedef (y) ayrımı
X = ml_data[feature_columns]
y = ml_data[target_column]

# Veriyi eğitim ve test setine böl
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# SMOTE uygulama
smote = SMOTE(random_state=42)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)
print(f"SMOTE sonrası eğitim seti boyutları: {X_train_resampled.shape}, {y_train_resampled.shape}")

# Optuna ile hiperparametre optimizasyonu
def objective(trial):
    param = {
        'criterion': trial.suggest_categorical('criterion', ['gini', 'entropy']),
        'max_depth': trial.suggest_int('max_depth', 5, 20, step=5),
        'min_samples_split': trial.suggest_int('min_samples_split', 5, 20, step=5),
        'min_samples_leaf': trial.suggest_int('min_samples_leaf', 2, 10, step=2),
        'max_features': trial.suggest_categorical('max_features', ['sqrt', 'log2', None]),
        'random_state': 42
    }
    model = DecisionTreeClassifier(**param)
    scores = cross_val_score(model, X_train_resampled, y_train_resampled, cv=5, scoring='accuracy')
    return scores.mean()

# Optuna çalışmasını başlat
study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=50)

# En iyi parametreler ve doğruluğu yazdır
print("\n--------------------------")
print("En iyi parametreler:", study.best_params)
print("En iyi model doğruluğu (Cross-Validation):", study.best_value)
print("--------------------------")

# En iyi modeli eğit ve değerlendirme yap
best_params = study.best_params
best_model = DecisionTreeClassifier(**best_params)
best_model.fit(X_train_resampled, y_train_resampled)

y_pred = best_model.predict(X_test)

# Test doğruluğunu yazdır
accuracy = accuracy_score(y_test, y_pred)
print(f"\n--------------------------\nTest Doğruluğu: {accuracy:.2f}")
print("\nSınıflandırma Raporu:\n", classification_report(y_test, y_pred))
print("--------------------------")

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
