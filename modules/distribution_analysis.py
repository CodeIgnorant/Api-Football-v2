import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def run_distribution_analysis(df, output_folder="data"):
    """
    Veri setindeki sütunların dağılımını analiz eder ve görselleştirir.
    :param df: Analiz edilecek DataFrame.
    :param output_folder: Çıktıların kaydedileceği ana klasör.
    :return: None
    """
    # Analiz için özel bir alt klasör oluştur
    analysis_folder = os.path.join(output_folder, "distribution_analysis")
    os.makedirs(analysis_folder, exist_ok=True)
    
    print("Veri dağılımı analizi yapılıyor...")

    # Sayısal sütunlar için histogramlar
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
    for col in numeric_columns:
        plt.figure(figsize=(10, 6))
        sns.histplot(df[col], kde=True, bins=30, color="blue")
        plt.title(f"Histogram of {col}")
        plt.xlabel(col)
        plt.ylabel("Frequency")
        plot_path = os.path.join(analysis_folder, f"{col}_distribution.png")
        plt.savefig(plot_path)
        plt.close()
        print(f"{col} için histogram kaydedildi: {plot_path}")

    # Kategorik sütunlar için bar grafikleri
    categorical_columns = df.select_dtypes(include=['object', 'category']).columns
    for col in categorical_columns:
        plt.figure(figsize=(10, 6))
        df[col].value_counts().plot(kind='bar', color="orange")
        plt.title(f"Bar Chart of {col}")
        plt.xlabel(col)
        plt.ylabel("Count")
        plot_path = os.path.join(analysis_folder, f"{col}_distribution.png")
        plt.savefig(plot_path)
        plt.close()
        print(f"{col} için bar grafiği kaydedildi: {plot_path}")

    print("Veri dağılımı analizi tamamlandı.")