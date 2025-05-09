import random

class PowerUp:
    @staticmethod
    def apply(powerup_type, game_rules, player):
        if powerup_type == "Reroll":
            return random.randint(1, 6)  # New dice roll
        elif powerup_type == "Superposition":
            roll1 = random.randint(1, 6)
            roll2 = random.randint(1, 6)
            return max(roll1, roll2)  # Choose better roll
        return None
