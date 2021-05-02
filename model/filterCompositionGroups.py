from model.CompositionGroup import CompositionGroup

def filter_composition_groups_by_items(composition_groups, items, item_map):

    # list of resulting composition groups
    result_composition_groups = []

    # loop over every composition group
    for current_comp_group in composition_groups:

        # composition groups can have 1 or more equal composition-items
        #   => consider only first composition
        current = current_comp_group.compositions[0]

        found_items = 0

        # iterate over composition champions
        for champion in current.champions:
            for item in items:
                if item_map[item] in champion.items:
                    found_items += 1
        
        # append the composition group to result if filters are accepted
        if found_items >= len(items):
            result_composition_groups.append(current_comp_group)

    return result_composition_groups

def filter_composition_groups_by_traits(composition_groups, traits, tier_relevant):

    # list of resulting composition groups
    result_composition_groups = []

    # loop over every composition group
    for current_comp_group in composition_groups:

        # composition groups can have 1 or more equal composition-traits
        #   => consider only first composition
        current = current_comp_group.compositions[0]

        # decides, whether composition is accepted by the filter or not
        eligible = True

        # iterate over filter dictionary
        for key in traits:
            # validate if trait is in traits
            if key in current.traits:
                # if tier is relevant, filter by that aswell
                if tier_relevant and current.traits[key] != traits[key]:
                    eligible = False
            else:
                eligible = False
        
        # append the composition group to result if filters are accepted
        if eligible:
            result_composition_groups.append(current_comp_group)

    return result_composition_groups


def filter_composition_groups_by_champions(composition_groups, champions, star_relevant):

    # list of resulting composition groups
    result_composition_groups = []

    # loop over every composition group
    for current_comp_group in composition_groups:

        # composition groups can have 1 or more equal composition-champions
        #   => consider only first composition
        current = current_comp_group.compositions[0]

        # decides, whether composition is accepted by the filter or not
        eligible = True

        # iterate over filter dictionary
        for key in champions:
            # validate if champion is in champions
            if key in current.champion_names:
                # if tier is relevant, filter by that aswell
                if star_relevant:
                    eligible = False
                    # loop over champions and ..
                    for champion in current.champions:
                        # .. validate whether the champion has the preferred star
                        if champion.name == key and champion.tier == champions[key]:
                            eligible = True
            else:
                eligible = False

        # append the composition group to result if filters are accepted
        if eligible:
            result_composition_groups.append(current_comp_group)

    return result_composition_groups


def filter_composition_groups_by_placement(composition_groups, max_placement):

    # list of resulting composition groups
    result_composition_groups = []
       
    # loop over every composition group
    for current_comp_group in composition_groups:

        current_valid_compositions = []
        for composition in current_comp_group.compositions:

            # append the composition group to current valid compositions if placement is better or equal than filter
            if composition.placement <= max_placement:
                current_valid_compositions.append(composition)
                
        # if more than 1 composition was found, append them as composition group to result
        if len(current_valid_compositions) > 0:
            result_composition_groups.append(CompositionGroup(current_valid_compositions))

    return result_composition_groups

def filter_composition_groups(composition_groups, filters, item_name_to_id_map):
    # list of resulting composition groups
    result_composition_groups = []

    # validate which filters are considered
    trait_filter_active     = len(filters["traits"])    > 0
    champion_filter_active  = len(filters["champions"]) > 0
    item_filter_active      = len(filters["items"])     > 0

    # no filters set => do nothing
    if not trait_filter_active and not champion_filter_active and not item_filter_active:
        return composition_groups

    # filter for traits
    if trait_filter_active:
        result_composition_groups = filter_composition_groups_by_traits(composition_groups  = composition_groups, 
                                                                        traits              = filters["traits"],
                                                                        tier_relevant       = filters["traitTier"])

    # filter for champions
    if champion_filter_active:
        result_composition_groups = filter_composition_groups_by_champions( composition_groups  = composition_groups, 
                                                                            champions           = filters["champions"],
                                                                            star_relevant       = filters["championStar"])

    # filter for items
    if item_filter_active:
        result_composition_groups = filter_composition_groups_by_items( composition_groups  = composition_groups, 
                                                                        items               = filters["items"],
                                                                        item_map            = item_name_to_id_map)
    
    return result_composition_groups