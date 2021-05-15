from model.Composition      import Composition
from model.Champion         import Champion
from model.Item             import Item
from model.sortUtilities    import sort_players_by_rank, sort_champions_by_stars

import requests
import re
import time


# requests Api
def request_api(region, api_key, base_url, parameter_url):
    url = f"https://{region}.{base_url}{parameter_url}?api_key={api_key}"
    return requests.get(url).json()

# requests TFT-Matches Api
def request_matches_by_match_id(region, api_key, base_url, parameter_url):
    url = f"https://{region}.{base_url}{parameter_url}?api_key={api_key}"
    return requests.get(url).json()

# requests TFT-Matches Api
def request_matches_by_puuid(region, api_key, base_url, parameter_url, count):
    url = f"https://{region}.{base_url}{parameter_url}?count={str(count)}&api_key={api_key}"
    return requests.get(url).json()
    
def get_compositions(region, players_per_region, games_per_player, current_patch, ranked_league):

    api_key     = open("apikey.txt", "r").read()
    base_url    = "api.riotgames.com"
    analyzed_games  = []
    compositions    = []
    response = ""
    requests_per_minute = 99
    current_requests = 0

    if region == "europe":
        platform_routing_value  = "euw1"
        regional_routing_value  = "europe"
    elif region == "korea":
        platform_routing_value  = "kr"
        regional_routing_value  = "asia"
    else:
        platform_routing_value  = "unknown"
        regional_routing_value  = "unknown"

    try:
        # request for current players and consider only the highest rankeds
        response = request_api( region          = platform_routing_value,
                                api_key         = api_key, 
                                base_url        = base_url, 
                                parameter_url   = f"/tft/league/v1/{ranked_league}")

        current_requests += 1
        player_list = response["entries"]
    
    except KeyError:
        print(response)
        return

    player_list     = sort_players_by_rank(player_list)
    best_players    = player_list[0:players_per_region]

    # loop over each player
    for player in best_players:
        summoner_name   = player["summonerName"]

        if current_requests == requests_per_minute:
                time.sleep(120)
                current_requests = 0
        try:
            # request puuid of each player
            current_url     = f"/tft/summoner/v1/summoners/by-name/{summoner_name}"
            puuid           = request_api(  region          = platform_routing_value,
                                            api_key         = api_key,
                                            base_url        = base_url,
                                            parameter_url   = current_url)["puuid"]

            current_requests += 1

        except KeyError:
            print("KeyError: Api Request failed. Try again!")
            return

        if current_requests == requests_per_minute:
                time.sleep(120)
                current_requests = 0

        # request last X games of each player
        current_url = f"/tft/match/v1/matches/by-puuid/{puuid}/ids"
        matches     = (request_matches_by_puuid(region          = regional_routing_value,
                                                api_key         = api_key,
                                                base_url        = base_url ,
                                                parameter_url   = current_url,
                                                count           = games_per_player))

        current_requests += 1

        # do not consider matches multiple times
        for match in matches:
            analyzed_games.append(match) if match not in analyzed_games else analyzed_games

    for match in analyzed_games:
        if current_requests == requests_per_minute:
                time.sleep(120)
                current_requests = 0
        try:
            current_url = f"/tft/match/v1/matches/{match}"
            api_result  = request_matches_by_match_id(  region          = regional_routing_value,
                                                        api_key         = api_key,
                                                        base_url        = base_url,
                                                        parameter_url   = current_url)

            participants        = api_result["info"]["participants"]
            current_requests    += 1

        except KeyError:
            print(api_result)
            return

        patch = re.search("<Releases/(.*)>", api_result["info"]["game_version"]).group(1)
        if patch != current_patch: continue

        for participant in participants:
            if participant["placement"] > 4: continue      

            champions_unsorted   = []
            for unit in participant["units"]:
                item_list = []

                for item in unit["items"]:
                    item_list.append(Item(item))
                    
                champions_unsorted.append(Champion( name   = unit["character_id"],
                                                    items  = item_list,
                                                    tier   = unit["tier"],
                                                    rarity = unit["rarity"]))

            champions = sort_champions_by_stars(champions_unsorted)

            trait_dict = {}
            for trait in participant["traits"]:
                # only consider active traits
                if trait["style"] > 0:
                    trait_name = trait["name"].split("_")
                    if len(trait_name) > 1: trait_name_short = trait_name[1]
                    else:                   trait_name_short = trait_name[0]

                    trait_dict.update({trait_name_short : trait["style"]})

            # sort the trait dictionary for tiers
            sorted_traits = {}
            sorted_keys = sorted(trait_dict, key=trait_dict.get, reverse=True)
            
            for x in sorted_keys:
                sorted_traits[x] = trait_dict[x]

            compositions.append(Composition(level       = participant["level"],
                                            placement   = participant["placement"],
                                            champions   = champions,
                                            traits      = sorted_traits,
                                            patch       = patch))
    return compositions