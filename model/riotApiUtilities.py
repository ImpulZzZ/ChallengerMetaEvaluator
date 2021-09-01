import time
import requests

## Checks if request was successfull and handles Key limits
def valid_request(response):
    if response.status_code != 200:
        print(response.content)
        return False

    request_limits  = response.headers["X-App-Rate-Limit"].split(",")
    request_counter = response.headers["X-App-Rate-Limit-Count"].split(",")
    requests_per_seconds             = int(request_limits[0].split(":")[0])
    requests_per_two_minutes         = int(request_limits[1].split(":")[0])
    current_requests_per_seconds     = int(request_counter[0].split(":")[0])
    current_requests_per_two_minutes = int(request_counter[1].split(":")[0])

    if (requests_per_seconds - current_requests_per_seconds == 1):
        time.sleep(1)
    
    if (requests_per_two_minutes - current_requests_per_two_minutes == 1):
        sleep_counter = 120
        while sleep_counter > 0:
            print(f"Sleeping {sleep_counter} seconds...")
            time.sleep(15)
            sleep_counter -= 15
        print("Continue processing data...")
    
    return True

## Requests Api
def request_api(region, api_key, parameter_url):
    url = f"https://{region}.api.riotgames.com{parameter_url}?api_key={api_key}"
    response = requests.get(url)
    if valid_request(response): return response.json()
    return None

## Requests TFT-Matches Api
def request_match_by_match_id(region, api_key, match):
    url = f"https://{region}.api.riotgames.com/tft/match/v1/matches/{match}?api_key={api_key}"
    response = requests.get(url)
    if valid_request(response): return response.json()
    return None

## Requests TFT-Matches Api
def request_matches_by_puuid(region, api_key, puuid, count):
    url = f"https://{region}.api.riotgames.com/tft/match/v1/matches/by-puuid/{puuid}/ids?count={str(count)}&api_key={api_key}"
    response = requests.get(url)
    if valid_request(response): return response.json()
    return None

## Requests puuid of a summoner by name
def request_puuid_by_summonername(region, api_key, summoner_name):
    url = f"https://{region}.api.riotgames.com/tft/summoner/v1/summoners/by-name/{summoner_name}?&api_key={api_key}"
    response = requests.get(url)
    if valid_request(response): return response.json()["puuid"]
    return None

## Requests playerlist by league
def request_players_by_league(region, api_key, ranked_league):
    url = f"https://{region}.api.riotgames.com/tft/league/v1/{ranked_league}?api_key={api_key}"
    response = requests.get(url)
    if valid_request(response): return response.json()["entries"]
    return None

## Requests participant list by match id
def request_participants_by_match_id(region, api_key, match):
    url = f"https://{region}.api.riotgames.com/tft/match/v1/matches/{match}?api_key={api_key}"
    response = requests.get(url)
    if valid_request(response): return response.json()["info"]["participants"]
    return None

## Requests summonername by puuid
def request_summonername_by_puuid(region, api_key, puuid):
    url = f"https://{region}.api.riotgames.com/tft/summoner/v1/summoners/by-puuid/{puuid}?api_key={api_key}"
    response = requests.get(url)
    if valid_request(response): return response.json()["name"]
    return None