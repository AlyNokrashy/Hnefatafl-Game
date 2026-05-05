from .state import GameState
from constants import ATTACKER, DEFENDER, DIRECTIONS
from .rules import get_possible_moves, is_valid_move
# defender is min, attacker is max

class AI_Player:
    def __init__(self, difficulty: int, isAttacker: bool) -> None:
        self.isAttacker = isAttacker
        self.difficultyLevel = difficulty

    # Uses distance from corner for minimizing player
    # Uses number of attackers around the king for maximizing player
    def evaluate(self, isMaximizing: bool, gameState: GameState) -> int:
        if (gameState.check_game_over):
            return float('inf') if gameState.winner == ATTACKER else -float('inf')
        
        kingI, kingJ = gameState.get_king_position()
        pieces = gameState.count_pieces()
        attackerDifference = pieces.get(ATTACKER) - pieces.get(DEFENDER)
        DefenderDifference = pieces.get(DEFENDER) - pieces.get(ATTACKER)
        if isMaximizing:
            count = attackerDifference
            # neighbours = [(kingI - 1, kingJ), (kingI, kingJ - 1), (kingI + 1, kingJ), (kingI, kingJ + 1)]
            for direction in DIRECTIONS:
                if (gameState.get_piece_at(direction[0] + kingI, direction[1] + kingJ) == ATTACKER 
                    or gameState.is_restricted(direction[0] + kingI, direction[1] + kingJ)):
                    count += 1

            return count

        else:
            distance = float('inf')
            # Get distance between king and nearest corner
            for corner in gameState.corners:
                distance = min(distance, (abs(kingI - corner[0]) + abs(kingJ - corner[1])))
            return distance
        
    # Returns all moves that can be done by the player
    def get_moves(self, gameState) -> list[tuple[int, int]]:
        player = gameState.current_player
        pieces = gameState.getDefenderPieces if player == DEFENDER else gameState.getAttackerPieces
        moves = []
        for i, j in pieces:
            for move in get_possible_moves(game_state=gameState, position=(i, j)):
                moves.append(move)
        return moves
            
    def alphabeta(self, gameState, depth, alpha, beta, isMaximizing):
        if (gameState.check_game_over or depth == 0):
            return self.evaluate(isMaximizing, gameState)

        if isMaximizing:
            maxValue = -float('inf')
            for move in self.get_moves(gameState):
                tmp = self.alphabeta(gameState, depth - 1, alpha, beta, False)
                maxValue = max(maxValue, tmp)

                alpha = max(alpha, maxValue)
                if (beta <= alpha):
                    break
            return maxValue
        else:
            minValue = float('inf')
            for move in self.get_moves(gameState):
                tmp = self.alphabeta(gameState, depth - 1, alpha, beta, True)
                minValue = min(minValue, tmp)

                beta = min(beta, minValue)
                if beta <= alpha:
                    break
            return minValue


