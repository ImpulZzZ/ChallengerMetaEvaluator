class Item:
    def __init__(self, id, data):
        self.id = str(id)

        self.icon = data.item_static_data[self.id]

        #self.not_component = True if int(id) > 9 else False
        ## Not easily interpretable anymore
        self.not_component = True