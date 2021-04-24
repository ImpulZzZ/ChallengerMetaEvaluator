class CompositionGroup:
    def __init__(self, compositions):
        assert isinstance(compositions, list)
        self.compositions = compositions

        self.counter = len(compositions)