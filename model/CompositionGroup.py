class CompositionGroup:
    def __init__(self, compositions):
        assert isinstance(compositions, list)
        self.compositions = compositions

        self.counter = len(compositions)

        self.avg_placement = 0
        for composition in compositions:
            self.avg_placement += composition.placement
        self.avg_placement /= self.counter
        self.avg_placement = round(self.avg_placement, 2)