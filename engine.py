"""
File name: engine.py

Creation Date: Mi 03 Feb 2021

Description:

"""

# Python Libraries
# -----------------------------------------------------------------------------
import chess.polyglot
from tables import bishopstable, pawntable, rookstable, knightstable, queenstable
import numpy as np

# Local Application Modules
# -----------------------------------------------------------------------------

class Engine:
    def __init__(self, depth):
        self.depth = depth

    def selectmove(self, board):
        try:
            self.getBookMove(board)
            return
        except:
            pass
        bestMove = chess.Move.null()
        bestValue  = -99999
        alpha = -99999
        beta = 99999
        
        assert( not board.is_stalemate() and
                not board.is_checkmate() and 
                not board.is_insufficient_material())
        
        for move in board.legal_moves:
            board.push(move)
            boardValue = -self.alphabeta(alpha=-beta, beta=-alpha, depth_left = self.depth-1, board = board)
            board.pop()
            if boardValue > bestValue:
                bestValue = boardValue
                bestMove = move
            alpha = max(bestValue, boardValue)


        board.push(bestMove)


    def alphabeta(self, alpha, beta, depth_left, board):
        bestscore = -9999

        if depth_left == 0:
            return self.evaluate(board)

        for move in board.legal_moves:
            board.push(move)
            boardValue = -self.alphabeta(alpha=-beta, beta=-alpha, depth_left = depth_left-1, board=board)
            board.pop()
            bestscore = max(bestscore, boardValue)

            alpha = max(alpha, bestscore)

            if beta<=alpha:
                return beta

        return bestscore

    def quiesce(self, alpha, beta, board):
        stand_pat = evaluate_board(board)
        print(alpha, beta, board)
        print(board.turn)
        if (stand_pat >= beta):
            return beta
        if (alpha < stand_pat):
            alpha = stand_pat

        for move in board.legal_moves:
            if board.is_capture(move):
                board.push(move)
                score = -quiesce(-beta, -alpha, board)
                board.pop()
                

                if score>=beta:
                    return beta
                if score>alpha:
                    alpha = score
        return alpha
            

    def getBookMove(self, board):
   
        move = chess.polyglot.MemoryMappedReader("Perfect2017.bin").weighted_choice(board).move
        board.push(move)

    def evaluate(self, board):
        if board.is_checkmate():
            if board.turn:
                return -9999
            else:
                return 9999

        if board.is_stalemate():
            return 0
        if board.is_insufficient_material():
            return 0

        wp = len(board.pieces(chess.PAWN, chess.WHITE))
        bp = len(board.pieces(chess.PAWN, chess.BLACK))
        wn = len(board.pieces(chess.KNIGHT, chess.WHITE))
        bn = len(board.pieces(chess.KNIGHT, chess.BLACK))
        wb = len(board.pieces(chess.BISHOP, chess.WHITE))
        bb = len(board.pieces(chess.BISHOP, chess.BLACK))
        wr = len(board.pieces(chess.ROOK, chess.WHITE))
        br = len(board.pieces(chess.ROOK, chess.BLACK))
        wq = len(board.pieces(chess.QUEEN, chess.WHITE))
        bq = len(board.pieces(chess.QUEEN, chess.BLACK))

        material = 100*(wp-bp) + 320*(wn-bn) + 330*(wb-bb) + 500 * (wr-br) + 900*(wq-bq)
        pawnsq = np.sum([pawntable[i] for i in board.pieces(chess.PAWN, chess.WHITE)])
        pawnsq += np.sum([-pawntable[chess.square_mirror(i)] 
            for i in board.pieces(chess.PAWN, chess.BLACK)])

        bishopsq = np.sum([bishopstable[i] for i in board.pieces(chess.BISHOP, chess.WHITE)])
        bishopsq += np.sum([-bishopstable[chess.square_mirror(i)] 
            for i in board.pieces(chess.BISHOP, chess.BLACK)])

        knightsq = np.sum([knightstable[i] for i in board.pieces(chess.KNIGHT, chess.WHITE)])
        knightsq += np.sum([-knightstable[chess.square_mirror(i)] 
            for i in board.pieces(chess.KNIGHT, chess.BLACK)])

        rooksq = np.sum([rookstable[i] for i in board.pieces(chess.ROOK, chess.WHITE)])
        rooksq += np.sum([-rookstable[chess.square_mirror(i)] 
            for i in board.pieces(chess.ROOK, chess.BLACK)])

        queensq = np.sum([queenstable[i] for i in board.pieces(chess.QUEEN, chess.WHITE)])
        queensq += np.sum([-queenstable[chess.square_mirror(i)] 
            for i in board.pieces(chess.QUEEN, chess.BLACK)])

        evaluation = material + pawnsq + bishopsq + rooksq + knightsq + queensq

        #if white's turn
        if board.turn:
            return evaluation
        else: 
            return -evaluation

