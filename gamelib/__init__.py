
import json
from .texture import *
from .keys import *

from OpenGL.GL import *
from OpenGL.GLU import *

class Cell:
    ground = 0

class Level:
    w = 0
    h = 0
    cells = None



class Tilemap:
    mapw = 512
    maph = 512
    tw = 32
    th = 32
    width_on_screen = 16*4
    height_on_screen = 16*4
    width_in_cells = 0
    height_in_cells = 0

    def __init__(self, texture_file_name):
        self.width_in_cells = self.mapw // self.tw
        self.height_in_cells = self.maph // self.th
        self.texture_file_name = texture_file_name
        self.names = ['' for i in range(self.width_in_cells*self.height_in_cells)]

    def no_from_xy(self, x, y):
        return x + y * self.width_in_cells

    def start_draw(self):
        set_texture(self.texture_file_name)
        glBegin(GL_QUADS)
        glColor4f(1.0, 1.0, 1.0, 1.0)

    def end_draw(self):
        glEnd()

    def draw(self, tile, px ,py):
        tilex = tile.no % self.width_in_cells
        tiley = tile.no // self.width_in_cells
        tx = tilex * self.tw
        ty = tiley * self.th
        tw = self.tw
        th = self.th
        w = self.width_on_screen
        h = self.height_on_screen

        tx = tx / float(self.mapw)
        ty = ty / float(self.maph)

        tw /= float(self.mapw)
        th /= float(self.maph)

        glTexCoord2f(tx, ty)
        glVertex2f(px, py)

        glTexCoord2f(tx+tw, ty)
        glVertex2f(px+w, py)

        glTexCoord2f(tx+tw, ty+th)
        glVertex2f(px+w, py+h)

        glTexCoord2f(tx, ty+th)
        glVertex2f(px, py+h)

class Tile:
    no = 0

class GroundTile(Tile):
    can_go = True
    cat_fly = True

class UrbanCharacterSprite:
    def __init__(self):
        pass

    def draw(self):
        pass

class Player:
    x = 0
    y = 0
    def __init__(self):
        self.tile = Tile()

    def process(self):
        player = self
        walking = False
        if keys_down.get(pygame.K_w):
            walking = True
            player.y -= 3
            #player.player_sprite.anim.pose = Pose.WALKING
            #player.player_sprite.direction = Directions.N
        if keys_down.get(pygame.K_s):
            walking = True
            player.y += 3
            #player.player_sprite.anim.pose = Pose.WALKING
            #player.player_sprite.direction = Directions.S
        if keys_down.get(pygame.K_a):
            walking = True
            player.x -= 3
            #player.player_sprite.anim.pose = Pose.WALKING
            #player.player_sprite.direction = Directions.W
        if keys_down.get(pygame.K_d):
            walking = True
            player.x += 3
            #player.player_sprite.anim.pose = Pose.WALKING
            #player.player_sprite.direction = Directions.E
        if keys_down.get(pygame.K_e):
            #player.player_sprite.anim.pose = Pose.ACTING
            #player.player_sprite.anim.time = 0
            pass
        if keys_down.get(pygame.K_c):
            #player.player_sprite.anim.pose = Pose.FALLING
            #player.player_sprite.anim.time = 0
            pass
        #if not walking and player.player_sprite.anim.pose == Pose.WALKING:
        #    player.player_sprite.anim.pose = Pose.IDLE


class Game:
    def __init__(self):
        self.player = Player()
        self.tilemap = Tilemap('data/pics/urban.png')
        self.ground_tiles = {}
        self.ground_tiles_by_no = {}

        def add_tile(name, x, y, can_go=True, can_fly=True, on_stand=None):
            t = GroundTile()
            t.no = self.tilemap.no_from_xy(x, y)
            t.name = name
            self.ground_tiles[name] = t
            self.ground_tiles_by_no[t.no] = t

        self.level = Level()
        add_tile('wall', 8, 0, can_go=False, can_fly=False)
        add_tile('lift', 6, 0)
        add_tile('fire_door', 6, 1)
        add_tile('escape_door', 6, 2)
        add_tile('wooden_door', 6, 2)
        add_tile('yellow_floor', 2, 14)
        add_tile('green_floor', 1, 14)
        add_tile('blue_floor', 2, 12)

    def init(self):
        self.load('')

    def load(self, filename):
        self.level = Level()
        js = json.loads(open('data/facility.json').read())
        self.level.w = int(js['layers'][0]['width'])
        self.level.h = int(js['layers'][0]['height'])
        self.level.cells = [Cell() for i in range(self.level.w * self.level.h)]
        for e in range(len(js['layers'][0]['data'])):
            idx = int(js['layers'][0]['data'][e])
            x = e % self.level.w
            y = e // self.level.w
            self.level.cells[e].ground = self.ground_tiles_by_no.get(e, self.ground_tiles['blue_floor'])
    def draw(self):
        glClearColor(0.56, 0.66, 0.79, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluOrtho2D(0, 800, 600, 0)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self.tilemap.start_draw()
        for i in range(16):
            for j in range(10):
                a = i * 16 * 4
                b = j * 16 * 4
                cell = self.level.cells[i + j * self.level.w]
                self.tilemap.draw(cell.ground,
                                  a, b)

        self.player.process()
        self.tilemap.draw(self.player.tile, self.player.x, self.player.y)
        self.tilemap.end_draw()
