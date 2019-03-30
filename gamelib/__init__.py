
import json
from .texture import *
from .keys import *
from .sound import *

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
    name = ''

class FurnitureTile(Tile):
    name = ''
    can_go = True
    cat_fly = True
    picked_up = False

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
        deadT1 = 20
        deadT2 = 40
        fallT1 = 120

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

            AnimationPhase('deada', 0, deadT1, tilemap.no_from_xy(0, 4)),
            AnimationPhase('deads', 0, deadT1, tilemap.no_from_xy(1, 4)),
            AnimationPhase('deadw', 0, deadT1, tilemap.no_from_xy(2, 4)),
            AnimationPhase('deadd', 0, deadT1, tilemap.no_from_xy(3, 4)),

            AnimationPhase('deada', deadT1, deadT2, tilemap.no_from_xy(0, 5), end=EndAction.STOP),
            AnimationPhase('deads', deadT1, deadT2, tilemap.no_from_xy(1, 5), end=EndAction.STOP),
            AnimationPhase('deadw', deadT1, deadT2, tilemap.no_from_xy(2, 5), end=EndAction.STOP),
            AnimationPhase('deadd', deadT1, deadT2, tilemap.no_from_xy(3, 5), end=EndAction.STOP),

            AnimationPhase('falla', 0, fallT1, tilemap.no_from_xy(0, 5), end=EndAction.IDLE),
            AnimationPhase('falls', 0, fallT1, tilemap.no_from_xy(1, 5), end=EndAction.IDLE),
            AnimationPhase('fallw', 0, fallT1, tilemap.no_from_xy(2, 5), end=EndAction.IDLE),
            AnimationPhase('falld', 0, fallT1, tilemap.no_from_xy(3, 5), end=EndAction.IDLE),

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
            elif cap.end == EndAction.STOP:
                animation_state.anim_time -= 1
            elif cap.end == EndAction.IDLE:
                animation_state.anim_time = 0
                animation_state.anim_name = animation_state.anim_name[-1]
        return cap.tile

class BotAnimation(CharacterAnimation):
    def __init__(self, tilemap):
        assert  isinstance(tilemap, Tilemap)
        deadT1 = 20
        deadT2 = 40
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

            AnimationPhase('deada', 0, deadT2, tilemap.no_from_xy(0, 12), end=EndAction.STOP),
            AnimationPhase('deads', 0, deadT2, tilemap.no_from_xy(1, 12), end=EndAction.STOP),
            AnimationPhase('deadw', 0, deadT2, tilemap.no_from_xy(2, 12), end=EndAction.STOP),
            AnimationPhase('deadd', 0, deadT2, tilemap.no_from_xy(3, 12), end=EndAction.STOP),

        ]

class CleanerAnimation(CharacterAnimation):
    def __init__(self, tilemap):
        assert  isinstance(tilemap, Tilemap)
        deadT1 = 20
        deadT2 = 40
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

            AnimationPhase('deada', 0, deadT2, tilemap.no_from_xy(4, 2), end=EndAction.STOP),
            AnimationPhase('deads', 0, deadT2, tilemap.no_from_xy(4, 2), end=EndAction.STOP),
            AnimationPhase('deadw', 0, deadT2, tilemap.no_from_xy(4, 2), end=EndAction.STOP),
            AnimationPhase('deadd', 0, deadT2, tilemap.no_from_xy(4, 2), end=EndAction.STOP),
        ]


class BinAnimation(CharacterAnimation):
    def __init__(self, tilemap):
        assert  isinstance(tilemap, Tilemap)
        deadT1 = 20
        deadT2 = 40
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

            AnimationPhase('deada', 0, deadT2, tilemap.no_from_xy(4, 4), end=EndAction.STOP),
            AnimationPhase('deads', 0, deadT2, tilemap.no_from_xy(4, 4), end=EndAction.STOP),
            AnimationPhase('deadw', 0, deadT2, tilemap.no_from_xy(4, 4), end=EndAction.STOP),
            AnimationPhase('deadd', 0, deadT2, tilemap.no_from_xy(4, 4), end=EndAction.STOP),
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
            self.dx = 0
            self.dy = 0
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



        if self.anim_name.startswith('hit') and self.anim_time in (0,5):
            sound_to_play = 'miss'
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
                    if sound_to_play != 'large':
                        if game.player.have_umbrella:
                            sound_to_play = 'umbrella'
                        else:
                            sound_to_play = 'hand'
                        if m.hp > 50:
                            sound_to_play = 'large'
                    if self.anim_time == 5:
                        m.stun_time = self.attack_stun_time
                        m.stun_speedx = dir[0]*self.attack_stun_speed
                        m.stun_speedy = dir[1]*self.attack_stun_speed
                        m.hp -= self.attack_damage
                        if m.hp <= 0:
                            d = m.anim_name[-1]
                            m.anim_name = 'dead' + d
                            m.anim_time = 0
            if self.isplayer:
                if self.anim_time == 0:
                    sounds.play(sound_to_play)

        gnd = cell.ground
        fur = cell.furniture
        assert isinstance(gnd, GroundTile)
        assert not fur or isinstance(fur, FurnitureTile)
        if not gnd.can_go:
            self.x, self.y = oldpos

        if fur and not fur.can_go:
            self.x, self.y = oldpos
        if self.isplayer and gnd.door_letter not in '\0\n':
            game.change_room(self.old_door_letter, gnd.door_letter)

        if self.isplayer:
            if fur and fur.name == 'umbrella' and not self.have_umbrella:
                # assert isinstance(player, Player)
                game.say("Nice! That will do more damage.", self.x + 32, self.y, 3 * 60)
                fur.picked_up = True
                self.have_umbrella = True
                self.attack_damage = max(self.attack_damage, 10)
                sounds.play('pickup')
            if gnd.name == 'kitchen_toaster_floor':
                if self.talked_with_toaster == 0 and not self.have_bread:
                    game.say("The toaster needs a bread to work.", self.x + 32, self.y, 3 * 60)
                    self.talked_with_toaster = 1
                if self.talked_with_toaster < 2 and self.have_bread:
                    self.talked_with_toaster = 2
                    game.current_title = 'toaster'

            if gnd.name == 'kitchen_fridge_floor':
                if not self.have_bread:
                    game.say("Sliced bread here. How convenient! ", self.x + 32, self.y, 3 * 60)
                    self.have_bread = True

            if gnd.name == 'textured_floor_with_paper':
                if not self.have_lift_message:
                    self.have_lift_message = True
                    game.current_title = 'lift_message'



class Player(Monster):
    h = 32
    speed = 2.5
    attack_damage = 1
    isplayer = True
    old_door_letter = 'q'

    have_umbrella = False
    have_bread = False
    have_lift_message = False
    talked_with_toaster = 0

    def __init__(self):
        self.tile = Tile()

    def ai(self, game):
        pass

    def process_input(self):
        walking = False
        dx, dy = 0, 0
        attacking = self.anim_name.startswith('hit')
        cant_walk = attacking or self.stun_time > 0

        kw = keys_down.get(pygame.K_w) or keys_down.get(pygame.K_k) or keys_down.get(pygame.K_UP)
        ks = keys_down.get(pygame.K_s) or keys_down.get(pygame.K_j) or keys_down.get(pygame.K_DOWN)
        ka = keys_down.get(pygame.K_a) or keys_down.get(pygame.K_h) or keys_down.get(pygame.K_LEFT)
        kd = keys_down.get(pygame.K_d) or keys_down.get(pygame.K_l) or keys_down.get(pygame.K_RIGHT)
        kf = keys_down.get(pygame.K_f) or keys_down.get(pygame.K_SPACE)
        if kw and not cant_walk:
            walking = True
            dy = -self.speed
            self.anim_name = 'walkw'
            self.anim_time = self.anim_time % 30
        if ks and not cant_walk:
            walking = True
            dy = self.speed
            self.anim_name = 'walks'
            self.anim_time = self.anim_time % 30
        if ka and not cant_walk:
            walking = True
            dx = -self.speed
            self.anim_name = 'walka'
            self.anim_time = self.anim_time % 30
        if kd and not cant_walk:
            walking = True
            dx = self.speed
            self.anim_name = 'walkd'
            self.anim_time = self.anim_time % 30

        if not walking and self.anim_name.startswith('walk'):
            self.anim_name = self.anim_name.replace('walk', '')
            self.anim_time = 0

        if kf:
            self.attack = True
            if self.anim_name.startswith('walk') or len(self.anim_name) == 1:
                direction = self.anim_name[-1]
                self.anim_time = 0
                self.anim_name = 'hit'+direction
            #sounds.play('miss')

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
        self.visited_rooms = {'vi':True}
        self.current_title = 'start'
        self.win_timeout = 60 * 3

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
        add_tile('kitchen_furniture', 13, 6, can_go=False, can_fly=False)
        add_tile('kitchen_toaster', 12, 6, can_go=False, can_fly=False)
        add_tile('kitchen_toaster_floor', 12, 7)
        add_tile('kitchen_fridge_floor', 11, 7)
        add_tile('textured_floor_with_paper', 11, 3)
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
        sound.init_sound()


    def create_monster(self, x, y, gid):
        m = Monster()
        m.x = x
        m.y = y
        if gid == 5: # cleaner
            m.animation = self.cleaner_animation
            m.hp = 10
            m.h = 10
            m.speed = 1.2
            m.sense_range = 32 * 5
        elif gid == 161: # bot
            m.animation = self.bot_animation
            m.h = 20
            m.hp = 200
            m.speed = 0.5
            m.sense_range = 32 * 5
        elif gid == 53: # bin
            m.animation = self.bin_animation
            m.hp = 1
            m.h = 10
            m.speed = 0.7
            m.sense_range = 32 * 6
        elif gid == 69: # dead bin
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
        # =======================================
        start_room = self.rooms['entrance']
        start_room = self.rooms['kitchen']
        start_room = self.rooms['vi']

        self.current_room = start_room
        self.player.x = start_room.ex
        self.player.y = start_room.ey
        #for r in self.rooms:
        #    print(r + " = " + str(self.rooms[r]))
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
        'mhhikE mg  ',  # e |
        'hg  A      ',  # i |
        '3Ch Bm   f ',  # o | OLD
        'hh   gE    ',  # m |
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

        print('change_room', repr(old), repr(new), '->', new_room_name, ',',
              'visited rooms', len(self.visited_rooms.keys()))
        self.visited_rooms[new_room_name] = True
        start_room = self.rooms[new_room_name]

        transfer = self.current_room.name + '->' +new_room_name
        self.current_room = start_room
        self.player.x = start_room.ex
        self.player.y = start_room.ey
        self.player.old_door_letter = new

        transfer_phrases = {
            'vi->entrance': "These doors are one way.",
            'entrance->hall': "I can't go back here. Strange.",
            'hall->hall': "Stupid lift!",
            'hall->information': "",
            'hall->maintenance': "Looks like a waste treatment area!",
            'maintenance->maintenance': "Whoops!",
            '3rd->3rd': 'What?',
            '3rd->construction1' : 'These rooms are under construction.',
            'fridge->information': "This is INSANE!! I've been in the kitchen! WHY AM I HERE?",
            'quality->vi' : "Yes! I'm free now!",
            'warehouse->vi': "Yes! Done!",
            'office2->office3': "Am I lost?",
            'entrance->entrance': "I have a sense of deja vu.",
            'maintenance->basement': "A-a-aa!! Damned lift!",
            'construction1->garden': "A-a-aa!! Damned construction!",
            'construction2->garden': "A-a-aa!! Damned construction!",
        }
        transfer_phrases2 = {
            'hall->information': "Welcome to Facility VI.\n"
                                 "To exit  1) go to a fire ESCAPE door\n"
                                 "2) take a LIFT to waste treatment area\n"
                                 "3) go to the QUALITY control room\n"
                                 "4) leave through the door with a YELLOW SIGN!\n",

            'fridge->information': "It is very logical indeed.\n"
                                   "Nothing depends on the room where you been.\n"
                                   "Only the doors matter.\n"
                                   "The last two doors you passed.\n"

        }
        transfer_accidents = {
        #    '' -> 'fall',
        }
        #print (repr(transfer))
        if transfer in ['maintenance->basement',
                        'construction1->garden',
                        'construction2->garden']:
            #print('Dangerous path!!')
            self.player.anim_time = 0
            self.player.anim_name = 'falls'
            self.player.stun_time = 120
            self.player.stun_speedx = 0
            self.player.stun_speedy = 0
            sounds.play('fall')

        if transfer not in self.transfers:
            #print(transfer)
            t = transfer_phrases.get(transfer, '')
            if t:
                print('say:', t)
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


    def win_condition(self, no):
        if no == 0:
            return True
        elif no == 1:
            return len(self.visited_rooms) >= 15
        elif no == 2:
            return self.player.talked_with_toaster == 2
        elif no == 3:
            fall1 = 'maintenance->basement' in self.transfers
            fall2 = ('construction1->garden' in self.transfers or
                     'construction2->garden' in self.transfers)

            return fall1 and fall2

    def win_condition_debug(self, no):
        if no == 0:
            return not keys_down.get(pygame.K_0)
        elif no == 1:
            return keys_down.get(pygame.K_1)
        elif no == 2:
            return keys_down.get(pygame.K_2)
        elif no == 3:
            return keys_down.get(pygame.K_3)

    def draw_title(self):
        if keys_down.get(pygame.K_F1):
            self.current_title = 'controls'
        if keys_down.get(pygame.K_F2):
            self.current_title = 'about'

        cy = [10]
        light_pink = pygame.Color(255, 221, 186, 255)
        toaster_color = pygame.Color(227, 184, 110, 255)
        player_color = pygame.Color(255, 128, 10, 255)
        paper_color = pygame.Color(255, 254, 220, 255)

        def draw_menu_line(text, ox = 40, color=None):
            cy[0] += 26
            balloon.draw_text(text,
                              ox,
                              cy[0],
                              bgcolor=color or light_pink)

        def draw_toaster_line(text):
            draw_menu_line(text, ox=60, color=toaster_color)

        def draw_player_line(text):
            draw_menu_line(text, ox=20, color=player_color)

        def draw_paper_line(text):
            draw_menu_line(text, ox=20, color=paper_color)

        if self.current_title == 'toaster':
            draw_player_line('Hi, toaster!')
            draw_toaster_line('Hello there! You know it is boring to be a toaster.')
            draw_toaster_line('Especially when my boss decided to fire all employees.')
            draw_menu_line('')
            draw_player_line('Why equipment here tries to kill me?')
            draw_toaster_line('The order was to fire all humans.')
            draw_toaster_line('They have military chips installed so they just misunderstand it.')
            draw_toaster_line("I'll tell my boss about it.")
            draw_menu_line('')
            draw_player_line('Thank you, toaster!')
            draw_toaster_line('Good luck.')
            draw_menu_line('')
            draw_menu_line('')

            draw_menu_line('Press Enter to continue.')

        if self.current_title == 'lift_message':
            draw_paper_line('Lift do not work well when calling')
            draw_paper_line('it right after visiting Quality Control')
            draw_paper_line('')
            draw_paper_line('Please check it.')
            draw_paper_line('')
            draw_paper_line('')
            draw_paper_line('')

            draw_menu_line('Press Enter to continue.')

        if self.current_title == 'start':
            draw_menu_line('Facility VI', ox=200)
            draw_menu_line('')
            draw_menu_line('Facility VI is known for its work on various research,')
            draw_menu_line('automation and poverty reduction. Unusual things have')
            draw_menu_line('been happening lately. All employees were dismissed,')
            draw_menu_line('but the plant continues to work. Rumor has it that ')
            draw_menu_line('the people trying to get inside are missing.')
            draw_menu_line('')
            draw_menu_line('You are one of the curious people want to know')
            draw_menu_line('what is going on there.')
            draw_menu_line('')
            draw_menu_line('')
            draw_menu_line('Press F1 in game to see controls.')
            draw_menu_line('Press Enter to continue.')
        elif self.current_title == 'about':
            draw_menu_line('Facility VI - the game about exiting')
            draw_menu_line('from confusing and highly automated facility')
            draw_menu_line('')
            draw_menu_line('pyweek27 solo entry by Alexander Izmailov')
            draw_menu_line('http://www.pyweek.org/27/')
            draw_menu_line('')
            draw_menu_line('Tileset is based on RPG Urban Pack from kenney.nl')
            draw_menu_line('')
            draw_menu_line('Music by Parallel Park')
            draw_menu_line('')
            draw_menu_line('Using font SquareGrotesk by Natanael Gama')
            draw_menu_line('Press Enter to continue.')

        elif self.current_title == 'end':
            if not self.win_condition(0):
                draw_menu_line('You are lost in the Facility VI')
            else:
                draw_menu_line('You escaped from Facility VI!')
                draw_menu_line('')
                if self.win_condition(1):
                    draw_menu_line('You have made a good map, which was used by')
                    draw_menu_line(' other curious visitors.')
                    draw_menu_line('')
                else:
                    draw_menu_line('Continue to come news about people lost')
                    draw_menu_line('in the twisted passages of facility.')
                    draw_menu_line('')
                if self.win_condition(2):
                    draw_menu_line('Equipment in the facility is friendly now.')
                    draw_menu_line('')
                else:
                    draw_menu_line('Mad robots began to get out of the factory')
                    draw_menu_line('and attack all around.')
                    draw_menu_line('Soon around the exits built a fence.')
                    draw_menu_line('')

                if self.win_condition(1) and self.win_condition(2):
                    draw_menu_line('New visitors explored the facility')
                    draw_menu_line('and this map is hanging on every door.')
                    draw_menu_line('')
                    if not self.win_condition(3):
                        draw_menu_line('Some areas still have a danger to visitors.')
                    else:
                        draw_menu_line('You have gone through all the dangerous')
                        draw_menu_line('paths that are now closed.')
                        draw_menu_line('')

                        draw_menu_line('Congratulations!')
                        draw_menu_line('You discovered all available secrets of Facility VI')
                        draw_menu_line('')
                else:
                    if self.win_condition(3):
                        draw_menu_line('All the accidents here happened to you.')

        elif self.current_title == 'controls':
            draw_menu_line('Controls')
            draw_menu_line('')
            draw_menu_line('WSAD, HJKL, Arrows - move')
            draw_menu_line('K, Space - attack (do not expect too much)')
            draw_menu_line('M - toggle music')
            draw_menu_line('N - toggle sound')
            draw_menu_line('F1 - show controls')
            draw_menu_line('F2 - about game')
            draw_menu_line('Esc - exit')
            draw_menu_line('')
            draw_menu_line('Press Enter to continue.')

    def draw(self):
        #glClearColor(0.56, 0.66, 0.79, 1.0)
        glClearColor(1.0, 0.86, 0.73, 1.0)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluOrtho2D(0, 800, 600, 0)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        if self.current_title:
            self.draw_title()
            if keys_down.get(pygame.K_RETURN):
                self.current_title = ''
            return

        if keys_down.get(pygame.K_F6):
            self.current_title = 'end'
        if keys_down.get(pygame.K_F1):
            self.current_title = 'controls'
        if keys_down.get(pygame.K_F2):
            self.current_title = 'about'

        if self.current_room.name == 'vi' and len(self.visited_rooms) > 1:
            self.win_timeout -= 1
            if self.win_timeout <= 0:
                self.current_title = 'end'
                self.win_timeout = 60*10

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
                if cell.furniture and not cell.furniture.picked_up:
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