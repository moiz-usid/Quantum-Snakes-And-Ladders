def evaluate_board(board, players, player_id):
    player = next(p for p in players if p.id == player_id)
    opponent = next(p for p in players if p.id != player_id)
    
    # Heuristic: Distance to goal (100)
    player_distance = 100 - player.position
    opponent_distance = 100 - opponent.position
    
    # Power-up bonus
    powerup_score = 10 if player.powerups else 0
    
    # Avoid snakes, aim for ladders
    snake_penalty = -20 if board.is_snake(player.position) else 0
    ladder_bonus = 20 if board.is_ladder(player.position) else 0
    
    # Total score
    return player_distance - opponent_distance + powerup_score + snake_penalty + ladder_bonus
