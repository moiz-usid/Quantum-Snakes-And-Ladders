from game.powerups import PowerUp
from ai.mcts import MCTS
import random
import copy

class GameRules:
    def __init__(self, board, players, config):
        self.board = board
        self.players = players
        self.config = config
        self.current_player = 0
        self.move_history = []
    
    def get_possible_moves(self, player):
        moves = [f"roll_{i}" for i in range(1, 7)]  # Possible dice rolls
        if player.powerups:
            moves.extend(player.powerups)  # Add power-ups as moves
        return moves
    
    def make_move(self, move, simulate=False):
        player = self.players[self.current_player]
        player.moves += 1
        
        if move.startswith("roll_"):
            roll = int(move.split("_")[1])
        elif move in ["Reroll", "Superposition"]:
            roll = PowerUp.apply(move, self, player)
            if move in player.powerups:
                player.powerups.remove(move)
        else:
            roll = random.randint(1, 6)
        
        new_position = min(player.position + roll, 100)
        new_position = self.board.get_new_position(new_position)
        
        player.position = new_position
        
        if self.board.has_powerup(new_position) and len(player.powerups) < 2:
            player.powerups.append(random.choice(["Reroll", "Superposition"]))
        
        if not simulate:
            self.move_history.append((player.id, move, player.position))
            self.current_player = (self.current_player + 1) % len(self.players)
        return roll
    
    def undo_move(self):
        if self.move_history:
            player_id, _, old_position = self.move_history.pop()
            player = next(p for p in self.players if p.id == player_id)
            player.position = old_position
            player.moves -= 1
            self.current_player = (self.current_player - 1) % len(self.players)
    
    def is_game_over(self):
        return any(p.position == 100 for p in self.players)
    
    def get_winner(self):
        winners = [p for p in self.players if p.position == 100]
        if winners:
            return min(winners, key=lambda p: p.moves)
        return None
