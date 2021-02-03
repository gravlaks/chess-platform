"""
File name: chessBoard.py

Creation Date: Mi 03 Feb 2021

Description:

"""

# Python Libraries
# -----------------------------------------------------------------------------
import chess
import chess.svg

from IPython.display import SVG, display
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt, QTimer, QEventLoop
import numpy as np

# Local Application Modules
# -----------------------------------------------------------------------------

from Qwindow import MainWindow




class ChessBoard(MainWindow, chess.Board):
    def __init__(self, engine):

        super().__init__()
        self.engine = engine

        self.svg = chess.svg.board(self).encode("UTF-8")
        self.widgetSvg.load(self.svg)
        self.boardSize = min(self.widgetSvg.width(),
                             self.widgetSvg.height())
        
        self.coordinates = True
        self.margin = 0.05 * self.boardSize if self.coordinates else 0
        self.squareSize = (self.boardSize - 2 * self.margin) / 8.0
        self.last_square = chess.Move.null()

    def paintEvent(self, event):
        self.svg = chess.svg.board(self).encode("UTF-8")
        self.widgetSvg.load(self.svg)
    
    def drawBoard(self):
        self.chessboardSvg = chess.svg.board(self).encode("UTF-8")
        self.widgetSvg.load(self.chessboardSvg)


    def mousePressEvent(self, event):
        print("mouse press")
        if event.buttons() == Qt.RightButton:
            pass
            

        if event.buttons() == Qt.LeftButton:
            if event.x() <= self.boardSize and event.y() <= self.boardSize:
                if (self.margin < event.x() < self.boardSize - self.margin and 
                        self.margin < event.y() < self.boardSize - self.margin):
                    file_coord = int((event.x() - self.margin)/self.squareSize)
                    rank = 7 - int((event.y() - self.margin)/self.squareSize)

                    self.current_square = chess.square(file_coord, rank)

                    if self.move_piece(self.last_square, self.current_square):
                        self.current_square = chess.Move.null()
                        self.last_square = chess.Move.null()
                        self.engine.selectmove(self)
                    self.last_square = self.current_square
                    

            self.drawBoard()
        
    def move_piece(self, last_square, current_square):
        print("moving piece")
        if (current_square != last_square and
                last_square != chess.Move.null() and
                current_square != chess.Move.null()):
            move = chess.Move(last_square, current_square)
        else:
            return False
        print(move)
        if move in self.legal_moves:
            self.push(move)
            print("move taken")
            return True
        return False


