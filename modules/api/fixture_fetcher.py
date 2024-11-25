import logging

def fetch_fixtures(api_client, league_id, season_year, timezone="Europe/Istanbul"):
    """
    Seçilen ligin ve sezonun tüm maçlarını API'den indirir.
    :param api_client: API bağlantısı için kullanılan istemci.
    :param league_id: Lig ID'si.
    :param season_year: Sezon yılı.
    :param timezone: Zaman dilimi parametresi (varsayılan: "Europe/Istanbul").
    :return: Maç verilerinin listesi veya None.
    """
    logging.info(f"{season_year} sezonu için maçlar indiriliyor...")

    # 'fixtures' endpoint'ine istek gönder
    response = api_client.send_request("fixtures", league=league_id, season=season_year, timezone=timezone)
    
    if "error" in response:
        logging.error("Maç verileri alınamadı. Lütfen tekrar deneyin.")
        return None

    fixtures = response.get("response", [])
    if not fixtures:
        logging.warning("Seçilen lig ve sezon için tamamlanmış maç bulunamadı.")
        return None

    logging.info(f"{len(fixtures)} maç başarıyla indirildi.")
    return fixtures