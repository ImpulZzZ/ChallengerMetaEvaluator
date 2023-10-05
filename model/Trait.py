class Trait:
    def __init__(self, id, style, num_units, data):
        self.id        = str(id)
        self.name      = data.trait_static_data[self.id]["name"]
        self.icon      = data.trait_static_data[self.id]["image"]
        self.style     = style
        self.num_units = num_units

    def is_single_unit_trait(self):
        if self.num_units == 1: return True
        return False