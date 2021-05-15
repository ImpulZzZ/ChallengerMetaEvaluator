def dissolve_composition_groups(composition_groups):
    compositions = []

    for composition_group in composition_groups:
        for composition in composition_group.compositions:
            compositions.append(composition)

    return compositions