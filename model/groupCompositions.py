from model.CompositionGroup             import CompositionGroup
from model.dissolveCompositionGroups    import dissolve_composition_groups

def group_compositions_by_n_traits(compositions, all_traits, n):
    combination_dict    = {}
    result_one          = {}
    result_two          = {}
    visited             = {}

    if n > 0:
        for trait in all_traits:
            combination_dict.update({trait : {1 : {}, 2 : {}, 3 : {}, 4 : {}}})
            for tier in combination_dict[trait]:
                combination_dict[trait][tier].update({"compositions" : [], "counter" : 0, "avg_placement" : 0})

    for trait_combination in combination_dict:
        for composition in compositions:
            for trait in composition.traits:
                if trait == trait_combination:
                    combination_dict[trait_combination][composition.traits[trait]]["compositions"].append(composition)
                    combination_dict[trait_combination][composition.traits[trait]]["counter"]       += 1
                    combination_dict[trait_combination][composition.traits[trait]]["avg_placement"] += composition.placement


    for trait in combination_dict:
        for tier in combination_dict[trait]:
            try:
                if combination_dict[trait][tier]["counter"] > 1:
                    combination_dict[trait][tier]["avg_placement"] /= combination_dict[trait][tier]["counter"]
                    result_one.update({trait : { tier : combination_dict[trait][tier]}})
            except KeyError:
                continue

    # if n > 1:
    #     for trait_x in result_one:
    #         for tier_x in result_one[trait_x]:
    #             for trait_y in result_one:
    #                 for tier_y in result_one[trait_y]:
    #                     try:
    #                         if result_one[trait_x][tier_x] == result_one[trait_y][tier_y]:
    #                             key = f"{trait_x}+{trait_y}"
    #                             try:
    #                                 result_two[key].append
    #                             except KeyError:
    #                                 result_two.update({key : })
    #                     except KeyError:
    #                         continue
                
    else:
        return result_one





    print(result_one)
    return result_one

def group_compositions_by_items(compositions):
    processed   = []
    result      = []
    num_comps   = len(compositions)
    
    # loop over every composition
    for x in range(0, num_comps):

        # skip processed compositions
        if x in processed: continue

        # initialize new composition group with current composition
        current_comp_group = [compositions[x]]

        # compare each element x with y > x
        for y in range(x+1, num_comps):
            if compositions[x].champion_item_dict == compositions[y].champion_item_dict:
                current_comp_group.append(compositions[y])
                processed.append(y)
                        
        result.append(CompositionGroup(current_comp_group))
    
    return result

def group_compositions_by_traits(compositions):
    processed   = []
    result      = []
    num_comps   = len(compositions)
    
    # loop over every composition
    for x in range(0, num_comps):

        # skip processed compositions
        if x in processed: continue

        # initialize new composition group with current composition
        current_comp_group = [compositions[x]]

        # compare each element x with y > x
        for y in range(x+1, num_comps):
            if compositions[x].traits == compositions[y].traits:
                current_comp_group.append(compositions[y])
                processed.append(y)
        
        result.append(CompositionGroup(current_comp_group))
    
    return result

def group_compositions_by_champions(compositions):
    processed   = []
    result      = []
    num_comps   = len(compositions)
    
    # loop over every composition
    for x in range(0, num_comps):

        # skip processed compositions
        if x in processed: continue

        # initialize new composition group with current composition
        current_comp_group = [compositions[x]]

        # compare each element x with y > x
        for y in range(x+1, num_comps):
            if compositions[x].champion_names == compositions[y].champion_names:
                current_comp_group.append(compositions[y])
                processed.append(y)
        
        result.append(CompositionGroup(current_comp_group))
    
    return result

def group_compositions(checkboxes, composition_groups, group_by, all_traits, n):

    considered_regions = {}
    composition_groups_copy = composition_groups.copy()

    for region in checkboxes["regions"]:
        if checkboxes["regions"][region]:
            if composition_groups_copy[region]["grouped_by"] != group_by:
                compositions = dissolve_composition_groups(composition_groups_copy[region]["database"])

                if group_by == "traits":
                    composition_groups_copy[region]["database"]     = group_compositions_by_traits(compositions)
                    composition_groups_copy[region]["grouped_by"]   = group_by
                elif group_by == "champions":
                    composition_groups_copy[region]["database"]     = group_compositions_by_champions(compositions)
                    composition_groups_copy[region]["grouped_by"]   = group_by
                elif group_by == "items":
                    composition_groups_copy[region]["database"]     = group_compositions_by_items(compositions)
                    composition_groups_copy[region]["grouped_by"]   = group_by
                elif group_by == "n_traits":
                    composition_groups_copy[region]["database"]     = group_compositions_by_n_traits(compositions, all_traits, n)
                    composition_groups_copy[region]["grouped_by"]   = group_by
                else: return {}

            considered_regions.update({region : composition_groups_copy[region]["database"]})

    return (considered_regions, composition_groups_copy)