class Composition:
    def __init__(self, level, placement, champions, traits):
        assert isinstance(level, int)
        self.level = level
        assert isinstance(placement, int)
        self.placement = placement
        assert isinstance(champions, list)
        self.champions = champions
        assert isinstance(traits, dict)
        self.traits = traits


class CompositionGroup:
    def __init__(self, compositions):
        assert isinstance(compositions, list)
        self.compositions = compositions

        self.counter = len(compositions)