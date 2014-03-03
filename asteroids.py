#! /usr/bin/env python2
# Encoding: UTF-8

"""Hra typu Asteroids

Tahle hra ukaze použití tříd.

Ovládání:
Doprava/Doleva: Otáčení vesmírné lodi
Dopredu/Dozadu: Zrychlovat/Zpomalovat
"""

import math
import random

import pyglet
from pyglet import gl
from pyglet.window import key

# Sada kláves, která jsou právě stisknuté (nastavuje se ve funkcích
# stisk_klavesy a pusteni_klavesy)
klavesy = set()

# Konstanty
ZRYCHLENI = 500  # px/s^2
UHLOVA_RYCHLOST = 200  # stupnu/s
UHLOVA_RYCHLOST_ASTEROIDU = 200  # max, stupnu/s
VELIKOST_LODI = 20  # px
VELIKOST_ASTEROIDU = 40  # px, pocatecni
SISATOST = 5 # px
RYCHLOST_ASTEROIDU = 100  # max, px/s
POCET_VYSECI_ASTEROIDU = 13
VELIKOST_TORPEDA = 3
RYCHLOST_TORPEDA = 500

# Vytvoření okna
#window = pyglet.window.Window(width=1024, height=768)
window = pyglet.window.Window(width=800, height=600)

class VesmirnyObjekt(object):
    """Trojúhelníkovtý objekt s polohou, rychlostí, a natočením

    Poloha (v pixelech) je uložena v atributech ``x`` a ``y``, rychlost
    v ``rychlost_x`` a ``rychlost_y``, a natočení (ve stupních) v atributu
    ``rotace``.
    """
    def __init__(self):
        self.x = window.width / 2
        self.y = window.height / 2
        self.rychlost_x = 0
        self.rychlost_y = 0
        self.rotace = 0
        self.uhlova_rychlost = 0
        self.delka_drahy = 0

    def nakresli(self):
        """Vykresli objekt 9x, aby fungoval přechod přes hranu obrazovky"""
        for x in (self.x - window.width, self.x, self.x + window.width):
            for y in (self.y - window.height, self.y, self.y + window.height):
                self.nakresli_jednou(x, y)

    def nakresli_jednou(self, x, y):
        """Vykresli objekt na dané pozici"""
        # Zapamatovat si stav souřadného systému
        gl.glPushMatrix()
        # Posunout počátek souřadnic na pozici rakety
        gl.glTranslatef(x, y, 0)
        # Otočit systém souřadnic o příslušný úhel
        gl.glRotatef(self.rotace, 0, 0, 1)
        self.nakresli_tvar()
        # Vrátit souřadný systém do původního stavu (zapamatovaného
        # pomocí glPushMatrix)
        gl.glPopMatrix()

    def pohyb(self, dt):
        self.x += self.rychlost_x * dt
        self.y += self.rychlost_y * dt
        self.delka_drahy += math.sqrt(
            (self.rychlost_x * dt) ** 2 +
            (self.rychlost_y * dt) ** 2
        )
        self.rotace += self.uhlova_rychlost * dt
        # Pokud vesmírná loď vyletí z obrazovky, přesuneme ji na druhý okraj.
        # Dosáhneme tím nekonečného vesmíru!
        if self.x > window.width:
            self.x -= window.width
        if self.y > window.height:
            self.y -= window.height
        if self.x < 0:
            self.x += window.width
        if self.y < 0:
            self.y += window.height

    def posun(self, dt):
        self.pohyb(dt)


class Raketa(VesmirnyObjekt):
    def nakresli_tvar(self):
        """Nakreslí trojúhelník"""
        # Začít kreslit trojúhelník
        gl.glBegin(gl.GL_TRIANGLE_FAN)
        # Zadat souřadnice vrcholu trojúhelníka (X značí vrcholy, + počátek)
        gl.glVertex2f(-VELIKOST_LODI, VELIKOST_LODI/2)   #  X
        gl.glVertex2f(VELIKOST_LODI, 0)                  #     +  X
        gl.glVertex2f(-VELIKOST_LODI, -VELIKOST_LODI/2)  #  X
        # Konec kreslení trojuhelníka
        gl.glEnd()

    def posun(self, dt):
        """Aktualizuj stav rakety po ``dt`` uplynulých sekundách"""
        # Změna polohy = rychlost krát čas
        self.pohyb(dt)
        if key.LEFT in klavesy:
            self.rotace += dt * UHLOVA_RYCHLOST
        if key.RIGHT in klavesy:
            self.rotace -= dt * UHLOVA_RYCHLOST
        # Spocitat uhel otoceni rakety v radianech (``rotace`` je ve stupnich)
        uhel = self.rotace * math.pi / 180
        # Šipky nahoru/dolů mění rychlost ve směru natočení rakety.
        # Využijeme goniometrických funkcí:
        #         y
        #         ^
        #         |
        #  sin α -+------X - špička rakety, ve směru kam chceme letět
        #         |     /|
        #         |    / |
        #         |   /  |
        #         |  /   |
        #         | /\   |
        #         |/α|  .| - pravý úhel
        #   ------+------+--------------->x
        #         |      |
        #         |    cos α
        #         |
        #
        if key.UP in klavesy:
            self.rychlost_x += dt * ZRYCHLENI * math.cos(uhel)
            self.rychlost_y += dt * ZRYCHLENI * math.sin(uhel)
        if key.DOWN in klavesy:
            self.rychlost_x -= dt * ZRYCHLENI * math.cos(uhel)
            self.rychlost_y -= dt * ZRYCHLENI * math.sin(uhel)


class Asteroid(VesmirnyObjekt):
    def __init__(self):
        VesmirnyObjekt.__init__(self)
        self.uhlova_rychlost = 1
        self.rychlost_x = random.uniform(-RYCHLOST_ASTEROIDU,
                                         RYCHLOST_ASTEROIDU)
        self.rychlost_y = random.uniform(-RYCHLOST_ASTEROIDU,
                                         RYCHLOST_ASTEROIDU)
        if random.choice([True, False]):
            self.x = 0
            self.y = random.uniform(0, window.height)
        else:
            self.x = random.uniform(0, window.width)
            self.y = 0
        self.uhlova_rychlost = random.uniform(
            -UHLOVA_RYCHLOST_ASTEROIDU,
            UHLOVA_RYCHLOST_ASTEROIDU)
        self.tvar = []
        for i in range(POCET_VYSECI_ASTEROIDU):
            self.tvar.append(random.uniform(-1, 1))

    def nakresli_tvar(self):
        """Nakreslí asteroid"""
        gl.glBegin(gl.GL_TRIANGLE_FAN)
        gl.glVertex2f(0, 0)
        for i, s in enumerate(self.tvar + self.tvar[:1]):
            delka = VELIKOST_ASTEROIDU + s * SISATOST
            uhel = i * math.pi * 2 / POCET_VYSECI_ASTEROIDU
            gl.glVertex2f(
                math.cos(uhel) * delka,
                math.sin(uhel) * delka)
        gl.glEnd()


class Torpedo(VesmirnyObjekt):
    def __init__(self, raketa):
        VesmirnyObjekt.__init__(self)
        uhel = raketa.rotace * math.pi / 180
        self.x = raketa.x + VELIKOST_LODI * math.cos(uhel)
        self.y = raketa.y + VELIKOST_LODI * math.sin(uhel)
        self.rychlost_x = raketa.rychlost_x + RYCHLOST_TORPEDA * math.cos(uhel)
        self.rychlost_y = raketa.rychlost_y + RYCHLOST_TORPEDA * math.sin(uhel)
        self.rotace = raketa.rotace

    def nakresli_tvar(self):
        gl.glBegin(gl.GL_TRIANGLE_FAN)
        gl.glVertex2f(-VELIKOST_TORPEDA, -VELIKOST_TORPEDA/2)
        gl.glVertex2f(-VELIKOST_TORPEDA, VELIKOST_TORPEDA/2)
        gl.glVertex2f(VELIKOST_TORPEDA, VELIKOST_TORPEDA/2)
        gl.glVertex2f(VELIKOST_TORPEDA, -VELIKOST_TORPEDA/2)
        gl.glEnd()


# Vytvoření instance (objektu) typu Raketa + nastavení atributů
raketa = Raketa()

objekty = [raketa]

for i in range(3):
    objekty.append(Asteroid())

def vykresli():
    """Vykresli celou scénu"""
    # Reset okýnka
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    # Nastavení barvy, kterou budeme kreslit
    gl.glColor3f(1, 1, 1)
    # Reset souřadného systému
    gl.glLoadIdentity()
    # Nakreslení samotných objektů
    for objekt in objekty:
        objekt.nakresli()

def update(dt):
    """Aktualizuj stav celé hry po ``dt`` uplynulých sekundách"""
    # Aktualizuj všechny objekty
    for objekt in objekty:
        objekt.posun(dt)

def vystrel():
    objekty.append(Torpedo(raketa))

def stisk_klavesy(klavesa, mod):
    """Zaznamenej stisk klávesy"""
    klavesy.add(klavesa)
    if klavesa == key.SPACE:
        vystrel()

def pusteni_klavesy(klavesa, mod):
    """Zaznamenej puštění klávesy"""
    klavesy.discard(klavesa)

# Nastavení funkcí, které se zavolají pro různé události okna:
window.push_handlers(
    on_draw=vykresli,
    on_key_press=stisk_klavesy,
    on_key_release=pusteni_klavesy,
)
# Funkce "update" se bude volat pro každý obrázek animace
pyglet.clock.schedule(update)

# 3... 2... 1... Start!
# (Spustit mechanismus, který reaguje na události a volá funkce registrované
# výše pomocí push_handlers a schedule)
pyglet.app.run()
