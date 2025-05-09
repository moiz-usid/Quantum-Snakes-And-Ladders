from ai.heuristics import evaluate_board
from game.rules import GameRules
import random
import math
import copy

class MCTNode:
    def __init__(self, state, parent=None, move=None):
        self.state = state
        self.parent = parent
        self.move = move
        self.children = []
        self.visits = 0
        self.value = 0

class MCTS:
    def __init__(self, game_rules: GameRules, iterations=100):
        self.game_rules = game_rules
        self.iterations = iterations
    
    def get_best_move(self, player):
        root = MCTNode(copy.deepcopy(self.game_rules))
        for _ in range(self.iterations):
            node = self.select(root)
            value = self.simulate(node)
            self.backpropagate(node, value)
        
        best_child = max(root.children, key=lambda c: c.visits, default=None)
        return best_child.move if best_child else random.choice(self.game_rules.get_possible_moves(player))
    
    def select(self, node):
        while node.children:
            node = max(node.children, key=lambda c: c.value / c.visits + math.sqrt(2 * math.log(node.visits + 1) / (c.visits + 1)))
        if not node.state.is_game_over():
            for move in node.state.get_possible_moves(node.state.players[node.state.current_player]):
                new_state = copy.deepcopy(node.state)
                new_state.make_move(move)
                child = MCTNode(new_state, node, move)
                node.children.append(child)
            return random.choice(node.children)
        return node
    
    def simulate(self, node):
        state = copy.deepcopy(node.state)
        while not state.is_game_over():
            moves = state.get_possible_moves(state.players[state.current_player])
            if moves:
                state.make_move(random.choice(moves))
            else:
                break
        return evaluate_board(state.board, state.players, state.players[0].id)
    
    def backpropagate(self, node, value):
        while node:
            node.visits += 1
            node.value += value
            node = node.parent
