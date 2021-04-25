from model.Composition                  import Composition
from model.CompositionGroup             import CompositionGroup
from model.dissolveCompositionGroups    import dissolve_composition_groups

def group_compositions_by_traits(compositions):
    processed   = []
    num_comps   = len(compositions)
    result = []
    
    # loop over every composition
    for x in range(0, num_comps):

        # skip processed compositions
        if x in processed:
            continue

        # initialize new composition group with current composition
        current_comp_group = [compositions[x]]

        # compare each element x with y > x
        for y in range(x+1, num_comps):
            if compositions[x].traits == compositions[y].traits:
                current_comp_group.append(compositions[y])
                processed.append(y)
        
        result.append(CompositionGroup(current_comp_group))
    
    return result

# TODO does not work correctly
def group_compositions_by_champions(compositions):
    processed   = []
    num_comps   = len(compositions)
    result = []
    
    # loop over every composition
    for x in range(0, num_comps):

        # skip processed compositions
        if x in processed:
            continue

        # initialize new composition group with current composition
        current_comp_group = [compositions[x]]

        # compare each element x with y > x
        for y in range(x+1, num_comps):

            # lists of champion ids
            x_champions = (champion.name for champion in compositions[x].champions)
            y_champions = (champion.name for champion in compositions[y].champions)

            # compare lists
            if x_champions == y_champions:
                current_comp_group.append(compositions[y])
                processed.append(y)
        
        result.append(CompositionGroup(current_comp_group))
    
    return result

def group_compositions(checkboxes, composition_groups, group_by):

    considered_regions = {}

    composition_groups_copy = composition_groups.copy()

    for region in checkboxes["regions"]:
        if checkboxes["regions"][region]:
            if composition_groups_copy[region]["grouped_by"] != "traits":
                compositions = dissolve_composition_groups(composition_groups_copy[region]["groups"])

                if group_by == "traits":
                    composition_groups_copy[region]["groups"]        = group_compositions_by_traits(compositions)
                    composition_groups_copy[region]["grouped_by"]    = group_by
                elif group_by == "champions":
                    composition_groups_copy[region]["groups"]        = group_compositions_by_champions(compositions)
                    composition_groups_copy[region]["grouped_by"]    = group_by
                elif group_by == "items":
                    print("Work in Progress")
                else:
                    return {}

            considered_regions.update({region : composition_groups_copy[region]["groups"]})

    return (considered_regions, composition_groups_copy)