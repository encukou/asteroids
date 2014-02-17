import math

import pyglet
from pyglet import gl
from pyglet.window import key

window = pyglet.window.Window()

class Raketa(object):
    def nakresli(self):
        gl.glLoadIdentity()
        gl.glPushMatrix()
        gl.glTranslatef(self.x, self.y, 0)
        gl.glRotatef(self.rotace, 0, 0, 1)
        gl.glBegin(gl.GL_TRIANGLE_FAN)
        gl.glVertex2f(-20, 10)
        gl.glVertex2f(20, 0)
        gl.glVertex2f(-20, -10)
        gl.glEnd()
        gl.glPopMatrix()

    def posun(self, dt):
        self.x += self.rychlost_x * dt
        self.y += self.rychlost_y * dt
        uhel = self.rotace * math.pi / 180
        if key.LEFT in klavesy:
            self.rotace += dt * 200
        if key.RIGHT in klavesy:
            self.rotace -= dt * 200
        if key.UP in klavesy:
            self.rychlost_x += dt * 100 * math.cos(uhel)
            self.rychlost_y += dt * 100 * math.sin(uhel)
        if key.DOWN in klavesy:
            self.rychlost_x -= dt * 100 * math.cos(uhel)
            self.rychlost_y -= dt * 100 * math.sin(uhel)
        if self.x > window.width:
            self.x -= window.width
        if self.y > window.height:
            self.y -= window.height
        if self.x < 0:
            self.x += window.width
        if self.y < 0:
            self.y += window.height

raketa = Raketa()
raketa.x = 100
raketa.y = 100
raketa.rychlost_x = 0
raketa.rychlost_y = 0
raketa.rotace = 0

def vykresli():
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    gl.glColor3f(1, 1, 1)
    raketa.nakresli()

def update(dt):
    raketa.posun(dt)

klavesy = set()

def stisk_klavesy(klavesa, mod):
    klavesy.add(klavesa)

def pusteni_klavesy(klavesa, mod):
    klavesy.discard(klavesa)

window.push_handlers(
    on_draw=vykresli,
    on_key_press=stisk_klavesy,
    on_key_release=pusteni_klavesy,
)
pyglet.clock.schedule(update)

pyglet.app.run()
