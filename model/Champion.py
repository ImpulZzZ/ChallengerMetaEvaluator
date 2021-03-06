class Champion:
    def __init__(self, name, items, tier, rarity):
        assert isinstance(name, str)
        splitted_name = name.split("_")
        self.name = splitted_name[1] if len(splitted_name) > 1 else splitted_name[0]

        assert isinstance(items, list)
        
        self.items = sorted(items, key=lambda x: x.id)

        assert isinstance(tier, int)
        self.tier = tier
        
        assert isinstance(rarity, int)
        self.rarity = rarity

        self.icon = f"Set5_5_static_data/champions/{name}.png"