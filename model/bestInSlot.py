from model.sortUtilities import sort_dict_by_occurence_and_placement

# returns dictionary with occurences of items on each champion and the average placement
def compute_best_in_slot(composition_groups, item_amount, max_avg_placement):
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
                            if item.not_component:
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
                        try: test = counter_dict[champion.name]
                        except KeyError: counter_dict.update({champion.name : {}})

                        # different handling for when champions have 2 or 3 items. Do not consider item components
                        if len(champion.items) == 2 and champion.items[0].not_component and champion.items[1].not_component:
                            combinations = [f"{champion.items[0].id}+{champion.items[1].id}"]
                        elif len(champion.items) == 3 and champion.items[0].not_component and champion.items[1].not_component and champion.items[2].not_component:
                            combinations = [f"{champion.items[0].id}+{champion.items[1].id}",
                                            f"{champion.items[0].id}+{champion.items[2].id}",
                                            f"{champion.items[1].id}+{champion.items[2].id}"]
                        else: continue
                
                        for combination in combinations:
                            # validate if the item combination is not in dict yet, if not add it
                            try:
                                counter_dict[champion.name][combination]["counter"] += 1
                                counter_dict[champion.name][combination]["avg_placement"] += composition.placement
                            except KeyError:
                                counter_dict[champion.name].update({combination : {"counter" : 1, "avg_placement" : composition.placement}})

    # handling for 3-item combination
    else:
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

                        # only consider 3 item-combinations
                        if len(champion.items) == 3 and champion.items[0].not_component and champion.items[1].not_component and champion.items[2].not_component:
                            combination = f"{champion.items[0].id}+{champion.items[1].id}+{champion.items[2].id}"
                        else: continue
                
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
            ## Do not consider unique occurences
            if counter_dict[champion][items]["counter"] > 1:
                counter_dict[champion][items]["avg_placement"] /= counter_dict[champion][items]["counter"]
                counter_dict[champion][items]["avg_placement"] = round(counter_dict[champion][items]["avg_placement"], 2)

                if counter_dict[champion][items]["avg_placement"] <= max_avg_placement:
                    result_dict[champion].update({items : {}})
                    result_dict[champion][items].update({"counter" : counter_dict[champion][items]["counter"]})
                    result_dict[champion][items].update({"avg_placement" : counter_dict[champion][items]["avg_placement"]})

        sorted_dict = sort_dict_by_occurence_and_placement(result_dict[champion])
        result_dict[champion] = sorted_dict

    return result_dict