import pandas as pd
import pytz
from datetime import datetime, timezone

def process_fixture_data(fixtures, season_year):
    """
    API'den indirilen maç verilerini işler ve bir pandas DataFrame'e dönüştürür.
    Zaman damgasını Türkiye saatine dönüştürür.
    """
    # Türkiye saat dilimi (Europe/Istanbul)
    istanbul_tz = pytz.timezone("Europe/Istanbul")

    # JSON verisinden seçilen bilgileri çıkar ve işlenmiş bir liste oluştur
    fixtures_data = []
    for fixture in fixtures:
        timestamp = fixture.get("fixture", {}).get("timestamp")
        
        # Zaman dilimini dönüştür
        if timestamp:
            # Unix zaman damgasını datetime objesine dönüştür
            utc_time = datetime.fromtimestamp(timestamp, tz=timezone.utc)
            # UTC zamanını Türkiye saatine dönüştür
            local_time = utc_time.astimezone(istanbul_tz)
            # Türkiye saatine uygun formatta string'e dönüştür
            local_time_str = local_time.strftime('%Y-%m-%d %H:%M:%S')
        else:
            local_time_str = None  # Eğer zaman bilgisi yoksa

        fixtures_data.append({
            "Fixture ID": fixture.get("fixture", {}).get("id"),
            "Timestamp": local_time_str,  # Türkiye saati olarak kaydedildi
            "Status Long": fixture.get("fixture", {}).get("status", {}).get("long"),
            "Status Short": fixture.get("fixture", {}).get("status", {}).get("short"),
            "League ID": fixture.get("league", {}).get("id"),
            "League Name": fixture.get("league", {}).get("name"),
            "League Country": fixture.get("league", {}).get("country"),
            "League Season": fixture.get("league", {}).get("season"),
            "Round": fixture.get("league", {}).get("round"),
            "Home Team ID": fixture.get("teams", {}).get("home", {}).get("id"),
            "Home Team Name": fixture.get("teams", {}).get("home", {}).get("name"),
            "Away Team ID": fixture.get("teams", {}).get("away", {}).get("id"),
            "Away Team Name": fixture.get("teams", {}).get("away", {}).get("name"),
            "Halftime Home Score": fixture.get("score", {}).get("halftime", {}).get("home"),
            "Halftime Away Score": fixture.get("score", {}).get("halftime", {}).get("away"),
            "Fulltime Home Score": fixture.get("score", {}).get("fulltime", {}).get("home"),
            "Fulltime Away Score": fixture.get("score", {}).get("fulltime", {}).get("away")
        })
    
    # DataFrame oluştur
    df = pd.DataFrame(fixtures_data)
    
    return df