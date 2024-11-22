import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from model_random_forest import train_model

# DataFrame'i oluşturmak için data.xlsx dosyasını oku
def load_data(file_path):
    try:
        df = pd.read_excel(file_path)
        print("Veri başarıyla yüklendi.")
        return df
    except FileNotFoundError:
        print("data.xlsx dosyası bulunamadı. Lütfen dosya yolunu kontrol edin.")
        return None

# Örnek kullanım
data_path = "data/data.xlsx"
data_df = load_data(data_path)

if data_df is not None:
    print(f"Yüklenen veri boyutları: {data_df.shape}")
    print(data_df.dtypes)
    print(data_df.isnull().sum())

    # Kategorik sütunlar
    data_df['Home Team ID'] = data_df['Home Team ID'].astype('category')
    data_df['Away Team ID'] = data_df['Away Team ID'].astype('category')
    data_df['Goal Range'] = data_df['Goal Range'].astype('category')

    # Yeni sütunlar (Home/Away Win Binary sütunları ekle)
    data_df['Binary Home Win'] = data_df['Fulltime Result'].apply(lambda x: 1 if x == "1" else 0)
    data_df['Binary Away Win'] = data_df['Fulltime Result'].apply(lambda x: 1 if x == "2" else 0)

    # Status Short sütununa göre bitmiş ve bitmemiş maçları ayır
    model_df = data_df[data_df['Status Short'] == 'FT'].copy()  # Bitmiş maçlar (Eğitim verisi)
    prediction_df = data_df[data_df['Status Short'] != 'FT'].copy()  # Bitmeyen maçlar (Tahmin verisi)

    print(f"Eğitim verisi boyutu: {model_df.shape}")
    print(f"Tahmin verisi boyutu: {prediction_df.shape}")

    # Normalize edilecek sütunların isimlerini listeye ekle
    features_to_normalize = [
        'Halftime Cumulative Goals - Home', 'Halftime Average Goals - Home', 'Halftime Scoring Rate - Home',
        'Halftime Cumulative Goals - Away', 'Halftime Average Goals - Away', 'Halftime Scoring Rate - Away',
        'Second Half Cumulative Goals - Home', 'Second Half Average Goals - Home', 'Second Half Scoring Rate - Home',
        'Second Half Cumulative Goals - Away', 'Second Half Average Goals - Away', 'Second Half Scoring Rate - Away',
        'Fulltime Cumulative Goals - Home', 'Fulltime Average Goals - Home', 'Fulltime Scoring Rate - Home',
        'Fulltime Cumulative Goals - Away', 'Fulltime Average Goals - Away', 'Fulltime Scoring Rate - Away',
        'Home Fulltime Result Home Win', 'Home Fulltime Result Away Win', 'Home Fulltime Result Draw',
        'Away Fulltime Result Home Win', 'Away Fulltime Result Away Win', 'Away Fulltime Result Draw',
        'Home Halftime Result Home Win', 'Home Halftime Result Away Win', 'Home Halftime Result Draw',
        'Away Halftime Result Home Win', 'Away Halftime Result Away Win', 'Away Halftime Result Draw',
        'Home Secondhalf Result Home Win', 'Home Secondhalf Result Away Win', 'Home Secondhalf Result Draw',
        'Away Secondhalf Result Home Win', 'Away Secondhalf Result Away Win', 'Away Secondhalf Result Draw'
    ]

    # .loc[] ile sütunları ve türleri 'float64' olarak dönüştür
    # Model ve tahmin verisi üzerinde aynı işlemi yapıyoruz
    model_df[features_to_normalize] = model_df[features_to_normalize].astype('float64')
    prediction_df[features_to_normalize] = prediction_df[features_to_normalize].astype('float64')

    # MinMaxScaler ile normalize et
    scaler = MinMaxScaler()

    # Normalizasyon işlemini uygulayalım
    model_df[features_to_normalize] = scaler.fit_transform(model_df[features_to_normalize])
    prediction_df[features_to_normalize] = scaler.transform(prediction_df[features_to_normalize])

    # İşlemin tamamlandığını kontrol etmek için normalize edilmiş sütunları görüntüleyelim
    print(model_df[features_to_normalize].head())
    print(prediction_df[features_to_normalize].head())

    # Labels (model_df için)
    y = model_df['Fulltime Result']

    # Features (model_df için)
    features = [
        'Home Team ID', 'Away Team ID',
        'Halftime Cumulative Goals - Home', 'Halftime Average Goals - Home', 'Halftime Scoring Rate - Home',
        'Halftime Cumulative Goals - Away', 'Halftime Average Goals - Away', 'Halftime Scoring Rate - Away',
        'Second Half Cumulative Goals - Home', 'Second Half Average Goals - Home', 'Second Half Scoring Rate - Home',
        'Second Half Cumulative Goals - Away', 'Second Half Average Goals - Away', 'Second Half Scoring Rate - Away',
        'Fulltime Cumulative Goals - Home', 'Fulltime Average Goals - Home', 'Fulltime Scoring Rate - Home',
        'Fulltime Cumulative Goals - Away', 'Fulltime Average Goals - Away', 'Fulltime Scoring Rate - Away',
        'Home Fulltime Result Home Win', 'Home Fulltime Result Away Win', 'Home Fulltime Result Draw',
        'Away Fulltime Result Home Win', 'Away Fulltime Result Away Win', 'Away Fulltime Result Draw',
        'Home Halftime Result Home Win', 'Home Halftime Result Away Win', 'Home Halftime Result Draw',
        'Away Halftime Result Home Win', 'Away Halftime Result Away Win', 'Away Halftime Result Draw',
        'Home Secondhalf Result Home Win', 'Home Secondhalf Result Away Win', 'Home Secondhalf Result Draw',
        'Away Secondhalf Result Home Win', 'Away Secondhalf Result Away Win', 'Away Secondhalf Result Draw'
    ]
    
    # target_column (hedef sütun) 'Fulltime Result' olarak belirlendi
    target_column = 'Fulltime Result'

    # `train_model` fonksiyonunu çağırıyoruz ve model_df ile prediction_df'yi gönderiyoruz.
    train_model(model_df, prediction_df, features, target_column)