def sort_composition_groups_by_occurence_and_placement(composition_groups):
    return sorted(composition_groups, key=lambda x: (x.counter, (-1 * x.avg_placement)), reverse=True)