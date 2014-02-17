import pyglet
from pyglet import gl

window = pyglet.window.Window()

class Raketa(object):
    def nakresli(self):
        gl.glLoadIdentity()
        gl.glPushMatrix()
        gl.glTranslatef(self.x, self.y, 0)
        gl.glRotatef(self.rotace * 100, 0, 0, 1)
        gl.glBegin(gl.GL_TRIANGLE_FAN)
        gl.glVertex2f(-20, -20)
        gl.glVertex2f(0, 20)
        gl.glVertex2f(20, -20)
        gl.glEnd()
        gl.glPopMatrix()

    def posun(self, dt):
        self.x += self.rychlost_x * dt
        self.y += self.rychlost_y * dt

raketa = Raketa()
raketa.x = 100
raketa.y = 100
raketa.rychlost_x = 0
raketa.rychlost_y = 10
raketa.rotace = 0

def vykresli():
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    gl.glColor3f(1, 1, 1)
    raketa.nakresli()

def update(dt):
    raketa.posun(dt)

window.push_handlers(on_draw=vykresli)
pyglet.clock.schedule(update)

pyglet.app.run()
