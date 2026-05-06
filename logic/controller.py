import sys
import pygame

from .state import GameState
from .ai import AI_Player
from .rules import check_captures, is_current_player_piece, get_possible_moves
from gui.board_renderer import BoardRenderer
from gui.choiceMenu import run_menu
from constants import (ATTACKER_PLAYER, DEFENDER_PLAYER,  
                       DIFFICULTIES, FPS, DELAY, DEFAULT_BOARD_SIZE, HUMAN, AI)

class Controller:

    def __init__(self):
        pygame.init()
        
        self.difficulty = "Medium"
        
        self.board_size = DEFAULT_BOARD_SIZE
        self.game_state = GameState(self.board_size)
        self.renderer = BoardRenderer(self.board_size, self.difficulty)

        
        self.human_player = ATTACKER_PLAYER
        self.aiRole = DEFENDER_PLAYER

        self.aiPlayer = AI_Player(difficulty=DIFFICULTIES.get(self.difficulty), role=self.aiRole)

        # For later setup - Default for now
        self.player_type = {
            ATTACKER_PLAYER: HUMAN,
            DEFENDER_PLAYER: AI
        }

        # Pygame
        self.clock = pygame.time.Clock()

        # Animation
        self.last_move_time = - DELAY
        self.current_time = pygame.time.get_ticks()
        self.can_move = True


    def initialize_game_from_menu(self):

        # Get game settings
        mode, humanRole, difficulty, board_size = run_menu(self.renderer.screen)

        self.mode = mode
        self.difficulty = difficulty
        self.board_size = board_size

        if mode == "Human vs Human":
            # Both players are human, no AI needed
            self.player_type = {
                ATTACKER_PLAYER: HUMAN,
                DEFENDER_PLAYER: HUMAN
            }
            self.aiPlayer = None

        else:  # Human vs AI
            self.human_player = humanRole
            self.aiRole = DEFENDER_PLAYER if humanRole == ATTACKER_PLAYER else ATTACKER_PLAYER
            self.aiPlayer = AI_Player(difficulty=DIFFICULTIES.get(self.difficulty), role=self.aiRole)
            self.player_type = {
                self.human_player: HUMAN,
                self.aiRole: AI
            }

        # Initialize game state and renderer with the chosen settings 
        self.game_state = GameState(board_size)
        self.renderer = BoardRenderer(self.board_size, self.difficulty)

        # Reset move timer so the first turn has no delay
        self.last_move_time = pygame.time.get_ticks() - DELAY


    def start_game(self):

        running = True
        while running:
            self.clock.tick(FPS)

            current_player_type = self.player_type[self.game_state.current_player]
            
            # Delay between turns
            self.current_time = pygame.time.get_ticks()
            self.can_move = self.current_time - self.last_move_time > DELAY

            # Listen for events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        running = False
                        break
                    
                    elif event.key == pygame.K_r:
                        self.initialize_game_from_menu()
                    
                elif (event.type == pygame.MOUSEBUTTONDOWN 
                        and event.button == 1 
                        and self.can_move
                        and current_player_type == HUMAN):
                    self.play_human_turn(event)

                    self.renderer.update_board(self.game_state)
                    pygame.display.flip()
                    continue

            if self.game_state.check_game_over():
                break

            # AI
            if current_player_type == AI and self.can_move:
                self.play_AI_turn()

            # Refresh the board to reflect turn 
            self.renderer.update_board(self.game_state)
            pygame.display.flip()

        pygame.quit()


    def play_human_turn(self, event):
        made_move = self.handle_click(*event.pos)
        
        if made_move:
            self.last_move_time = pygame.time.get_ticks()


    def play_AI_turn(self):
        initial, final = self.aiPlayer.getBestMove(gameState=self.game_state)
        self.applyAIMove(initial, final)
        self.last_move_time = pygame.time.get_ticks()


    def handle_click(self, px, py):
        
        if self.game_state.game_over:
            return False

        position = self.renderer.screen_to_board(px, py)
        if position is None:
            return False

        piece = self.game_state.get_piece_at(*position)
        
        if is_current_player_piece(self.game_state, piece):
            valid_moves = get_possible_moves(self.game_state, position)
            self.renderer.set_selection(position, valid_moves)
        
        elif self.renderer.selected_position and position in self.renderer.valid_moves:
            
            from_position = self.renderer.selected_position
            self.renderer.clear_selection()
            
            self.game_state.apply_move(from_position, position)

            captured_positions = check_captures(self.game_state, position)
            self.game_state.record_move(from_position, position, captured_positions)
            return True
        
        else:
            self.renderer.clear_selection()

        return False


    def applyAIMove(self, piece, move):
        self.game_state.get_piece_at(piece[0], piece[1])
        valid_moves = get_possible_moves(self.game_state, piece)
        
        self.renderer.set_selection(piece, valid_moves)

        self.game_state.apply_move(piece, move)
        self.game_state.record_move(piece, move, check_captures(self.game_state, move))
        self.renderer.clear_selection()



def main():
    controller = Controller()
    controller.initialize_game_from_menu()
    controller.start_game()

if __name__ == "__main__":
    main()