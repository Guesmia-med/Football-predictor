
import requests

API_KEY = "7cU7K51e54NYIsn27AAIBhV64o9rytaNK1pOm3ydzj7Em5wWfZFkD50ltGc5"
BASE_URL = "https://api.sportmonks.com/v3/football"

def get_upcoming_matches():
    url = f"{BASE_URL}/fixtures?api_token={API_KEY}&include=localTeam,visitorTeam&per_page=10"
    res = requests.get(url)
    matches = res.json().get("data", [])
    return [{
        "id": match["id"],
        "home": match["localTeam"]["data"]["name"],
        "away": match["visitorTeam"]["data"]["name"]
    } for match in matches]

def get_last_matches_avg_goals(team_id, limit=5):
    url = f"{BASE_URL}/teams/{team_id}/fixtures?api_token={API_KEY}&include=results&limit={limit}"
    res = requests.get(url)
    data = res.json().get("data", [])
    goals = [int(match["scores"]["localteam_score"] if match["localteam_id"] == team_id else match["scores"]["visitorteam_score"]) for match in data]
    return sum(goals) / len(goals) if goals else 1.0
