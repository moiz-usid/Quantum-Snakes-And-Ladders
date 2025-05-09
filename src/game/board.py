from utils.config import Config

class Board:
    def __init__(self, config: Config):
        self.size = config.board_size
        self.snakes = {16: 6, 47: 26, 49: 11}  # Head: Tail
        self.ladders = {3: 38, 8: 28, 20: 42}  # Bottom: Top
        self.powerup_positions = [10, 30, 50]  # Positions with power-ups
    
    def is_snake(self, position):
        return position in self.snakes
    
    def is_ladder(self, position):
        return position in self.ladders
    
    def has_powerup(self, position):
        return position in self.powerup_positions
    
    def get_new_position(self, position):
        if self.is_snake(position):
            return self.snakes[position]
        elif self.is_ladder(position):
            return self.ladders[position]
        return position
