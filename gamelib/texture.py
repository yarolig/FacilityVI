
import pygame

from OpenGL.GL import *
from OpenGL.GLU import *
textures = {}

def load_texture(filename):
    surface = pygame.image.load(filename)
    surface = pygame.transform.flip(surface, False, True)

    data = pygame.image.tostring(surface, "RGBA", 1)

    width = surface.get_width()
    height = surface.get_height()
    id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, id)
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
    #glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA,
        GL_UNSIGNED_BYTE, data)
    print (id,width,height)
    return id


def get_texture(filename):
    if filename in textures:
        return textures[filename]
    textures[filename] = load_texture(filename)
    return textures[filename]

def set_texture(filename):
    t = get_texture(filename)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, t)
