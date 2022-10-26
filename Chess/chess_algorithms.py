import random
from abc import ABC
from sre_constants import SUCCESS
from time import sleep

from chess import Board, Move

from chess_evaluations import DefaultEvaluation
from util import is_game_over


def get_successors(board: Board, move: Move):
    if move is None:
        return board.legal_moves

    board.push_uci(move.uci())
    successors = board.legal_moves
    board.pop()
    return successors


class Algorithm(ABC):

    def __init__(self, evaluation=DefaultEvaluation(), max_depth=2):
        self.evaluation = evaluation
        self.max_depth = max_depth

    def next_move(self, state: Board) -> Move:
        raise NotImplemented()


class RandomAlgorithm(Algorithm):
    """
    Generates random move from successors and calls sleep() to make gameplay easy to watch
    """

    def next_move(self, state: Board) -> Move:
        legal_moves = state.legal_moves
        rand = random.randint(0, legal_moves.count() - 1)
        i = 0

        for move in legal_moves:
            if rand == i:
                return move
            i = i + 1
        sleep(1)


class NegamaxAlgorithm(Algorithm):
    """
    Generates next move from successors using negamax
    """

    def __init__(self, evaluation=DefaultEvaluation(), max_depth=2):
        super().__init__(evaluation, max_depth)

    def next_move(self, state: Board):
        return self.negamax(state, 0)[1]

    def negamax(self, state: Board, depth):
        if self.max_depth == depth or is_game_over(state):
            return self.evaluation.evaluate(state), None

        best_score = float('-inf')
        best_move = None
        for move in state.legal_moves:
            state.push_uci(move.uci())
            score = -self.negamax(state, depth + 1)[0]
            if score > best_score:
                best_score = score
                best_move = move
            state.pop()
        return best_score, best_move


class NegascoutAlgorithm(Algorithm):
    def __init__(self, evaluation=DefaultEvaluation(), max_depth=2):
        super().__init__(evaluation, max_depth)

    def next_move(self, state: Board):
        return self.negascout(state, None, 0, float('-inf'), float('inf'))[1]

    def negascout(self, state: Board, nextMove: Move, depth, alpha, beta):
        if depth == self.max_depth or is_game_over(state):
            state.push_uci(nextMove.uci())
            evaluation = self.evaluation.evaluate(state)
            state.pop()
            return evaluation, nextMove

        best_score = float("-inf")
        best_move = None
        b = beta

        for move in get_successors(state, nextMove):
            score, local_best = self.negascout(state, move, depth + 1, -b, -alpha)
            score *= -1
            if score > best_score:
                if alpha < score < beta:
                    best_score = score
                    best_move = local_best
                else:
                    best_score, best_move = self.negascout(state, move, depth + 1, -beta, -score)
                    best_score *= -1

            alpha = max(score, alpha)
            if alpha > beta:
                return alpha, move
            b = alpha + 1
        return best_score, best_move


class PvsAlgorithm(Algorithm):

    def __init__(self, evaluation=DefaultEvaluation(), max_depth=2):
        super().__init__(evaluation, max_depth)

    def next_move(self, state: Board):
        return self.pvs(state, None, 0, float('-inf'), float('inf'))[1]

    def pvs(self, state: Board, nextMove: Move, depth, alpha, beta):
        if depth == self.max_depth or is_game_over(state):
            state.push_uci(nextMove.uci())
            evaluation = self.evaluation.evaluate(state)
            state.pop()
            return evaluation, nextMove

        best_score = float("-inf")
        best_move = None
        b = beta

        for move in get_successors(state, nextMove):
            score, local_best = self.pvs(state, move, depth + 1, -b, -alpha)
            score *= -1
            if score > best_score:
                if alpha < score < beta:
                    best_score = score
                    best_move = local_best
                else:
                    best_score, best_move = self.pvs(state, move, depth + 1, -beta, -score)
                    best_score *= -1

            if alpha > beta:
                return alpha, move
            b = alpha + 1
        return best_score, best_move
