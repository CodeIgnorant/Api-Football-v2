import logging
import pandas as pd

def make_predictions(model, prediction_df, features):
    """
    Logistic Regression modeli kullanarak tahminleri gerçekleştirir ve terminalde gösterir.

    Args:
        model: Eğitimde kullanılan Logistic Regression modeli.
        prediction_df (DataFrame): Tahmin yapılacak veri seti.
        features (list): Kullanılacak özellik sütunlarının listesi.

    Returns:
        None
    """
    logging.info("Tahmin işlemi başlatılıyor...")

    try:
        # Özellik sütunlarını kontrol et
        if not all(feature in prediction_df.columns for feature in features):
            missing_features = [feature for feature in features if feature not in prediction_df.columns]
            raise ValueError(f"Eksik özellik sütunları: {missing_features}")

        # Tahmin işlemi
        X_prediction = prediction_df[features]
        prediction_df['Prediction'] = model.predict(X_prediction)

        # Tahmin sonuçlarını terminalde göster
        print("\n=== Tahmin Sonuçları ===")
        for index, row in prediction_df.iterrows():
            home_team = row.get("Home Team Name", "Unknown Home")
            away_team = row.get("Away Team Name", "Unknown Away")
            prediction = row['Prediction']

            result_mapping = {
                0: "Draw",
                1: "Home Win",
                2: "Away Win"
            }
            predicted_result = result_mapping.get(prediction, "Unknown Result")
            print(f"{home_team} vs {away_team}: Tahmin - {predicted_result}")

        logging.info("Tahmin işlemi tamamlandı.")

    except ValueError as ve:
        logging.error(f"Tahmin sırasında bir değer hatası oluştu: {ve}")
    except Exception as e:
        logging.error(f"Tahmin işlemi sırasında beklenmeyen bir hata oluştu: {e}")
