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

class Piece:
    def __init__(self, rank, file, piece_id, color):
        self.rank, self.file = rank, file
        self.piece_id = piece_id
        self.color = color

    # This function represents the possible squares that a piece can go to
    def get_possible_moves(self):
        pass

    # This function evaluates a list of moves and returns a modified list with only the moves that are within the bounds
    # of the board
    def check_square_bounds(self, square_list):
        for (rank, file) in square_list:
            if rank < 0 or rank > 7 or file < 0 or file > 7:
                square_list.remove((rank, file))
        return square_list

    # Move the piece to a new square
    def move(self, rank, file):
        self.rank = rank
        self.file = file

class Pawn(Piece):
    def __init__(self, rank, file, color):
        self.piece_id = ChessPieces.PAWN
        super(Pawn, self).__init__(rank, file, self.piece_id, color)

    def get_possible_moves(self):
        destination_squares = []
        # We need to determine which color the pawn is to determine which way it is moving
        if self.color == ChessPieces.WHITE:
            # White pawn can move up one square
            destination_squares.append((self.rank + 1, self.file))
            # If the pawn is on the 2nd self.rank, it can move 2 squares
            if self.rank == 1:
                destination_squares.append((self.rank + 2, self.file))
            # If there is a black piece to the left or right of the pawn, it can capture
            destination_squares.append((self.rank + 1, self.file + 1))
            destination_squares.append((self.rank + 1, self.file - 1))

        elif self.color == ChessPieces.BLACK:
            # Black pawn can move down one square
            destination_squares.append((self.rank - 1, self.file))
            # If the pawn is on the 2nd self.rank, it can move 2 squares
            if self.rank == 6:
                destination_squares.append((self.rank - 2, self.file))
            # If there is a black piece to the left or right of the pawn, it can capture
            destination_squares.append((self.rank - 1, self.file + 1))
            destination_squares.append((self.rank - 1, self.file - 1))

        # Before we return the list of pawn moves, check which moves are out of bounds
        destination_squares = self.check_square_bounds(destination_squares)
        return destination_squares

class Knight(Piece):
    def __init__(self, rank, file, color):
        self.piece_id = ChessPieces.KNIGHT
        super(Knight, self).__init__(rank, file, self.piece_id, color)

    # This function returns the valid knight moves from a given square on the board
    def get_possible_moves(self):
        # Find all 8 knight moves of +/- 1/2 ranks and +/- 2/1 files
        destination_squares = [(self.rank + 2, self.file + 1), (self.rank + 2, self.file - 1),
                     (self.rank - 2, self.file + 1), (self.rank - 2, self.file - 1),
                     (self.rank - 1, self.file + 2), (self.rank - 1, self.file - 2),
                     (self.rank + 1, self.file + 2), (self.rank + 1, self.file - 2)]
        destination_squares = self.check_square_bounds(destination_squares)
        return destination_squares

class Bishop(Piece):
    def __init__(self, rank, file, color):
        self.piece_id = ChessPieces.BISHOP
        super(Bishop, self).__init__(rank, file, self.piece_id, color)

    def get_possible_moves(self):
        destination_squares = []
        # We find all squares diagonally aligned with the bishop within the width of a board (8 squares)
        for increment in range(8):
            destination_squares.append((self.rank + increment, self.file + increment))
            destination_squares.append((self.rank + increment, self.file - increment))
            destination_squares.append((self.rank - increment, self.file + increment))
            destination_squares.append((self.rank - increment, self.file - increment))
        # Then we remove all squares out of bounds of the board
        destination_squares = self.check_square_bounds(destination_squares)
        return destination_squares

class Rook(Piece):
    def __init__(self, rank, file, color):
        self.piece_id = ChessPieces.ROOK
        super(Rook, self).__init__(rank, file, self.piece_id, color)

    def get_possible_moves(self):
        destination_squares = []
        # We find all squares horizontally and vertically aligned with the rook within the width of the board
        # (8 squares)
        for new_rank in range(8):
            for new_file in range(8):
                destination_squares.append((self.rank + new_rank, self.file))
                destination_squares.append((self.rank - new_rank, self.file))
                destination_squares.append((self.rank, self.file + new_file))
                destination_squares.append((self.rank, self.file - new_file))
        # Then we remove all squares out of bounds of the board
        destination_squares = self.check_square_bounds(destination_squares)
        return destination_squares

class Queen(Piece):
    def __init__(self, rank, file, color):
        self.piece_id = ChessPieces.QUEEN
        super(Queen, self).__init__(rank, file, self.piece_id, color)

    def get_possible_moves(self):
        destination_squares = []
        # We find all squares vertically, horizontally, and diagonally aligned with the Queen within the width of the
        # board (8 squares)
        for increment in range(8):
            destination_squares.append((self.rank + increment, self.file + increment))
            destination_squares.append((self.rank + increment, self.file - increment))
            destination_squares.append((self.rank - increment, self.file + increment))
            destination_squares.append((self.rank - increment, self.file - increment))
            destination_squares.append((self.rank + increment, self.file))
            destination_squares.append((self.rank - increment, self.file))
            destination_squares.append((self.rank, self.file + increment))
            destination_squares.append((self.rank, self.file - increment))
        # Then we remove all squares out of bounds of the board
        destination_squares = self.check_square_bounds(destination_squares)
        return destination_squares

class King(Piece):
    def __init__(self, rank, file, color):
        self.piece_id = ChessPieces.KING
        super(King, self).__init__(rank, file, self.piece_id, color)

    def get_possible_moves(self):
        # This list contains all squares of distance 1 away from the king
        destination_squares = [(self.rank + 1, self.file), (self.rank + 1, self.file),
                     (self.rank, self.file + 1), (self.rank, self.file - 1),
                     (self.rank - 1, self.file + 1), (self.rank - 1, self.file - 1),
                     (self.rank + 1, self.file + 1), (self.rank + 1, self.file - 1)]
        # Then we remove all squares from the list that are out of bounds
        destination_squares = self.check_square_bounds(destination_squares)
        return destination_squares