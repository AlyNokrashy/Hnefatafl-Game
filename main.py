import sys

import pygame

from constants import (ATTACKER_PLAYER, BOARD_MARGIN, CELL_SIZE,
                       DEFAULT_BOARD_SIZE, DEFENDER_PLAYER, DIFFICULTY_DEPTH,
                       FPS, INFO_PANEL_WIDTH, WINDOW_TITLE)
from gui.board_renderer import BoardRenderer
from state import GameState

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
    s = font_sm.render(f"Depth: {DIFFICULTY_DEPTH[difficulty]}", True, DIM_COLOR)
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


def main(board_size: int = DEFAULT_BOARD_SIZE, difficulty: str = "Medium"):
    pygame.init()

    w, h = window_size(board_size)
    screen = pygame.display.set_mode((w, h))
    pygame.display.set_caption(WINDOW_TITLE)
    clock = pygame.time.Clock()

    font_big = pygame.font.SysFont("Segoe UI", 20, bold=True)
    font_med = pygame.font.SysFont("Segoe UI", 16)
    font_sm = pygame.font.SysFont("Segoe UI", 13)
    fonts = (font_big, font_med, font_sm)

    panel_x = CELL_SIZE * board_size + BOARD_MARGIN * 2

    game_state = GameState(board_size)
    renderer = BoardRenderer(screen, game_state)

    # ── Click handler ─────────────────────────────────────────
    def handle_click(px, py):
        if game_state.game_over:
            return

        pos = renderer.screen_to_board(px, py)
        if pos is None:
            return

        # ── Member 2 replaces this block ──────────────────────
        if renderer.selected_position is None:
            piece = game_state.get_piece_at(*pos)
            if piece and piece != 0:
                renderer.set_selection(pos, valid_moves=[])
                # Member 2: moving pieces logic
        else:
            # Member 2: validate move, compute captures, call apply_move

            renderer.clear_selection()
        # ── Member 2 block ends ───────────────────────────────

    # ── Game loop ─────────────────────────────────────────────
    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                elif event.key == pygame.K_r:
                    game_state = GameState(board_size)
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
    main(board_size=DEFAULT_BOARD_SIZE, difficulty="Medium")
