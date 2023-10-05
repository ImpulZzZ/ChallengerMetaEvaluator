class Trait:
    def __init__(self, id, style, num_units, data):
        self.id        = str(id)   ## Name of trait that is given by api
        self.name      = data.trait_static_data[self.id]["name"]
        self.icon      = data.trait_static_data[self.id]["image"]
        self.style     = style     ## Current active level (0 = inactive, 1 = bronze, 2 = silver, 3 = gold, 4 = prismatic)
        self.num_units = num_units ## Number of units that have this trait

    def is_single_unit_trait(self):
        if self.num_units == 1: return True
        return False