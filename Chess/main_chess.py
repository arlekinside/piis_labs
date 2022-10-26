from chess_algorithms import Algorithm, NegamaxAlgorithm, NegascoutAlgorithm, PvsAlgorithm
from chess_evaluations import ResponsibleEvaluation, DefaultEvaluation, ChessmateEvaluation, Evaluation
from chess_game import ChessGame

eval_num = 1
alg_num = 2
depth = 3

def choose_eval(num) -> Evaluation:
    if num == 1:
        return ResponsibleEvaluation()
    if num == 2:
        return ChessmateEvaluation()

    return DefaultEvaluation()

def choose_algo(algo, eva, depth) -> Algorithm:
    ev = choose_eval(eva)
    if algo == 1:
        return NegamaxAlgorithm(ev, depth)
    if algo == 2:
        return NegascoutAlgorithm(ev, depth)
    if algo == 3:
        return PvsAlgorithm(ev, depth)

    return NegascoutAlgorithm(ev)


if __name__ == '__main__':

    game = ChessGame(choose_algo(alg_num, eval_num, depth), False)

    game.play()
