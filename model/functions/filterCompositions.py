from model.classes.CompositionGroup import CompositionGroup

def filter_compositions_by_traits(compositions, traits):

    result_compositions = []
    
    # loop over every composition
    for current in compositions:
        # decides, whether composition is accepted by the filter or not
        eligible = True

        for key in traits:
            try:
                # value not equal
                if current.traits[key] != traits[key]:
                    eligible = False
            # key does not exist
            except KeyError:
                eligible = False
        
        # append the composition to result if filters are accepted
        if eligible:
            result_compositions.append(current)
    
    return result_compositions


def filter_compositions_by_placements(compositions, placements):
    result_compositions = []

    # loop over every composition
    for current in compositions:

        # decides, whether composition is accepted by the filter or not
        eligible = True

        for champion in current.placements:
            if champion.name not in placements:
                eligible = False

        # append the composition to result if filters are accepted
        if eligible:
            result_compositions.append(current)
    
    return result_compositions


def filter_compositions_by_champions(compositions, champions):
    result_compositions = []

    # loop over every composition
    for current in compositions:

        # decides, whether composition is accepted by the filter or not
        eligible = True

        for champion in current.champions:
            if champion.name not in champions:
                eligible = False

        # append the composition to result if filters are accepted
        if eligible:
            result_compositions.append(current)
    
    return result_compositions


def filter_compositions(compositions, filters):
    trait_filter_active     = len(filters["traits"])    > 0
    champion_filter_active  = len(filters["champions"]) > 0
    placement_filter_active = filters["placements"]     != []

    # no filters set
    if not trait_filter_active and not placement_filter_active and not champion_filter_active:
        return compositions

    # filter for traits
    if trait_filter_active:
        result_compositions = filter_compositions_by_traits(compositions, filters["traits"])

    # filter for placements
    if placement_filter_active:
        result_compositions = filter_compositions_by_placements(compositions, filters["placements"])

    # filter for champions
    if champion_filter_active:
        result_compositions = filter_compositions_by_champions(compositions, filters["champions"])

    return result_compositions