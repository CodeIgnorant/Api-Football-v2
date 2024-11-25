import logging
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE

# Sabit parametreler
TEST_SIZE = 0.2  # Eğitim-test oranı
RANDOM_STATE = 42  # Rastgelelik kontrolü

# Logging yapılandırması
logging.basicConfig(
    level=logging.INFO,  # INFO seviyesinde log kaydı
    format="%(asctime)s - %(levelname)s - %(message)s",  # Tarih, seviye ve mesaj formatı
    handlers=[logging.StreamHandler()]  # Logları konsola yazdır
)

def prepare_ml_data(dataframe, selected_features, selected_labels):
    """
    ML için veri hazırlık işlemleri. ml_df'nin tamamını kullanır, ancak sadece 
    seçilen features ve labels üzerinde işlem yapar.

    Args:
        dataframe (DataFrame): İşlenecek veri (ml_df).
        selected_features (list): Özellik sütunlarının adları.
        selected_labels (list): Etiket sütunlarının adları.

    Returns:
        X_train_scaled, X_test_scaled, y_train_resampled, y_test: Model eğitimi için hazır veriler.
    """
    logging.info("Veri hazırlama süreci başlatıldı.")

    # 1. Özellikler ve etiketleri ayır
    logging.info("Özellikler (features) ve etiketler (labels) ayrılıyor...")
    try:
        X = dataframe[selected_features]
        y = dataframe[selected_labels[0]]  # Tek bir hedef sütun kabul ediliyor
    except KeyError as e:
        logging.error(f"Sütun seçimi sırasında hata: {e}")
        raise

    # 2. Eğitim ve test setine ayır
    logging.info("Veri eğitim ve test olarak ayrılıyor...")
    try:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
        )
    except ValueError as e:
        logging.error(f"Train-test bölme sırasında hata: {e}")
        raise

    # 3. SMOTE ile veri dengelemesi
    logging.info("SMOTE ile veri dengeleniyor...")
    try:
        smote = SMOTE(random_state=RANDOM_STATE)
        X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)
    except Exception as e:
        logging.error(f"SMOTE sırasında hata: {e}")
        raise

    # 4. Özelliklerin ölçeklendirilmesi
    logging.info("Özellikler ölçeklendiriliyor...")
    try:
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train_resampled)
        X_test_scaled = scaler.transform(X_test)
    except Exception as e:
        logging.error(f"Ölçeklendirme sırasında hata: {e}")
        raise

    logging.info("Veri hazırlama süreci başarıyla tamamlandı.")
    return X_train_scaled, X_test_scaled, y_train_resampled, y_test