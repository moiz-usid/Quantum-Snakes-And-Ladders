from ai.heuristics import evaluate_board
from game.rules import GameRules
from utils.config import Config
import random

class MinimaxAI:
    def __init__(self, game_rules: GameRules, config: Config):
        self.game_rules = game_rules
        self.config = config
        self.max_depth = 3  # Limit depth for performance
    
    def get_best_move(self, player):
        best_value = float('-inf')
        best_move = None
        possible_moves = self.game_rules.get_possible_moves(player)
        
        for move in possible_moves:
            self.game_rules.make_move(move, simulate=True)
            value = self.minimax(self.max_depth, False, float('-inf'), float('inf'), player.id)
            self.game_rules.undo_move()
            if value > best_value:
                best_value = value
                best_move = move
        
        return best_move or random.choice(possible_moves)
    
    def minimax(self, depth, is_maximizing, alpha, beta, player_id):
        if depth == 0 or self.game_rules.is_game_over():
            return evaluate_board(self.game_rules.board, self.game_rules.players, player_id)
        
        if is_maximizing:
            max_eval = float('-inf')
            for move in self.game_rules.get_possible_moves(self.game_rules.players[player_id - 1]):
                self.game_rules.make_move(move, simulate=True)
                eval = self.minimax(depth - 1, False, alpha, beta, player_id)
                self.game_rules.undo_move()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            opponent = next(p for p in self.game_rules.players if p.id != player_id)
            for move in self.game_rules.get_possible_moves(opponent):
                self.game_rules.make_move(move, simulate=True)
                eval = self.minimax(depth - 1, True, alpha, beta, player_id)
                self.game_rules.undo_move()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval
