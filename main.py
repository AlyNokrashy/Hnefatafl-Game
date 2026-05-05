import sys

import pygame

from constants import (ATTACKER_PLAYER, BOARD_MARGIN, CELL_SIZE,
                       DEFAULT_BOARD_SIZE, DEFENDER_PLAYER, DIFFICULTIES, ROLES,
                       FPS, INFO_PANEL_WIDTH, WINDOW_TITLE)
from gui.board_renderer import BoardRenderer
from logic.state import GameState
from logic.rules import get_possible_moves, is_current_player_piece, check_captures
from logic.ai import AI_Player
from gui.choiceMenu import run_menu

# ── Colors ─────────────────────────────────
BG_COLOR = (30, 25, 20)
PANEL_COLOR = (20, 18, 14)
TEXT_COLOR = (220, 210, 190)
DIM_COLOR = (120, 110, 90)
ACCENT = (210, 165, 40)


def window_size(board_size: int) -> tuple:
    board_px = CELL_SIZE * board_size + BOARD_MARGIN * 2
    return board_px + INFO_PANEL_WIDTH, board_px


def draw_panel(screen, panel_x, game_state, difficulty, fonts):
    font_big, font_med, font_sm = fonts
    w = INFO_PANEL_WIDTH
    h = screen.get_height()
    x = panel_x + 14

    pygame.draw.rect(screen, PANEL_COLOR, (panel_x, 0, w, h))
    pygame.draw.line(screen, (60, 50, 35), (panel_x, 0), (panel_x, h), 2)

    y = 18

    # Title
    s = font_big.render("Hnefatafl", True, ACCENT)
    screen.blit(s, (x, y))
    y += s.get_height() + 2
    s = font_sm.render("Viking Chess  ·   AI", True, DIM_COLOR)
    screen.blit(s, (x, y))
    y += s.get_height() + 16

    # Divider
    pygame.draw.line(screen, (60, 50, 35), (panel_x + 10, y), (panel_x + w - 10, y), 1)
    y += 10

    # Current turn
    s = font_sm.render("Current Turn", True, DIM_COLOR)
    screen.blit(s, (x, y))
    y += s.get_height() + 4

    player = game_state.current_player.capitalize()
    color = (
        (220, 80, 60)
        if game_state.current_player == ATTACKER_PLAYER
        else (200, 200, 180)
    )
    s = font_big.render(player, True, color)
    screen.blit(s, (x, y))
    y += s.get_height() + 16

    # Divider
    pygame.draw.line(screen, (60, 50, 35), (panel_x + 10, y), (panel_x + w - 10, y), 1)
    y += 10

    # Difficulty
    s = font_sm.render("Difficulty", True, DIM_COLOR)
    screen.blit(s, (x, y))
    y += s.get_height() + 4
    s = font_med.render(difficulty, True, TEXT_COLOR)
    screen.blit(s, (x, y))
    y += s.get_height() + 2
    s = font_sm.render(f"Depth: {DIFFICULTIES.get(difficulty)}", True, DIM_COLOR)
    screen.blit(s, (x, y))
    y += s.get_height() + 16

    # Divider
    pygame.draw.line(screen, (60, 50, 35), (panel_x + 10, y), (panel_x + w - 10, y), 1)
    y += 10

    # Piece counts
    s = font_sm.render("Pieces on board", True, DIM_COLOR)
    screen.blit(s, (x, y))
    y += s.get_height() + 4

    counts = game_state.count_pieces()
    for label, key, color in [
        ("Attackers", 1, (220, 80, 60)),
        ("Defenders", 2, (200, 200, 180)),
    ]:
        s = font_sm.render(f"{label}: {counts.get(key, 0)}", True, color)
        screen.blit(s, (x, y))
        y += s.get_height() + 3

    # Game over
    if game_state.game_over:
        y += 16
        pygame.draw.line(
            screen, (60, 50, 35), (panel_x + 10, y), (panel_x + w - 10, y), 1
        )
        y += 12
        winner = game_state.winner.capitalize() if game_state.winner else "Nobody"
        s = font_big.render(f"{winner} wins!", True, ACCENT)
        screen.blit(s, (x, y))
        y += s.get_height() + 6
        s = font_sm.render("Press R to restart", True, DIM_COLOR)
        screen.blit(s, (x, y))

    # Controls at bottom
    by = h - 55
    pygame.draw.line(
        screen, (60, 50, 35), (panel_x + 10, by), (panel_x + w - 10, by), 1
    )
    by += 8
    for line in ["[Click] Select / Move", "[R] Restart   [Q] Quit"]:
        s = font_sm.render(line, True, DIM_COLOR)
        screen.blit(s, (x, by))
        by += s.get_height() + 3


def main(board_size: int = DEFAULT_BOARD_SIZE):
    pygame.init()

    w, h = window_size(board_size)
    screen = pygame.display.set_mode((w, h))
    pygame.display.set_caption(WINDOW_TITLE)
    aiRole, difficulty = run_menu(screen)

    clock = pygame.time.Clock()

    font_big = pygame.font.SysFont("Segoe UI", 20, bold=True)
    font_med = pygame.font.SysFont("Segoe UI", 16)
    font_sm = pygame.font.SysFont("Segoe UI", 13)
    fonts = (font_big, font_med, font_sm)

    panel_x = CELL_SIZE * board_size + BOARD_MARGIN * 2

    game_state = GameState(board_size)
    aiPlayer = AI_Player(difficulty=DIFFICULTIES.get(difficulty), isAttacker=ROLES.get(aiRole))
    renderer = BoardRenderer(screen, game_state)
    # print(game_state.getAttackerPieces())
    # print(game_state.getDefenderPieces())

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
            # print(captured_position)
            game_state.apply_move(from_position, pos)
            captured_positions = check_captures(game_state, pos)
            game_state.record_move(from_position, pos, captured_positions)

            renderer.clear_selection()
        
        # Invalid move
        else:
            renderer.clear_selection()

    # ── Game loop ─────────────────────────────────────────────
    running = True
    while running:
        clock.tick(FPS)

        # if game_over(game_state):
        #     print("Game over")
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                elif event.key == pygame.K_r:
                    aiRole, difficulty = run_menu(screen)
                    game_state = GameState(board_size)
                    aiPlayer = AI_Player(difficulty=DIFFICULTIES.get(difficulty), isAttacker=ROLES.get(aiRole))
                    renderer = BoardRenderer(screen, game_state)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                handle_click(*event.pos)

        # ── Member 3: AI turn ───────────────
        #
        # ── Member 3 block ends ───────────────────────────────

        screen.fill(BG_COLOR)
        renderer.draw()
        renderer.draw_labels(font_sm)
        draw_panel(screen, panel_x, game_state, difficulty, fonts)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main(board_size=DEFAULT_BOARD_SIZE)
