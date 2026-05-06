from .state import GameState
from constants import (ATTACKER, DEFENDER, DIRECTIONS, DEFENDER_PLAYER, POINTS_FOR_SURROUNDING,
                        POINTS_FOR_CORNER_DISTANCE, ATTACKER_PLAYER, DEFENDER_PLAYER, INF, STEP_FACTOR)
from .rules import get_possible_moves, is_valid_move
# defender is min, attacker is max

class AI_Player:
    def __init__(self, difficulty: int, role: str) -> None:
        print(f"aiRole {role}")
        self.role = role
        self.depth = difficulty

    # Uses distance from corner for minimizing player
    # Uses number of attackers around the king for maximizing player
    def evaluate(self, isMaximizing: bool, gameState: GameState, steps: int) -> int:
        if (gameState.check_game_over()):
            steps *= STEP_FACTOR
            return (INF - steps) if gameState.winner == ATTACKER else (-INF + steps)
        
        kingI, kingJ = gameState.get_king_position()
        score = 0
        # For each direction the king is blocked by attackers, add points
        for direction in DIRECTIONS:
                if (gameState.get_piece_at(direction[0] + kingI, direction[1] + kingJ) == ATTACKER 
                    or gameState.is_restricted(direction[0] + kingI, direction[1] + kingJ)):
                    score += POINTS_FOR_SURROUNDING

        distance = INF
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
    def get_moves(self, gameState, isMaximizing) -> list[list[tuple[int, int]]]:
        # player = gameState.current_player
        pieces = gameState.getAttackerPieces() if isMaximizing else gameState.getDefenderPieces()
        moves = []
        for i, j in pieces:
            # print(f"Pos ({i}, {j}): can go to {get_possible_moves(gameState, (i, j))}")
            for move in get_possible_moves(game_state=gameState, position=(i, j)):
                moves.append([(i, j), move])
        #print(f"Moves: {moves}")
        return moves
            
    def alphabeta(self, gameState, depth, alpha, beta, isMaximizing):
        if (gameState.check_game_over() or depth == 0):
            return self.evaluate(isMaximizing, gameState, self.depth - depth)

        if isMaximizing:
            maxValue = -INF
            for move in self.get_moves(gameState, isMaximizing):
                # print(f"Old game state:\n{gameState}")
                newState = gameState.getResultingState(oldLocation=move[0], newLocation=move[1])
                # player = "A" if isMaximizing else "D"
                # print(f"Player: {player} from {move[0]} to {move[1]} New state:\n{newState}")
                tmp = self.alphabeta(newState, depth - 1, alpha, beta, False)
                maxValue = max(maxValue, tmp)

                alpha = max(alpha, maxValue)
                if (beta <= alpha):
                    break
            return maxValue
        else:
            minValue = INF
            for move in self.get_moves(gameState, isMaximizing):
                newState = gameState.getResultingState(oldLocation=move[0], newLocation=move[1])
                tmp = self.alphabeta(newState, depth - 1, alpha, beta, True)
                minValue = min(minValue, tmp)

                beta = min(beta, minValue)
                if beta <= alpha:
                    break
            return minValue

    def getBestMove(self, gameState) -> list[tuple[int, int]]:
        bestScore = -INF if self.role == ATTACKER_PLAYER else INF
        # bestMove is a list of 2 tuples, the first is the initail position, the second is the new position
        bestMove = []

        for move in self.get_moves(gameState, self.role == ATTACKER_PLAYER):
            newState = gameState.getResultingState(oldLocation=move[0], newLocation=move[1])
            # Attacker is maximizing
            if self.role == ATTACKER_PLAYER:
                score = self.alphabeta(gameState=newState, depth=self.depth - 1,
                                    alpha=-INF, beta=INF, isMaximizing=False)
                if score > bestScore:
                    bestScore = score
                    bestMove = move
            # Defender is minimizing
            elif self.role == DEFENDER_PLAYER:
                score = self.alphabeta(gameState=newState, depth=self.depth - 1,
                                    alpha=-INF, beta=INF, isMaximizing=True)
                if score < bestScore:
                    bestScore = score
                    bestMove = move
            

        print(f"Best move: {bestMove}, score: {score}")
        return bestMove
