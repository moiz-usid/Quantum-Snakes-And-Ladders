import pygame
from utils.config import Config

class PygameGUI:
    def __init__(self, config: Config, board, players, game_rules):
        self.config = config
        self.board = board
        self.players = players
        self.game_rules = game_rules
        self.screen = pygame.display.set_mode((config.screen_width, config.screen_height))
        pygame.display.set_caption("Quantum Snakes & Ladders")
        self.font = pygame.font.SysFont("arial", 20)
        self.cell_size = config.screen_width // config.board_size
    
    def draw(self):
        self.screen.fill((255, 255, 255))  # White background
        
        # Draw grid
        for row in range(self.config.board_size):
            for col in range(self.config.board_size):
                pos = (col * self.cell_size, row * self.cell_size)
                pygame.draw.rect(self.screen, (0, 0, 0), (*pos, self.cell_size, self.cell_size), 1)
                cell_num = row * self.config.board_size + col + 1
                if cell_num <= 100:
                    text = self.font.render(str(cell_num), True, (0, 0, 0))
                    self.screen.blit(text, (pos[0] + 10, pos[1] + 10))
        
        # Draw snakes (red lines)
        for head, tail in self.board.snakes.items():
            head_pos = self.get_cell_pos(head)
            tail_pos = self.get_cell_pos(tail)
            pygame.draw.line(self.screen, (255, 0, 0), head_pos, tail_pos, 3)
        
        # Draw ladders (green lines)
        for bottom, top in self.board.ladders.items():
            bottom_pos = self.get_cell_pos(bottom)
            top_pos = self.get_cell_pos(top)
            pygame.draw.line(self.screen, (0, 255, 0), bottom_pos, top_pos, 3)
        
        # Draw power-ups (blue stars)
        for pos in self.board.powerup_positions:
            x, y = self.get_cell_pos(pos)
            pygame.draw.polygon(self.screen, (0, 0, 255), [
                (x, y - 10), (x + 10, y + 10), (x - 10, y + 10)
            ])
        
        # Draw players
        for player in self.players:
            x, y = self.get_cell_pos(player.position)
            color = (255, 0, 0) if player.id == 1 else (0, 0, 255)
            pygame.draw.circle(self.screen, color, (x, y), 10)
        
        # Draw status
        current = self.players[self.game_rules.current_player]
        status = f"Player {current.name}'s turn | Power-ups: {', '.join(current.powerups) or 'None'}"
        text = self.font.render(status, True, (0, 0, 0))
        self.screen.blit(text, (10, self.config.screen_height - 30))
    
    def get_cell_pos(self, cell_num):
        if cell_num > 100:
            cell_num = 100
        row = (cell_num - 1) // self.config.board_size
        col = (cell_num - 1) % self.config.board_size
        x = col * self.cell_size + self.cell_size // 2
        y = row * self.cell_size + self.cell_size // 2
        return x, y
    
    def handle_click(self, pos):
        if self.game_rules.current_player == 0:  # Human player
            moves = self.game_rules.get_possible_moves(self.players[0])
            button_y = self.config.screen_height - 60
            for i, move in enumerate(moves):
                button_x = 100 + i * 100
                if button_x <= pos[0] <= button_x + 80 and button_y <= pos[1] <= button_y + 40:
                    self.game_rules.make_move(move)
                    break
    
    def display_winner(self):
        winner = self.game_rules.get_winner()
        if winner:
            text = self.font.render(f"{winner.name} wins!", True, (255, 0, 0))
            self.screen.blit(text, (self.config.screen_width // 2 - 50, self.config.screen_height // 2))
            pygame.display.flip()
