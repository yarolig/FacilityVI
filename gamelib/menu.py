
import pyglet
from pyglet.gl import *

class CheckedState:
    NA = 0
    CHECKED = 1
    UNCHECKED = -1

def never_mind(*args, **kwargs):
    pass


class MegaLabel:
    checked = CheckedState.NA
    enabled = True
    text = ''
    click_handler = never_mind

    def __init__(self, text="qwe",pos=None):
        x, y = pos
        self.text = text
        self.label=pyglet.text.DocumentLabel(text,
            font_name='Times New Roman',
            font_size=36,
            x=x, y=y)

    def click(self, x, y):
        if not self.enabled:
            return
        self.checked *= -1
        self.click_handler(x,y)
        if self.checked != 0:
            prefix = {0: '', 1: '[v] ', -1: '[ ] '}[self.checked]
            self.label.text = prefix + self.text

    def draw(self):
        self.label.draw()


class Menu:
    def __init__(self):
        pass

    def add_button(self, text):
        pass

    def add_checkbox(self, text):
        pass

    def draw(self):
        pass

    def on_click(self, x, y):
        pass
    def on_key(self, key):
        pass


