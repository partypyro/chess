import src.constants

# Parent class for all pieces - basic functions to get possible moves, move the piece, and check if a square is in the
# bounds of the board
class Piece:
    def __init__(self, rank, file, piece_id, color):
        self.rank, self.file = rank, file
        self.piece_id = piece_id
        self.color = color

    # This function represents the possible squares that a piece can go to, given no obstacles on infinite
    def get_possible_moves(self, board):
        return []

    def get_legal_moves(self, board):
        move_list = self.get_possible_moves(board)
        for i, vector in enumerate(move_list):
            move_list[i] = self.remove_out_of_bounds(vector)
        self.remove_illegal_moves(move_list, board)
        return sum(move_list, [])

    # This function evaluates a list of moves and returns a modified list with only the moves that are within the bounds
    # of the board
    def remove_out_of_bounds(self, square_list):
        for (rank, file) in square_list:
            if rank < 0 or rank > 7 or file < 0 or file > 7:
                square_list.remove((rank, file))
        return square_list

    # This function evaluates a list of move vectors, or lists of moves, and evaluates if there is a obstacle in the way
    # of that piece continuing its path
    def remove_illegal_moves(self, vector_list, board):
        for i, vector in enumerate(vector_list):
            vector_list[i] = self.remove_out_of_bounds(vector)
            is_blocked = False
            for (rank, file) in vector.copy():
                square = board.check_square(rank, file)
                if is_blocked:
                    vector.remove((rank, file))
                elif square is not None:
                    if square.color == board.player_turn:
                        vector.remove((rank, file))
                        is_blocked = True
                    elif square.color != board.player_turn:
                        is_blocked = True

    # Move the piece to a new square
    def move(self, rank, file):
        self.rank = rank
        self.file = file

class Pawn(Piece):
    def __init__(self, rank, file, color):
        self.piece_id = src.constants.PAWN
        super(Pawn, self).__init__(rank, file, self.piece_id, color)

    def get_possible_moves(self, board):
        destination_squares = []
        # We need to determine which color the pawn is to determine which way it is moving
        if self.color == src.constants.WHITE:
            # White pawn can move up one square
            destination_squares.append((self.rank + 1, self.file))
            # If the pawn is on the 2nd self.rank, it can move 2 squares
            if self.rank == 1:
                destination_squares.append((self.rank + 2, self.file))
            # If there is a black piece to the left or right of the pawn, it can capture
            if board.check_square(self.rank + 1, self.file + 1) is not None:
                destination_squares.append((self.rank + 1, self.file + 1))
            if board.check_square(self.rank + 1, self.file - 1) is not None:
                destination_squares.append((self.rank - 1, self.file - 1))

        elif self.color == src.constants.BLACK:
            # Black pawn can move down one square
            destination_squares.append((self.rank - 1, self.file))
            # If the pawn is on the 2nd self.rank, it can move 2 squares
            if self.rank == 6:
                destination_squares.append((self.rank - 2, self.file))
            # If there is a black piece to the left or right of the pawn, it can capture
            if board.check_square(self.rank - 1, self.file + 1) is not None:
                destination_squares.append((self.rank - 1, self.file + 1))
            if board.check_square(self.rank - 1, self.file - 1) is not None:
                destination_squares.append((self.rank - 1, self.file - 1))

        # Before we return the list of pawn moves, check which moves are out of bounds
        destination_squares = self.remove_out_of_bounds(destination_squares)
        return destination_squares

    def get_legal_moves(self, board):
        move_list = self.get_possible_moves(board)
        self.remove_out_of_bounds(move_list)
        return move_list

class Knight(Piece):
    def __init__(self, rank, file, color):
        self.piece_id = src.constants.KNIGHT
        super(Knight, self).__init__(rank, file, self.piece_id, color)

    # This function returns the valid knight moves from a given square on the board
    def get_possible_moves(self, board):
        # Find all 8 knight moves of +/- 1/2 ranks and +/- 2/1 files
        destination_squares = [(self.rank + 2, self.file + 1), (self.rank + 2, self.file - 1),
                     (self.rank - 2, self.file + 1), (self.rank - 2, self.file - 1),
                     (self.rank - 1, self.file + 2), (self.rank - 1, self.file - 2),
                     (self.rank + 1, self.file + 2), (self.rank + 1, self.file - 2)]
        return destination_squares

    def get_legal_moves(self, board):
        move_list = self.get_possible_moves(board)
        self.remove_out_of_bounds(move_list)
        return move_list

class Bishop(Piece):
    def __init__(self, rank, file, color):
        self.piece_id = src.constants.BISHOP
        super(Bishop, self).__init__(rank, file, self.piece_id, color)

    def get_possible_moves(self, board):
        # We find all squares diagonally aligned with the bishop within the width of a board (8 squares)
        destination_squares = [
            [(self.rank + increment, self.file + increment) for increment in range(1,8)],
            [(self.rank + increment, self.file - increment) for increment in range(1,8)],
            [(self.rank - increment, self.file + increment) for increment in range(1,8)],
            [(self.rank - increment, self.file - increment) for increment in range(1,8)]
        ]
        return destination_squares

class Rook(Piece):
    def __init__(self, rank, file, color):
        self.piece_id = src.constants.ROOK
        super(Rook, self).__init__(rank, file, self.piece_id, color)

    def get_possible_moves(self, board):
        # We find all squares horizontally and vertically aligned with the rook within the width of the board
        # (8 squares)
        destination_squares = [
            [(self.rank + increment, self.file) for increment in range(1,8)],
            [(self.rank - increment, self.file) for increment in range(1,8)],
            [(self.rank, self.file + increment) for increment in range(1,8)],
            [(self.rank, self.file - increment) for increment in range(1,8)]
        ]
        return destination_squares

class Queen(Piece):
    def __init__(self, rank, file, color):
        self.piece_id = src.constants.QUEEN
        super(Queen, self).__init__(rank, file, self.piece_id, color)

    def get_possible_moves(self, board):
        # We find all squares vertically, horizontally, and diagonally aligned with the Queen within the width of the
        # board (8 squares)
        destination_squares = [
            [(self.rank + increment, self.file + increment) for increment in range(1,8)],
            [(self.rank + increment, self.file - increment) for increment in range(1,8)],
            [(self.rank - increment, self.file + increment) for increment in range(1,8)],
            [(self.rank - increment, self.file - increment) for increment in range(1,8)],
            [(self.rank + increment, self.file) for increment in range(1,8)],
            [(self.rank - increment, self.file) for increment in range(1,8)],
            [(self.rank, self.file + increment) for increment in range(1,8)],
            [(self.rank, self.file - increment) for increment in range(1,8)]
        ]
        return destination_squares

class King(Piece):
    def __init__(self, rank, file, color):
        self.piece_id = src.constants.KING
        super(King, self).__init__(rank, file, self.piece_id, color)

    def get_possible_moves(self, board):
        # This list contains all squares of distance 1 away from the king
        destination_squares = [
             [(self.rank + 1, self.file)], [(self.rank + 1, self.file)],
             [(self.rank, self.file + 1)], [(self.rank, self.file - 1)],
             [(self.rank - 1, self.file + 1)], [(self.rank - 1, self.file - 1)],
             [(self.rank + 1, self.file + 1)], [(self.rank + 1, self.file - 1)]
        ]
        return destination_squares