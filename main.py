import sys, time

import pygame

from constants import (ATTACKER_PLAYER, BOARD_MARGIN, CELL_SIZE,
                       DEFAULT_BOARD_SIZE, DEFENDER_PLAYER, DIFFICULTIES, ROLES,
                       FPS, INFO_PANEL_WIDTH, WINDOW_TITLE, ATTACKER, DEFENDER, DELAY)
from gui.board_renderer import BoardRenderer
from logic.state import GameState
from logic.rules import get_possible_moves, is_current_player_piece, check_captures
from logic.ai import AI_Player
from gui.choiceMenu import run_menu


def main(board_size: int = DEFAULT_BOARD_SIZE):
    pygame.init()

    game_state = GameState(board_size)
    renderer = BoardRenderer(board_size, game_state)

    humanRole, difficulty = run_menu(renderer.screen)
    renderer.set_difficulty(difficulty)

    aiRole = ATTACKER_PLAYER if ROLES.get(humanRole) == DEFENDER_PLAYER else DEFENDER_PLAYER
    aiPlayer = AI_Player(difficulty=DIFFICULTIES.get(difficulty), role=aiRole)

    # Setting up the AI player
    # print(game_state.getAttackerPieces())
    # print(game_state.getDefenderPieces())

    clock = pygame.time.Clock()

    # ── Click handler ─────────────────────────────────────────
    def handle_click(px, py):
        if game_state.game_over:
            return

        pos = renderer.screen_to_board(px, py)
        if pos is None:
            return

        piece = game_state.get_piece_at(*pos)
        
        # If player chose one of his pieces, get the valid moves of it
        if is_current_player_piece(game_state, piece):
            valid_moves = get_possible_moves(game_state, pos)
            renderer.set_selection(pos, valid_moves)
        
        # If a valid move of the selected piece was chosen, apply the move 
        elif renderer.selected_position and pos in renderer.valid_moves:
            from_position = renderer.selected_position
            renderer.clear_selection()
            
            game_state.apply_move(from_position, pos)
            # renderer.update_board()
            # pygame.display.flip()

            captured_positions = check_captures(game_state, pos)
            # print(captured_position)
            
            # pygame.time.delay(200)
            game_state.record_move(from_position, pos, captured_positions)
            return True
        
        # Invalid move
        else:
            renderer.clear_selection()

        return False

        # renderer.update_board()
        # pygame.display.flip()


    # piece and move are tuples of coordinates
    def applyAIMove(piece, move):
        game_state.get_piece_at(piece[0], piece[1])
        valid_moves = get_possible_moves(game_state, piece)
        
        renderer.set_selection(piece, valid_moves)

        game_state.apply_move(piece, move)
        game_state.record_move(piece, move, check_captures(game_state, move))
        renderer.clear_selection()

        print("finished the second handle")

        # renderer.update_board()
        # pygame.display.flip() # Force a redraw so we see the selection
    

    # ── Game loop ─────────────────────────────────────────────
    running = True
    last_move_time = - DELAY
    can_go = True
    while running:
        clock.tick(FPS)

        # if game_over(game_state):
        #     print("Game over")


        current_time = pygame.time.get_ticks()
        # print(last_move_time)
        can_move = current_time - last_move_time > DELAY
        can_go = True
        
        print(can_move)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                elif event.key == pygame.K_r:
                    game_state = GameState(board_size)
                    renderer = BoardRenderer(board_size, game_state)
                    humanRole, difficulty = run_menu(renderer.screen)
                    aiRole = ATTACKER_PLAYER if ROLES.get(humanRole) == DEFENDER_PLAYER else DEFENDER_PLAYER
                    aiPlayer = AI_Player(difficulty=DIFFICULTIES.get(difficulty), role=aiRole)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and can_move:
                is_move = handle_click(*event.pos)
                if is_move:
                    last_move_time = pygame.time.get_ticks()
                    can_go = False
                print("Click happened")


        # Memeber 3
        if not game_state.game_over and game_state.current_player == aiRole and can_move and can_go:
            print("AI moved")
            # Add a small delay or check so the AI doesn't move 
            # the exact millisecond the player finishes their turn
            initial, final = aiPlayer.getBestMove(gameState=game_state)
            print("got the move")
            applyAIMove(initial, final)
            last_move_time = pygame.time.get_ticks()
        # ── Member 3 block ends ───────────────────────────────

    
        renderer.update_board()
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main(board_size=DEFAULT_BOARD_SIZE)
