from model.Composition      import Composition
from model.Champion         import Champion
from model.Item             import Item
from model.sortUtilities    import sort_players_by_rank, sort_champions_by_stars
from model.riotApiUtilities import *

import re

def get_compositions(region, players_per_region, games_per_player, current_patch, ranked_league):

    api_key         = open("apikey.txt", "r").read()
    games_counter   = 0
    visited_matches = {}
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

    player_list = request_players_by_league(region        = platform_routing_value, 
                                            api_key       = api_key,
                                            ranked_league = ranked_league)

    player_list  = sort_players_by_rank(player_list)
    best_players = player_list[0:players_per_region]

    for player in best_players:
        puuid = request_puuid_by_summonername(region        = platform_routing_value,
                                              api_key       = api_key,
                                              summoner_name = player["summonerName"])
                                                    
        matches = request_matches_by_puuid(region  = regional_routing_value,
                                           api_key = api_key,
                                           puuid   = puuid,
                                           count   = games_per_player)
        
        ## Ignore multiple occurences of a match
        for match in matches:
            if match not in visited_matches: visited_matches.update({match : 1})

    for match in visited_matches:
        api_result = request_match_by_match_id(region   = regional_routing_value,
                                               api_key  = api_key,
                                               match    = match)

        patch = re.search("<Releases/(.*)>", api_result["info"]["game_version"]).group(1)
        if patch != current_patch: continue

        participants   = api_result["info"]["participants"]
        games_counter += 1

        for participant in participants:
            #if participant["placement"] > 4: continue

            champions_unsorted = []
            for unit in participant["units"]:
                item_list = []

                for item in unit["items"]:
                    item_list.append(Item(item))
                    
                champions_unsorted.append(Champion(name   = unit["character_id"],
                                                   items  = item_list,
                                                   tier   = unit["tier"],
                                                   rarity = unit["rarity"]))

            champions = sort_champions_by_stars(champions_unsorted)

            trait_dict = {}
            for trait in participant["traits"]:
                ## Only consider active traits
                if trait["style"] > 0:
                    trait_name = trait["name"].split("_")
                    if len(trait_name) > 1: trait_name_short = trait_name[1]
                    else:                   trait_name_short = trait_name[0]

                    trait_dict.update({trait_name_short : trait["style"]})

            ## Sort the trait dictionary by tiers
            sorted_traits = {}
            sorted_keys   = sorted(trait_dict, key=trait_dict.get, reverse=True)
            
            for x in sorted_keys:
                sorted_traits[x] = trait_dict[x]

            compositions.append(Composition(level     = participant["level"],
                                            placement = participant["placement"],
                                            champions = champions,
                                            traits    = sorted_traits,
                                            patch     = patch))

    return {"compositions" : compositions, "analyzed_games" : games_counter}