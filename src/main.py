import pyglet

width, height = 1200, 1200

window = pyglet.window.Window()
window.set_size(width=width, height=height)

@window.event
def on_draw():
    window.clear()


pyglet.app.run()