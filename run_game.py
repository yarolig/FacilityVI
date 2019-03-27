#! /usr/bin/env python3

#from gamelib import main
#main.main()

import pygame
import pygame.freetype
import pygame.mixer
import pygame.image
import pygame.freetype

import os
import sys

from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.display import  *


'''
0x91AACC
0x325E99 0.19, 0.36, 0.59
0xCFFCFF 0.80, 0.98, 0.80
0xFFAB8F 1.0, 0.66, 0.55
0xC6655A 0.77, 0.39, 0.35
'''

from gamelib.texture import *

keys_down={}
class Directions:
    N = (0, -1)
    S = (0, 1)
    W = (-1, 0)
    E = (1, 0)

class Pose:
    IDLE = 0
    WALKING = 1
    ACTING = 2
    FALLING = 3

class Animation:
    pose = Pose.IDLE
    time = 0

class CharacterSprite:
    mapw = 128
    maph = 256
    tw = 32
    th = 32
    def __init__(self):
        self.direction = Directions.N
        self.anim = Animation()

    def offset_for_direction(self, dir):
        if dir == Directions.N:
            return (2, 2)
        if dir == Directions.S:
            return (21, 2)
        if dir == Directions.W:
            return (40, 2)
        if dir == Directions.E:
            return (59, 2)

    def offset_for_anim(self, anim):
        assert isinstance(anim, Animation)
        if anim.pose == Pose.IDLE:
            if anim.time // 30 % 2 == 0:
               return (0,0)
            return (0,0)
        if anim.pose == Pose.WALKING:
            if anim.time // 15 % 2 == 0:
               return (0,96)
            return (0,128)
        if anim.pose == Pose.ACTING:
            if anim.time // 30 % 2 == 0:
               return (0,32)
            return (0,0)
        if anim.pose == Pose.FALLING:
            if anim.time < 30 == 0:
               return (0,160)
            return (0,192)

    def draw(self):
        dx, dy = self.offset_for_direction(self.direction)
        ax, ay = self.offset_for_anim(self.anim)
        tx = dx + ax
        ty = dy + ay

        tx = tx / float(self.mapw)
        ty = ty / float(self.maph)

        w, h = 16*4, 16*4
        tw = self.tw / float(self.mapw)
        th = self.th / float(self.maph)

        #tx, ty = 0, 0
        #tw, th = 1,1 #64.0 / 128.0, 64.0 / 256.0

        glBegin(GL_QUADS)
        glColor4f(1.0, 1.0, 1.0, 1.0)
        glTexCoord2f(tx, ty)
        glVertex2f(0, 0)

        glTexCoord2f(tx+tw, ty)
        glVertex2f(w, 0)

        glTexCoord2f(tx+tw, ty+th)
        glVertex2f(w, h)

        glTexCoord2f(tx, ty+th)
        glVertex2f(0, h)
        glEnd()

class UrbanCharacterSprite(CharacterSprite):
    mapw = 512
    maph = 512
    tw = 32
    th = 32
    def offset_for_direction(self, dir):
        if dir == Directions.W:
            return (0, 0)
        if dir == Directions.S:
            return (32, 0)
        if dir == Directions.N:
            return (64, 0)
        if dir == Directions.E:
            return (96, 0)

    def offset_for_anim(self, anim):
        assert isinstance(anim, Animation)
        if anim.pose == Pose.IDLE:
            if anim.time // 30 % 2 == 0:
               return (0,0)
            return (0,0)
        if anim.pose == Pose.WALKING:
            if anim.time // 15 % 2 == 0:
               return (0, 32)
            return (0, 64)
        if anim.pose == Pose.ACTING:
            if anim.time // 30 % 2 == 0:
               return (0,96)
            return (0,0)
        if anim.pose == Pose.FALLING:
            if anim.time < 10:
               return (0,128)
            return (0,160)


class Tilemap:
    mapw = 512
    maph = 512
    tw = 16
    th = 16
    def __init__(self):
        pass
    def draw(self, tile, px ,py):
        tx = tile.ox
        ty = tile.oy
        tw = self.tw
        th = self.th
        w = 16*4
        h = 16*4

        tx = tx / float(self.mapw)
        ty = ty / float(self.maph)

        tw /= float(self.mapw)
        th /= float(self.maph)

        glBegin(GL_QUADS)
        glColor4f(1.0, 1.0, 1.0, 1.0)
        glTexCoord2f(tx, ty)
        glVertex2f(px, py)

        glTexCoord2f(tx+tw, ty)
        glVertex2f(px+w, py)

        glTexCoord2f(tx+tw, ty+th)
        glVertex2f(px+w, py+h)

        glTexCoord2f(tx, ty+th)
        glVertex2f(px, py+h)
        glEnd()

class GroundTile:
    ox = 128+16
    oy = 48+16





class Player:
    x = 0
    y = 0

    def __init__(self):
        self.player_sprite = UrbanCharacterSprite()


    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, 0)
        self.player_sprite.anim.time += 1
        self.player_sprite.draw()
        glPopMatrix()

    def process(self):
        walking = False
        if keys_down.get(pygame.K_w):
            walking = True
            player.y -= 3
            player.player_sprite.anim.pose = Pose.WALKING
            player.player_sprite.direction = Directions.N
        if keys_down.get(pygame.K_s):
            walking = True
            player.y += 3
            player.player_sprite.anim.pose = Pose.WALKING
            player.player_sprite.direction = Directions.S
        if keys_down.get(pygame.K_a):
            walking = True
            player.x -= 3
            player.player_sprite.anim.pose = Pose.WALKING
            player.player_sprite.direction = Directions.W
        if keys_down.get(pygame.K_d):
            walking = True
            player.x += 3
            player.player_sprite.anim.pose = Pose.WALKING
            player.player_sprite.direction = Directions.E
        if keys_down.get(pygame.K_e):
            player.player_sprite.anim.pose = Pose.ACTING
            player.player_sprite.anim.time = 0
        if keys_down.get(pygame.K_c):
            player.player_sprite.anim.pose = Pose.FALLING
            player.player_sprite.anim.time = 0

        if not walking and player.player_sprite.anim.pose == Pose.WALKING:
            player.player_sprite.anim.pose = Pose.IDLE

player = Player()

def draw():
    glClearColor(0.56, 0.66, 0.79, 1.0)
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluOrtho2D(0, 800, 600, 0)

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    #set_texture('data/pics/worker-sheet_default.png')

    set_texture('data/pics/urban/Tilemap/tilemap_packed.png')
    tm = Tilemap()
    tile = GroundTile()
    for i in range(10):
        for j in range(10):
            a = i * 16 * 4
            b = j * 16 * 4
            tm.draw(tile, a, b)

    set_texture('data/pics/urban.png')
    player.process()
    player.draw()


def main():
    pygame.display.init()
    pygame.init()
    pygame.display.set_mode((800,600),
                            pygame.OPENGL |
                            pygame.RESIZABLE |
                            pygame.DOUBLEBUF)
    while True:
        for event in pygame.event.get():

            print(event)
            if event.type == pygame.QUIT:
                break
            if event.type == pygame.KEYDOWN:
                if event.unicode == 'q':
                    sys.exit()

            if event.type == pygame.KEYUP:
                keys_down[event.key] = False

            if event.type == pygame.KEYDOWN:
                keys_down[event.key] = True

        draw()
        pygame.display.flip()

if __name__ == '__main__':
    main()