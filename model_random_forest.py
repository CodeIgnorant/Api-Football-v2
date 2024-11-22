import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import pickle

def train_model(model_df, prediction_df, features, target_column='Fulltime Result'):
    # Eğitim verisi (X ve y)
    X_train = model_df[features]
    y_train = model_df[target_column]
    
    # Random Forest modelini oluştur
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    
    # Modeli eğit
    rf_model.fit(X_train, y_train)
    
    # Eğitim sonuçlarını yazdır
    print(f"Model eğitim başarı skoru: {accuracy_score(y_train, rf_model.predict(X_train))}")
    print("Eğitim Seti Sınıflandırma Raporu:")
    print(classification_report(y_train, rf_model.predict(X_train)))
    
    # Tahmin için veriyi hazırla
    X_test = prediction_df[features]
    
    # Tahmin yap
    predictions = rf_model.predict(X_test)
    
    # Tahmin sonuçlarını prediction_df'ye ekle
    prediction_df['Predicted Fulltime Result'] = predictions
    
    # Tahminleri yazdır
    print(f"Tahmin Sonuçları:")
    
    # Home Team ID ve Away Team ID yerine Home Team Name ve Away Team Name kullanarak yazdıralım
    print(prediction_df[['Home Team Name', 'Away Team Name', 'Fulltime Result']].head())
    
    return rf_model