#! /usr/bin/env python3

#from gamelib import main
#main.main()

import pygame
import pygame.freetype
import pygame.mixer
import pygame.image
import pygame.freetype

import gamelib


import os
import sys

from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.display import  *
from gamelib.texture import *
from gamelib.keys import *

game = gamelib.Game()


def main():
    pygame.display.init()
    pygame.init()
    pygame.display.set_mode((800,600),
                            pygame.OPENGL |
                            pygame.RESIZABLE |
                            pygame.DOUBLEBUF)
    pygame.display.set_caption('Facility VI - pyweek27')
    game.init()
    while True:
        for event in pygame.event.get():

            #print(event)
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_m:
                    gamelib.sounds.toggle_music()
                if event.key == pygame.K_n:
                    gamelib.sounds.toggle_sound()

            if event.type == pygame.KEYUP:
                keys_down[event.key] = False

            if event.type == pygame.KEYDOWN:
                keys_down[event.key] = True
        game.draw()
        pygame.display.flip()

if __name__ == '__main__':
    pygame.mixer.pre_init(frequency=44100, buffer=1024  )
    main()