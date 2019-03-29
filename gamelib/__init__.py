
import json
from .texture import *
from .keys import *

from OpenGL.GL import *
from OpenGL.GLU import *

class Cell:
    ground = 0
    marked = False

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
    door_letter = '\0'

class FurnitureTile(Tile):
    can_go = True
    cat_fly = True
   

class UrbanCharacterSprite:
    def __init__(self):
        pass

    def draw(self):
        pass

class Room:
    x = 0
    y = 0
    name = ''
    ex = 0
    ey = 0
    def __str__(self):
        return  "Room({} {}:{} {}:{})".format(self.name, self.x, self.y, self.ex, self.ey)

class Player:
    x = 0
    y = 0
    old_door_letter = ':'
    def __init__(self):
        self.tile = Tile()

    def process(self, game):
        assert isinstance(game, Game)
        player = self
        walking = False
        oldpos = player.x, player.y

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
        cell = game.get_cell_for_pxpy(self.x, self.y)
        #print (cell, cell.ground)
        gnd = cell.ground
        assert isinstance(gnd, GroundTile)
        if not gnd.can_go:
            self.x, self.y = oldpos
        if gnd.door_letter not in '\0\n':
            game.change_room(self.old_door_letter, gnd.door_letter)

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
        self.rooms = {}
        self.current_room = Room()
        def add_tile(name, x, y,
                     can_go=True,
                     can_fly=True,
                     on_stand=None,
                     door_letter='\0'):
            t = GroundTile()
            t.no = self.tilemap.no_from_xy(x, y)
            t.name = name
            t.can_go = can_go
            t.can_fly = can_fly
            t.door_letter = door_letter
            self.ground_tiles[name] = t
            self.ground_tiles_by_no[t.no] = t

        self.level = Level()
        add_tile('wall', 8, 0, can_go=False, can_fly=False)
        add_tile('lift', 6, 0, door_letter=':')
        add_tile('doorA', 6, 1, door_letter='a')
        add_tile('doorE', 6, 2, door_letter='e')
        add_tile('doorI', 6, 3, door_letter='i')
        add_tile('doorO', 6, 4, door_letter='o')
        add_tile('doorM', 6, 5, door_letter='m')
        add_tile('doorN', 6, 6, door_letter='n')
        add_tile('doorQ', 6, 7, door_letter='q')
        add_tile('doorW', 6, 8, door_letter='w')
        add_tile('doorF', 6, 9, door_letter='f')
        add_tile('door!', 6, 10, door_letter='!')

        add_tile('yellow_floor', 14, 2)
        add_tile('yellow_floor2', 15, 2)
        add_tile('green_floor', 15, 1)
        add_tile('tile_floor', 15, 1)
        add_tile('blue_floor', 12, 2)
        add_tile('textured_floor', 15, 3)
        add_tile('gray_floor', 14, 1)
        add_tile('kitchen_furniture', 13, 6)
        add_tile('asphalt', 9, 0)
        add_tile('gray_floor2', 14, 0)
        add_tile('grass', 13, 1)

    def init(self):
        self.load('')

    def load(self, filename):
        self.level = Level()
        js = json.loads(open('data/facility.json').read())
        self.level.w = int(js['layers'][0]['width'])
        self.level.h = int(js['layers'][0]['height'])
        self.level.cells = [Cell() for i in range(self.level.w * self.level.h)]
        for e in range(len(js['layers'][0]['data'])):
            idx = int(js['layers'][0]['data'][e]) -1
            x = e % self.level.w
            y = e // self.level.w
            gnd = self.ground_tiles_by_no.get(idx)
            if not gnd and idx != -1:
                print('bad gnd: {} ({} {})'.format(idx, idx % 16, idx // 16))
            self.level.cells[e].ground = gnd or self.ground_tiles['blue_floor']

        def get_room(name):
            if name in self.rooms:
                return self.rooms[name]
            r = Room()
            r.name = name
            self.rooms[name] = r
            return self.rooms[name]

        for o in js['layers'][3]['objects']:
            if o['type'] == 'room':
                r = get_room(o['name'])
                r.x = int(o['x']) // 32 * 32
                r.y = int(o['y']) // 32 * 32
            if o['type'] == 'start':
                r = get_room(o['name'])
                r.ex = int(o['x']) // 32 * 32
                r.ey = int(o['y']) // 32 * 32
        start_room = self.rooms['entrance']
        self.current_room = start_room
        self.player.x = start_room.ex
        self.player.y = start_room.ey
        for r in self.rooms:
            print(r + " = " + str(self.rooms[r]))
        for r in self.rooms.values():
            if r.name and (r.ex == 0 and r.ey == 0):
                raise Exception('no start for room ' + str(r))

    def change_room(self, old, new):
        dl=':aeiomnqwf!'

        if new not in dl:
            print('change_room', repr(old), repr(new), 'BAD')
            return
        oi = dl.index(old)
        ni = dl.index(new)
        transits= [
        #:aeiomnqwf! <--NEW
        'hhmiAD qw  ',  # :
        '3hhiA      ',  # a
        'mhhik  ig  ',  # e |
        'h   A      ',  # i |
        ' Ch B    f ',  # o | OLD
        'h    3E    ',  # m |
        'h 3  Dl    ',  # n |
        '  m       W',  # q
        '  m i  W   ',  # w
        '  k      i ',  # f
        '           ',  # !
        ]
        short_names = {
             "3" : "3rd",
             "D" : "construction1",
             "E" : "construction2",
             "e" : "entrance",
             "f" : "fridge",
             "h" : "hall",
             "m" : "maintenance",
             "i" : "information",
             "k" : "kitchen",
             "l" : "library",
             "g" : "garden",
             "A" : "office1",
             "B" : "office2",
             "C" : "office3",
             "q" : "quality",
             "w" : "warehouse",
             "W" : "WIN",
        }
        new_room_sname = transits[oi][ni]
        new_room_name = short_names.get(new_room_sname, 'entrance')

        print('change_room', repr(old), repr(new), '->', new_room_name)
        start_room = self.rooms[new_room_name]
        self.current_room = start_room
        self.player.x = start_room.ex
        self.player.y = start_room.ey
        self.player.old_door_letter = new

    def get_cell_for_pxpy(self, px ,py):
        ii = (px + 15) // 32
        jj = (py + 30) // 32
        cell = self.level.cells[ii + jj * self.level.w]
        #print(ii, jj, cell)
        return cell

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
                ii = i + self.current_room.x // 32
                jj = j + self.current_room.y // 32
                cell = self.level.cells[ii + jj * self.level.w]
                if not cell.marked:
                    self.tilemap.draw(cell.ground,
                                  a, b)

        self.player.process(self)
        #print (self.player.x - self.current_room.x,
        #       self.player.y - self.current_room.y)
        for c in self.level.cells:
            c.marked = False
        c = self.get_cell_for_pxpy(self.player.x, self.player.y)
        c.marked = True
        self.tilemap.draw(self.player.tile,
                          (self.player.x - self.current_room.x)*2,
                           (self.player.y - self.current_room.y)*2)
        self.tilemap.end_draw()
