from model.sortUtilities                import sort_dict_by_occurence_and_placement

def group_composition_groups_by_n_traits(composition_groups, all_traits, n):
    if n < 1: return

    compositions        = []
    keys                = []
    combination_dict    = {}
    result_one          = {}
    result_two          = {}
    tmp_result          = {}
    
    for composition_group in composition_groups:
        for composition in composition_group.compositions:
            compositions.append(composition)
    
    for trait in all_traits:
        for tier in [1,2,3,4]:
            key = f"{tier}--{trait}"
            combination_dict.update({key : {}})
            combination_dict[key].update({"compositions" : [], "counter" : 0, "avg_placement" : 0})

    for trait_combination in combination_dict:
        (combination_tier, combination_trait) = trait_combination.split("--")
        for composition in compositions:
            for trait in composition.traits:       
                if trait == combination_trait and composition.traits[trait] == int(combination_tier):
                    combination_dict[trait_combination]["compositions"].append(composition)
                    combination_dict[trait_combination]["counter"]       += 1
                    combination_dict[trait_combination]["avg_placement"] += composition.placement

        if combination_dict[trait_combination]["counter"] > 2:
            combination_dict[trait_combination]["avg_placement"] /= combination_dict[trait_combination]["counter"]
            combination_dict[trait_combination]["avg_placement"] = round(combination_dict[trait_combination]["avg_placement"], 2)
            result_one.update({trait_combination : combination_dict[trait_combination]})

    if n < 2: return sort_dict_by_occurence_and_placement(result_one)

    for key in result_one:
        keys.append(key)
    keys_len = len(keys)

    # compare each unique permutation
    for x in range(0, keys_len):
        (x_tier, x_trait) = keys[x].split('--')
        x_tier = int(x_tier)
        for y in range(x+1, keys_len):
            for y_composition in result_one[keys[y]]["compositions"]:
                if x_trait in y_composition.traits and x_tier == y_composition.traits[x_trait]:
                    key = f"{keys[x]}+{keys[y]}"
                    try:
                        tmp_result[key]["compositions"].append(y_composition)
                        tmp_result[key]["counter"] += 1
                        tmp_result[key]["avg_placement"] += y_composition.placement
                    except KeyError:
                        tmp_result.update({key : {}})
                        tmp_result[key].update({"compositions" : [y_composition], "counter" : 1, "avg_placement" : y_composition.placement})

    for combination in tmp_result:
        if tmp_result[combination]["counter"] > 2:
            tmp_result[combination]["avg_placement"] /= tmp_result[combination]["counter"]
            tmp_result[combination]["avg_placement"] = round(tmp_result[combination]["avg_placement"], 2)
            result_two.update({combination : tmp_result[combination]})      
    
    if n < 3: return sort_dict_by_occurence_and_placement(result_two)

    # for key in result_two:
    #     keys.append(key)
    # keys_len = len(keys)

    # # compare each unique permutation
    # for x in range(0, keys_len):
    #     x_trait_tier_pairs = keys[x].split('+')
    #     for x_keys in x_trait_tier_pairs:
    #         (x_tier, x_trait) = keys[x].split('--')
    #         x_tier = int(x_tier)
    #         for y in range(x+1, keys_len):
    #             for y_composition in result_two[keys[y]]["compositions"]:
    #                 if x_trait in y_composition.traits and x_tier == y_composition.traits[x_trait]:
    #                     key = f"{keys[x]}+{keys[y]}"
    #                     try:
    #                         tmp_result[key]["compositions"].append(y_composition)
    #                         tmp_result[key]["counter"] += 1
    #                         tmp_result[key]["avg_placement"] += y_composition.placement
    #                     except KeyError:
    #                         tmp_result.update({key : {}})
    #                         tmp_result[key].update({"compositions" : [y_composition], "counter" : 1, "avg_placement" : y_composition.placement})

    # for combination in tmp_result:
    #     if tmp_result[combination]["counter"] > 2:
    #         tmp_result[combination]["avg_placement"] /= tmp_result[combination]["counter"]
    #         tmp_result[combination]["avg_placement"] = round(tmp_result[combination]["avg_placement"], 2)
    #         result_two.update({combination : tmp_result[combination]}) 
    
    return