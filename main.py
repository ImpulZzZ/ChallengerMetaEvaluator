from model.getCompositions      import get_compositions
from model.groupCompositions    import group_compositions_by_traits
from model.Composition          import CompositionGroup

europe = get_compositions(  region="europe",
                            games_per_player=4,
                            players_per_region=5)

comps = group_compositions_by_traits(europe)