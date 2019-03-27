



class Tilemap:
    mapw = 512
    maph = 512
    cellw = 32
    cellh = 32
    def __init__(self, filename):
        self.filename = filename
        self.tw = self.mapw // self.cellw
        self.th = self.maph // self.cellh

class TileDesc:
    cx = 0
    cy = 0
    cy0 = 0
    desc = {}
    tilemap = None
    def set_base(self, x, y):
        self.cx = x
        self.cy = y
        self.cy0 = y

    def add_desc(self, name):
        self.desc[name] = (self.cx, self.cy)
        self.cx += 1

    def newline(self):
        self.cy += 1
        self.cx = self.cy0

class TileBase:
    tilemap = None
    name = ''
    def __init__(self):
        self.pos_in_tilemap = (0, 0)

    def get_pos(self):
        return self.pos_in_tilemap

    def draw(self):
        pass

class AnimatedObject:
    anim_time = 0
    anim_name = ''

class EndAction:
    NONE = 0
    LOOP = 1
    STOP = 2

class Animation:
    def __init__(self, name, tfrom, tto, ox, oy, endaction=EndAction.NONE):
        self.name = name
        self.tfrom = tfrom
        self.tto = tto
        self.ox = ox
        self.oy = oy
        self.endaction = endaction

class AnimatedTile(TileBase):
    type_ox = 0
    type_oy = 0
    def __init__(self):
        self.anims = {}
    def get_anim(self, obj, name, time) -> Animation:
        assert isinstance(obj, AnimatedObject)
        for a in self.anims:
            if a.name == name and (a.tfrom <= time < a.tto):
                return a
        else:
            raise Exception("no anim "+name+"in"+obj)

    def draw(self, obj):
        assert isinstance(obj, AnimatedObject)
        anim = self.get_anim(obj, obj.anim_name, obj.anim_time)
        self.ox = anim.ox + self.type_ox
        self.oy = anim.oy + self.type_oy
        TileBase.draw(self)

        obj.anim_time += 1
        if obj.anim_time == anim.tto:
            if anim.endaction == EndAction.LOOP:
                obj.anim_time = 0
            elif anim.endaction == EndAction.STOP:
                obj.anim_time -= 1


class GroundTile(TileBase):
    pass


class CharacterTile(TileBase):
    pass

class ItemTile(TileBase):
    pass

class EffectTile(AnimatedObject):
    pass

class Item:
    name = 'umbrella'

class Monster:
    name = 'trashbin'
    x = 0
    y = 0

def load_tiles():
    tm = Tilemap('data/pics/urban.png')
    td = TileDesc()
    td.set_base(0, 0)
    td.add_desc('standA');td.add_desc('standS'); td.add_desc('standW'); td.add_desc('standD');
    td.add_desc('doA1');  td.add_desc('goS1');   td.add_desc('goW1');   td.add_desc('goD1');
    td.add_desc('doA2');  td.add_desc('goS2');   td.add_desc('goW2');   td.add_desc('goD2');
    td.add_desc('pushA');td.add_desc('pushS'); td.add_desc('pushW'); td.add_desc('pushD');
    td.add_desc('fallA');td.add_desc('fallS'); td.add_desc('fallW'); td.add_desc('fallD');
    td.add_desc('deadA');td.add_desc('deadS'); td.add_desc('deadW'); td.add_desc('deadD');


class Player(Monster):
    pass


class Cell:
    name = 'floor'

class CellRef:
    def __init__(self, cell, x, y, level):
        self.cell = cell
        self.x = x
        self.y = y
        self.level = level
    def draw(self):
        pass

class Level:
    w = 16
    h = 16
    def __init__(self):
        self.cells = [Cell() for i in range(self.w * self.h)]
        self.monsters = []
        self.items = []
        self.effects = []

    def enum_cells(self):
        for y in range(self.h):
            for x in range(self.w):
                yield  CellRef(self.cell(x, y), x, y, self)

    def cell(self, x, y):
        assert 0 <= x < self.w
        assert 0 <= y < self.h
        return self.cells[x+y*self.w]

    def draw(self):
        for e in self.enum_cells():
            e.draw()
        for e in self.items:
            e.draw()
        for e in self.monsters:
            e.draw()

