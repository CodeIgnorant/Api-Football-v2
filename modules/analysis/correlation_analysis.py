import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging

def run_correlation_analysis(df, output_folder="data"):
    """
    Verilen DataFrame'deki sayısal sütunlar için korelasyon analizi yapar ve sonuçları raporlar.
    
    :param df: Analiz edilecek DataFrame.
    :param output_folder: Sonuçların kaydedileceği klasör.
    :return: None
    """
    # Analiz için alt klasörü oluştur
    analysis_folder = os.path.join(output_folder, "correlation_analysis")
    os.makedirs(analysis_folder, exist_ok=True)
    logging.info(f"Korelasyon analizi için klasör oluşturuldu: {analysis_folder}")

    # 1. Sayısal sütunları seç
    numeric_df = df.select_dtypes(include=['float64', 'int64'])
    logging.info(f"Sayısal sütunlar seçildi. Toplam {len(numeric_df.columns)} sütun bulundu.")

    # 2. Korelasyon matrisini hesapla
    correlation_matrix = numeric_df.corr()
    logging.info("Korelasyon matrisi hesaplandı.")

    # 3. Yüksek korelasyonları filtrele
    high_corr_pairs = []
    for col in correlation_matrix.columns:
        for idx in correlation_matrix.index:
            if col != idx and abs(correlation_matrix.loc[idx, col]) > 0.7:
                high_corr_pairs.append((idx, col, correlation_matrix.loc[idx, col]))
    logging.info(f"Yüksek korelasyonlu {len(high_corr_pairs)} çift bulundu.")

    # 4. Korelasyon matrisini Excel olarak kaydet
    correlation_excel_path = os.path.join(analysis_folder, "correlation_matrix.xlsx")
    with pd.ExcelWriter(correlation_excel_path, engine="openpyxl") as writer:
        correlation_matrix.to_excel(writer, sheet_name="Correlation Matrix")
        if high_corr_pairs:
            high_corr_df = pd.DataFrame(
                high_corr_pairs, columns=["Feature 1", "Feature 2", "Correlation"]
            )
            high_corr_df.to_excel(writer, sheet_name="High Correlations", index=False)
    logging.info(f"Korelasyon matrisi ve yüksek korelasyonlar Excel dosyasına kaydedildi: {correlation_excel_path}")

    # 5. Korelasyon ısı haritasını görselleştir
    plt.figure(figsize=(12, 10))
    sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm", cbar=True)
    heatmap_path = os.path.join(analysis_folder, "correlation_heatmap.png")
    plt.title("Korelasyon Matrisi Isı Haritası")
    plt.savefig(heatmap_path)
    plt.close()
    logging.info(f"Korelasyon ısı haritası kaydedildi: {heatmap_path}")

    # 6. Yüksek korelasyon çiftlerini konsola raporla
    if high_corr_pairs:
        logging.info("Yüksek korelasyon bulunan çiftler:")
        for idx, col, corr_value in high_corr_pairs:
            logging.info(f"{idx} ve {col}: {corr_value:.2f}")
    else:
        logging.info("Yüksek korelasyonlu çiftler bulunamadı.")