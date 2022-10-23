import chess
from chess import Board, PieceType


def is_game_over(state: Board) -> bool:
    return state.is_stalemate() or state.is_checkmate() or state.is_fivefold_repetition() or state.is_variant_end()


def get_pieces_num(board: Board, isWhite: bool):
    return (get_piece_num(board, chess.PAWN, isWhite),
            get_piece_num(board, chess.KNIGHT, isWhite),
            get_piece_num(board, chess.BISHOP, isWhite),
            get_piece_num(board, chess.ROOK, isWhite),
            get_piece_num(board, chess.QUEEN, isWhite))


def get_piece_num(board: Board, pieceType: PieceType, isWhite: bool):
    return len(board.pieces(pieceType, isWhite))

def get_figure_eval(board: Board, table: list[int], pieceType: PieceType):
    return sum([table[i] for i in board.pieces(pieceType, chess.WHITE)]) \
           + sum([-table[chess.square_mirror(i)] for i in board.pieces(pieceType, chess.BLACK)])
