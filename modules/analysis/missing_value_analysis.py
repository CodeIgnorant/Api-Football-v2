import pandas as pd
import os
import logging

def run_missing_value_analysis(df, output_folder="data"):
    """
    Verilen DataFrame'deki eksik değerleri analiz eder ve raporlar.
    :param df: Analiz edilecek DataFrame.
    :param output_folder: Çıktıların kaydedileceği ana klasör.
    :return: None
    """
    # Analiz için özel bir alt klasör oluştur
    analysis_folder = os.path.join(output_folder, "missing_value_analysis")
    os.makedirs(analysis_folder, exist_ok=True)
    logging.info(f"Eksik veri analizi için '{analysis_folder}' klasörü oluşturuldu.")

    # Eksik değerlerin sayısını ve yüzdesini hesapla
    logging.info("Eksik veri analizi başlatılıyor...")
    missing_counts = df.isnull().sum()
    missing_percentage = (missing_counts / len(df)) * 100
    missing_data = pd.DataFrame({
        "Column": df.columns,
        "Missing Count": missing_counts,
        "Missing Percentage": missing_percentage
    }).sort_values(by="Missing Percentage", ascending=False)
    
    # Sadece eksik verisi olan sütunları filtrele
    missing_data = missing_data[missing_data["Missing Count"] > 0]
    
    if not missing_data.empty:
        logging.info("Eksik veri bulunan sütunlar analiz edildi.")
        logging.debug(f"\n{missing_data}")
    else:
        logging.info("Eksik veri bulunamadı.")

    # Eksik veri raporunu kaydet
    output_path = os.path.join(analysis_folder, "missing_value_analysis.xlsx")
    if not missing_data.empty:
        missing_data.to_excel(output_path, index=False)
        logging.info(f"Eksik veri analizi Excel dosyasına kaydedildi: {output_path}")
    else:
        logging.info(f"Eksik veri bulunamadı. '{analysis_folder}' klasörüne herhangi bir dosya oluşturulmadı.")