# takes composition groups and creates a list of all compositions
def dissolve_composition_groups(composition_groups):

    # initialize empty result list
    compositions = []

    # loop over each composition group
    for composition_group in composition_groups:
        # loop over each composition in each composition group
        for composition in composition_group.compositions:
            # append the composition to result
            compositions.append(composition)

    return compositions