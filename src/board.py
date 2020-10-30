import src.constants
from src.piece import Pawn, Knight, Bishop, Rook, Queen, King

class ChessBoard:
    def __init__(self, board=None):
        self.player_turn = src.constants.WHITE
        self.pieces = []
        self.white_captured_pieces = []
        self.black_captured_pieces = []
        # If
        if board is None:
            self.clear_board()

    def clear_board(self):
        # Add in the major pieces
        self.pieces = [Rook(0, 0, src.constants.WHITE), Rook(0, 7, src.constants.WHITE),
                             Knight(0, 1, src.constants.WHITE), Knight(0, 6, src.constants.WHITE),
                             Bishop(0, 2, src.constants.WHITE), Bishop(0, 5, src.constants.WHITE),
                             King(0, 3, src.constants.WHITE), Queen(0, 4, src.constants.WHITE),
                             Rook(7, 0, src.constants.BLACK), Rook(7, 7, src.constants.BLACK),
                             Knight(7, 1, src.constants.BLACK), Knight(7, 6, src.constants.BLACK),
                             Bishop(7, 2, src.constants.BLACK), Bishop(7, 5, src.constants.BLACK),
                             King(7, 3, src.constants.BLACK), Queen(7, 4, src.constants.BLACK)]
        # Add in the pawns
        for i in range(0, 8):
            self.pieces.append(Pawn(1, i, src.constants.WHITE))
            self.pieces.append(Pawn(6, i, src.constants.BLACK))

    def check_square(self, rank, file):
        for piece in self.pieces:
            if piece.rank == rank and piece.file == file:
                return piece

    def move(self, piece, move):
        self.player_turn = not self.player_turn
        rank, file = move
        piece.rank = rank
        piece.file = file

    def print_board(self):
        print(self.board)

