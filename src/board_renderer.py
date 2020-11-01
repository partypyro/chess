import pyglet
from pyglet.shapes import Rectangle, Circle
from pyglet.sprite import Sprite

import src.constants
from src.board import ChessBoard
from src.piece import Queen, Rook, Knight, Bishop, King, Pawn


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
        self.selected_piece_batch = pyglet.graphics.Batch()
        self.selected_piece_moves = []
        self.selected_offset = 0, 0
        self.selected_sprite = None
        self.selected_piece = None

        # Vars to help with displaying game result
        self.game_result_message = None
        self.game_result_batch = pyglet.graphics.Batch()

        # Vars to help with pawn promotion
        self.is_promoting = False
        self.promotion_menu_pos = (0, 0)
        self.pawn_promotion = []
        self.pawn_promotion_batch = pyglet.graphics.Batch()

    def draw(self):
        self.tile_batch.draw()
        self.selected_piece_batch.draw()
        self.pieces_batch.draw()
        self.game_result_batch.draw()
        if self.is_promoting:
            self.pawn_promotion_batch.draw()

    def update(self):
        # We don't need to re-render the tiles as they are static
        self.render_pieces()
        self.render_selected_piece_moves()
        self.render_checked_king()
        if self.board.is_gameover:
            self.render_gameover_message()
        if self.is_promoting:
            self.render_pawn_promotion()

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
            self.selected_piece_moves = []
            # Get all the possible moves of the piece
            legal_moves = self.selected_piece.get_legal_moves(self.board)
            for (rank, file) in legal_moves:
                square = self.board.look_at(rank, file)
                # Center the xy-coords in the center of the tile
                if square is None:
                    circ = Circle(
                        x=self.board_x + (file * self.tile_width) + (self.tile_width * 0.5),
                        y=self.board_y + (rank * self.tile_height) + (self.tile_height * 0.5),
                        radius=self.tile_width * .25,
                        color=(100,100,100),
                        batch=self.selected_piece_batch
                    )
                    self.selected_piece_moves.append(circ)
                # If there is an enemy piece on the square we can move to, draw a red circle
                elif square is not None:
                    if square.color is not self.board.player_turn:
                        circ = Circle(
                            x=self.board_x + (file * self.tile_width) + (self.tile_width * 0.5),
                            y=self.board_y + (rank * self.tile_height) + (self.tile_height * 0.5),
                            radius=self.tile_width * .4,
                            color=(255, 0, 0),
                            batch=self.selected_piece_batch
                        )
                        self.selected_piece_moves.append(circ)
        else:
            self.selected_piece_moves = []
            self.selected_piece_batch = pyglet.graphics.Batch()

    def render_checked_king(self):
        # Find the white king and black king and see if either is in check
        for king in self.board.pieces:
            if king.id == src.constants.KING and self.board.is_in_check(king.color):
                circ = Circle(
                    x=self.board_x + (king.file * self.tile_width) + (self.tile_width * 0.5),
                    y=self.board_y + (king.rank * self.tile_height) + (self.tile_height * 0.5),
                    radius=self.tile_width * .4,
                    color=(255, 0, 0),
                    batch=self.selected_piece_batch
                )
                self.selected_piece_moves.append(circ)

    def render_gameover_message(self):
        if self.board.is_gameover:
            if self.board.game_result == 'WHITE':
                self.game_result_message = pyglet.text.Label(
                    'WHITE WINS',
                    font_name='Times New Roman',
                    font_size=src.constants.WINNER_TEXT_SIZE,
                    x=self.board_x + (self.board_width // 2),
                    y=self.board_y + (self.board_height // 2),
                    anchor_x='center', anchor_y='center',
                    batch=self.game_result_batch
                )
            elif self.board.game_result == 'BLACK':
                self.game_result_message = pyglet.text.Label(
                    'BLACK WINS',
                    font_name='Times New Roman',
                    font_size=src.constants.WINNER_TEXT_SIZE,
                    x=self.board_x + (self.board_width // 2),
                    y=self.board_y + (self.board_height // 2),
                    anchor_x='center', anchor_y='center',
                    batch=self.game_result_batch,
                    color=(0,0,0,255)
                )
            elif self.board.game_result == 'DRAW':
                self.game_result_message = pyglet.text.Label(
                    'DRAW',
                    font_name='Times New Roman',
                    font_size=src.constants.WINNER_TEXT_SIZE,
                    x=self.board_x + (self.board_width // 2),
                    y=self.board_y + (self.board_height // 2),
                    anchor_x='center', anchor_y='center',
                    batch=self.game_result_batch,
                    color=(127,127,127,255)
                )

    # Render the pawn promotion prompt
    def render_pawn_promotion(self):
        promoted_piece = self.board.get_promoting_piece()
        if promoted_piece is not None:
            self.pawn_promotion = []
            background = pyglet.graphics.OrderedGroup(0)
            foreground = pyglet.graphics.OrderedGroup(1)
            rank, file = promoted_piece.rank, promoted_piece.file
            x, y = self.rank_file_to_xy(rank, file)
            self.promotion_menu_pos = x, y
            # Draw the four possible piece promotions at 1/4 the scale of each piece
            queen_image = src.constants.get_image(Queen(0, 0, promoted_piece.color))
            queen = Sprite(queen_image, x=x, y=y, batch=self.pawn_promotion_batch, group=foreground)
            queen.scale = (0.5 * self.tile_width) / queen_image.width
            self.pawn_promotion.append(queen)
            rook_image = src.constants.get_image(Rook(0, 0, promoted_piece.color))
            rook = Sprite(rook_image, x=x + (0.5 * self.tile_width), y=y,
                          batch=self.pawn_promotion_batch, group=background)
            rook.scale = (0.5 * self.tile_width) / rook_image.width
            self.pawn_promotion.append(rook)
            knight_image = src.constants.get_image(Knight(0, 0, promoted_piece.color))
            knight = Sprite(knight_image, x=x, y=y + (0.5 * self.tile_width),
                            batch=self.pawn_promotion_batch, group=foreground)
            knight.scale = (0.5 * self.tile_width) / knight_image.width
            self.pawn_promotion.append(knight)
            bishop_image = src.constants.get_image(Bishop(0, 0, promoted_piece.color))
            bishop = Sprite(bishop_image, x=x + (0.5 * self.tile_width) , y=y + (0.5 * self.tile_width),
                            batch=self.pawn_promotion_batch, group=foreground)
            bishop.scale = (0.5 * self.tile_width) / bishop_image.width
            self.pawn_promotion.append(bishop)
            # Draw a grey box on the square as a background for the promotion menu
            rect = Rectangle(
                x=x, y=y,
                width=self.tile_width, height=self.tile_height,
                color=(127, 127, 127),
                batch=self.pawn_promotion_batch,
                group=background
            )
            self.pawn_promotion.append(rect)

    # Based on the xy coords, get the piece/sprite at that location
    def select_piece_at(self, x, y):
        sprite, piece = self.find_piece_at(x, y)
        if piece is not None and not self.board.is_gameover and not self.is_promoting:
            if piece.color == self.board.player_turn:
                self.selected_sprite, self.selected_piece = sprite, piece
                self.render_selected_piece_moves()
                self.render_checked_king()
        elif self.is_promoting:
            self.get_promotion_selection(x, y)
            self.update()

    def find_piece_at(self, x, y):
        for sprite in self.piece_sprites:
            # Check to see if the selection overlaps with one of the pieces on the board
            if sprite.x <= x <= sprite.x + sprite.width:
                if sprite.y <= y <= sprite.y + sprite.height:
                    rank, file = self.xy_to_rank_file(sprite.x, sprite.y)
                    piece = self.board.look_at(rank, file)
                    # Figure out how far to offset the piece sprite from the mouse, so that it aligns with where the player
                    # originally clicked the piece
                    x = x - sprite.x
                    y = y - sprite.y
                    self.selected_offset = x, y
                    return sprite, piece
        return None, None

    def get_promotion_selection(self, x, y):
        menu_x, menu_y = self.promotion_menu_pos
        piece = self.board.get_promoting_piece()
        selection = None
        if menu_x <= x <= menu_x + (self.tile_width * 0.5):
            if menu_y <= y <= menu_y + (self.tile_width * 0.5):
                selection = Queen
        if menu_x + (self.tile_width * 0.5) <= x <= menu_x + self.tile_width:
            if menu_y <= y <= menu_y + (self.tile_width * 0.5):
                selection = Rook
        if menu_x <= x <= menu_x + (self.tile_width * 0.5):
            if menu_y + (self.tile_width * 0.5) <= y <= menu_y + self.tile_width:
                selection = Knight
        if menu_x + (self.tile_width * 0.5) <= x <= menu_x + self.tile_width:
            if menu_y + (self.tile_width * 0.5) <= y <= menu_y + self.tile_width:
                selection = Bishop
        if selection is not None:
            self.board.promote_pawn(piece, selection)
            self.is_promoting = False
            self.pawn_promotion = []

    def make_legal_move(self, piece, move):
        # TODO: Move most of logic to actual board class
        legal_moves = piece.get_legal_moves(self.board)
        if move in legal_moves:
            self.selected_piece, self.selected_sprite = None, None
            success = self.board.move(piece, move)
            self.update()
            # Check if a pawn promotion is available after the move is made
            if self.board.can_promote():
                self.is_promoting = True
                self.render_pawn_promotion()
            return success
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