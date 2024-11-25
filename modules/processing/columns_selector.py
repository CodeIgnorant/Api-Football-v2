def select_columns(dataframe):
    """
    Kullanıcıdan sütun seçimlerini alır ve labels ile features sütunlarını ayırır.

    Args:
        dataframe (DataFrame): Sütunları ayrılacak olan veri.

    Returns:
        labels (DataFrame): Etiket sütunları.
        features (DataFrame): Özellik sütunları.
        selected_labels (list): Seçilen etiket sütun adları.
        selected_features (list): Seçilen özellik sütun adları.
    """
    # Sütunları listele
    print("Veri sütunları aşağıdaki gibidir:")
    for i, column in enumerate(dataframe.columns):
        print(f"{i + 1}. {column}")

    # Labels sütunlarını seçme
    label_indices = input("\nLabels (etiket) sütunlarının numaralarını virgülle ayırarak giriniz: ")
    label_indices = [int(idx.strip()) - 1 for idx in label_indices.split(",")]
    selected_labels = [dataframe.columns[idx] for idx in label_indices]
    print(f"Seçilen labels sütunları: {selected_labels}")

    # Features sütunlarını seçme
    feature_indices = input("\nFeatures (özellikler) sütunlarının numaralarını virgülle ayırarak giriniz: ")
    feature_indices = [int(idx.strip()) - 1 for idx in feature_indices.split(",")]
    selected_features = [dataframe.columns[idx] for idx in feature_indices]
    print(f"Seçilen features sütunları: {selected_features}")

    # Veriyi ayırma
    labels = dataframe[selected_labels]
    features = dataframe[selected_features]

    return labels, features, selected_labels, selected_features