import random
import sys
from time import sleep

from chess import Board, Move
from chessboard import display

from chess_algorithms import Algorithm
from util import is_game_over

def pick_random_move(state: Board) -> Move:
    successors = state.legal_moves
    rand = random.randint(0, successors.count() - 1)

    i = 0
    for move in successors:
        if i == rand:
            return move
        i += 1

def print_end_game(state: Board):
    print('End game')
    if state.is_fivefold_repetition():
        print("fivefold_repetition")
        return
    if state.is_checkmate():
        if state.turn:
            print("Black wins")
        else:
            print("White wins")
        return
    print("Draw")

class ChessGame:

    def __init__(self, algo: Algorithm, isWhiteRandom = True):
        """
        Creates new chessboard and start the display
        """
        self.algo = algo
        self.isWhiteRandom = isWhiteRandom

        self.board = Board()
        self.display_board = display.start(self.board.fen())

    def play(self):
        """
        Starts the game loop by calling algorith on each iteration
        """
        while not display.check_for_quit():
            if is_game_over(self.board):
                print_end_game(self.board)
                sleep(60)
                sys.exit(0)

            if self.board.turn:
                if self.isWhiteRandom:
                    nextMove = pick_random_move(self.board)
                else:
                    nextMove = self.algo.next_move(self.board)
            else:
                nextMove = self.algo.next_move(self.board)
            self.board.push_uci(nextMove.uci())
            display.update(self.board.fen(), self.display_board)

