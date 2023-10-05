class Item:
    def __init__(self, id, data):
        self.id = str(id)
        self.name = data.item_static_data[self.id]["name"]
        self.icon = data.item_static_data[self.id]["image"]

        #self.not_component = True if int(id) > 9 else False
        ## Not easily interpretable anymore
        self.not_component = True