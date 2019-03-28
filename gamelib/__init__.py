
import json


from OpenGL.GL import *
from OpenGL.GLU import *
def load(self, filename):
    js = json.loads(open('data/facility.json').read())
    self.w = int(js['layers'][0]['width'])
    self.h = int(js['layers'][0]['height'])
    self.cells = [Cell() for i in range(self.w * self.h)]
    for e in range(len(js['layers'][0]['data'])):
        idx = int(js['layers'][0]['data'][e])
        x = e % self.w
        y = e // self.w
