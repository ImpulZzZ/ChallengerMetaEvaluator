class Champion:
    def __init__(self, name, items, tier, rarity):
        assert isinstance(name, str)
        
        splitted_name = name.split("_")
        if len(splitted_name) > 1:
            self.name = splitted_name[1]
        else:
            self.name = splitted_name[0]

        assert isinstance(items, list)
        self.items = items
        assert isinstance(tier, int)
        self.tier = tier
        assert isinstance(rarity, int)
        self.rarity = rarity

        self.item_icons = []
        for item in self.items:
            self.item_icons.append("Set5_static_data/items/" + str(item) + ".png")

        self.icon = "Set5_static_data/champions/" + str(name) + ".png"
