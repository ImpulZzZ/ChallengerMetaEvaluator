from model.Composition import Composition
from model.Champion import Champion

import requests


# requests Api
def request_api(region, api_key, base_url, parameter_url):
    url = "https://" + region + "." + base_url + parameter_url + "?api_key=" + api_key
    return requests.get(url).json()


# requests TFT-Matches Api
def request_matches_by_match_id(region, api_key, base_url, parameter_url):
    url = "https://" + region + "." + base_url + parameter_url + "?api_key=" + api_key
    return requests.get(url).json()


# requests TFT-Matches Api
def request_matches_by_puuid(region, api_key, base_url, parameter_url, count):
    url = "https://" + region + "." + base_url + parameter_url + "?count=" + str(count) + "&api_key=" + api_key
    return requests.get(url).json()
    
def get_compositions(region, players_per_region, games_per_player):

    # initialize API Request variables
    api_key     = open("apikey.txt", "r").read()
    base_url    = "api.riotgames.com"

    # initialize fields
    analyzed_games  = []
    compositions    = []

    if region == "europe":
        platform_routing_value  = "euw1"
        regional_routing_value  = "europe"
    elif region == "korea":
        platform_routing_value  = "kr"
        regional_routing_value  = "asia"
    else:
        platform_routing_value  = "unknown"
        regional_routing_value  = "unknown"


    # request for current challenger players and consider only the highest rankeds
    response = request_api( region          = platform_routing_value,
                            api_key         = api_key, 
                            base_url        = base_url, 
                            parameter_url   = "/tft/league/v1/challenger")

    challenger_players = response["entries"]
    challenger_players = sorted(challenger_players, key=lambda k: k['leaguePoints'], reverse=True)
    best_players = challenger_players[0:players_per_region]

    # loop over each player
    for player in best_players:
        summoner_name   = player["summonerName"]

        # request puuid of each player
        current_url     = "/tft/summoner/v1/summoners/by-name/" + summoner_name
        puuid           = request_api(  region          = platform_routing_value,
                                        api_key         = api_key,
                                        base_url        = base_url,
                                        parameter_url   = current_url)["puuid"]

        # request last X games of each player
        current_url = "/tft/match/v1/matches/by-puuid/" + puuid + "/ids"
        matches     = (request_matches_by_puuid(region          = regional_routing_value,
                                                api_key         = api_key,
                                                base_url        = base_url ,
                                                parameter_url   = current_url,
                                                count           = games_per_player))

        # do not consider matches multiple times
        for match in matches:
            analyzed_games.append(match) if match not in analyzed_games else analyzed_games


    # loop over each match
    for match in analyzed_games:
        current_url = "/tft/match/v1/matches/" + match
        participants = request_matches_by_match_id( region          = regional_routing_value,
                                                    api_key         = api_key,
                                                    base_url        = base_url,
                                                    parameter_url   = current_url)["info"]["participants"]

        for participant in participants:
            # only consider top4
            if participant["placement"] > 4:
                continue      

            # create list of champions
            champions   = []
            for unit in participant["units"]:
                champions.append(Champion(  name            = unit["name"],
                                            items           = unit["items"],
                                            tier            = unit["tier"],
                                            character_id    = unit["character_id"]))

            # create dictionary with e.g. Vanguard:1 (= Bronze Vanguard)
            trait_dict = {}
            for trait in participant["traits"]:
                # only consider active traits
                if trait["style"] > 0:
                    trait_dict.update({trait["name"] : trait["style"]})


            # create a composition of current player and append it to list
            compositions.append(Composition(level       = participant["level"],
                                            placement   = participant["placement"],
                                            champions   = champions,
                                            traits      = trait_dict))

    return compositions