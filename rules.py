from constants import EMPTY, ATTACKER, ATTACKER_PLAYER, DEFENDER_PLAYER, DEFENDER, KING

directions = [
    (-1, 0), # Up
    (1, 0),  # Down
    (0, -1), # Left
    (0, 1)   # Right
]

def get_possible_moves(game_state, position) -> list[tuple[int, int]]:
    
    valid_moves = []
    board_size = game_state.board_size
    row, col = position

    for row_direction, col_direction in directions:

        current_row = row + row_direction 
        current_col = col + col_direction

        while within_board(board_size, current_row, current_col):

            # Obstacle found (another piece)
            if game_state.get_piece_at(current_row, current_col) != EMPTY:
                break
            
            if is_valid_move(board_size, game_state, (current_row, current_col)):
                valid_moves.append((current_row, current_col))

            current_row += row_direction
            current_col += col_direction

    return valid_moves


def is_valid_move(board_size, game_state, position) -> bool:
    row, col = position

    if (within_board(board_size, row, col)
            and game_state.get_piece_at(row, col) == EMPTY):
        
        if game_state.current_player == ATTACKER_PLAYER:   
            return not game_state.is_restricted(row, col)
        
        return True

    return False


def within_board(board_size, row, col) -> bool:
    return (0 <= row < board_size) and (0 <= col < board_size)


def is_current_player_piece(game_state, piece) -> bool:
    player = game_state.current_player
    return (
        (player == ATTACKER_PLAYER and piece == ATTACKER) or
        (player == DEFENDER_PLAYER and piece in (DEFENDER, KING))
    )


def check_captures(game_state, pos) -> list[tuple[int, int]]:
    row, col = pos
    current_player_pieces = [ATTACKER] if game_state.current_player == ATTACKER_PLAYER else [DEFENDER, KING]
    opponent = [DEFENDER, KING] if game_state.current_player == ATTACKER_PLAYER else [ATTACKER]
    captured = []
    board_size = game_state.board_size

    def is_ally_or_hostile(r, c, team):
        if not within_board(board_size, r, c):
            return False
        piece = game_state.get_piece_at(r, c)
        if piece and piece in team:
            return True
        return game_state.is_restricted(r, c)

    def check_sandwiched(r, c, attacking_pieces):
        
        return False

    # 1. Check opponent neighbors sandwiched by the move
    for dr, dc in directions:
        adj_r, adj_c = row + dr, col + dc
        if not within_board(board_size, adj_r, adj_c):
            continue
        adj_piece = game_state.get_piece_at(adj_r, adj_c)
        if not adj_piece or is_current_player_piece(game_state, adj_piece):
            continue
        if check_sandwiched(adj_r, adj_c, current_player_pieces):
            captured.append((adj_r, adj_c))

    # 2. Check if moved piece walked into a sandwich
    if check_sandwiched(row, col, opponent):
        captured.append((row, col))

    # 3. King capture: surrounded on all 4 sides
    king_pos = game_state.get_king_position()
    if king_pos and game_state.current_player == ATTACKER_PLAYER:
        kr, kc = king_pos
        if all(is_ally_or_hostile(kr + dr, kc + dc, current_player_pieces) for dr, dc in directions):
            captured.append((kr, kc))

    return captured


    
def game_over(game_state):
    king_pos = game_state.get_king_position()

    # Attackers win: king captured
    if king_pos is None:
        return True

    # Defenders win: king reached a corner
    kr, kc = king_pos
    if game_state.is_corner(kr, kc):
        return True

    # Current player has no moves
    pieces = [ATTACKER] if game_state.current_player == ATTACKER_PLAYER else [DEFENDER, KING]
    for piece in pieces:
        for position in game_state.get_all_pieces(piece):
            if get_possible_moves(game_state, position):
                return False

    return True