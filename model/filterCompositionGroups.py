from model.CompositionGroup import CompositionGroup

def filter_composition_groups(composition_groups, filters):
    # list of resulting composition groups
    result_composition_groups = []

    # validate which filters are considered
    trait_filter_active     = len(filters["traits"])    > 0
    champion_filter_active  = len(filters["champions"]) > 0

    # no filters set => do nothing
    if not trait_filter_active and not champion_filter_active:
        return composition_groups

    # filter for traits
    if trait_filter_active:
       
        # loop over every composition group
        for current_comp_group in composition_groups:

            # composition groups can have 1 or more equal composition-traits
            #   => consider only first composition
            current = current_comp_group.compositions[0]

            # decides, whether composition is accepted by the filter or not
            eligible = True

            # iterate over filter dictionary
            for key in filters["traits"]:
                try:
                    # value not equal
                    if current.traits[key] != filters["traits"][key]:
                        eligible = False
                # key does not exist
                except KeyError:
                    eligible = False
            
            # append the composition group to result if filters are accepted
            if eligible:
                result_composition_groups.append(current_comp_group)

    return result_composition_groups


def filter_composition_groups_by_placement(composition_groups, max_placement):

    print("filter_composition_groups_by_placement()")

    # list of resulting composition groups
    result_composition_groups = []
       
    # loop over every composition group
    for current_comp_group in composition_groups:

        print("New current comp group:")

        current_compositions = current_comp_group.compositions.copy()

        for composition in current_compositions:

            print("composition.placement = ", composition.placement, " > ", max_placement,  "?")

            # append the composition group to current filtered composition group if placement is better or equal than filter
            if composition.placement > max_placement:
                print("Yes! => Remove")
                current_compositions.remove(composition)
            else:
                print("No! => Keep")

        print("len(current_compositions) = ", len(current_compositions))
        # if the filtered composition group has more than 1 composition, append it to result
        if len(current_compositions) > 0:
            result_composition_groups.append(CompositionGroup(current_compositions))

    return result_composition_groups