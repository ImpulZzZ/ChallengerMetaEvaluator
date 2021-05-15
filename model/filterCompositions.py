from model.CompositionGroup import CompositionGroup

def filter_compositions_by_traits(compositions, traits):

    result_compositions = []
    
    for current in compositions:

        eligible = True
        for key in traits:
            try:
                if current.traits[key] != traits[key]: eligible = False

            except KeyError: eligible = False
        
        if eligible: result_compositions.append(current)
    
    return result_compositions

def filter_compositions_by_placement(compositions, max_placement):
    result_compositions = []

    for current in compositions:

        if current.placement <= max_placement: result_compositions.append(current)
    
    return result_compositions

def filter_compositions_by_champions(compositions, champions):
    result_compositions = []

    for current in compositions:

        eligible = True
        for champion in current.champions:
            if champion.name not in champions: eligible = False

        if eligible: result_compositions.append(current)
    
    return result_compositions

def filter_compositions(compositions, filters):
    trait_filter_active     = len(filters["traits"])    > 0
    champion_filter_active  = len(filters["champions"]) > 0

    if not trait_filter_active and not champion_filter_active: return compositions

    if trait_filter_active: result_compositions = filter_compositions_by_traits(compositions, filters["traits"])

    if champion_filter_active: result_compositions = filter_compositions_by_champions(compositions, filters["champions"])

    return result_compositions