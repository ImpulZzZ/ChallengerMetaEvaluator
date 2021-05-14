# returns dictionary with occurences of items on each champion and the sum
# { 'Draven':
# {'16': {'counter': 4, 'avg_placement': 6}, 
# '19': {'counter': 5, 'avg_placement': 10}, 
# '1023': {'counter': 2, 'avg_placement': 3}, 
# '1019': {'counter': 1, 'avg_placement': 1}, 
# '25': {'counter': 1, 'avg_placement': 2}}}
def compute_best_in_slot(composition_groups, item_amount):       
    # count each champion-item pair and compute their average placement
    if item_amount == 1:
        counter_dict = {}
        for regional_composition_groups in composition_groups:
            for composition_group in regional_composition_groups:
                for composition in composition_group.compositions:
                    for champion in composition.champions:
                        # validate if the champion is not in dict yet, if not add it
                        try:
                            test = counter_dict[champion.name]
                        except KeyError:
                            counter_dict.update({champion.name : {}})
                        
                        for item in champion.items:
                            # validate if the item is not in dict yet, if not add it
                            try:
                                counter_dict[champion.name][item.id]["counter"] += 1
                                counter_dict[champion.name][item.id]["avg_placement"] += composition.placement
                            except KeyError:
                                counter_dict[champion.name].update({item.id : {"counter" : 1, "avg_placement" : composition.placement}})

    # create result dict with only valid entries
    result_dict = {}
    for champion in counter_dict:
        result_dict.update({champion : {}})
        
        for item in counter_dict[champion]:
            # do not consider unique occurences and no item components
            if counter_dict[champion][item]["counter"] > 2 and int(item) > 9:
                counter_dict[champion][item]["avg_placement"] /= counter_dict[champion][item]["counter"]
                counter_dict[champion][item]["avg_placement"] = round(counter_dict[champion][item]["avg_placement"], 2)

                result_dict[champion].update({item : {}})
                result_dict[champion][item].update({"counter" : counter_dict[champion][item]["counter"]})
                result_dict[champion][item].update({"avg_placement" : counter_dict[champion][item]["avg_placement"]})

    return result_dict