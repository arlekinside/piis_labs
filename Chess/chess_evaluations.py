import random
from abc import ABC

import chess
from chess import Board

from Chess.eval_const import pawn_table, knights_table, bishops_table, rooks_table, queens_table, kings_table
from Chess.util import get_pieces_num, get_figure_eval


class Evaluation(ABC):

    def evaluate(self, board: Board) -> int:
        raise NotImplemented()


class DefaultEvaluation(Evaluation):
    """
    Simply returns random
    """

    def evaluate(self, board: Board) -> int:
        return random.randint(-100, 100)


class ResponsibleEvaluation(Evaluation):

    def evaluate(self, board: Board) -> int:
        if board.is_checkmate():
            if board.turn:
                return -9999
            else:
                return 9999
        if board.is_stalemate():
            return 0
        if board.is_insufficient_material():
            return 0

        # Pawn, Knight, Bishop, Rook and Queen num
        wp, wn, wb, wr, wq = get_pieces_num(board, chess.WHITE)
        bp, bn, bb, br, bq = get_pieces_num(board, chess.BLACK)

        material = 100 * (wp - bp) + 320 * (wn - bn) + 330 * (wb - bb) + 500 * (wr - br) + 900 * (wq - bq)

        pawns_eval = get_figure_eval(board, pawn_table, chess.PAWN)
        knights_eval = get_figure_eval(board, knights_table, chess.KNIGHT)
        bishops_eval = get_figure_eval(board, bishops_table, chess.BISHOP)
        rooks_eval = get_figure_eval(board, rooks_table, chess.BISHOP)
        queens_eval = get_figure_eval(board, queens_table, chess.QUEEN)
        kings_eval = get_figure_eval(board, kings_table, chess.KING)

        evaluation = material + pawns_eval + knights_eval + bishops_eval + rooks_eval + queens_eval + kings_eval
        if board.turn:
            return evaluation
        else:
            return -evaluation
