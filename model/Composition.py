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

        self.champion_names = []
        for champion in self.champions:
            self.champion_names.append(champion.name)
        self.champion_names = sorted(self.champion_names)

        