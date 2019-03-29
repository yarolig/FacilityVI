
import json
from .texture import *
from .keys import *

from OpenGL.GL import *
from OpenGL.GLU import *

class Cell:
    ground = None
    furniture = None
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
        if isinstance(tile, Tile):
            tile = tile.no
        tilex = tile % self.width_in_cells
        tiley = tile // self.width_in_cells
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

class EndAction:
    NONE = 0
    LOOP = 1
    STOP = 2

class AnimationPhase:
    end = EndAction.NONE
    def __init__(self, name, f, t, tile, end=EndAction.NONE):
        self.name = name
        self.f= f
        self.t = t
        self.end = end
        self.tile = tile

class Animated:
    anim_name = 'd'
    anim_time = 0

class CharacterAnimation:
    def __init__(self, tilemap):
        assert  isinstance(tilemap, Tilemap)
        self.phases = [
            AnimationPhase('a', 0, 15, tilemap.no_from_xy(0, 0), end=EndAction.LOOP),
            AnimationPhase('s', 0, 15, tilemap.no_from_xy(1, 0), end=EndAction.LOOP),
            AnimationPhase('w', 0, 15, tilemap.no_from_xy(2, 0), end=EndAction.LOOP),
            AnimationPhase('d', 0, 15, tilemap.no_from_xy(3, 0), end=EndAction.LOOP),

            AnimationPhase('walka', 0, 15, tilemap.no_from_xy(0, 1)),
            AnimationPhase('walks', 0, 15, tilemap.no_from_xy(1, 1)),
            AnimationPhase('walkw', 0, 15, tilemap.no_from_xy(2, 1)),
            AnimationPhase('walkd', 0, 15, tilemap.no_from_xy(3, 1)),

            AnimationPhase('walka', 15, 30, tilemap.no_from_xy(0, 2), end=EndAction.LOOP),
            AnimationPhase('walks', 15, 30, tilemap.no_from_xy(1, 2), end=EndAction.LOOP),
            AnimationPhase('walkw', 15, 30, tilemap.no_from_xy(2, 2), end=EndAction.LOOP),
            AnimationPhase('walkd', 15, 30, tilemap.no_from_xy(3, 2), end=EndAction.LOOP),
        ]
    def anim_tile(self, animation_state):
        cap = None
        anim_name, time = animation_state.anim_name, animation_state.anim_time
        for ap in self.phases:
            if ap.name == anim_name and ap.f <= time < ap.t:
                cap = ap
                break
        else:
            raise Exception('anim not found {} {}'.format(anim_name, time))
        animation_state.anim_time += 1
        if animation_state.anim_time == cap.t:
            if cap.end == EndAction.LOOP:
                animation_state.anim_time = 0
            elif cap.end == EndAction.LOOP:
                animation_state.anim_time -= 1
        return cap.tile

class BotAnimation(CharacterAnimation):
    def __init__(self, tilemap):
        assert  isinstance(tilemap, Tilemap)
        self.phases = [
            AnimationPhase('a', 0, 15, tilemap.no_from_xy(0, 10), end=EndAction.LOOP),
            AnimationPhase('s', 0, 15, tilemap.no_from_xy(1, 10), end=EndAction.LOOP),
            AnimationPhase('w', 0, 15, tilemap.no_from_xy(2, 10), end=EndAction.LOOP),
            AnimationPhase('d', 0, 15, tilemap.no_from_xy(3, 10), end=EndAction.LOOP),

            AnimationPhase('walka', 0, 15, tilemap.no_from_xy(0, 10)),
            AnimationPhase('walks', 0, 15, tilemap.no_from_xy(1, 10)),
            AnimationPhase('walkw', 0, 15, tilemap.no_from_xy(2, 10)),
            AnimationPhase('walkd', 0, 15, tilemap.no_from_xy(3, 10)),

            AnimationPhase('walka', 15, 30, tilemap.no_from_xy(0, 11), end=EndAction.LOOP),
            AnimationPhase('walks', 15, 30, tilemap.no_from_xy(1, 11), end=EndAction.LOOP),
            AnimationPhase('walkw', 15, 30, tilemap.no_from_xy(2, 11), end=EndAction.LOOP),
            AnimationPhase('walkd', 15, 30, tilemap.no_from_xy(3, 11), end=EndAction.LOOP),
        ]

class CleanerAnimation(CharacterAnimation):
    def __init__(self, tilemap):
        assert  isinstance(tilemap, Tilemap)
        self.phases = [
            AnimationPhase('a', 0, 15, tilemap.no_from_xy(4, 0), end=EndAction.LOOP),
            AnimationPhase('s', 0, 15, tilemap.no_from_xy(4, 0), end=EndAction.LOOP),
            AnimationPhase('w', 0, 15, tilemap.no_from_xy(4, 0), end=EndAction.LOOP),
            AnimationPhase('d', 0, 15, tilemap.no_from_xy(4, 0), end=EndAction.LOOP),

            AnimationPhase('walka', 0, 15, tilemap.no_from_xy(4, 0)),
            AnimationPhase('walks', 0, 15, tilemap.no_from_xy(4, 0)),
            AnimationPhase('walkw', 0, 15, tilemap.no_from_xy(4, 0)),
            AnimationPhase('walkd', 0, 15, tilemap.no_from_xy(4, 0)),

            AnimationPhase('walka', 15, 30, tilemap.no_from_xy(4, 1), end=EndAction.LOOP),
            AnimationPhase('walks', 15, 30, tilemap.no_from_xy(4, 1), end=EndAction.LOOP),
            AnimationPhase('walkw', 15, 30, tilemap.no_from_xy(4, 1), end=EndAction.LOOP),
            AnimationPhase('walkd', 15, 30, tilemap.no_from_xy(4, 1), end=EndAction.LOOP),
        ]


class BinAnimation(CharacterAnimation):
    def __init__(self, tilemap):
        assert  isinstance(tilemap, Tilemap)
        self.phases = [
            AnimationPhase('a', 0, 15, tilemap.no_from_xy(4, 4), end=EndAction.LOOP),
            AnimationPhase('s', 0, 15, tilemap.no_from_xy(4, 4), end=EndAction.LOOP),
            AnimationPhase('w', 0, 15, tilemap.no_from_xy(4, 4), end=EndAction.LOOP),
            AnimationPhase('d', 0, 15, tilemap.no_from_xy(4, 4), end=EndAction.LOOP),

            AnimationPhase('walka', 0, 15, tilemap.no_from_xy(4, 4)),
            AnimationPhase('walks', 0, 15, tilemap.no_from_xy(4, 4)),
            AnimationPhase('walkw', 0, 15, tilemap.no_from_xy(4, 4)),
            AnimationPhase('walkd', 0, 15, tilemap.no_from_xy(4, 4)),

            AnimationPhase('walka', 15, 30, tilemap.no_from_xy(4, 4), end=EndAction.LOOP),
            AnimationPhase('walks', 15, 30, tilemap.no_from_xy(4, 4), end=EndAction.LOOP),
            AnimationPhase('walkw', 15, 30, tilemap.no_from_xy(4, 4), end=EndAction.LOOP),
            AnimationPhase('walkd', 15, 30, tilemap.no_from_xy(4, 4), end=EndAction.LOOP),
        ]


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

class Player(Animated):
    x = 0
    y = 0
    old_door_letter = ':'
    def __init__(self):
        self.tile = Tile()

    def process(self, game):
        assert isinstance(game, Game)
        player = self
        walking = False
        firing = False
        oldpos = player.x, player.y
        dx, dy = 0, 0

        if keys_down.get(pygame.K_f):
            firing = True
            dy = -3

        if keys_down.get(pygame.K_w):
            walking = True
            dy = -3
            self.anim_name = 'walkw'
            #player.player_sprite.anim.pose = Pose.WALKING
            #player.player_sprite.direction = Directions.N
        if keys_down.get(pygame.K_s):
            walking = True
            dy = 3
            self.anim_name = 'walks'
            #player.player_sprite.anim.pose = Pose.WALKING
            #player.player_sprite.direction = Directions.S
        if keys_down.get(pygame.K_a):
            walking = True
            dx = -3
            self.anim_name = 'walka'
            #player.player_sprite.anim.pose = Pose.WALKING
            #player.player_sprite.direction = Directions.W
        if keys_down.get(pygame.K_d):
            walking = True
            dx = 3
            self.anim_name = 'walkd'
            #player.player_sprite.anim.pose = Pose.WALKING
            #player.player_sprite.direction = Directions.E

        def can_go(x, y):

            for dx, dy in [(0, 0),  (-10, 0),  (10, 0),
                           (0, -15),(-10, -15),(10,-15),]:
                cell = game.get_cell_for_pxpy(x+dx, y+dy)
                gnd = cell.ground
                fur = cell.furniture
                assert isinstance(gnd, GroundTile)
                if not gnd.can_go:
                    return False
                if fur and not fur.can_go:
                    return False
                if gnd.door_letter != '\0':
                    break

            return True

        if can_go(player.x + dx, player.y + dy):
            player.x, player.y = player.x + dx, player.y + dy
        elif can_go(player.x + dx, player.y):
            player.x, player.y = player.x + dx, player.y
        elif can_go(player.x, player.y + dy):
            player.x, player.y = player.x, player.y + dy

        cell = game.get_cell_for_pxpy(self.x, self.y)
        #print (cell, cell.ground)

        gnd = cell.ground
        fur = cell.furniture
        assert isinstance(gnd, GroundTile)
        if not gnd.can_go:
            self.x, self.y = oldpos

        if fur and not fur.can_go:
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
        if not walking and player.anim_name.startswith('walk'):
            player.anim_name = player.anim_name.replace('walk','')
            player.anim_time = 0


class Monster(Animated):
    x = 0
    y = 0
    hp = 10
    animation = None

class Game:
    def __init__(self):
        self.player = Player()
        self.tilemap = Tilemap('data/pics/urban.png')
        self.ground_tiles = {}
        self.ground_tiles_by_no = {}
        self.furniture_tiles = {}
        self.furniture_tiles_by_no = {}
        self.rooms = {}
        self.current_room = Room()
        self.monsters = []
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
        def add_furniture_tile(name, x, y,
                     can_go=True,
                     can_fly=True,
                     on_stand=None,
                     door_letter='\0'):
            t = FurnitureTile()
            t.no = self.tilemap.no_from_xy(x, y)
            t.name = name
            t.can_go = can_go
            t.can_fly = can_fly
            t.door_letter = door_letter
            self.furniture_tiles[name] = t
            self.furniture_tiles_by_no[t.no] = t

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

        add_furniture_tile('sofa', 11, 4, can_go=False)
        add_furniture_tile('tables', 12, 4, can_go=False)
        add_furniture_tile('shelve', 12, 5, can_go=False)
        add_furniture_tile('tabler', 13, 4, can_go=False)
        add_furniture_tile('tree', 14, 4,  can_go=False)
        add_furniture_tile('waste', 15, 0,  can_go=False)
        add_furniture_tile('tank', 11, 0,  can_go=False)

    def init(self):
        self.player_animation = CleanerAnimation(self.tilemap)
        self.bot_animation = BotAnimation(self.tilemap)
        self.bin_animation = BinAnimation(self.tilemap)
        self.cleaner_animation = CleanerAnimation(self.tilemap)

        self.load('')

    def create_monster(self, x, y, gid):
        m = Monster()
        m.x = x
        m.y = y
        if gid == 5: # cleaner
            m.animation = self.cleaner_animation
            m.hp = 20
        elif gid == 69: # bin
            m.animation = self.bin_animation
            m.hp = 20
        elif gid == 161: # bot
            m.animation = self.bot_animation
            m.hp = 20
        elif gid == 53: # dead bin
            m.animation = self.bin_animation
            m.hp = 0
        else:

            raise Exception('Unknown monster gid {} = {}:{}'.format(
                repr(gid),
                gid % 16,
                gid // 16
            ))
        return m
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

        for e in range(len(js['layers'][1]['data'])):
            idx = int(js['layers'][1]['data'][e]) -1
            x = e % self.level.w
            y = e // self.level.w
            fur = self.furniture_tiles_by_no.get(idx)
            if not fur and idx != -1:
                print('bad fur: {} ({} {})'.format(idx, idx % 16, idx // 16))
            self.level.cells[e].furniture = fur or None

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
            if 'gid' in o:
                m = self.create_monster(int(o['x']), int(o['y']), int(o['gid']))
                self.monsters.append(m)
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
        'mhhikm ig  ',  # e |
        'h   A      ',  # i |
        '3Ch Bm   f ',  # o | OLD
        'h    3E    ',  # m |
        'h 3  Dl    ',  # n |
        '  m l     W',  # q
        '  m i  W   ',  # w
        '  k h    i ',  # f
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
             "W" : "vi",
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
                #if not cell.marked:
                self.tilemap.draw(cell.ground,
                                  a, b)
                if cell.furniture:
                    self.tilemap.draw(cell.furniture,
                                  a, b)

        self.player.process(self)
        #print (self.player.x - self.current_room.x,
        #       self.player.y - self.current_room.y)
        for c in self.level.cells:
            c.marked = False
        c = self.get_cell_for_pxpy(self.player.x, self.player.y)
        c.marked = True
        self.tilemap.draw(self.player_animation.anim_tile(self.player),
                          (self.player.x - self.current_room.x)*2,
                           (self.player.y - self.current_room.y)*2)

        for m in self.monsters:
            self.tilemap.draw(m.animation.anim_tile(m),
                              (m.x - self.current_room.x) * 2,
                              (m.y - self.current_room.y) * 2)

        self.tilemap.end_draw()
