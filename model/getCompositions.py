from model.Composition  import Composition
from model.Champion     import Champion

import requests
import re
import time


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
    
def get_compositions(region, players_per_region, games_per_player, current_patch, ranked_league):

    # API key limits
    requests_per_minute = 99
    total_requests = 2 * players_per_region * games_per_player + 1
    current_requests = 0

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

    try:
        # request for current players and consider only the highest rankeds
        response = request_api( region          = platform_routing_value,
                                api_key         = api_key, 
                                base_url        = base_url, 
                                parameter_url   = "/tft/league/v1/" + ranked_league)

        current_requests += 1
        
        player_list = response["entries"]
    
    except KeyError:
        print("KeyError: ", response)
        print("Try again!")
        return

    
    player_list = sorted(player_list, key=lambda k: k['leaguePoints'], reverse=True)
    best_players = player_list[0:players_per_region]

    # loop over each player
    for player in best_players:
        summoner_name   = player["summonerName"]

        if current_requests == requests_per_minute:
                time.sleep(60)
                current_requests = 0

        try:
            # request puuid of each player
            current_url     = "/tft/summoner/v1/summoners/by-name/" + summoner_name
            puuid           = request_api(  region          = platform_routing_value,
                                            api_key         = api_key,
                                            base_url        = base_url,
                                            parameter_url   = current_url)["puuid"]

            current_requests += 1

        except KeyError:
            print("KeyError: Api Request failed. Try again!")
            return

        if current_requests == requests_per_minute:
                time.sleep(60)
                current_requests = 0

        # request last X games of each player
        current_url = "/tft/match/v1/matches/by-puuid/" + puuid + "/ids"
        matches     = (request_matches_by_puuid(region          = regional_routing_value,
                                                api_key         = api_key,
                                                base_url        = base_url ,
                                                parameter_url   = current_url,
                                                count           = games_per_player))

        current_requests += 1

        # do not consider matches multiple times
        for match in matches:
            analyzed_games.append(match) if match not in analyzed_games else analyzed_games


    # loop over each match
    for match in analyzed_games:
        if current_requests == requests_per_minute:
                time.sleep(60)
                current_requests = 0
        try:

            current_url = "/tft/match/v1/matches/" + match
            api_result  = request_matches_by_match_id(  region          = regional_routing_value,
                                                        api_key         = api_key,
                                                        base_url        = base_url,
                                                        parameter_url   = current_url)

            participants    = api_result["info"]["participants"]
            current_requests += 1

        except KeyError:
            print("KeyError: Api Request failed. Try again!")
            print(api_result)
            return

        patch = re.search("<Releases/(.*)>", api_result["info"]["game_version"]).group(1)

        # only consider current patch
        if patch != current_patch:
            continue

        for participant in participants:
            # only consider top4
            if participant["placement"] > 4:
                continue      

            # create list of champions
            champions_unsorted   = []
            for unit in participant["units"]:
                champions_unsorted.append(Champion( name   = unit["character_id"],
                                                    items  = unit["items"],
                                                    tier   = unit["tier"],
                                                    rarity = unit["rarity"]))

            # sort champions on stars (=tiers)
            champions_unsorted.sort(key=lambda x: x.tier, reverse=True)
            champions = sorted(champions_unsorted, key=lambda x: x.tier, reverse=True)


            # create dictionary with e.g. Vanguard:1 (= Bronze Vanguard)
            trait_dict = {}
            for trait in participant["traits"]:
                # only consider active traits
                if trait["style"] > 0:
                    trait_name = trait["name"].split("_")
                    if len(trait_name) > 1:
                        trait_name_short = trait_name[1]
                    else:
                        trait_name_short = trait_name[0]

                    trait_dict.update({trait_name_short : trait["style"]})

            # sort the trait dictionary for tiers
            sorted_traits = {}
            sorted_keys = sorted(trait_dict, key=trait_dict.get, reverse=True)
            
            for x in sorted_keys:
                sorted_traits[x] = trait_dict[x]

            # create a composition of current player and append it to list
            compositions.append(Composition(level       = participant["level"],
                                            placement   = participant["placement"],
                                            champions   = champions,
                                            traits      = sorted_traits,
                                            patch       = patch))

    return compositions