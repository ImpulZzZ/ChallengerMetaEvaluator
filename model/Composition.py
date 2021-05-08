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
        self.champion_item_dict = {}

        for champion in self.champions:
            self.champion_names.append(champion.name)
            self.champion_item_dict.update({champion.name : []})
            for item in champion.items:
                self.champion_item_dict[champion.name].append(int(item.id))
            
            self.champion_item_dict[champion.name] = sorted(self.champion_item_dict[champion.name])

        self.champion_names = sorted(self.champion_names)