import pygame

from constants import (ATTACKER, BOARD_MARGIN, CELL_SIZE, COLOR_ATTACKER,
                       COLOR_CORNER, COLOR_DARK, COLOR_DEFENDER, COLOR_GRID,
                       COLOR_KING, COLOR_LIGHT, COLOR_SELECTED, COLOR_THRONE,
                       COLOR_VALID, DEFENDER, EMPTY, KING)


class BoardRenderer:
    def __init__(self, screen: pygame.Surface, game_state) -> None:
        self.screen = screen
        self.game_state = game_state
        self.cell_size = CELL_SIZE
        self.margin = BOARD_MARGIN

        self.selected_position = None
        self.valid_moves = []
        self.last_moved = None

        # ---- Public Setters ---------------------------------------------------------------------------------

        # set current selected piece and its valid moves, highlight selected cell and valid moves
        def set_selection(self, position, valid_moves) -> None:
            self.selected_postition = position
            self.valid_moves = valid_moves or []

        # clear current selection, to reset ui highlights
        def clear_selection(self) -> None:
            self.selected_position = None
            self.valid_moves = []

        # store the last moved position, to highlights the latest move
        def set_last_moved(self, position) -> None:
            self.last_moved = position

        # ---- Helpers ------------------------------------------------------------------------------------------

        # convert board coordinates to pixels on screen
        def board_to_screen(self, row, col) -> tuple[int, int]:
            return (self.margin + col * self.cs, self.margin + row * self.cs)

        # convert mouse click to board coordinates
        def screen_to_board(self, px, py) -> tuple[int, int] | None:
            col = (px - self.margin) // self.cs
            row = (py - self.margin) // self.cs
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
                cx = self.margin + i * self.cs + self.cs // 2
                self.screen.blit(surface, (cx - surface.get_width() // 2, 8))
                surface = font.render(str(i + 1), True, dim)
                cy = self.margin + i * self.cs + self.cs // 2
                self.screen.blit(surface, (8, cy - surface.get_height() // 2))
