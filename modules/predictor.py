from modules.predictor import get_upcoming_matches

def main():
    """
    Programın ana fonksiyonu.
    """
    # ... Önceki adımlar (fixtures_df oluşturuldu)

    # Sıradaki maçları seç
    upcoming_matches = get_upcoming_matches(fixtures_df)
    
    # Sıradaki maçları kaydet veya işlemek üzere döndür
    if not upcoming_matches.empty:
        upcoming_matches_file = "data/upcoming_matches.xlsx"
        upcoming_matches.to_excel(upcoming_matches_file, index=False)
        print(f"Sıradaki maçlar '{upcoming_matches_file}' dosyasına kaydedildi.")
    else:
        print("Tahmin yapılacak maç bulunamadı.")