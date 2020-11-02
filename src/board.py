import copy

import src.constants
from src.piece import Pawn, Knight, Bishop, Rook, Queen, King

class ChessBoard:
    # TODO: Add board initialization based on given position
    def __init__(self, pieces=None):
        self.player_turn = src.constants.WHITE
        self.move_list = []
        self.pieces = []
        self.captured_pieces = []
        self.is_branch = False
        self.is_gameover = False
        self.is_promoting = False
        self.game_result = None
        if pieces is not None:
            self.pieces = pieces
        else:
            self.clear_board()

    # Set the pieces on the board to the default position
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

    # This function takes a piece and move to be made for that piece. If the function is able to make the move, it
    # return true, otherwise false.
    def move(self, piece, move):
        # Check if the move is one of the piece's possible moves
        legal_moves = piece.get_legal_moves(self)
        if move in legal_moves:
            # Unpack the move and see what piece is in the destination square
            rank, file = move
            dest_piece = self.look_at(rank, file)
            # If the king is moving more than two squares, it is a castling move
            if piece.id == src.constants.KING and abs(file - piece.file) >= 2 and piece.can_castle:
                self.move_list.append((piece, (piece.rank, piece.file), move))
                # Check if left castle or right castle:
                if (file - piece.file) > 0:
                    r_rook = self.look_at(piece.rank, piece.file + 3)
                    r_rook.file = file - 1
                    piece.file = file
                    r_rook.can_castle = False
                else:
                    l_rook = self.look_at(piece.rank, piece.file - 4)
                    l_rook.file = file + 1
                    piece.file = file
                    l_rook.can_castle = False
                piece.can_castle = False
                # Swap the turn variable to the opposite player
                self.player_turn = not self.player_turn
                self.check_gameover()
                return True
            # If the piece is a pawn moving diagonally
            elif piece.id == src.constants.PAWN and abs(piece.file - file) > 1 and dest_piece is None:
                captured_pawn = self.look_at(piece.rank, file)
                self.captured_pieces.append(captured_pawn)
                self.pieces.remove(captured_pawn)
                success = True
            if dest_piece is not None:
                if dest_piece.capturable:
                    self.captured_pieces.append(dest_piece)
                    self.pieces.remove(dest_piece)
                    success = True
                else:
                    return False
            else:
                success = True
            if success:
                self.move_list.append((piece, (piece.rank, piece.file), move))
                # Move the piece to the destination square
                piece.rank = rank
                piece.file = file
                # If the piece is a rook or king and it moves, it can no longer castle
                piece.can_castle = False
                # Swap the turn variable to the opposite player
                self.player_turn = not self.player_turn
                self.check_gameover()
                if self.can_promote():
                    self.is_promoting = True
                return True
            return False

    def branch(self, piece, move):
        branch = copy.deepcopy(self)
        branch.is_branch = True
        for future_piece in branch.pieces:
            if piece.rank == future_piece.rank and piece.file == future_piece.file:
                    branch.move(future_piece, move)
        return branch

    # This function returns true if the king of the specified color is in check. Otherwise, false.
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

    # This function checks if the game is over and stores the result in self.game_result
    def check_gameover(self):
        # Check if the player is in check and if they have any legal moves
        legal_moves = []
        is_checked = self.is_in_check(self.player_turn)
        piece_count = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
        color_count = {0: 0, 1: 0}
        for piece in self.pieces:
            piece_count[piece.id] = piece_count[piece.id] + 1
            color_count[piece.color] = color_count[piece.color] + 1
            if piece.color == self.player_turn:
                legal_moves += piece.get_legal_moves(self)
                if len(legal_moves) > 0:
                    return
        if len(legal_moves) == 0:
            if is_checked:
                if self.player_turn == src.constants.WHITE:
                    self.is_gameover = True
                    self.game_result = 'BLACK'
                elif self.player_turn == src.constants.BLACK:
                    self.is_gameover = True
                    self.game_result = 'WHITE'
            else:
                self.is_gameover = True
                self.game_result = 'DRAW'
        # Check if there is sufficient material for checkmate
        if piece_count.get(src.constants.PAWN) <= 0 and piece_count.get(src.constants.QUEEN) <= 0 and \
            piece_count.get(src.constants.ROOK) <= 0:
            if color_count[src.constants.WHITE] < 3 and color_count[src.constants.BLACK] < 3:
                self.is_gameover = True
                self.game_result = 'DRAW'
        # TODO: Check for 3-fold repetition draw

    def can_promote(self):
        for piece in self.pieces:
            if piece.id == src.constants.PAWN:
                if piece.color == src.constants.WHITE and piece.rank == 7:
                    return True
                elif piece.color == src.constants.BLACK and piece.rank == 0:
                    return True
        return False

    def get_promoting_piece(self):
        for piece in self.pieces:
            if piece.id == src.constants.PAWN:
                if piece.color == src.constants.WHITE and piece.rank == 7:
                    return piece
                elif piece.color == src.constants.BLACK and piece.rank == 0:
                    return piece
        return None

    def promote_pawn(self, piece, promotion_type):
        if piece.id == src.constants.PAWN:
            for promoter in self.pieces:
                if promoter.rank == piece.rank and promoter.file == piece.file:
                    self.pieces.remove(promoter)
            self.pieces.append(promotion_type(piece.rank, piece.file, piece.color))

