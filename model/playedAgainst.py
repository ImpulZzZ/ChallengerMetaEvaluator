from model.riotApiUtilities import request_match_by_match_id, request_puuid_by_summonername, request_matches_by_puuid, request_summonername_by_puuid
from model.sortUtilities    import sort_dict_by_value

## Requests for the last 200 games and counts appearances of enemies
def played_with(summoner_name, region, api_key):

    if region == "europe":
        platform_routing_value  = "euw1"
        regional_routing_value  = "europe"
    elif region == "korea":
        platform_routing_value  = "kr"
        regional_routing_value  = "asia"
    else:
        platform_routing_value  = "unknown"
        regional_routing_value  = "unknown"

    puuid = request_puuid_by_summonername(region        = platform_routing_value,
                                          api_key       = api_key,
                                          summoner_name = summoner_name)
    
    # request last X games of each player
    matches = request_matches_by_puuid(region  = region,
                                       api_key = api_key,
                                       puuid   = puuid,
                                       count   = 200)
    enemies = {}
    result  = {}
    for match_id in matches:

        match = request_match_by_match_id(region  = region, 
                                          api_key = api_key, 
                                          match   = match_id)

        for participant_puuid in match["metadata"]["participants"]:
            if participant_puuid == puuid: continue

            try:
                enemies[participant_puuid] += 1
            except KeyError:
                enemies.update({participant_puuid : 1})

    for participant_puuid in enemies:
        if enemies[participant_puuid] > 1:
            name = request_summonername_by_puuid(region  = platform_routing_value,
                                                 api_key = api_key,
                                                 puuid   = participant_puuid)
            result.update({name : enemies[participant_puuid]})

    result = sort_dict_by_value(result, descending=True)

    return result

    
