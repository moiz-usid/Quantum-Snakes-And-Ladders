import pygame
from game.board import Board
from game.player import Player
from game.rules import GameRules
from gui.pygame_gui import PygameGUI
from ai.minimax import MinimaxAI
from utils.config import Config

def main():
    pygame.init()
    config = Config()
    board = Board(config)
    players = [
        Player(1, "Human", is_ai=False),
        Player(2, "AI", is_ai=True)
    ]
    game_rules = GameRules(board, players, config)
    minimax_ai = MinimaxAI(game_rules, config)
    gui = PygameGUI(config, board, players, game_rules)
    
    clock = pygame.time.Clock()
    running = True
    while running and not game_rules.is_game_over():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not players[game_rules.current_player].is_ai:
                gui.handle_click(event.pos)
        
        if players[game_rules.current_player].is_ai and not game_rules.is_game_over():
            move = minimax_ai.get_best_move(players[game_rules.current_player])
            game_rules.make_move(move)
        
        gui.draw()
        pygame.display.flip()
        clock.tick(config.fps)
    
    gui.display_winner()
    pygame.time.wait(2000)  # Show winner for 2 seconds
    pygame.quit()

if __name__ == "__main__":
    main()
