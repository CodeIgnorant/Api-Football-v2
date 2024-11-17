def select_country(api_client):
    """
    Kullanıcıya mevcut ülkeleri sunar ve birini seçmesini ister.
    """
    # API'den ülke verilerini al
    response = api_client.send_request("countries")
    if "error" in response:
        print("Ülke verileri alınamadı.")
        return None

    countries = response.get("response", [])
    if not countries:
        print("Ülke listesi boş. Devam edilemiyor.")
        return None

    # Ülkeleri kullanıcıya listele
    for index, country in enumerate(countries, start=1):
        print(f"{index}. {country.get('name')}")

    # Kullanıcının seçimini al
    try:
        choice = int(input("Bir ülke numarası seçin: "))
        if 1 <= choice <= len(countries):
            selected_country = countries[choice - 1]
            print(f"Seçilen ülke: {selected_country['name']}")
            return selected_country['name']
        else:
            print("Geçersiz seçim. Lütfen geçerli bir numara seçin.")
            return None
    except ValueError:
        print("Geçersiz giriş. Lütfen bir sayı girin.")
        return None

def select_league(api_client, country_name):
    """
    Kullanıcıya seçilen ülkenin aktif liglerini sunar ve birini seçmesini ister.
    Ligler sadece isimlerine göre listelenir.
    """
    # API'den lig verilerini al
    response = api_client.send_request("leagues", country=country_name, current="true", type="league")
    if "error" in response:
        print(f"{country_name} için lig verileri alınamadı.")
        return None, None

    leagues = response.get("response", [])
    if not leagues:
        print(f"{country_name} için aktif lig bulunamadı.")
        return None, None

    # Ligleri ID'ye göre sıralayıp kullanıcıya listele
    leagues_sorted = sorted(leagues, key=lambda x: x.get("league", {}).get("id"))
    print("Ligler:")
    for index, league in enumerate(leagues_sorted, start=1):
        league_name = league.get("league", {}).get("name", "Bilinmeyen Lig")
        print(f"{index}. {league_name}")

    # Kullanıcının seçimini al
    try:
        choice = int(input("Bir lig numarası seçin: "))
        if 1 <= choice <= len(leagues_sorted):
            selected_league = leagues_sorted[choice - 1]
            league_id = selected_league.get("league", {}).get("id")
            current_season = next(
                (season for season in selected_league.get("seasons", []) if season.get("current")),
                None
            )
            season_year = current_season.get("year") if current_season else None
            print(f"Seçilen lig: {selected_league.get('league', {}).get('name')} (Sezon: {season_year})")
            return league_id, season_year
        else:
            print("Geçersiz seçim. Lütfen geçerli bir numara seçin.")
            return None, None
    except ValueError:
        print("Geçersiz giriş. Lütfen bir sayı girin.")
        return None, None

def select_country_and_league(api_client):
    """
    Ülke ve lig seçim sürecini yönetir.
    Başarısız olursa None döner.
    """
    # Kullanıcıdan ülke seçimi
    country_name = select_country(api_client)
    if not country_name:
        print("Ülke seçimi başarısız oldu. Program sonlanıyor.")
        return None, None

    # Kullanıcıdan lig seçimi
    league_id, season_year = select_league(api_client, country_name)
    if not league_id or not season_year:
        print("Lig seçimi başarısız oldu. Program sonlanıyor.")
        return None, None

    # Seçilen ülke ve lig bilgilerini döndür
    return league_id, season_year
