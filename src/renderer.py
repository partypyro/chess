from src.board_renderer import ChessBoardRenderer
from src.piece import Piece
import pyglet

class Renderer(pyglet.window.Window):
    def __init__(self, x=0, y=0, width=800, height=800):
        super(Renderer, self).__init__(width, height)

        # Create the chess board object that will store the game information
        self.chess_board = ChessBoardRenderer(x, y, 800, 800)

        # Start the application
        pyglet.app.run()

    # Main rendering loop
    def on_draw(self):
        self.clear()
        self.chess_board.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if not self.chess_board.is_selected():
            self.chess_board.select_piece_at(x, y)
        else:
            move = self.chess_board.xy_to_rank_file(x, y)
            dest_sprite, dest_piece = self.chess_board.find_piece_at(x, y)
            if dest_piece is None:
                if not self.chess_board.make_legal_move(self.chess_board.selected_piece, move):
                    self.chess_board.select_piece_at(x, y)
            elif dest_piece.color == self.chess_board.board.player_turn:
                self.chess_board.select_piece_at(x, y)
            elif dest_piece != self.chess_board.selected_piece:
                self.chess_board.make_legal_move(self.chess_board.selected_piece, move)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        # If we have picked up a piece, we need to draw that piece at the current cursor postion
        if self.chess_board.is_selected():
            self.chess_board.update_selected(x, y)

    def on_mouse_release(self, x, y, button, modifiers):
        # Drop the piece back the original position
        if self.chess_board.is_selected():
            self.chess_board.update_selected(x, y)
            move = self.chess_board.xy_to_rank_file(x, y)
            if not self.chess_board.make_legal_move(self.chess_board.selected_piece, move):
                self.chess_board.reset_selected()