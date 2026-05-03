import copy

from constants import (ATTACKER, ATTACKER_PLAYER, BOARD_11, DEFAULT_BOARD_SIZE,
                       DEFENDER, DEFENDER_PLAYER, EMPTY, KING)


class GamState:
    # board[row][col]
    def __init__(self, board_size: int = DEFAULT_BOARD_SIZE):
        self.board_size = board_size
        self.current_player = ATTACKER_PLAYER  # attacker moves first
        self.game_over = False
        self.winner = None

        mid = board_size // 2
        self.throne = (mid, mid)
        self.corners = [
            (0, 0),
            (0, board_size - 1),
            (board_size - 1, 0),
            (board_size - 1, board_size - 1),
        ]

        self.move_history: list[dict] = []
        self.board = self._init_board()

        # ------------------------- board initialization -----------------------------------------------------

    def _init_board(self) -> list[list[int]]:
        board = []
        for i in range(self.board_size):
            row = [EMPTY] * self.board_size
            board.append(row)
        if self.board_size == 11:
            self._setup_11x11(board)
        else:
            self._setup_9x9(board)
        return board

    def _setup_11x11(self, board: list[list[int]]) -> None:
        mid = self.board_size // 2

        # KING
        board[mid][mid] = KING

        # 12 defenders around the king - offsets relative to mid
        defender_offsets = [
            # vertical
            (-2, 0),
            (-1, 0),
            (1, 0),
            (2, 0),
            # horizontal
            (0, -2),
            (0, -1),
            (0, 1),
            (0, 2),
            # diagonal
            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1),
        ]

        for offset_row, offset_col in defender_offsets:
            board[mid + offset_row][mid + offset_col] = DEFENDER

        # 24 Attackers — 6 per side
        attacker_positions = [
            # Top
            (0, 3),
            (0, 4),
            (0, 5),
            (0, 6),
            (0, 7),
            (1, 5),
            # Bottom
            (10, 3),
            (10, 4),
            (10, 5),
            (10, 6),
            (10, 7),
            (9, 5),
            # Left
            (3, 0),
            (4, 0),
            (5, 0),
            (6, 0),
            (7, 0),
            (5, 1),
            # Right
            (3, 10),
            (4, 10),
            (5, 10),
            (6, 10),
            (7, 10),
            (5, 9),
        ]

        for row, col in attacker_positions:
            board[row][col] = ATTACKER

    def _setup_9x9(self, board: list[list[int]]) -> None:
        mid = self.board_size // 2

        board[mid][mid] = KING

        defender_offsets = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
            (-2, 0),
            (2, 0),
            (0, -2),
            (0, 2),
        ]

        for offset_row, offset_col in defender_offsets:
            board[mid + offset_row][mid + offset_col] = DEFENDER

            # 16 Attackers
            attacker_positions = [
                (0, 3),
                (0, 4),
                (0, 5),
                (1, 4),
                (8, 3),
                (8, 4),
                (8, 5),
                (7, 4),
                (3, 0),
                (4, 0),
                (5, 0),
                (4, 1),
                (3, 8),
                (4, 8),
                (5, 8),
                (4, 7),
            ]
            for row, col in attacker_positions:
                board[row][col] = ATTACKER

    # returns copy of the current game state as a dict
    def get_state(self) -> dict:
        return {
            "board": [row[:] for row in self.board],  # copies all rows
            "board_size": self.board_size,
            "current_player": self.current_player,
            "game_over": self.game_over,
            "winner": self.winner,
            "throne": self.throne,
            "corners": list(self.corners),
        }
