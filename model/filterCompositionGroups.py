from model.CompositionGroup import CompositionGroup
from model.Data             import Data
from model.sortUtilities    import sort_composition_groups_by_occurence_and_placement

def filter_composition_groups_by_items(composition_groups, items):
    item_map                    = Data().item_name_to_id_map
    result_composition_groups   = []

    for current_comp_group in composition_groups:

        ## Here items of compostition 0 equals items of composition n
        current = current_comp_group.compositions[0]

        found_items = 0
        for champion in current.champions:
            for item in items:
                if item_map[item] in champion.items: found_items += 1
        
        if found_items >= len(items): result_composition_groups.append(current_comp_group)

    return result_composition_groups

def filter_composition_groups_by_traits(composition_groups, traits, tier_relevant):
    result_composition_groups = []

    for current_comp_group in composition_groups:
        
        ## Traits of compostition 0 equals traits of composition n
        current = current_comp_group.compositions[0]

        eligible = True
        for key in traits:
            if key in current.traits:
                if tier_relevant and current.traits[key] < traits[key]: eligible = False
            else: eligible = False
        
        if eligible: result_composition_groups.append(current_comp_group)

    return result_composition_groups

def filter_composition_groups_by_champions(composition_groups, champions, star_relevant):
    result_composition_groups = []

    for current_comp_group in composition_groups:

        ## Champions of compostition 0 equals champions of composition n
        current = current_comp_group.compositions[0]

        eligible = True
        for key in champions:
            if key in current.champion_names:
                if star_relevant:
                    eligible = False
                    for champion in current.champions:
                        if champion.name == key and champion.tier >= champions[key]: eligible = True
            else: eligible = False

        if eligible: result_composition_groups.append(current_comp_group)

    return result_composition_groups

def filter_composition_groups_by_placement(composition_groups, max_placement):
    result_composition_groups = []
       
    for current_comp_group in composition_groups:

        current_valid_compositions = []
        for composition in current_comp_group.compositions:
            if composition.placement <= max_placement: current_valid_compositions.append(composition)
                
        if len(current_valid_compositions) > 0:
            result_composition_groups.append(CompositionGroup(current_valid_compositions))
            
    return result_composition_groups

def remove_compositions_from_group_by_avg_placement(composition_groups, max_avg_placement):
    result_composition_groups = []
       
    for current_comp_group in composition_groups:
        if current_comp_group.avg_placement <= max_avg_placement: result_composition_groups.append(current_comp_group)
                
    return result_composition_groups

def filter_composition_groups(composition_groups, filters):
    result = []

    trait_filter_active     = len(filters["traits"])    > 0
    champion_filter_active  = len(filters["champions"]) > 0
    item_filter_active      = len(filters["items"])     > 0

    if not trait_filter_active and not champion_filter_active and not item_filter_active: return composition_groups

    if trait_filter_active:    result = filter_composition_groups_by_traits( composition_groups = composition_groups, 
                                                                             traits             = filters["traits"],
                                                                             tier_relevant      = filters["traitTier"] )

    if champion_filter_active: result = filter_composition_groups_by_champions( composition_groups = composition_groups, 
                                                                                champions          = filters["champions"],
                                                                                star_relevant      = filters["championStar"] )

    if item_filter_active:     result = filter_composition_groups_by_items( composition_groups = composition_groups, 
                                                                            items              = filters["items"] )
    
    return result


def filter_and_sort_composition_groups(composition_groups, filters):
    result_composition_groups = []

    result_composition_groups = filter_composition_groups_by_placement( composition_groups = composition_groups,
                                                                        max_placement      = filters["placements"] )

    result_composition_groups = filter_composition_groups( composition_groups = result_composition_groups, 
                                                           filters            = filters )

    result_composition_groups = remove_compositions_from_group_by_avg_placement( composition_groups = result_composition_groups,
                                                                                 max_avg_placement  = filters["avgPlacement"] )

    result_composition_groups = sort_composition_groups_by_occurence_and_placement( result_composition_groups )

    return result_composition_groups