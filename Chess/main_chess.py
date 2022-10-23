import chess_algorithms
from Chess.chess_evaluations import DefaultEvaluation
from Chess.chess_game import ChessGame

if __name__ == '__main__':
    evaluation = DefaultEvaluation()
    algo = chess_algorithms.NegamaxAlgorithm(evaluation, 3)
    game = ChessGame(algo)

    game.play()
