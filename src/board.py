class ChessPieces:
    NONE = 0

    PAWN = 1
    KNIGHT = 2
    BISHOP = 3
    ROOK = 4
    QUEEN = 5
    KING = 6

    WHITE = 1
    BLACK = 2

class ChessBoard:
    def __init__(self, piece_board=None, color_board=None):
        if piece_board is not None and color_board is not None:
            self.piece_board = piece_board
            self.color_board = color_board
        else:
            self.clear_board()
        # We keep track of each king's position so we don't have to search the entire board for it
        self.white_king_pos = 0, 3
        self.black_king_pos = 7, 3
        self.player_turn = ChessPieces.WHITE
        self.white_captured_pieces = []
        self.black_captured_pieces = []

    def clear_board(self):
        self.color_board = \
            [[1, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [2, 2, 2, 2, 2, 2, 2, 2],
             [2, 2, 2, 2, 2, 2, 2, 2]]

        self.piece_board = \
            [[4, 2, 3, 6, 5, 3, 2, 4],
             [1, 1, 1, 1, 1, 1, 1, 1],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [1, 1, 1, 1, 1, 1, 1, 1],
             [4, 2, 3, 6, 5, 3, 2, 4]]

    # This function checks if a move is legal and changes the board state to the respective move if the move is legal.
    # If the move is legal, make the move and return true. If the move is illegal, leave the board unchanged and return
    # false. A move is defined by a tuple of tuples, where the first tuple is the starting position and the second tuple
    # is the ending position of the piece being moved.
    def make_legal_move(self, player_color, move):
        if self.is_legal_move(player_color, move):
            self.make_move(move)

    # This function checks if the specified move is legal. Returns true if the move is legal, false is the move is
    # illegal.
    def is_legal_move(self, player_color, move):
        # Unpack the move
        start_pos, end_pos = move
        start_rank, start_file = start_pos
        end_rank, end_file = end_pos
        # Search for the piece we are trying to move
        board_color, piece = self.check_square(start_rank, start_file)
        # Check to make sure the move is within the bounds of the board.
        if len(self.check_move_bounds([end_pos])) == 0:
            return False
        # Lets check to make sure we are moving an actual piece. If a piece does not exist at the starting square,
        # return false.
        if piece == 0:
            return False
        # Check if the piece we are moving is our color.
        if board_color != player_color:
            return False
        # Next, before we move, we have to make sure our king is not in check.
        if self.is_checked(player_color):
            # If we are in check and the piece we are moving is not our king, this is illegal.
            if piece != ChessPieces.KING:
                return False
            # If we are in check and the piece we are moving is our king, then we have to check if the square the king
            # is moving to would put us in check.
            elif piece == ChessPieces.KING:
                if self.will_be_checked(player_color, end_rank, end_file):
                    return False
                else:
                    return True
        # If we are not in check, but the piece being move is the king, we still need to make sure the square we are
        # moving to will not put us in check.
        elif piece == ChessPieces.KING and self.will_be_checked(player_color, end_rank, end_file):
            return False
        # Simulate the move to see if it would put us in check -- this helps us check for pins that would make a move
        # illegal.
        future_board = ChessBoard(piece_board=self.piece_board.copy(), color_board=self.color_board.copy())
        future_board.make_move(move)
        if future_board.is_checked(player_color):
            return False
        # If the the possible illegality cases have been checked, return true - the move is legal.
        return True

    # This function moves the piece at the initial square to the destination square. If a piece is captured in the
    # process, it is added to the appropriate list of captured pieces.
    def make_move(self, move):
        start_pos, end_pos = move
        start_rank, start_file = start_pos
        end_rank, end_file = end_pos
        # Check if the square we are moving to contains a piece:
        color, piece = self.check_square(start_rank, start_file)
        attacked_color, attacked_piece = self.check_square(end_rank, end_file)
        # If the square does contain a piece, add that piece to the appropriate list of captured pieces
        if (attacked_color, attacked_piece) != (-1, -1):
            if color == ChessPieces.WHITE:
                self.white_captured_pieces.append((attacked_color, attacked_piece))
            elif color == ChessPieces.BLACK:
                self.black_captured_pieces.append((attacked_color, attacked_piece))
        # Set the destination square of the piece to the piece being moved
        self.set_board_square(color, piece, end_rank, end_file)
        # Set the starting square of the piece to empty
        self.set_board_square(ChessPieces.NONE, ChessPieces.NONE, start_rank, start_file)
        # If the piece we moved is the king, update the king position
        if piece == ChessPieces.KING:
            if color == ChessPieces.WHITE:
                self.white_king_pos = end_pos
            elif color == ChessPieces.BLACK:
                self.black_king_pos = end_pos

    # This function sets the square at the given rank and file to the given piece and color
    def set_board_square(self, color, piece, rank, file):
        self.color_board[rank][file] = color
        self.piece_board[rank][file] = piece

    # This function returns a color and piece tuple for a given square.
    def check_square(self, rank, file):
        try:
            color = self.color_board[rank][file]
            piece = self.piece_board[rank][file]
            return color,piece
        except IndexError:
            return -1,-1

    # This function evaluates the board and determines if the specified color king is in check
    def is_checked(self, color):
        if color == ChessPieces.WHITE:
            rank, file = self.white_king_pos
        else:
            rank, file = self.black_king_pos
        # Based on the position of the king, we have to check all the squares that pieces could potentially be attacking
        # from, and then check if the corresponding piece is on a square it could be attacking from.

        # Pawns attack diagonally from the opposite direction of the player's pawns
        if color == ChessPieces.WHITE:
            attacker_squares = [(rank + 1, file + 1), (rank + 1, file - 1)]
            for (rank, file) in attacker_squares:
                if (ChessPieces.BLACK, ChessPieces.PAWN) == self.check_square(rank, file):
                    return True
        if color == ChessPieces.BLACK:
            attacker_squares = [(rank - 1, file + 1), (rank - 1, file - 1)]
            for (rank, file) in attacker_squares:
                if (ChessPieces.BLACK, ChessPieces.PAWN) == self.check_square(rank, file):
                    return True
        # For the remaining possible attacking pieces, we can simple compare the alignment of the king to the potential
        # positions of attacking pieces
        attacker_squares = self.get_knight_moves(rank, file)
        for (rank, file) in attacker_squares:
            if (not color, ChessPieces.KNIGHT) == self.check_square(rank, file):
                return True
        attacker_squares = self.get_bishop_moves(rank, file)
        for (rank, file) in attacker_squares:
            if (not color, ChessPieces.BISHOP) == self.check_square(rank, file):
                return True
        attacker_squares = self.get_rook_moves(rank, file)
        for (rank, file) in attacker_squares:
            if (not color, ChessPieces.ROOK) == self.check_square(rank, file):
                return True
        attacker_squares = self.get_queen_moves(rank, file)
        for (rank, file) in attacker_squares:
            if (not color, ChessPieces.QUEEN) == self.check_square(rank, file):
                return True
        # If we have not found any attackers, return false, the king is not in check
        return False

    # This function evaluates the board and determines if the specified location would put a king in check
    def will_be_checked(self, color, rank, file):
        # Based on the position of the king, we have to check all the squares that pieces could potentially be attacking
        # from, and then check if the corresponding piece is on a square it could be attacking from.

        # Pawns attack diagonally from the opposite direction of the player's pawns
        if color == ChessPieces.WHITE:
            attacker_squares = [(rank + 1, file + 1), (rank + 1, file - 1)]
            for (rank, file) in attacker_squares:
                if (ChessPieces.BLACK, ChessPieces.PAWN) == self.check_square(rank, file):
                    return True
        if color == ChessPieces.BLACK:
            attacker_squares = [(rank - 1, file + 1), (rank - 1, file - 1)]
            for (rank, file) in attacker_squares:
                if (ChessPieces.BLACK, ChessPieces.PAWN) == self.check_square(rank, file):
                    return True
        # For the remaining possible attacking pieces, we can simple compare the alignment of the king to the potential
        # positions of attacking pieces
        attacker_squares = self.get_knight_moves(rank, file)
        for (rank, file) in attacker_squares:
            if (not color, ChessPieces.KNIGHT) == self.check_square(rank, file):
                return True
        attacker_squares = self.get_bishop_moves(rank, file)
        for (rank, file) in attacker_squares:
            if (not color, ChessPieces.BISHOP) == self.check_square(rank, file):
                return True
        attacker_squares = self.get_rook_moves(rank, file)
        for (rank, file) in attacker_squares:
            if (not color, ChessPieces.ROOK) == self.check_square(rank, file):
                return True
        attacker_squares = self.get_queen_moves(rank, file)
        for (rank, file) in attacker_squares:
            if (not color, ChessPieces.QUEEN) == self.check_square(rank, file):
                return True
        # If we have not found any attackers, return false, the king is not in check
        return False

    # This function evaluates the board and determines if either king is in checkmate and which color king is in check
    def is_checkmated(self, player_color):
        if player_color == ChessPieces.WHITE:
            rank, file = self.white_king_pos
        else:
            rank, file = self.black_king_pos
        # In order for the king to be in checkmate, it first must be checked. Otherwise, return false.
        if self.is_checked(player_color):
            # If the king is in check, next we have to check that all possible king moves are illegal.
            possible_king_moves = self.get_king_moves(rank, file)
            is_any_move_legal = False
            future_board = ChessBoard(piece_board=self.piece_board.copy(), color_board=self.color_board.copy())
            for possible_move in possible_king_moves:
                # If there is a legal king move,
                if future_board.is_legal_move(player_color, possible_move):
                    is_any_move_legal = True
            # If no move is legal, return true - the player is checkmated.
            return not is_any_move_legal
        return False

    # This function evaluates the board and returns true if the position is a stalemate or draw, and false is the
    # position is not a or draw.
    def is_draw(self):
        self # dummy statement
        #TODO: check if the board is in a drawn position

    # This function evaluates a list of moves and returns a modified list with only the moves that are within the bounds
    # of the board
    def check_move_bounds(self, move_list):
        for (rank, file) in move_list:
            if rank < 0 or rank > 7:
                move_list.remove((rank, file))
            if file < 0 or rank > 7:
                move_list.remove((rank, file))
        return move_list

    # This function returns the valid pawn moves given the location and color of a pawn.
    def get_pawn_moves(self, rank, file, color):
        move_list = []
        # We need to determine which color the pawn is to determine which way it is moving
        if color == ChessPieces.WHITE:
            # White pawn can move up one square
            move_list.append((rank + 1, file))
            # If the pawn is on the 2nd rank, it can move 2 squares
            if rank == 1:
                move_list.append((rank + 2, file))
            # If there is a black piece to the left or right of the pawn, it can capture
            color, piece = self.check_square(rank + 1, file + 1)
            if color == ChessPieces.BLACK:
                move_list.append((rank + 1, file + 1))
            color, piece = self.check_square(rank + 1, file - 1)
            if color == ChessPieces.BLACK:
                move_list.append((rank + 1, file - 1))

        elif color == ChessPieces.BLACK:
            # Black pawn can move down one square
            move_list.append((rank - 1, file))
            # If the pawn is on the 2nd rank, it can move 2 squares
            if rank == 1:
                move_list.append((rank - 2, file))
            # If there is a black piece to the left or right of the pawn, it can capture
            color, piece = self.check_square(rank - 1, file + 1)
            if color == ChessPieces.BLACK:
                move_list.append((rank - 1, file + 1))
            color, piece = self.check_square(rank, file - 1)
            if color == ChessPieces.BLACK:
                move_list.append((rank - 1, file - 1))

        # Before we return the list of pawn moves, check which moves are out of bounds
        move_list = self.check_move_bounds(move_list)
        return move_list

    # This function returns the valid knight moves from a given square on the board
    def get_knight_moves(self, rank, file):
        # Find all 8 knight moves of +/- 1/2 ranks and +/- 2/1 files
        move_list = [(rank + 2, file + 1), (rank + 2, file - 1), (rank - 2, file + 1), (rank - 2, file - 1),
                     (rank - 1, file + 2), (rank - 1, file - 2), (rank + 1, file + 2), (rank + 1, file - 2)]
        move_list = self.check_move_bounds(move_list)
        return move_list

    # This function returns the valid bishop moves from a given square on the board
    def get_bishop_moves(self, rank, file):
        move_list = []
        # We find all squares diagonally aligned with the bishop within the width of a board (8 squares)
        for new_rank in range(8):
            for new_file in range(8):
                move_list.append((rank + new_rank, file + new_file))
                move_list.append((rank + new_rank, file - new_file))
                move_list.append((rank - new_rank, file + new_file))
                move_list.append((rank - new_rank, file - new_file))
        # Then we remove all squares out of bounds of the board
        move_list = self.check_move_bounds(move_list)
        return move_list

    # This function returns the valid rook moves from a given square on the board
    def get_rook_moves(self, rank, file):
        move_list = []
        # We find all squares horizontally and vertically aligned with the rook within the width of the board
        # (8 squares)
        for new_rank in range(8):
            for new_file in range(8):
                move_list.append((rank + new_rank, file))
                move_list.append((rank - new_rank, file))
                move_list.append((rank, file + new_file))
                move_list.append((rank, file - new_file))
        # Then we remove all squares out of bounds of the board
        move_list = self.check_move_bounds(move_list)
        return move_list

    # This function returns the valid queen moves from a given square on the board
    def get_queen_moves(self, rank, file):
        move_list = []
        # We find all squares vertically, horizontally, and diagonally aligned with the Queen within the width of the
        # board (8 squares)
        for new_rank in range(8):
            for new_file in range(8):
                move_list.append((rank + new_rank, file + new_file))
                move_list.append((rank + new_rank, file - new_file))
                move_list.append((rank - new_rank, file + new_file))
                move_list.append((rank - new_rank, file - new_file))
                move_list.append((rank + new_rank, file))
                move_list.append((rank - new_rank, file))
                move_list.append((rank, file + new_file))
                move_list.append((rank, file - new_file))
        # Then we remove all squares out of bounds of the board
        move_list = self.check_move_bounds(move_list)
        return move_list

    # This function returns the valid king moves from a given square on the baord
    def get_king_moves(self, rank, file):
        # This list contains all squares of distance 1 away from the king
        move_list = [(rank + 1, file), (rank + 1, file), (rank, file + 1), (rank, file - 1),
                     (rank - 1, file + 1), (rank - 1, file - 1), (rank + 1, file + 1), (rank + 1, file - 1)]
        # Then we remove all squares from the list that are out of bounds
        move_list = self.check_move_bounds(move_list)
        return move_list

    def print_board(self):
        print(self.color_board)
        print(self.piece_board)

