class Item:
    def __init__(self, id):
        assert isinstance(id, int)
        self.id = str(id)

        self.icon = (f"Set5_5_static_data/items/{id}.png")

        self.not_component = True if int(id) > 9 else False