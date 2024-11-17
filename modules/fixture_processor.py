import pandas as pd

def process_fixture_data(fixtures, season_year):
    """
    API'den indirilen maç verilerini işler ve bir pandas DataFrame'e dönüştürür.
    """
    # JSON verisinden seçilen bilgileri çıkar ve işlenmiş bir liste oluştur
    fixtures_data = []
    for fixture in fixtures:
        fixtures_data.append({
            "Fixture ID": fixture.get("fixture", {}).get("id"),
            "Timestamp": fixture.get("fixture", {}).get("timestamp"),
            "Status Long": fixture.get("fixture", {}).get("status", {}).get("long"),
            "Status Short": fixture.get("fixture", {}).get("status", {}).get("short"),
            "League ID": fixture.get("league", {}).get("id"),
            "League Name": fixture.get("league", {}).get("name"),
            "League Country": fixture.get("league", {}).get("country"),
            "League Season": fixture.get("league", {}).get("season"),
            "Round": fixture.get("league", {}).get("round"),  # Round ham haliyle alınıyor
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