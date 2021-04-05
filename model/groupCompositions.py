from model.Composition import Composition
from model.Composition import CompositionGroup

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