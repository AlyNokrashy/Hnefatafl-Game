import copy

from constants import (ATTACKER, ATTACKER_PLAYER, BOARD_11, DEFAULT_BOARD_SIZE,
                       DEFENDER, DEFENDER_PLAYER, EMPTY, KING)


class GameState:
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

    # ------- Public --------------------------------------------------------------------------------------------------------------------------

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

    # executes a VALIDATED/LEGAL move
    # returns true -> move applied
    def apply_move(
        self,
        from_position,
        to_position,
        captured_positions: list[tuple[int, int]] | None = None,
    ) -> bool:
        from_row, from_col = from_position
        to_row, to_col = to_position

        # if source empty
        piece = self.board[from_row][from_col]
        if piece == EMPTY:
            return False

        self.move_history.append(
            {
                "from": from_position,
                "to": to_position,
                "piece": piece,
                "captures": (
                    list(captured_positions)  # makes a copy of captured_positions
                    if captured_positions
                    else []
                ),
            }
        )

        # move piece
        self.board[to_row][to_col] = piece
        self.board[from_row][from_col] = EMPTY

        # remove captured
        if captured_positions:
            for row, col in captured_positions:
                self.board[row][col] = EMPTY

        # next turn
        self._switch_player()
        return True

    # returns a copy of the game state (for the AI)
    def clone_state(self) -> "GameState":
        clone = GameState.__new__(GameState)  # creates empty GameState
        clone.board_size = self.board_size
        clone.board = copy.deepcopy(self.board)
        clone.current_player = self.current_player
        clone.game_over = self.game_over
        clone.winner = self.winner
        clone.throne = self.throne
        clone.corners = list(self.corners)
        clone.move_history = []
        return clone

    # game finished
    def set_game_over(self, winner: str | None) -> None:
        self.game_over = True
        self.winner = winner

    # ------------------ Helpers ---------------------------------------------------------------------------------------------------------------------

    def _switch_player(self) -> None:
        self.current_player = (
            DEFENDER_PLAYER
            if self.current_player == ATTACKER_PLAYER
            else ATTACKER_PLAYER
        )

    # return piece at (row,col) or None if out of bounds
    def get_piece_at(self, row, col) -> int | None:
        if 0 <= row < self.board_size and 0 <= col < self.board_size:
            return self.board[row][col]
        return None

    # return all (row, col) that have the given piece_type
    def get_all_pieces(self, piece_type) -> list[tuple[int, int]]:
        return [
            (row, col)
            for row in range(self.board_size)
            for col in range(self.board_size)
            if self.board[row][col] == piece_type
        ]

    def is_corner(self, row, col) -> bool:
        return (row, col) in self.corners

    def is_throne(self, row, col) -> bool:
        return (row, col) == self.throne

    # corners and throne are for the king only
    def is_restricted(self, row, col) -> bool:
        return self.is_corner(row, col) or self.is_throne(row, col)

    # return king posotion or None if king is captured
    def get_king_position(self) -> tuple[int, int] | None:
        positions = self.get_all_pieces(KING)
        return positions[0] if positions else None

    # piece count
    def count_pieces(self) -> dict:
        count = {ATTACKER: 0, DEFENDER: 0, KING: 0}
        for row in range(self.board_size):
            for col in range(self.board_size):
                piece = self.board[row][col]
                if piece in count:
                    count[piece] += 1
        return count

    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self) -> str:
        symbols = {EMPTY: ".", ATTACKER: "A", DEFENDER: "D", KING: "K"}
        header = "   " + " ".join("ABCDEFGHIJK"[: self.board_size])
        rows = [
            f"{i+1:2} " + " ".join(symbols[cell] for cell in row)
            for i, row in enumerate(self.board)
        ]
        return "\n".join([header] + rows)
