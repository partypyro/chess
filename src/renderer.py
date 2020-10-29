from src.board import ChessBoard, ChessPieces
import pyglet
from pyglet.shapes import Rectangle, Circle

class Renderer(pyglet.window.Window):
    def __init__(self, x=0, y=0, width=800, height=800):
        super(Renderer, self).__init__(width, height)
        # Set up the location and size of our game board
        self.board_x = x
        self.board_y = y
        self.board_width = width
        self.board_height = height

        # Set up the width and height of our board tiles
        self.tile_width = self.board_width // 8
        self.tile_height = self.board_height // 8
        # Create a rendering batch to store the tile primitives and list to store the tiles
        self.tile_batch = pyglet.graphics.Batch()
        self.tile_list = []
        # Render the tiles into the batch
        self.render_tiles()

        # Define a dictionary to reference our image assets from
        self.image_dict = {}
        # Load the image assets into our dictionary
        self.piece_scale = 0
        self.load_image_assets()
        # Start the application

        # Create the chess board object that will store the game information
        self.chess_board = ChessBoard()
        self.selected_piece_moves_list = []
        self.selected_piece_moves = pyglet.graphics.Batch()
        self.selected_piece_offset = 0, 0
        self.selected_piece = None
        self.selected_sprite = None

        # Create our batch to draw our piece sprites from and a list to reference the piece sprites
        self.pieces_batch = pyglet.graphics.Batch()
        self.piece_sprites = []
        self.render_pieces()

        pyglet.app.run()

    def load_image_assets(self):
        # Load each piece image and label it according to its color and piece type
        self.image_dict[(ChessPieces.WHITE, ChessPieces.PAWN)] =   pyglet.image.load('../assets/white_pawn.png')
        self.image_dict[(ChessPieces.WHITE, ChessPieces.KNIGHT)] = pyglet.image.load('../assets/white_knight.png')
        self.image_dict[(ChessPieces.WHITE, ChessPieces.BISHOP)] = pyglet.image.load('../assets/white_bishop.png')
        self.image_dict[(ChessPieces.WHITE, ChessPieces.ROOK)] =   pyglet.image.load('../assets/white_rook.png')
        self.image_dict[(ChessPieces.WHITE, ChessPieces.QUEEN)] =  pyglet.image.load('../assets/white_queen.png')
        self.image_dict[(ChessPieces.WHITE, ChessPieces.KING)] =   pyglet.image.load('../assets/white_king.png')
        self.image_dict[(ChessPieces.BLACK, ChessPieces.PAWN)] =   pyglet.image.load('../assets/black_pawn.png')
        self.image_dict[(ChessPieces.BLACK, ChessPieces.KNIGHT)] = pyglet.image.load('../assets/black_knight.png')
        self.image_dict[(ChessPieces.BLACK, ChessPieces.BISHOP)] = pyglet.image.load('../assets/black_bishop.png')
        self.image_dict[(ChessPieces.BLACK, ChessPieces.ROOK)] =   pyglet.image.load('../assets/black_rook.png')
        self.image_dict[(ChessPieces.BLACK, ChessPieces.QUEEN)] =  pyglet.image.load('../assets/black_queen.png')
        self.image_dict[(ChessPieces.BLACK, ChessPieces.KING)] =   pyglet.image.load('../assets/black_king.png')

        # Figure how large we should scale each asset
        reference_image = pyglet.image.load('../assets/black_king.png')
        width = reference_image.width
        self.piece_scale = self.tile_width / width

    def render_pieces(self):
        # CLear the list of sprites
        self.piece_sprites = []
        # Iterate through the chess board
        for piece in self.chess_board.get_all_pieces():
            piece_sprite = pyglet.sprite.Sprite(
                self.image_dict[(piece.color, piece.piece_id)],
                x=self.board_x + (piece.file * self.tile_width),
                y=self.board_y + (piece.rank * self.tile_height),
                batch=self.pieces_batch
            )
            # Scale the piece to the appropriate size
            piece_sprite.scale = self.piece_scale
            # Add it to the global list of piece sprites so we can reference it later
            self.piece_sprites.append(piece_sprite)

    def render_tiles(self):
        light_square = (0, 122, 4)
        dark_square = (128, 255, 132)
        # Size each square to an eigth of the size of the board
        alternating_count = 0
        # Create a 2D array of rectangles to represent the squares on the board
        for rank in range(9):
            for file in range(9):
                rect = Rectangle(
                    x=self.board_x + (file * self.tile_width),
                    y=self.board_y + (rank * self.tile_height),
                    width=self.tile_width, height=self.tile_height,
                    color = dark_square if alternating_count % 2 == 0 else light_square,
                    batch=self.tile_batch
                )
                alternating_count += 1
                self.tile_list.append(rect)

    def get_clicked_piece(self, x, y):
        file = (x - self.board_x) // self.tile_width
        rank = (y - self.board_y) // self.tile_height
        for sprite in self.piece_sprites:
            if sprite.x <= x <= sprite.x + sprite.width:
                if sprite.y <= y <= sprite.y + sprite.height:
                    return sprite, rank, file
        return None, rank, file

    def render_selected_piece_moves(self):
        self.selected_piece_moves_list = []
        possible_moves = self.selected_piece.get_possible_moves()
        print(possible_moves)
        for move in possible_moves:
            rank, file = move
            if self.chess_board.check_square(rank, file) is None:
                circ = Circle(
                    x=self.board_x + (file * self.tile_width) + (self.tile_width * 0.5),
                    y=self.board_y + (rank * self.tile_height) + (self.tile_height * 0.5),
                    radius=self.tile_width * .25,
                    color=(100,100,100),
                    batch=self.selected_piece_moves
                )
                self.selected_piece_moves_list.append(circ)

    def on_mouse_press(self, x, y, button, modifiers):
        sprite, rank, file = self.get_clicked_piece(x, y)
        self.selected_sprite = sprite
        self.selected_piece = self.chess_board.check_square(rank, file)

        # Figure out how far to offset the piece sprite from the mouse, so that it aligns with where the player
        # originally clicked the piece
        if self.selected_piece is not None:
            x = x - self.selected_sprite.x
            y = y - self.selected_sprite.y
            self.selected_piece_offset = x, y
            self.render_selected_piece_moves()

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.selected_piece is not None:
             self.selected_sprite.update(x=x - self.selected_piece_offset[0],
                                         y=y - self.selected_piece_offset[1])

    def on_mouse_release(self, x, y, button, modifiers):
        if self.selected_piece is not None:
            self.selected_sprite.update(
                x=self.board_x + (self.selected_piece.file * self.tile_width),
                y=self.board_y + (self.selected_piece.rank * self.tile_height)
            )

    def on_draw(self):
        self.clear()
        self.tile_batch.draw()
        self.selected_piece_moves.draw()
        self.pieces_batch.draw()