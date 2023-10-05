import json

class Champion:
    def __init__(self, name, items, tier, data):
        self.id    = name
        self.tier  = tier
        self.icon  = data.champion_static_data[self.id]["image"]
        self.items = sorted(items, key=lambda x: x.id)

        splitted_name = name.split("_")
        self.name = splitted_name[1] if len(splitted_name) > 1 else splitted_name[0]

        self.set_cost_by_champion_id(data.data_dir)
        self.set_stars_by_tier()


    ## Extract champion cost from static data, because api returns a rarity that is not equal to cost
    def set_cost_by_champion_id(self, data_dir):
        with open(f"{data_dir}/champions.json") as jsonfile:
            data = json.load(jsonfile)
            self.cost = data["data"][self.id]["tier"]
        return None
    
    ## Generates the amount of '*' for the table widget elements
    def set_stars_by_tier(self):
        if   self.tier == 1: self.star_text = "   *"
        elif self.tier == 2: self.star_text = "   **"
        elif self.tier == 3: self.star_text = "   ***"
        else:                self.star_text = "   ****"
        return None