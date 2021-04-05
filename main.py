from model.Composition import Composition
from model.Champion import Champion
from model.Trait import Trait

import requests


# requests Api
def request_api(region, api_key, base_url, parameter_url):
    url = "https://" + region + "." + base_url + parameter_url + "?api_key=" + api_key
    return requests.get(url).json()


# requests TFT-Matches Api
def request_matches_by_match_id(api_key, base_url, parameter_url):
    url = "https://europe." + base_url + parameter_url + "?api_key=" + api_key
    return requests.get(url).json()


# requests TFT-Matches Api
def request_matches_by_puuid(api_key, base_url, parameter_url, count):
    url = "https://europe." + base_url + parameter_url + "?count=" + str(count) + "&api_key=" + api_key
    return requests.get(url).json()
    


#############################################################
### Entrypoint ##############################################
#############################################################

# initialize static variables
ANALYZED_GAMES_PER_PLAYER   = 4
ANALYZED_PLAYERS_PER_REGION = 5

# initialize API Request variables
api_key     = open("apikey.txt", "r").read() 
region      = "euw1"
base_url    = "api.riotgames.com"
challenger  = "/tft/league/v1/challenger"

# initialize fields
analyzed_games  = []
compositions    = []

# request for current challenger players and consider only the highest rankeds
response = request_api(region, api_key, base_url, challenger)
challenger_players = response["entries"]
challenger_players = sorted(challenger_players, key=lambda k: k['leaguePoints'], reverse=True)
best_players = challenger_players[0:ANALYZED_PLAYERS_PER_REGION]

# loop over each player
for player in best_players:
    summoner_name   = player["summonerName"]

    # request puuid of each player
    current_url     = "/tft/summoner/v1/summoners/by-name/" + summoner_name
    puuid           = request_api(region, api_key, base_url, current_url)["puuid"]

    # request last X games of each player
    current_url     = "/tft/match/v1/matches/by-puuid/" + puuid + "/ids"
    matches = (request_matches_by_puuid(api_key, base_url, current_url, count=ANALYZED_GAMES_PER_PLAYER))

    # do not consider matches multiple times
    for match in matches:
        analyzed_games.append(match) if match not in analyzed_games else analyzed_games


# loop over each match
for match in analyzed_games:
    current_url = "/tft/match/v1/matches/" + match
    participants = request_matches_by_match_id(api_key, base_url, current_url)["info"]["participants"]

    for participant in participants:
        # only consider top4
        if participant["placement"] > 4:
            continue

        # initialize / clear fields
        champions   = []
        traits      = []

        # create list of champions
        for unit in participant["units"]:
            champions.append(Champion(  name    = unit["name"],
                                        items   = unit["items"],
                                        tier    = unit["tier"]))

        # create list of traits
        for trait in participant["traits"]:
            traits.append(Trait(name    = trait["name"],
                                amount  = trait["num_units"]))
        
        
        # create a composition of current player and append it to list
        compositions.append(Composition(level       = participant["level"],
                                        placement   = participant["placement"],
                                        champions   = champions,
                                        traits      = traits))