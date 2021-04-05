class Champion:
    def __init__(self, name, items, tier, character_id):
        assert isinstance(name, str)
        self.name = name
        assert isinstance(items, list)
        self.items = items
        assert isinstance(tier, int)
        self.tier = tier
        assert isinstance(character_id, str)
        self.character_id = character_id