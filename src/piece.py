import src.constants

# Parent class for all pieces - basic functions to get possible moves, move the piece, and check if a square is in the
# bounds of the board
class Piece:
    def __init__(self, rank, file, piece_id, color):
        self.rank, self.file = rank, file
        self.id = piece_id
        self.color = color
        self.capturable = True
        self.can_castle = False

    # This function represents the possible squares that a piece can go to, given no obstacles on infinite
    def get_possible_moves(self, board):
        return []

    def get_legal_moves(self, board):
        moves = self.get_possible_moves(board)
        # For every vector in the list of possible moves, remove every square out of bounds
        for i, vector in enumerate(moves):
            moves[i] = self.remove_out_of_bounds(vector)
        # Remove all the blocked squares from the list
        self.remove_illegal_moves(moves, board)
        # Take the list of move vectors and convert it into a single concatenated list of moves
        moves = sum(moves, [])
        # Finally, see if our color is in check and if any of the moves gets us out of check
        self.remove_check_moves(moves, board)
        # Append every move vector into a single list of possible moves
        return moves

    # This function evaluates a list of moves and returns a modified list with only the moves that are within the bounds
    # of the board
    def remove_out_of_bounds(self, square_list):
        for (rank, file) in square_list:
            if rank < 0 or rank > 7 or file < 0 or file > 7:
                square_list.remove((rank, file))
        return square_list

    def remove_check_moves(self, moves, board):
        if not board.is_branch:
            # Simulate the move and see if it puts the king in check
            for move in moves.copy():
                if board.branch(self, move).is_in_check(self.color):
                    moves.remove(move)

    # This function evaluates a list of move vectors, or lists of moves, and evaluates if there is a obstacle in the way
    # of that piece continuing its path
    def remove_illegal_moves(self, vector_list, board):
        for i, vector in enumerate(vector_list):
            vector_list[i] = self.remove_out_of_bounds(vector)
            is_blocked = False
            for (rank, file) in vector.copy():
                square = board.look_at(rank, file)
                # If the square was blocked by one of the previous squares in the vector, remove it from the vector
                if is_blocked:
                    vector.remove((rank, file))
                # Otherwise, if the square was filled with a piece
                elif square is not None:
                    # If the square is filled with a piece of the same color as the selected piece's color, every piece
                    # later in the vector will be blocked
                    if square.color == self.color:
                        vector.remove((rank, file))
                        is_blocked = True
                    # Otherwise, if the square has a piece of the opposite color, all remaining squares are blocked, but
                    # the move is kept as a capturing move
                    else:
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
            if board.look_at(self.rank + 1, self.file) is None:
                destination_squares.append((self.rank + 1, self.file))
                # If the pawn is on the 2nd self.rank, it can move 2 squares
                if self.rank == 1:
                    if board.look_at(self.rank + 2, self.file) is None:
                        destination_squares.append((self.rank + 2, self.file))
            # If there is a black piece to the left or right of the pawn, it can capture
            square = board.look_at(self.rank + 1, self.file + 1)
            if square is not None and square.capturable and square.color == src.constants.BLACK:
                destination_squares.append((self.rank + 1, self.file + 1))
            square = board.look_at(self.rank + 1, self.file - 1)
            if square is not None and square.capturable and square.color == src.constants.BLACK:
                destination_squares.append((self.rank + 1, self.file - 1))

        elif self.color == src.constants.BLACK:
            # Black pawn can move down one square
            if board.look_at(self.rank - 1, self.file) is None:
                destination_squares.append((self.rank - 1, self.file))
                # If the pawn is on the 2nd self.rank, it can move 2 squares
                if self.rank == 6:
                    if board.look_at(self.rank - 2, self.file) is None:
                        destination_squares.append((self.rank - 2, self.file))
            # If there is a black piece to the left or right of the pawn, it can capture
            square = board.look_at(self.rank - 1, self.file + 1)
            if square is not None and square.capturable and square.color == src.constants.WHITE:
                destination_squares.append((self.rank - 1, self.file + 1))
            square = board.look_at(self.rank - 1, self.file - 1)
            if square is not None and square.capturable and square.color == src.constants.WHITE:
                destination_squares.append((self.rank - 1, self.file - 1))

        # Before we return the list of pawn moves, check which moves are out of bounds
        destination_squares = self.remove_out_of_bounds(destination_squares)
        return destination_squares

    def get_legal_moves(self, board):
        moves = self.get_possible_moves(board)
        self.remove_out_of_bounds(moves)
        # Remove any moves that would put us in check
        self.remove_check_moves(moves, board)
        return moves

class Knight(Piece):
    def __init__(self, rank, file, color):
        self.piece_id = src.constants.KNIGHT
        super(Knight, self).__init__(rank, file, self.piece_id, color)

    # This function returns the valid knight moves from a given square on the board
    def get_possible_moves(self, board):
        # Find all 8 knight moves of +/- 1/2 ranks and +/- 2/1 files
        destination_squares = [
            (self.rank + 2, self.file + 1), (self.rank + 2, self.file - 1),
            (self.rank - 2, self.file + 1), (self.rank - 2, self.file - 1),
            (self.rank - 1, self.file + 2), (self.rank - 1, self.file - 2),
            (self.rank + 1, self.file + 2), (self.rank + 1, self.file - 2)
        ]
        return destination_squares

    def get_legal_moves(self, board):
        moves = self.get_possible_moves(board)
        self.remove_out_of_bounds(moves)
        for move in moves.copy():
            rank, file = move
            square = board.look_at(rank, file)
            if square is not None and square.color == self.color:
                moves.remove(move)
        # Remove any moves that would put us in check
        self.remove_check_moves(moves, board)
        return moves

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
        self.can_castle = True

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
        self.capturable = False
        self.can_castle = True

    def get_possible_moves(self, board):
        # This list contains all squares of distance 1 away from the king
        destination_squares = [
             (self.rank + 1, self.file), (self.rank - 1, self.file),
             (self.rank, self.file + 1), (self.rank, self.file - 1),
             (self.rank - 1, self.file + 1), (self.rank - 1, self.file - 1),
             (self.rank + 1, self.file + 1), (self.rank + 1, self.file - 1)
        ]
        return destination_squares

    def get_legal_moves(self, board):
        moves = self.get_possible_moves(board)
        # Remove all moves that are out of bounds
        self.remove_out_of_bounds(moves)
        # Remove all moves with the pieces of the same color in the destination square
        for (rank, file) in moves.copy():
            dest_square = board.look_at(rank, file)
            if dest_square is not None:
                if dest_square.color == self.color:
                    moves.remove((rank, file))
        if self.can_castle:
            moves += self.get_castle_moves(board)
        # Remove any moves that would put us in check
        self.remove_check_moves(moves, board)
        return moves

    def get_castle_moves(self, board):
        # Figure out if we can castle - we need to be on the back rank for our color
        castle_moves = []
        if self.color == src.constants.WHITE and self.rank == 0:
            # See which rooks are available for castling
            l_rook = board.look_at(0, 0)
            r_rook = board.look_at(0, 7)
            if l_rook is not None and l_rook.can_castle:
                # Check if any pieces are in the way of the left rook
                squares_to_check = [(0, 1), (0, 2), (0, 3)]
                is_blocked = False
                for (rank, file) in squares_to_check:
                    if board.look_at(rank, file) is not None:
                        is_blocked = True
                if not is_blocked:
                    castle_moves.append((0, 2))
            if r_rook is not None and r_rook.can_castle:
                # Check if any pieces are in the way of the right rook
                squares_to_check = [(0, 5), (0, 6)]
                is_blocked = False
                for (rank, file) in squares_to_check:
                    if board.look_at(rank, file) is not None:
                        is_blocked = True
                if not is_blocked:
                    castle_moves.append((0, 6))
        elif self.color == src.constants.BLACK and self.rank == 7:
            # See which rooks are available for castling
            l_rook = board.look_at(7, 0)
            r_rook = board.look_at(7, 7)
            if l_rook is not None and l_rook.can_castle:
                # Check if any pieces are in the way of the left rook
                squares_to_check = [(7, 1), (7, 2), (7, 3)]
                is_blocked = False
                for (rank, file) in squares_to_check:
                    if board.look_at(rank, file) is not None:
                        is_blocked = True
                if not is_blocked:
                    castle_moves.append((7, 2))
            if r_rook is not None and r_rook.can_castle:
                # Check if any pieces are in the way of the right rook
                squares_to_check = [(7, 5), (7, 6)]
                is_blocked = False
                for (rank, file) in squares_to_check:
                    if board.look_at(rank, file) is not None:
                        is_blocked = True
                if not is_blocked:
                    castle_moves.append((7, 6))
        return castle_moves

    def castle(self, board, move):
        # Check if left castle or right castle:
        rank, file = move
        if (file - self.file) > 0:
            r_rook = board.look_at(self.rank, self.file + 3)
            r_rook.file = file - 1
            self.file = file
        else:
            l_rook = board.look_at(self.rank, self.file - 4)
            l_rook.file = file + 1
            self.file = file