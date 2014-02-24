#! /usr/bin/env python2
# Encoding: UTF-8

"""Hra typu Asteroids

Tahle hra ukaze použití tříd.

Ovládání:
Doprava/Doleva: Otáčení vesmírné lodi
Dopredu/Dozadu: Zrychlovat/Zpomalovat
"""

import math

import pyglet
from pyglet import gl
from pyglet.window import key

# Sada kláves, která jsou právě stisknuté (nastavuje se ve funkcích
# stisk_klavesy a pusteni_klavesy)
klavesy = set()

# Konstanty
ZRYCHLENI = 500  # px/s^2
UHLOVA_RYCHLOST = 200  # stupnu/s
VELIKOST_LODI = 20  # px

# Vytvoření okna
window = pyglet.window.Window()

class Raketa(object):
    """Trojúhelníkovtý objekt s polohou, rychlostí, a natočením

    Poloha (v pixelech) je uložena v atributech ``x`` a ``y``, rychlost
    v ``rychlost_x`` a ``rychlost_y``, a natočení (ve stupních) v atributu
    ``rotace``.
    """
    def nakresli(self):
        """Vykresli raketu (trojúhelníček na správne pozici)"""
        # Zapamatovat si stav souřadného systému
        gl.glPushMatrix()
        # Posunout počátek souřadnic na pozici rakety
        gl.glTranslatef(self.x, self.y, 0)
        # Otočit systém souřadnic o příslušný úhel
        gl.glRotatef(self.rotace, 0, 0, 1)
        # Začít kreslit trojúhelník
        gl.glBegin(gl.GL_TRIANGLE_FAN)
        # Zadat souřadnice vrcholu trojúhelníka (X značí vrcholy, + počátek)
        gl.glVertex2f(-VELIKOST_LODI, VELIKOST_LODI/2)   #  X
        gl.glVertex2f(VELIKOST_LODI, 0)                  #     +  X
        gl.glVertex2f(-VELIKOST_LODI, -VELIKOST_LODI/2)  #  X
        # Konec kreslení trojuhelníka
        gl.glEnd()
        # Vrátit souřadný systém do původního stavu (zapamatovaného
        # pomocí glPushMatrix)
        gl.glPopMatrix()

    def posun(self, dt):
        """Aktualizuj stav rakety po ``dt`` uplynulých sekundách"""
        # Změna polohy = rychlost krát čas
        self.x += self.rychlost_x * dt
        self.y += self.rychlost_y * dt
        # C
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

# Vytvoření instance (objektu) typu Raketa + nastavení atributů
raketa = Raketa()
raketa.x = window.width / 2
raketa.y = window.height / 2
raketa.rychlost_x = 0
raketa.rychlost_y = 0
raketa.rotace = 0

def vykresli():
    """Vykresli celou scénu"""
    # Reset okýnka
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    # Nastavení barvy, kterou budeme kreslit
    gl.glColor3f(1, 1, 1)
    # Reset souřadného systému
    gl.glLoadIdentity()
    # Nakreslení samotné rakety
    raketa.nakresli()

def update(dt):
    """Aktualizuj stav celé hry po ``dt`` uplynulých sekundách"""
    # Jediná věc co potřebuje aktualizovat je naše raketa
    raketa.posun(dt)

def stisk_klavesy(klavesa, mod):
    """Zaznamenej stisk klávesy"""
    klavesy.add(klavesa)

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
