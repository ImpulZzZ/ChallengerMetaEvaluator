from model.Data             import Data
from model.sortUtilities    import sort_dict_by_occurence_and_placement

def group_composition_groups_by_n_traits(composition_groups, n, ignore_one_unit_traits):
    if n < 1: return

    data             = Data()
    compositions     = []
    single_traits    = []
    combination_dict = {}
    result_one       = {}
    result_two       = {}
    tmp_result       = {}

    for composition_group in composition_groups:
        for composition in composition_group.compositions:
            compositions.append(composition)
    
    for trait in data.traits:
        if ignore_one_unit_traits and trait in data.one_unit_traits: continue
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
        single_traits.append(key)
    single_traits_len = len(single_traits)

    # compare each unique permutation
    for x in range(0, single_traits_len):
        (x_tier, x_trait) = single_traits[x].split('--')
        x_tier = int(x_tier)
        for y in range(x+1, single_traits_len):
            for y_composition in result_one[single_traits[y]]["compositions"]:
                if x_trait in y_composition.traits and x_tier == y_composition.traits[x_trait]:
                    key = f"{single_traits[x]}+{single_traits[y]}"
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

    tmp_result           = {}
    result_three         = {}
    visited_combinations = []

    for tier_trait_pair_x in single_traits:
        (tier_x, trait_x) = tier_trait_pair_x.split('--')
        tier_x = int(tier_x)

        for double_tier_trait_pair in result_two:

            if tier_trait_pair_x in double_tier_trait_pair: continue

            current_visit_dict = {trait_x : tier_x}
            for tier_trait_pair_y in double_tier_trait_pair.split('+'):
                (tier_y, trait_y) = tier_trait_pair_y.split('--')
                tier_y = int(tier_y)
                current_visit_dict.update({trait_y : tier_y})

            if current_visit_dict in visited_combinations: continue

            for y_composition in result_two[double_tier_trait_pair]["compositions"]:
                if trait_x in y_composition.traits and tier_x == y_composition.traits[trait_x]:
                    key = f"{tier_trait_pair_x}+{double_tier_trait_pair}"
                    try:
                        tmp_result[key]["compositions"].append(y_composition)
                        tmp_result[key]["counter"] += 1
                        tmp_result[key]["avg_placement"] += y_composition.placement
                    except KeyError:
                        tmp_result.update({key : {}})
                        tmp_result[key].update({"compositions" : [y_composition], "counter" : 1, "avg_placement" : y_composition.placement})
                        
                        current_visit_dict = {}
                        combinations = key.split('+')
                        for combination in combinations:
                            (combination_tier, combination_trait) = combination.split('--')
                            combination_tier = int(combination_tier)
                            current_visit_dict.update({combination_trait : combination_tier})
                        visited_combinations.append(current_visit_dict)

    for combination in tmp_result:
        if tmp_result[combination]["counter"] > 2:
            tmp_result[combination]["avg_placement"] /= tmp_result[combination]["counter"]
            tmp_result[combination]["avg_placement"] = round(tmp_result[combination]["avg_placement"], 2)
            result_three.update({combination : tmp_result[combination]})

    return sort_dict_by_occurence_and_placement(result_three)