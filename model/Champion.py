class Champion:
    def __init__(self, name, items, tier):
        assert isinstance(name, str)
        self.name = name
        assert isinstance(items, list)
        self.items = items
        assert isinstance(tier, int)
        self.tier = tier