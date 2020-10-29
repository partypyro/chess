from src.piece import Pawn, Knight, Bishop, Rook, Queen, King
from src.piece import ChessPieces

class ChessBoard:
    def __init__(self, board=None):
        self.board = [[None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None]]
        self.player_turn = ChessPieces.WHITE
        self.white_pieces = []
        self.white_captured_pieces = []
        self.black_pieces = []
        self.black_captured_pieces = []

        if board is None:
            self.clear_board()
            self.set_pieces()

    def clear_board(self):
        # Add in the major pieces
        self.white_pieces = [Rook(0, 0, ChessPieces.WHITE), Rook(0, 7, ChessPieces.WHITE),
                             Knight(0, 1, ChessPieces.WHITE), Knight(0, 6, ChessPieces.WHITE),
                             Bishop(0, 2, ChessPieces.WHITE), Bishop(0, 5, ChessPieces.WHITE),
                             King(0, 3, ChessPieces.WHITE), Queen(0, 4, ChessPieces.WHITE)]
        self.black_pieces = [Rook(7, 0, ChessPieces.BLACK), Rook(7, 7, ChessPieces.BLACK),
                             Knight(7, 1, ChessPieces.BLACK), Knight(7, 6, ChessPieces.BLACK),
                             Bishop(7, 2, ChessPieces.BLACK), Bishop(7, 5, ChessPieces.BLACK),
                             King(7, 3, ChessPieces.BLACK), Queen(7, 4, ChessPieces.BLACK)]
        # Add in the pawns
        for i in range(0, 8):
            self.white_pieces.append(Pawn(1, i, ChessPieces.WHITE))
            self.black_pieces.append(Pawn(6, i, ChessPieces.BLACK))

    def set_pieces(self):
        # Create an array filled with the piece objects
        for piece in self.white_pieces:
            rank, file = piece.rank, piece.file
            self.board[rank][file] = piece
        for piece in self.black_pieces:
            rank, file = piece.rank, piece.file
            self.board[rank][file] = piece

    def get_all_pieces(self):
        return self.white_pieces + self.black_pieces

    def check_square(self, rank, file):
        return self.board[rank][file]

    def print_board(self):
        print(self.board)

