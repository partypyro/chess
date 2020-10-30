import pyglet
from pyglet.shapes import Rectangle, Circle
from pyglet.sprite import Sprite

import src.constants
from src.board import ChessBoard

class ChessBoardRenderer:
    def __init__(self, x, y, width, height):
        self.board = ChessBoard()
        # Set up the location and size of our game board
        self.board_x = x
        self.board_y = y
        self.board_width = width
        self.board_height = height

        # Set up the width and height of our board tiles
        self.tile_width = self.board_width // 8
        self.tile_height = self.board_height // 8
        # Create a list to store the board tiles and a batch for the tile geometries
        self.tile_batch = pyglet.graphics.Batch()
        self.tile_list = []
        # Render the tiles into the batch
        self.render_tiles()

        # Create our batch to draw our piece sprites from and a list to reference the piece sprites
        self.pieces_batch = pyglet.graphics.Batch()
        self.piece_sprites = []
        self.piece_scale = self.tile_width / width
        self.render_pieces()

        # Vars to help with which piece is selected on the screen
        self.selected_piece_moves = pyglet.graphics.Batch()
        self.selected_piece_moves_list = []
        self.selected_offset = 0, 0
        self.selected_sprite = None
        self.selected_piece = None

    def draw(self):
        self.tile_batch.draw()
        self.selected_piece_moves.draw()
        self.pieces_batch.draw()

    def update(self):
        # We don't need to re-render the tiles as they are static
        self.render_pieces()
        self.render_selected_piece_moves()

    def render_tiles(self):
        # The colors of each square
        light_square = (0, 122, 4)
        dark_square = (128, 255, 132)
        alternating_count = 0
        # Create a 2D array of rectangles to represent the squares on the board
        for rank in range(9):
            for file in range(9):
                # Generate a tile
                x, y = self.rank_file_to_xy(rank, file)
                rect = Rectangle(
                    x=x, y=y,
                    width=self.tile_width, height=self.tile_height,
                    # Use alternating_count to keep track of tile colorx
                    color=dark_square if alternating_count % 2 == 0 else light_square,
                    batch=self.tile_batch
                )
                alternating_count += 1
                self.tile_list.append(rect)

    def render_pieces(self):
        # CLear the list of sprites
        self.piece_sprites = []
        # Iterate through all pieces on the board and couple a sprite with each piece
        for piece in self.board.pieces:
            x, y = self.rank_file_to_xy(piece.rank, piece.file)
            image = src.constants.get_image(piece)
            piece_sprite = Sprite(image, x=x, y=y, batch = self.pieces_batch)
            piece_sprite.scale = self.tile_width / image.width
            self.piece_sprites.append(piece_sprite)

    def render_selected_piece_moves(self):
        if self.selected_sprite is not None:
            # Clear the list of possible move markers
            self.selected_piece_moves_list = []
            # Get all the possible moves of the piece
            legal_moves = self.selected_piece.get_legal_moves(self.board)
            for move in legal_moves:
                rank, file = move
                square = self.board.check_square(rank, file)
                # Center the xy-coords in the center of the tile
                if square is None:
                    circ = Circle(
                        x=self.board_x + (file * self.tile_width) + (self.tile_width * 0.5),
                        y=self.board_y + (rank * self.tile_height) + (self.tile_height * 0.5),
                        radius=self.tile_width * .25,
                        color=(100,100,100),
                        batch=self.selected_piece_moves
                    )
                    self.selected_piece_moves_list.append(circ)
                # If there is an enemy piece on the square we can move to, draw a red circle
                elif square is not None:
                    if square.color is not self.board.player_turn:
                        circ = Circle(
                            x=self.board_x + (file * self.tile_width) + (self.tile_width * 0.5),
                            y=self.board_y + (rank * self.tile_height) + (self.tile_height * 0.5),
                            radius=self.tile_width * .4,
                            color=(255, 0, 0),
                            batch=self.selected_piece_moves
                        )
                        self.selected_piece_moves_list.append(circ)
        else:
            self.selected_piece_moves_list = []
            self.selected_piece_moves = pyglet.graphics.Batch()

    # Based on the xy coords, get the piece/sprite at that location
    def select_piece_at(self, x, y):
        sprite, piece = self.find_piece_at(x, y)
        if piece is not None:
            if piece.color == self.board.player_turn:
                self.selected_sprite, self.selected_piece = sprite, piece
                self.render_selected_piece_moves()

    def find_piece_at(self, x, y):
        for sprite in self.piece_sprites:
            # Check to see if the selection overlaps with one of the pieces on the board
            if sprite.x <= x <= sprite.x + sprite.width:
                if sprite.y <= y <= sprite.y + sprite.height:
                    rank, file = self.xy_to_rank_file(sprite.x, sprite.y)
                    piece = self.board.check_square(rank, file)
                    # Figure out how far to offset the piece sprite from the mouse, so that it aligns with where the player
                    # originally clicked the piece
                    x = x - sprite.x
                    y = y - sprite.y
                    self.selected_offset = x, y
                    return sprite, piece
        return None, None

    def make_legal_move(self, piece, move):
        legal_moves = piece.get_legal_moves(self.board)
        if move in legal_moves:
            self.selected_piece, self.selected_sprite = None, None
            self.board.move(piece, move)
            self.update()
            return True
        return False

    def is_selected(self):
        return True if self.selected_sprite is not None else False

    def update_selected(self, x, y):
        self.selected_sprite.update(
            x=x-self.selected_offset[0],
            y=y-self.selected_offset[1]
        )

    def reset_selected(self):
        self.selected_offset = 0, 0
        x, y = self.rank_file_to_xy(self.selected_piece.rank, self.selected_piece.file)
        self.update_selected(x, y)

    def xy_to_rank_file(self, x, y):
        rank = (y - self.board_y) // self.tile_height
        file = (x - self.board_x) // self.tile_width
        return rank, file

    def rank_file_to_xy(self, rank, file):
        x = self.board_x + (file * self.tile_width)
        y = self.board_y + (rank * self.tile_height)
        return int(x), int(y)
