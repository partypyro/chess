import copy

import src.constants
from src.piece import Pawn, Knight, Bishop, Rook, Queen, King

class ChessBoard:
    # TODO: Add board initialization based on given position
    def __init__(self, pieces=None):
        self.player_turn = src.constants.WHITE
        self.pieces = []
        self.captured_pieces = []
        self.is_branch = False
        if pieces is not None:
            self.pieces = pieces
        else:
            self.clear_board()

    def clear_board(self):
        # Add in the major pieces
        self.pieces = [
            # White pieces
            Rook(0, 0, src.constants.WHITE), Rook(0, 7, src.constants.WHITE),
            Knight(0, 1, src.constants.WHITE), Knight(0, 6, src.constants.WHITE),
            Bishop(0, 2, src.constants.WHITE), Bishop(0, 5, src.constants.WHITE),
            King(0, 4, src.constants.WHITE), Queen(0, 3, src.constants.WHITE),
            # Black pieces
            Rook(7, 0, src.constants.BLACK), Rook(7, 7, src.constants.BLACK),
            Knight(7, 1, src.constants.BLACK), Knight(7, 6, src.constants.BLACK),
            Bishop(7, 2, src.constants.BLACK), Bishop(7, 5, src.constants.BLACK),
            King(7, 4, src.constants.BLACK), Queen(7, 3, src.constants.BLACK)
        ]
        # Add in the pawns
        for i in range(0, 8):
            self.pieces.append(Pawn(1, i, src.constants.WHITE))
            self.pieces.append(Pawn(6, i, src.constants.BLACK))

    def look_at(self, rank, file):
        # Search thru the piece list and find the piece with the same rank and file
        for piece in self.pieces:
            if piece.rank == rank and piece.file == file:
                return piece

    def move(self, piece, move):
        # If we are in check, the move we make has to get us out of check

        # Swap the turn variable to the opposite player
        # Unpack the move and see what piece is in the destination square
        rank, file = move
        dest_piece = self.look_at(rank, file)
        # If there is a piece in the destination square, remove the piece and add it to the list of captured pieces
        # See if the piece
        if piece.id == src.constants.KING:
            # If the king is moving more than two squares, it is a castling move
            if abs(file - piece.file) >= 2:
                piece.castle(self, move)
                self.player_turn = not self.player_turn
                return True
            else:
                # Set the king's new location
                piece.rank = rank
                piece.file = file
                self.player_turn = not self.player_turn
                return True
        else:
            if dest_piece is not None:
                if dest_piece.capturable:
                    self.captured_pieces.append(dest_piece)
                    self.pieces.remove(dest_piece)
                else:
                    return False
            # Set the piece's new location
            piece.rank = rank
            piece.file = file
            # If the piece being moved is a rook, it can no longer castle
            if piece.id == src.constants.ROOK:
                piece.can_castle = False
            self.player_turn = not self.player_turn
            return True

    def branch(self, piece, move):
        branch = copy.deepcopy(self)
        branch.is_branch = True
        for future_piece in branch.pieces:
            if piece.rank == future_piece.rank and piece.file == future_piece.file:
                    branch.move(future_piece, move)
        return branch

    def is_in_check(self, color):
        king = None
        for piece in self.pieces:
            # If the king of the current player's turn is in check, return true
            if piece.id == src.constants.KING and piece.color == color:
                king = piece
        for attacker in self.pieces:
            if attacker.color != king.color:
                attacks = attacker.get_legal_moves(self)
                for (rank, file) in attacks:
                    if rank == king.rank and file == king.file:
                        return True
        return False