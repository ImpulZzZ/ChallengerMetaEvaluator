# returns dictionary with occurences of items on each champion and the sum
# { 'Draven':
# {'16': {'counter': 4, 'avg_placement': 6}, 
# '19': {'counter': 5, 'avg_placement': 10}, 
# '1023': {'counter': 2, 'avg_placement': 3}, 
# '1019': {'counter': 1, 'avg_placement': 1}, 
# '25': {'counter': 1, 'avg_placement': 2}}}
# or with multiple items:
# { 'Draven':
# {'16+19': {'counter': 4, 'avg_placement': 6}, 
# '19+1023': {'counter': 5, 'avg_placement': 10}, 
# '25+16': {'counter': 1, 'avg_placement': 2}}}

def compute_best_in_slot(composition_groups, item_amount):
    if item_amount < 1:
        return

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

    # handling for 2-item combinations
    elif item_amount == 2:
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

                        #combinations = []
                        if len(champion.items) == 2:
                            combinations = [f"{champion.items[0].id}+{champion.items[1].id}"]
                        elif len(champion.items) == 3:
                            combinations = [f"{champion.items[0].id}+{champion.items[1].id}",
                                            f"{champion.items[0].id}+{champion.items[2].id}",
                                            f"{champion.items[1].id}+{champion.items[2].id}"]
                        else:
                            continue
                
                        for combination in combinations:
                            # validate if the item combination is not in dict yet, if not add it
                            try:
                                counter_dict[champion.name][combination]["counter"] += 1
                                counter_dict[champion.name][combination]["avg_placement"] += composition.placement
                            except KeyError:
                                counter_dict[champion.name].update({combination : {"counter" : 1, "avg_placement" : composition.placement}})

    # create result dict with only valid entries
    result_dict = {}
    for champion in counter_dict:
        result_dict.update({champion : {}})
    
        for items in counter_dict[champion]:
            # do not consider unique occurences and no item components
            # counter_dict[champion][items]["counter"] > 2 and int(item) > 9:
            counter_dict[champion][items]["avg_placement"] /= counter_dict[champion][items]["counter"]
            counter_dict[champion][items]["avg_placement"] = round(counter_dict[champion][items]["avg_placement"], 2)

            result_dict[champion].update({items : {}})
            result_dict[champion][items].update({"counter" : counter_dict[champion][items]["counter"]})
            result_dict[champion][items].update({"avg_placement" : counter_dict[champion][items]["avg_placement"]})

    return result_dict