
import json
from .texture import *
from .keys import *


from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
import pygame.freetype
import math
import random
from .balloon import *

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
    IDLE = 3

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
        hitT1 = 5
        hitT2 = 20
        hitT3 = 25
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

            AnimationPhase('hita', 0, hitT1, tilemap.no_from_xy(0, 6)),
            AnimationPhase('hits', 0, hitT1, tilemap.no_from_xy(1, 6)),
            AnimationPhase('hitw', 0, hitT1, tilemap.no_from_xy(2, 6)),
            AnimationPhase('hitd', 0, hitT1, tilemap.no_from_xy(3, 6)),

            AnimationPhase('hita', hitT1, hitT2, tilemap.no_from_xy(0, 3), end=EndAction.NONE),
            AnimationPhase('hits', hitT1, hitT2, tilemap.no_from_xy(1, 3), end=EndAction.NONE),
            AnimationPhase('hitw', hitT1, hitT2, tilemap.no_from_xy(2, 3), end=EndAction.NONE),
            AnimationPhase('hitd', hitT1, hitT2, tilemap.no_from_xy(3, 3), end=EndAction.NONE),

            AnimationPhase('hita', hitT2, hitT3, tilemap.no_from_xy(0, 0), end=EndAction.IDLE),
            AnimationPhase('hits', hitT2, hitT3, tilemap.no_from_xy(1, 0), end=EndAction.IDLE),
            AnimationPhase('hitw', hitT2, hitT3, tilemap.no_from_xy(2, 0), end=EndAction.IDLE),
            AnimationPhase('hitd', hitT2, hitT3, tilemap.no_from_xy(3, 0), end=EndAction.IDLE),
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
            elif cap.end == EndAction.IDLE:
                animation_state.anim_time = 0
                animation_state.anim_name = animation_state.anim_name[-1]
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
            AnimationPhase('a', 0, 15, tilemap.no_from_xy(4, 3), end=EndAction.LOOP),
            AnimationPhase('s', 0, 15, tilemap.no_from_xy(4, 3), end=EndAction.LOOP),
            AnimationPhase('w', 0, 15, tilemap.no_from_xy(4, 3), end=EndAction.LOOP),
            AnimationPhase('d', 0, 15, tilemap.no_from_xy(4, 3), end=EndAction.LOOP),

            AnimationPhase('walka', 0, 15, tilemap.no_from_xy(4, 3)),
            AnimationPhase('walks', 0, 15, tilemap.no_from_xy(4, 3)),
            AnimationPhase('walkw', 0, 15, tilemap.no_from_xy(4, 3)),
            AnimationPhase('walkd', 0, 15, tilemap.no_from_xy(4, 3)),

            AnimationPhase('walka', 15, 30, tilemap.no_from_xy(4, 3), end=EndAction.LOOP),
            AnimationPhase('walks', 15, 30, tilemap.no_from_xy(4, 3), end=EndAction.LOOP),
            AnimationPhase('walkw', 15, 30, tilemap.no_from_xy(4, 3), end=EndAction.LOOP),
            AnimationPhase('walkd', 15, 30, tilemap.no_from_xy(4, 3), end=EndAction.LOOP),
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


def rect_intersect(x,y,w,h,xx,yy,ww,hh):
    xoverlap = (xx <= x <= xx + ww) or (x <= xx <= x + w)
    yoverlap = (yy <= y <= yy + hh) or (y <= yy <= y + h)
    return xoverlap and yoverlap

def sign(i):
    if i > 0: return 1
    if i < 0: return -1
    return 0

class Monster(Animated):
    x = 0
    y = 0
    h = 32
    hp = 10
    dx = 0
    dy = 0
    attack_range = 32
    attack_stun_time = 20
    attack_stun_speed = 2
    attack_damage = 0
    stun_time = 0
    stun_speedx = 0
    stun_speedy = 0
    attack = False
    isplayer = False
    animation = None
    sense_range = 32 * 5
    stop_range = 20
    speed = 1

    def ai(self, game):
        walking = False
        dx, dy = 0, 0
        if self.hp <= 0:
            return

        p = game.player
        dist_to_player = ((p.x - self.x) ** 2 + (p.y - self.y) ** 2) ** 0.5
        dist_to_player = int(dist_to_player)
        if self.stop_range <= dist_to_player <= self.sense_range:
            dx = sign(p.x - self.x) * self.speed
            dy = sign(p.y - self.y) * self.speed
            if math.fabs(p.x - self.x) < self.speed:
                dx = 0
            if math.fabs(p.y - self.y) < self.speed:
                dy = 0

        if dx > 0:
            self.anim_name = 'walkd'
            self.anim_time = self.anim_time % 30
        elif dx < 0:
            self.anim_name = 'walka'
            self.anim_time = self.anim_time % 30
        elif dy > 0:
            self.anim_name = 'walks'
            self.anim_time = self.anim_time % 30
        elif dy < 0:
            self.anim_name = 'walkw'
            self.anim_time = self.anim_time % 30
        else:
            self.anim_name = self.anim_name.replace('walk', '')
            self.anim_time = 0
        self.dx = dx
        self.dy = dy


    def process(self, game):
        assert isinstance(game, Game)
        player = self
        oldpos = self.x, self.y
        dx = self.dx
        dy = self.dy
        if self.stun_time > 0:
            self.stun_time -= 1
            dx = self.stun_speedx
            dy = self.stun_speedy
            if self.stun_time == 0:
                dx = 0
                dy = 0
                self.stun_speedx = 0
                self.stun_speedy = 0

        def can_go(x, y):
            for dx, dy in [(0, 0), (-10, 0), (10, 0),
                           (0, -15), (-10, -15), (10, -15), ]:
                cell = game.get_cell_for_pxpy(x + dx, y + dy)
                gnd = cell.ground
                fur = cell.furniture
                assert isinstance(gnd, GroundTile)
                if not gnd.can_go:
                    return False
                if fur and not fur.can_go:
                    return False
                if gnd.door_letter != '\0':
                    break
            for m in game.monsters:
                if m is self:
                    continue
                if m.hp <= 0:
                    continue
                if rect_intersect(x, y, 32, self.h, m.x, m.y, 32, m.h):
                    if not rect_intersect(self.x, self.y, 32, self.h, m.x, m.y, 32, m.h):
                        return False
            return True

        if can_go(self.x + dx, self.y + dy):
            self.x, self.y = self.x + dx, self.y + dy
        elif can_go(self.x + dx, self.y):
            self.x, self.y = self.x + dx, self.y
        elif can_go(self.x, self.y + dy):
            self.x, self.y = self.x, self.y + dy

        cell = game.get_cell_for_pxpy(self.x, self.y)
        # print (cell, cell.ground)

        if self.anim_name.startswith('hit') and self.anim_time == 5:
            l2d={'w':(0,-1), 's':(0,1), 'a':(-1,0), 'd':(1,0), }
            dir = l2d[self.anim_name[-1]]
            x = self.x + dir[0]*self.attack_range
            y = self.y + dir[1]*self.attack_range
            for m in game.monsters:
                if m is self:
                    continue
                if m.hp <= 0:
                    continue
                if rect_intersect(x, y, 32, self.h, m.x, m.y, 32, m.h):
                    # hit monster
                    m.stun_time = self.attack_stun_time
                    m.stun_speedx = dir[0]*self.attack_stun_speed
                    m.stun_speedy = dir[1]*self.attack_stun_speed

        gnd = cell.ground
        fur = cell.furniture
        assert isinstance(gnd, GroundTile)
        if not gnd.can_go:
            self.x, self.y = oldpos

        if fur and not fur.can_go:
            self.x, self.y = oldpos
        if self.isplayer and gnd.door_letter not in '\0\n':
            game.change_room(self.old_door_letter, gnd.door_letter)


class Player(Monster):
    h = 32
    speed = 2.5
    isplayer = True
    old_door_letter = ':'
    def __init__(self):
        self.tile = Tile()

    def ai(self, game):
        pass

    def process_input(self):
        walking = False
        dx, dy = 0, 0
        attacking = self.anim_name.startswith('hit')
        if keys_down.get(pygame.K_w) and not attacking:
            walking = True
            dy = -self.speed
            self.anim_name = 'walkw'
            self.anim_time = self.anim_time % 30
        if keys_down.get(pygame.K_s) and not attacking:
            walking = True
            dy = self.speed
            self.anim_name = 'walks'
            self.anim_time = self.anim_time % 30
        if keys_down.get(pygame.K_a) and not attacking:
            walking = True
            dx = -self.speed
            self.anim_name = 'walka'
            self.anim_time = self.anim_time % 30
        if keys_down.get(pygame.K_d) and not attacking:
            walking = True
            dx = self.speed
            self.anim_name = 'walkd'
            self.anim_time = self.anim_time % 30

        if not walking and self.anim_name.startswith('walk'):
            self.anim_name = self.anim_name.replace('walk', '')
            self.anim_time = 0

        if keys_down.get(pygame.K_f):
            self.attack = True
            if self.anim_name.startswith('walk') or len(self.anim_name) == 1:
                direction = self.anim_name[-1]
                self.anim_time = 0
                self.anim_name = 'hit'+direction

        self.dx = dx
        self.dy = dy


class Phrase:
    x = 0
    y = 0
    ttl = 60 * 5
    text = "It's INSANE!"
    color = None
    def draw(self, game):
        if self.ttl > 0:
            balloon.draw_text(self.text,
                (self.x - game.current_room.x) * 2,
                (self.y - game.current_room.y) * 2,
                              bgcolor=self.color)

            self.ttl -= 1

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
        self.monsters = [self.player]
        self.phrases = []
        self.transfers = {}
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
        add_furniture_tile('terminal', 10, 4, can_go=False)
        add_furniture_tile('tables', 12, 4, can_go=False)
        add_furniture_tile('umbrella', 13, 5, can_go=True)
        add_furniture_tile('shelve', 12, 5, can_go=False)
        add_furniture_tile('tabler', 13, 4, can_go=False)
        add_furniture_tile('tree', 14, 4,  can_go=False)
        add_furniture_tile('waste', 15, 0,  can_go=False)
        add_furniture_tile('tank', 11, 0,  can_go=False)
        add_furniture_tile('grate', 13, 0,  can_go=False)
        add_furniture_tile('fridge', 11, 6,  can_go=False)

    def init(self):
        self.player_animation = CharacterAnimation(self.tilemap)
        self.bot_animation = BotAnimation(self.tilemap)
        self.bin_animation = BinAnimation(self.tilemap)
        self.cleaner_animation = CleanerAnimation(self.tilemap)

        self.load('')
        balloon.init()

    def create_monster(self, x, y, gid):
        m = Monster()
        m.x = x
        m.y = y
        if gid == 5: # cleaner
            m.animation = self.cleaner_animation
            m.hp = 20
            m.h = 10
            m.speed = 1.2
            m.sense_range = 32 * 5
        elif gid == 69: # bin
            m.animation = self.bin_animation
            m.hp = 20
            m.h = 10
            m.speed = 0.7
            m.sense_range = 32 * 6
        elif gid == 161: # bot
            m.animation = self.bot_animation
            m.h = 20
            m.hp = 20
            m.speed = 0.5
            m.sense_range = 32 * 5
        elif gid == 53: # dead bin
            m.animation = self.bin_animation
            m.h = 10
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
                m = self.create_monster(int(o['x']),
                                        int(o['y']) - 32,
                                        int(o['gid']))
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
        'mhhikm mg  ',  # e |
        'h   A      ',  # i |
        '3Ch Bm   f ',  # o | OLD
        'hg   3E    ',  # m |
        'h 3  Dl    ',  # n |
        'R m l     W',  # q
        '  m i  W   ',  # w
        '  k h    i ',  # f
        '           ',  # !
        ]
        short_names = {
             "3" : "3rd",
             "R" : "basement",
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

        transfer = self.current_room.name + '->' +new_room_name
        self.current_room = start_room
        self.player.x = start_room.ex
        self.player.y = start_room.ey
        self.player.old_door_letter = new

        transfer_phrases = {
            'entrance->hall': "I can't go back here. Strange.",
            'hall->hall': "Stupid lift!",
            'hall->information': "",
            'hall->maintenance': "Looks like a waste treatment area!",
            'maintenance->maintenance': "Whoops!",
            '3rd->3rd': 'What?',
            '3rd->construction1' : 'These rooms is under construction.',
            #'maintenance->maintenance': "Whoops!",
            'fridge->information': "This is INSANE!! I've been in the kithen! WHY AM I HERE?",
            'quality->vi' : "Yes! I'm free now!",
            'warehouse->vi': "Yes! Done!",
            'office2->office3': "Am I lost?",
            'maintenance->basement': "A-a-aa!! Damned lift!",
        }
        transfer_phrases2 = {
            'hall->information': "Welcome to Facility VI.\n"
                                 "To exit  1) go to fire ESCAPE door\n"
                                 "2) take LIFT to waste treatment area\n"
                                 "3) go to the QUALITY control room\n"
                                 "4) leave through the door with YELLOW SIGN!\n",

            'fridge->information': "It is very logical indeed.\n"
                                   "Nothing depends on room where you been.\n"
                                   "Only doors matter.\n"
                                   "The last two doors you passed.\n"

        }
        transfer_accidents = {
        #    '' -> 'fall',
        }

        if transfer not in self.transfers:
            print(transfer)
            t = transfer_phrases.get(transfer, '')
            if t:
                print('say', t)
                self.say(t, self.player.x + 32, self.player.y, 3 * 60)
            t2 = transfer_phrases2.get(transfer, '')
            if t2:
                print('say2', t2)
                yy = -118
                for tt in t2.split('\n'):
                    self.say(tt, self.player.x, self.player.y + yy, 10 * 60,)
                    yy += 14
        self.transfers[transfer] = True

    def get_cell_for_pxpy(self, px ,py):
        ii = int((px + 15) // 32)
        jj = int((py + 30) // 32)
        cell = self.level.cells[ii + jj * self.level.w]
        #print(ii, jj, cell)
        return cell

    def say(self, text, x, y, ttl, color=None):
        p = Phrase()
        p.text = text
        p.x = x
        p.y = y
        p.ttl = ttl
        p.color = color
        self.phrases.append(p)
        self.phrases = [p for p in self.phrases if p.ttl > 0]

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


        self.player.process_input()
        self.player.process(self)
        for m in self.monsters:
            assert isinstance(m, Monster)
            if m.isplayer:
                continue
            m.ai(self)
            m.process(self)
        #print (self.player.x - self.current_room.x,
        #       self.player.y - self.current_room.y)
        for c in self.level.cells:
            c.marked = False
        c = self.get_cell_for_pxpy(self.player.x, self.player.y)
        c.marked = True
        for m in self.monsters:
            if m.isplayer:
                continue
            self.tilemap.draw(m.animation.anim_tile(m),
                              (m.x - self.current_room.x) * 2,
                              (m.y - self.current_room.y) * 2)
        self.tilemap.draw(self.player_animation.anim_tile(self.player),
                          (self.player.x - self.current_room.x) * 2,
                          (self.player.y - self.current_room.y) * 2)

        self.tilemap.end_draw()
        unset_texture()
        for p in self.phrases:
            assert  isinstance(p, Phrase)
            p.draw(self)
        #balloon.draw_text("This is INSANE!", 100, 100)