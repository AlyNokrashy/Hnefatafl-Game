from .state import GameState
from constants import (ATTACKER, DEFENDER, DIRECTIONS, DEFENDER_PLAYER, POINTS_FOR_SURROUNDING,
                        POINTS_FOR_CORNER_DISTANCE)
from .rules import get_possible_moves, is_valid_move
# defender is min, attacker is max

class AI_Player:
    def __init__(self, difficulty: int, role: str) -> None:
        print(f"aiRole {role}")
        self.role = role
        self.depth = difficulty

    # Uses distance from corner for minimizing player
    # Uses number of attackers around the king for maximizing player
    def evaluate(self, isMaximizing: bool, gameState: GameState) -> int:
        if (gameState.check_game_over()):
            return float('inf') if gameState.winner == ATTACKER else -float('inf')
        
        kingI, kingJ = gameState.get_king_position()
        score = 0
        # For each direction the king is blocked by attackers, add points
        for direction in DIRECTIONS:
                if (gameState.get_piece_at(direction[0] + kingI, direction[1] + kingJ) == ATTACKER 
                    or gameState.is_restricted(direction[0] + kingI, direction[1] + kingJ)):
                    score += POINTS_FOR_SURROUNDING

        distance = float('inf')
        # Get distance between king and nearest corner
        for corner in gameState.corners:
            distance = min(distance, (abs(kingI - corner[0]) + abs(kingJ - corner[1])))
        
        # Closer distance, less points, better for min player (defender)
        score += distance * POINTS_FOR_CORNER_DISTANCE

        # pieces is a dict
        pieces = gameState.count_pieces()
        score += pieces.get(ATTACKER)
        score -= pieces.get(DEFENDER)

        return score
        
    # Returns all moves that can be done by the player
    def get_moves(self, gameState) -> list[list[tuple[int, int]]]:
        player = gameState.current_player
        pieces = gameState.getDefenderPieces() if player == DEFENDER_PLAYER else gameState.getAttackerPieces()
        moves = []
        for i, j in pieces:
            for move in get_possible_moves(game_state=gameState, position=(i, j)):
                moves.append([(i, j), move])
        return moves
            
    def alphabeta(self, gameState, depth, alpha, beta, isMaximizing):
        if (gameState.check_game_over or depth == 0):
            return self.evaluate(isMaximizing, gameState)

        if isMaximizing:
            maxValue = -float('inf')
            for move in self.get_moves(gameState):
                newState = gameState.getResultingState(oldLocation=move[0], newLocation=move[1])
                tmp = self.alphabeta(newState, depth - 1, alpha, beta, False)
                maxValue = max(maxValue, tmp)

                alpha = max(alpha, maxValue)
                if (beta <= alpha):
                    break
            return maxValue
        else:
            minValue = float('inf')
            for move in self.get_moves(gameState):
                newState = gameState.getResultingState(oldLocation=move[0], newLocation=move[1])
                tmp = self.alphabeta(newState, depth - 1, alpha, beta, True)
                minValue = min(minValue, tmp)

                beta = min(beta, minValue)
                if beta <= alpha:
                    break
            return minValue

    def getBestMove(self, gameState) -> tuple[int, int]:
        bestScore = -float('inf')
        # bestMove is a list of 2 tuples, the first is the initail position, the second is the new position
        bestMove = []
        for move in self.get_moves(gameState):
            newState = gameState.getResultingState(oldLocation=move[0], newLocation=move[1])
            score = self.alphabeta(gameState=gameState, depth=self.depth - 1,
                                    alpha=-float('inf'), beta=float('inf'), isMaximizing=True)
            if score > bestScore:
                bestScore = score
                bestMove = move

        return bestMove
