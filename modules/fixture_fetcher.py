def fetch_fixtures(api_client, league_id, season_year, timezone="Europe/Istanbul"):
    """
    Seçilen ligin ve sezonun tüm maçlarını API'den indirir.
    :param timezone: Zaman dilimi parametresi (varsayılan: "Europe/Istanbul").
    """
    print(f"{season_year} sezonu için maçlar indiriliyor...")

    # 'fixtures' endpoint'ine istek gönder
    response = api_client.send_request("fixtures", league=league_id, season=season_year, timezone=timezone)
    
    if "error" in response:
        print("Maç verileri alınamadı. Lütfen tekrar deneyin.")
        return None

    fixtures = response.get("response", [])
    if not fixtures:
        print("Seçilen lig ve sezon için tamamlanmış maç bulunamadı.")
        return None

    print(f"{len(fixtures)} maç başarıyla indirildi.")
    return fixtures