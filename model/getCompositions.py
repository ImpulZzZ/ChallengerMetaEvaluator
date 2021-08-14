from model.Composition      import Composition
from model.Champion         import Champion
from model.Item             import Item
from model.sortUtilities    import sort_players_by_rank, sort_champions_by_stars

import requests
import re
import time

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
def request_api(region, api_key, base_url, parameter_url):
    url = f"https://{region}.{base_url}{parameter_url}?api_key={api_key}"
    response = requests.get(url)
    keep_request_limits(response)
    return response.json()

# requests TFT-Matches Api
def request_matches_by_match_id(region, api_key, base_url, parameter_url):
    url = f"https://{region}.{base_url}{parameter_url}?api_key={api_key}"
    response = requests.get(url)
    keep_request_limits(response)
    return response.json()

# requests TFT-Matches Api
def request_matches_by_puuid(region, api_key, base_url, parameter_url, count):
    url = f"https://{region}.{base_url}{parameter_url}?count={str(count)}&api_key={api_key}"
    response = requests.get(url)
    keep_request_limits(response)
    return response.json()
    
def get_compositions(region, players_per_region, games_per_player, current_patch, ranked_league):

    api_key             = open("apikey.txt", "r").read()
    base_url            = "api.riotgames.com"
    analyzed_games      = []
    compositions        = []
    response            = ""

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

        player_list = response["entries"]
    
    except KeyError:
        print(response)
        return

    player_list     = sort_players_by_rank(player_list)
    best_players    = player_list[0:players_per_region]

    # loop over each player
    for player in best_players:
        summoner_name   = player["summonerName"]

        try:
            # request puuid of each player
            current_url     = f"/tft/summoner/v1/summoners/by-name/{summoner_name}"
            puuid           = request_api(  region          = platform_routing_value,
                                            api_key         = api_key,
                                            base_url        = base_url,
                                            parameter_url   = current_url)["puuid"]
        except KeyError:
            print("KeyError: Api Request failed. Try again!")
            return

        # request last X games of each player
        current_url = f"/tft/match/v1/matches/by-puuid/{puuid}/ids"
        matches     = (request_matches_by_puuid(region          = regional_routing_value,
                                                api_key         = api_key,
                                                base_url        = base_url ,
                                                parameter_url   = current_url,
                                                count           = games_per_player))

        # do not consider matches multiple times
        for match in matches:
            analyzed_games.append(match) if match not in analyzed_games else analyzed_games

    for match in analyzed_games:
        try:
            current_url = f"/tft/match/v1/matches/{match}"
            api_result  = request_matches_by_match_id(  region          = regional_routing_value,
                                                        api_key         = api_key,
                                                        base_url        = base_url,
                                                        parameter_url   = current_url)

            participants = api_result["info"]["participants"]

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