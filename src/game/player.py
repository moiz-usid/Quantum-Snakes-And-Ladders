class Player:
    def __init__(self, id, name, is_ai=False):
        self.id = id
        self.name = name
        self.is_ai = is_ai
        self.position = 1
        self.powerups = []  # List of power-up names
        self.moves = 0  # Track total moves
