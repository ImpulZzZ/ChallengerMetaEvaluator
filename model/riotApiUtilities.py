import time
import requests

# checks if request limit is near and if so, sleep
def keep_request_limits(response):
    request_limits  = response.headers["X-App-Rate-Limit"].split(",")
    request_counter = response.headers["X-App-Rate-Limit-Count"].split(",")
    requests_per_seconds             = int(request_limits[0].split(":")[0])
    requests_per_two_minutes         = int(request_limits[1].split(":")[0])
    current_requests_per_seconds     = int(request_counter[0].split(":")[0])
    current_requests_per_two_minutes = int(request_counter[1].split(":")[0])

    if (requests_per_seconds - current_requests_per_seconds == 1):
        time.sleep(1)
    
    if (requests_per_two_minutes - current_requests_per_two_minutes == 1):
        time.sleep(120)

# requests Api
def request_api(region, api_key, parameter_url):
    url = f"https://{region}.api.riotgames.com{parameter_url}?api_key={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        print(response.content)
        return None
    keep_request_limits(response)
    return response.json()

# requests TFT-Matches Api
def request_matches_by_match_id(region, api_key, match):
    url = f"https://{region}.api.riotgames.com/tft/match/v1/matches/{match}?api_key={api_key}"
    response = requests.get(url)
    if response.status_code != 200: 
        print(response.content)
        return None
    keep_request_limits(response)
    return response.json()

# requests TFT-Matches Api
def request_matches_by_puuid(region, api_key, puuid, count):
    url = f"https://{region}.api.riotgames.com/tft/match/v1/matches/by-puuid/{puuid}/ids?count={str(count)}&api_key={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        print(response.content)
        return None
    keep_request_limits(response)
    return response.json()

# requests puuid of a summoner by name
def request_puuid_by_summonername(region, api_key, summoner_name):
    url = f"https://{region}.api.riotgames.com/tft/summoner/v1/summoners/by-name/{summoner_name}?&api_key={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        print(response.content) 
        return None
    keep_request_limits(response)
    return response.json()["puuid"]

# requests playerlist by league
def request_players_by_league(region, api_key, ranked_league):
    url = f"https://{region}.api.riotgames.com/tft/league/v1/{ranked_league}?api_key={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        print(response.content) 
        return None
    keep_request_limits(response)
    return response.json()["entries"]

# requests TFT-Matches Api
def request_participants_by_match_id(region, api_key, match):
    url = f"https://{region}.api.riotgames.com/tft/match/v1/matches/{match}?api_key={api_key}"
    response = requests.get(url)
    if response.status_code != 200: 
        print(response.content)
        return None
    keep_request_limits(response)
    return response.json()["info"]["participants"]