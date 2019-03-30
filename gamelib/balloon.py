

import pygame
import pygame.freetype

from OpenGL.GL import *
from OpenGL.GLU import *

font = None
text_textures = {}

def init():
    global font
    pygame.freetype.init()
    font = pygame.freetype.Font('data/fonts/SquareGrotesk-Regular.otf',
                                size=18,
                                )

def draw_text(text, x, y, bgcolor=None):
    global font
    assert isinstance(font, pygame.freetype.Font)
    if bgcolor is None:
        bgcolor = pygame.Color(19*4, 36*4, 59*4, 255)
    if text not in text_textures:
        surface = pygame.Surface((512,256), flags=pygame.SRCALPHA)
        surface.fill(pygame.Color(127,127,127,0))
        rect = font.render_to(surface,
                       (0,0),
                       text,
                       bgcolor=bgcolor,
                       fgcolor=pygame.Color('black'))
        print('rect', rect)
        s = ''

        for i in range(100):
            for j in range(100):
                if pygame.Color(0, 0, 0, 255) == surface.get_at((j, i)):
                    s += '#'
                elif pygame.Color('green') == surface.get_at((j, i)):
                    s += '!'
                else:
                    s+='.'
            s+='\n'
        print(s)
        data = pygame.image.tostring(surface, "RGBA", 1)

        width = surface.get_width()
        height = surface.get_height()
        id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, id)
        glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA,
                     GL_UNSIGNED_BYTE, data)

        print(id, width, height)
        print(font)
        text_textures[text] = id
    else:
        glBindTexture(GL_TEXTURE_2D, text_textures[text])

    #print (text_textures[text], '->', text)
    glEnable(GL_TEXTURE_2D)
    px = x
    py = y
    w = 512
    h = 256

    glBegin(GL_QUADS)
    glColor4f(1.0,1.0,1.0,1.0)
    glTexCoord2f(0, 1)
    glVertex2f(px, py)

    glTexCoord2f(1, 1)
    glVertex2f(px + w, py)

    glTexCoord2f(1, 0)
    glVertex2f(px + w, py + h)

    glTexCoord2f(0, 0)
    glVertex2f(px, py + h)
    glEnd()
