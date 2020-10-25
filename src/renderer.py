import pyglet

class Renderer:
    board_x = 0
    board_y = 0
    board_width = 800
    board_height = 800

    def __init__(self, window, x, y, width, height):
        self.window =