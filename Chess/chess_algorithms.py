import random
from abc import ABC
from time import sleep

from chess import Board

from Chess.chess_evaluations import DefaultEvaluation
from Chess.util import is_game_over


class Algorithm(ABC):

    def __init__(self, evaluation=DefaultEvaluation(), max_depth=2):
        self.evaluation = evaluation
        self.max_depth = max_depth

    def next_move(self, state: Board) -> str:
        raise NotImplemented()


class RandomAlgorithm(Algorithm):
    """
    Generates random move from successors and calls sleep() to make gameplay easy to watch
    """

    def next_move(self, state: Board) -> str:
        legal_moves = state.legal_moves
        rand = random.randint(0, legal_moves.count() - 1)
        i = 0

        for move in legal_moves:
            if rand == i:
                return move.uci()
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
                best_move = move.uci()
            state.pop()
        return best_score, best_move
