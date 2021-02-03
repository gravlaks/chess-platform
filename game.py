"""
File name: game.py

Creation Date: Mi 03 Feb 2021

Description:

"""

# Python Libraries
# -----------------------------------------------------------------------------
from PyQt5.QtWidgets import QApplication, QWidget


# Local Application Modules
# -----------------------------------------------------------------------------
from chessBoard import ChessBoard
from engine import Engine

class Game:
    def __init__(self):
        self.app = QApplication([])

    def play(self):
        engine = Engine(3)
        chessboard = ChessBoard(engine)
        chessboard.show()
        self.app.exec()


if __name__ == "__main__":

    movehistory = []
    game = Game()
    game.play()
