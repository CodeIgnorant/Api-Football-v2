import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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

    # 1. Sayısal sütunları seç
    numeric_df = df.select_dtypes(include=['float64', 'int64'])

    # 2. Korelasyon matrisini hesapla
    correlation_matrix = numeric_df.corr()

    # 3. Yüksek korelasyonları filtrele
    high_corr_pairs = []
    for col in correlation_matrix.columns:
        for idx in correlation_matrix.index:
            if col != idx and abs(correlation_matrix.loc[idx, col]) > 0.7:
                high_corr_pairs.append((idx, col, correlation_matrix.loc[idx, col]))

    # 4. Korelasyon matrisini Excel olarak kaydet
    correlation_excel_path = os.path.join(analysis_folder, "correlation_matrix.xlsx")
    with pd.ExcelWriter(correlation_excel_path, engine="openpyxl") as writer:
        correlation_matrix.to_excel(writer, sheet_name="Correlation Matrix")
        if high_corr_pairs:
            high_corr_df = pd.DataFrame(
                high_corr_pairs, columns=["Feature 1", "Feature 2", "Correlation"]
            )
            high_corr_df.to_excel(writer, sheet_name="High Correlations", index=False)
    print(f"Korelasyon matrisi ve yüksek korelasyonlar '{correlation_excel_path}' olarak kaydedildi.")

    # 5. Korelasyon ısı haritasını görselleştir
    plt.figure(figsize=(12, 10))
    sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm", cbar=True)
    heatmap_path = os.path.join(analysis_folder, "correlation_heatmap.png")
    plt.title("Korelasyon Matrisi Isı Haritası")
    plt.savefig(heatmap_path)
    plt.close()
    print(f"Korelasyon ısı haritası '{heatmap_path}' olarak kaydedildi.")

    # 6. Yüksek korelasyon çiftlerini konsola raporla
    if high_corr_pairs:
        print("\nYüksek korelasyon bulunan çiftler:")
        for idx, col, corr_value in high_corr_pairs:
            print(f"{idx} ve {col}: {corr_value:.2f}")
    else:
        print("\nYüksek korelasyonlu çiftler bulunamadı.")