class Composition:
    def __init__(self, level, placement, champions, traits, patch):
        assert isinstance(level, int)
        self.level = level
        assert isinstance(placement, int)
        self.placement = placement
        assert isinstance(champions, list)
        self.champions = champions
        assert isinstance(traits, dict)
        self.traits = traits
        assert isinstance(patch, str)
        self.patch = patch


class CompositionGroup:
    def __init__(self, compositions):
        assert isinstance(compositions, list)
        self.compositions = compositions

        self.counter = len(compositions)