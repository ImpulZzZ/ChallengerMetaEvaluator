class Composition:
    def __init__(self, level, placement, champions, traits, patch):
        self.level = level
        self.placement = placement
        self.champions = champions
        self.traits = traits
        self.patch = patch

        self.champion_names = []
        self.champion_item_dict = {}

        for champion in self.champions:
            self.champion_names.append(champion.name)
            self.champion_item_dict.update({champion.name : []})
            for item in champion.items:
                self.champion_item_dict[champion.name].append(item.id)
            
            self.champion_item_dict[champion.name] = sorted(self.champion_item_dict[champion.name])

        self.champion_names = sorted(self.champion_names)