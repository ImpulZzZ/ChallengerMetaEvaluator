class Trait:
    def __init__(self, id, data, style=0):
        self.id        = str(id)   ## Name of trait that is given by api
        self.name      = data.trait_static_data[self.id]["name"]
        self.icon      = data.trait_static_data[self.id]["image"]
        self.style     = style     ## Current active level (0 = inactive, 1 = bronze, 2 = silver, 3 = gold, 4 = prismatic)

        if self.name in data.single_unit_traits: self.single_unit_trait = True
        else: self.single_unit_trait = False