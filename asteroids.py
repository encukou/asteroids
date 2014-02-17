import pyglet
from pyglet import gl

window = pyglet.window.Window()

def vykresli():
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    nakresli_obdelnik(10, 10, 100, 100)

def nakresli_obdelnik(x1, y1, x2, y2):
    gl.glBegin(gl.GL_TRIANGLE_FAN)
    gl.glVertex2f(int(x1), int(y1))
    gl.glVertex2f(int(x1), int(y2))
    gl.glVertex2f(int(x2), int(y2))
    gl.glVertex2f(int(x2), int(y1))
    gl.glEnd()

window.push_handlers(
    on_draw=vykresli,
)

pyglet.app.run()
