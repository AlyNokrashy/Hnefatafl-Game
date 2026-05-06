import pygame

from constants import (ATTACKER, BOARD_MARGIN, CELL_SIZE, COLOR_ATTACKER,
                       COLOR_CORNER, COLOR_DARK, COLOR_DEFENDER, COLOR_GRID,
                       COLOR_KING, COLOR_LIGHT, COLOR_SELECTED, COLOR_THRONE,
                       COLOR_VALID, DEFENDER, EMPTY, KING, INFO_PANEL_WIDTH, ATTACKER_PLAYER, DIFFICULTIES, WINDOW_TITLE)

BG_COLOR = (30, 25, 20)
PANEL_COLOR = (20, 18, 14)
TEXT_COLOR = (220, 210, 190)
DIM_COLOR = (120, 110, 90)
ACCENT = (210, 165, 40)

class BoardRenderer:
    def __init__(self, board_size, game_state) -> None:
        w, h = self.window_size(board_size)
        self.screen = pygame.display.set_mode((w, h))
        self.game_state = game_state
        self.cell_size = CELL_SIZE
        self.margin = BOARD_MARGIN

        self.selected_position = None
        self.valid_moves = []
        self.last_moved = None

        self.font_big = pygame.font.SysFont("Segoe UI", 20, bold=True)
        self.font_med = pygame.font.SysFont("Segoe UI", 16)
        self.font_sm = pygame.font.SysFont("Segoe UI", 13)
        self.fonts = (self.font_big, self.font_med, self.font_sm)
        self.panel_x = CELL_SIZE * board_size + BOARD_MARGIN * 2

        self.difficulty = DIFFICULTIES["Medium"]

        pygame.display.set_caption(WINDOW_TITLE)

    # ---- Public Setters ---------------------------------------------------------------------------------

    # set current selected piece and its valid moves, highlight selected cell and valid moves
    def set_selection(self, position, valid_moves) -> None:
        self.selected_position = position
        self.valid_moves = valid_moves or []

    # clear current selection, to reset ui highlights
    def clear_selection(self) -> None:
        self.selected_position = None
        self.valid_moves = []

    # store the last moved position, to highlights the latest move
    def set_last_moved(self, position) -> None:
        self.last_moved = position

    # ---- Coordinates ------------------------------------------------------------------------------------------

    # convert board coordinates to pixels on screen
    def board_to_screen(self, row, col) -> tuple[int, int]:
        return (self.margin + col * self.cell_size, self.margin + row * self.cell_size)

    # convert mouse click to board coordinates
    def screen_to_board(self, px, py) -> tuple[int, int] | None:
        col = (px - self.margin) // self.cell_size
        row = (py - self.margin) // self.cell_size
        size = self.game_state.board_size
        if 0 <= row < size and 0 <= col < size:
            return (row, col)
        return None

    # ---- Drawing -----------------------------------------------------------------------------------------

    # draws board:
    # 1.draw cell
    # 2.draw highlights
    # 3.draw pieces
    def draw(self) -> None:
        self._draw_cells()
        self._draw_highlights()
        self._draw_pieces()

    # draw row and col labels around board
    def draw_labels(self, font) -> None:
        size = self.game_state.board_size
        labels = "ABCDEFGHIJK"
        dim = (120, 100, 70)
        for i in range(size):
            surface = font.render(labels[i], True, dim)
            cx = self.margin + i * self.cell_size + self.cell_size // 2
            self.screen.blit(surface, (cx - surface.get_width() // 2, 8))
            surface = font.render(str(i + 1), True, dim)
            cy = self.margin + i * self.cell_size + self.cell_size // 2
            self.screen.blit(surface, (8, cy - surface.get_height() // 2))

    # -------------------------------------------------------------------------------------------------------------
    # draw board grid
    def _draw_cells(self) -> None:
        size = self.game_state.board_size
        cell_size = self.cell_size
        for row in range(size):
            for col in range(size):
                x, y = self.board_to_screen(row, col)
                if self.game_state.is_corner(row, col):
                    color = COLOR_CORNER
                elif self.game_state.is_throne(row, col):
                    color = COLOR_THRONE
                else:
                    color = color = COLOR_LIGHT if (row + col) % 2 == 0 else COLOR_DARK
                pygame.draw.rect(
                    self.screen, color, (x, y, cell_size, cell_size)
                )  # draw cell
                pygame.draw.rect(
                    self.screen, COLOR_GRID, (x, y, cell_size, cell_size), 1
                )  # draw grid borders

    # draw higlights for valid moves, last move, selected piece
    def _draw_highlights(self) -> None:
        cell_size = self.cell_size
        if self.last_moved:
            x, y = self.board_to_screen(*self.last_moved)
            pygame.draw.rect(
                self.screen, (255, 140, 0), (x, y, cell_size, cell_size), 3
            )
        if self.selected_position:
            x, y = self.board_to_screen(*self.selected_position)
            pygame.draw.rect(
                self.screen, COLOR_SELECTED, (x, y, cell_size, cell_size), 3
            )
        for position in self.valid_moves:
            x, y = self.board_to_screen(*position)
            size = cell_size // 3
            offset = (cell_size - size) // 2

            rect = (x + offset, y + offset, size, size)
            pygame.draw.rect(self.screen, COLOR_VALID, rect)

    # draws all peieces
    def _draw_pieces(self) -> None:
        board = self.game_state.board
        size = self.game_state.board_size
        cell_size = self.cell_size
        radius = cell_size // 2 - 6

        for row in range(size):
            for col in range(size):
                piece = board[row][col]
                if piece == EMPTY:
                    continue
                x, y = self.board_to_screen(row, col)
                cx, cy = x + cell_size // 2, y + cell_size // 2

                if piece == ATTACKER:
                    pygame.draw.circle(self.screen, COLOR_ATTACKER, (cx, cy), radius)
                    pygame.draw.circle(
                        self.screen, (100, 100, 100), (cx, cy), radius, 2
                    )

                if piece == DEFENDER:
                    pygame.draw.circle(self.screen, COLOR_DEFENDER, (cx, cy), radius)
                    pygame.draw.circle(
                        self.screen, (160, 160, 160), (cx, cy), radius, 2
                    )

                elif piece == KING:
                    # thicker radius for king piece
                    king_radius = radius + 3
                    points = [
                        (cx, cy - king_radius),
                        (cx + king_radius, cy),
                        (cx, cy + king_radius),
                        (cx - king_radius, cy),
                    ]
                    pygame.draw.polygon(
                        self.screen,
                        COLOR_KING,
                        points,
                    )
                    pygame.draw.polygon(self.screen, (180, 130, 0), points, 2)

    def window_size(self, board_size: int) -> tuple:
        board_px = CELL_SIZE * board_size + BOARD_MARGIN * 2
        return board_px + INFO_PANEL_WIDTH, board_px

    def draw_panel(self, difficulty):
        font_big, font_med, font_sm = self.fonts
        w = INFO_PANEL_WIDTH
        h = self.screen.get_height()
        x = self.panel_x + 14

        pygame.draw.rect(self.screen, PANEL_COLOR, (self.panel_x, 0, w, h))
        pygame.draw.line(self.screen, (60, 50, 35), (self.panel_x, 0), (self.panel_x, h), 2)

        y = 18

        # Title
        s = font_big.render("Hnefatafl", True, ACCENT)
        self.screen.blit(s, (x, y))
        y += s.get_height() + 2
        s = font_sm.render("Viking Chess  ·   AI", True, DIM_COLOR)
        self.screen.blit(s, (x, y))
        y += s.get_height() + 16

        # Divider
        pygame.draw.line(self.screen, (60, 50, 35), (self.panel_x + 10, y), (self.panel_x + w - 10, y), 1)
        y += 10

        # Current turn
        s = font_sm.render("Current Turn", True, DIM_COLOR)
        self.screen.blit(s, (x, y))
        y += s.get_height() + 4

        player = self.game_state.current_player.capitalize()
        color = (
            (220, 80, 60)
            if self.game_state.current_player == ATTACKER_PLAYER
            else (200, 200, 180)
        )
        s = font_big.render(player, True, color)
        self.screen.blit(s, (x, y))
        y += s.get_height() + 16

        # Divider
        pygame.draw.line(self.screen, (60, 50, 35), (self.panel_x + 10, y), (self.panel_x + w - 10, y), 1)
        y += 10

        # Difficulty
        s = font_sm.render("Difficulty", True, DIM_COLOR)
        self.screen.blit(s, (x, y))
        y += s.get_height() + 4
        s = font_med.render(difficulty, True, TEXT_COLOR)
        self.screen.blit(s, (x, y))
        y += s.get_height() + 2
        s = font_sm.render(f"Depth: {DIFFICULTIES.get(difficulty)}", True, DIM_COLOR)
        self.screen.blit(s, (x, y))
        y += s.get_height() + 16

        # Divider
        pygame.draw.line(self.screen, (60, 50, 35), (self.panel_x + 10, y), (self.panel_x + w - 10, y), 1)
        y += 10

        # Piece counts
        s = font_sm.render("Pieces on board", True, DIM_COLOR)
        self.screen.blit(s, (x, y))
        y += s.get_height() + 4

        counts = self.game_state.count_pieces()
        for label, key, color in [
            ("Attackers", 1, (220, 80, 60)),
            ("Defenders", 2, (200, 200, 180)),
        ]:
            s = font_sm.render(f"{label}: {counts.get(key, 0)}", True, color)
            self.screen.blit(s, (x, y))
            y += s.get_height() + 3

        # Game over
        if self.game_state.game_over:
            y += 16
            pygame.draw.line(
                self.screen, (60, 50, 35), (self.panel_x + 10, y), (self.panel_x + w - 10, y), 1
            )
            y += 12
            winner = self.game_state.winner.capitalize() if self.game_state.winner else "Nobody"
            s = font_big.render(f"{winner} wins!", True, ACCENT)
            self.screen.blit(s, (x, y))
            y += s.get_height() + 6
            s = font_sm.render("Press R to restart", True, DIM_COLOR)
            self.screen.blit(s, (x, y))

        # Controls at bottom
        by = h - 55
        pygame.draw.line(
            self.screen, (60, 50, 35), (self.panel_x + 10, by), (self.panel_x + w - 10, by), 1
        )
        by += 8
        for line in ["[Click] Select / Move", "[R] Restart   [Q] Quit"]:
            s = font_sm.render(line, True, DIM_COLOR)
            self.screen.blit(s, (x, by))
            by += s.get_height() + 3

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty

        
    def update_board(self):
        self.screen.fill(BG_COLOR)
        self.draw()
        self.draw_labels(self.font_sm)
        self.draw_panel(self.difficulty)