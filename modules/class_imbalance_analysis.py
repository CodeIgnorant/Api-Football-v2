import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def run_class_imbalance_analysis(df, labels, output_folder="data"):
    """
    Veri setindeki her bir sınıfın dağılımını analiz eder, görselleştirir ve sonuçları raporlar.
    :param df: Analiz edilecek DataFrame.
    :param labels: Sınıf dengesizliği analizi yapılacak sütunların listesi.
    :param output_folder: Çıktıların kaydedileceği ana klasör.
    :return: None
    """
    # Sınıf dengesizliği için alt klasör oluştur
    analysis_folder = os.path.join(output_folder, "class_imbalance_analysis")
    os.makedirs(analysis_folder, exist_ok=True)

    print("Sınıf dengesizliği analizi yapılıyor...")

    imbalance_results = []  # Sonuçları toplamak için bir liste

    for label in labels:
        if label not in df.columns:
            print(f"{label} sütunu DataFrame'de bulunamadı. Atlanıyor.")
            continue

        # Eksik değer kontrolü
        if df[label].isnull().any():
            print(f"{label} sütununda eksik değerler var. Atlınıyor.")
            continue
        
        # Sınıf dağılımı
        class_counts = df[label].value_counts()
        
        # Görselleştirme
        plt.figure(figsize=(10, 6))
        sns.countplot(x=label, data=df, color="blue")  # Tek renk ile uyarıyı önledik
        plt.title(f"Class Imbalance for {label}")
        plt.xlabel(label)
        plt.ylabel("Count")
        plot_path = os.path.join(analysis_folder, f"{label}_class_imbalance.png")
        plt.savefig(plot_path)
        plt.close()
        print(f"Sınıf dengesizliği grafiği kaydedildi: {plot_path}")
        
        # Sonuçları listeye ekle
        for cls, count in class_counts.items():
            imbalance_results.append({"Label": label, "Class": cls, "Count": count})

        # Konsola yazdırma
        print(f"\n{label} sınıf dağılımı:")
        print(class_counts)

    # Sonuçları Excel dosyasına kaydet
    if imbalance_results:
        imbalance_df = pd.DataFrame(imbalance_results)
        excel_path = os.path.join(analysis_folder, "class_imbalance_analysis.xlsx")
        imbalance_df.to_excel(excel_path, index=False)
        print(f"Sınıf dengesizliği analizi sonuçları Excel olarak kaydedildi: {excel_path}")

    print("Sınıf dengesizliği analizi tamamlandı.")