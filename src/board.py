from enum import Enum

class ChessPieces(Enum):
    NONE = 0

    PAWN = 1
    KNIGHT = 2
    BISHOP = 3
    ROOK = 4
    QUEEN = 5
    KING = 6

    WHITE = 1
    BLACK = 2

class ChessBoard():
    def __init__(self):
        self.clear_board()
        # We keep track of each king's position so we don't have to search the entire board for it
        self.white_king_pos = 0, 3
        self.black_king_pos = 7, 3
        self.player_turn = ChessPieces.WHITE

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

    # This method checks if a move is legal and changes the board state to the respective move if the move is legal.
    # If the move is legal, make the move and return true. If the move is illegal, leave the board unchanged and return
    # false. A move is defined by a tuple of tuples, where the first tuple is the starting position and the second tuple
    # is the ending position of the piece being moved.
    def make_move(self, player_color, move):
        # Unpack the move
        start_pos, end_pos = move
        start_rank, start_file = start_pos
        end_rank, end_file = end_pos
        # Search for the piece we are trying to move
        board_color, piece = self.check_square(start_rank, start_file)
        # Lets check to make sure we are moving an actual piece. If a piece does not exist at the starting square,
        # return false.
        if piece == 0:
            return False
        # Check if the piece we are moving is our color
        if board_color is not player_color:
            return False
        # Next, before we move, we have to make sure our king is not in check
        if self.is_checked(player_color):
            if piece == ChessPieces.KING:
                possible_moves = self.get_king_moves(start_rank, start_file)
                for rank, file in possible_moves:
                    if self.is_checked()


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
        elif color == ChessPieces.BLACK:
            rank, file = self.black_king_pos
        # Based on the position of the king, we have to check all the squares that pieces could potentially be attacking
        # from, and then check if there is a piece there.
        attacker_squares = []

    def is_checked(self, rank, file):


    # This function evaluates the board and determines if either king is in checkmate and which color king is in check
    def is_checkmate(self, rank, file):

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

