import pyglet.image

NONE = 0

PAWN = 1
KNIGHT = 2
BISHOP = 3
ROOK = 4
QUEEN = 5
KING = 6

WHITE = 1
BLACK = 2
image_dict = {}

def initialize():
    image_dict[(WHITE, PAWN)] = pyglet.image.load('../assets/white_pawn.png')
    image_dict[(WHITE, KNIGHT)] = pyglet.image.load('../assets/white_knight.png')
    image_dict[(WHITE, BISHOP)] = pyglet.image.load('../assets/white_bishop.png')
    image_dict[(WHITE, ROOK)] = pyglet.image.load('../assets/white_rook.png')
    image_dict[(WHITE, QUEEN)] = pyglet.image.load('../assets/white_queen.png')
    image_dict[(WHITE, KING)] = pyglet.image.load('../assets/white_king.png')
    image_dict[(BLACK, PAWN)] = pyglet.image.load('../assets/black_pawn.png')
    image_dict[(BLACK, KNIGHT)] = pyglet.image.load('../assets/black_knight.png')
    image_dict[(BLACK, BISHOP)] = pyglet.image.load('../assets/black_bishop.png')
    image_dict[(BLACK, ROOK)] = pyglet.image.load('../assets/black_rook.png')
    image_dict[(BLACK, QUEEN)] = pyglet.image.load('../assets/black_queen.png')
    image_dict[(BLACK, KING)] = pyglet.image.load('../assets/black_king.png')

def get_image(piece):
    key = (piece.color, piece.piece_id)
    return image_dict[key]