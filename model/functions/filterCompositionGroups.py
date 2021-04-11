def filter_composition_groups(composition_groups, filters):
    # list of resulting composition groups
    result_composition_groups = []

    # validate which filters are considered
    trait_filter_active     = len(filters["traits"])    > 0
    champion_filter_active  = len(filters["champions"]) > 0
    placement_filter_active = filters["placements"]     != []

    # no filters set => do nothing
    if not trait_filter_active and not placement_filter_active and not champion_filter_active:
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

    # filter for placements
    #if placement_filter_active:
        #result_composition_groups = filter_composition_groups_by_placements(composition_groups, filters["placements"])

    # filter for champions
    #if champion_filter_active:
        # loop over every composition group
        # for current_comp_group in composition_groups:

        #     # composition groups can have 1 or more equal composition-traits
        #     #   => consider only first composition
        #     current = current_comp_group.compositions[0]

        #     # decides, whether composition is accepted by the filter or not
        #     eligible = True

        #     # iterate over filter dictionary
        #     for key in filters["traits"]:
        #         try:
        #             # value not equal
        #             if current.traits[key] != filters["traits"][key]:
        #                 eligible = False
        #         # key does not exist
        #         except KeyError:
        #             eligible = False
            
        #     # append the composition group to result if filters are accepted
        #     if eligible:
        #         result_composition_groups.append(current_comp_group)

    return result_composition_groups