class Trait:
    def __init__(self, name, amount):
        assert isinstance(name, str)
        self.name = name
        assert isinstance(amount, int)
        self.amount = amount