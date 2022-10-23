import sys
from time import sleep

from chess import Board
from chessboard import display

from Chess.chess_algorithms import Algorithm
from Chess.util import is_game_over


class ChessGame:

    def __init__(self, algo: Algorithm):
        """
        Creates new chessboard and start the display
        """
        self.algo = algo

        self.board = Board()
        self.display_board = display.start(self.board.fen())

    def play(self):
        """
        Starts the game loop by calling algorith on each iteration
        """
        while not display.check_for_quit():
            if is_game_over(self.board):
                sleep(60)
                sys.exit(0)
            nextMove = self.algo.next_move(self.board)
            self.board.push_uci(nextMove)
            display.update(self.board.fen(), self.display_board)

