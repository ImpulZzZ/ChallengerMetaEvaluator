from model.getCompositions      import get_compositions
from model.groupCompositions    import group_compositions_by_traits
from model.filterCompositions   import filter_compositions

europe = get_compositions(  region="europe",
                            games_per_player=4,
                            players_per_region=5)

#comps = group_compositions_by_traits(europe)

filters={
    "traits"    : { "Boss"          : 3,
                    "Set4_Brawler"  : 3},
    "placements": [],
    "champions" : []
}

filtered_by_traits = filter_compositions(europe, filters)

for x in filtered_by_traits:
    print(x.traits)