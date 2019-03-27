#from . import data


import pyglet
from pyglet.gl import *
from pyglet import clock


config = pyglet.gl.Config()
config.double_buffer = True
window = pyglet.window.Window(config=config)
fps_display = pyglet.window.FPSDisplay(window)


print (config)
print (window)


class Cout:
    def __lshift__(self, other):
       print(other)
cout = Cout()


@window.event
def on_activate():
    cout << 'on activate'
    pass

@window.event
def on_close():
    cout << 'on close'
    pass

@window.event
def on_context_lost():
    cout << 'on c lost'
    pass

@window.event
def on_context_state_lost():
    cout << 'on c state lost'
    pass

@window.event
def on_deactivate():
    cout << 'on deactivate'
    pass

@window.event
def on_expose():
    cout << 'on expose'
    pass

@window.event
def on_hide():
    cout << 'on hide'
    pass

@window.event
def on_key_press(symbol, modifiers):
    cout << 'on k press %s %s' % (symbol, modifiers) 
    pass

@window.event
def on_key_release(symbol, modifiers):
    cout << 'on key release %s %s' % (symbol, modifiers)
    pass

@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    cout << ('on %d %d %d %d %s %s'%(x,y,dx,dy,button,modifiers)) 
    pass

@window.event
def on_mouse_enter(x, y):
    cout << 'on mouse enter'
    pass

@window.event
def on_mouse_leave(x, y):
    cout << 'on mouse leave'
    pass

@window.event
def on_mouse_motion(x, y, dx, dy):
    cout << 'on mouse motion'
    pass

@window.event
def on_mouse_press(x, y, button, modifiers):
    cout << 'on mouse press'
    pass

@window.event
def on_mouse_release(x, y, button, modifiers):
    cout << 'on mouse release'
    pass

@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    cout << 'on mouse scroll'
    pass

@window.event
def on_move(x, y):
    cout << 'on move'
    pass

@window.event
def on_show():
    cout << 'on show'
    pass



@window.event
def on_draw():
    cout << 'on_draw'
    redraw()
    
@window.event
def on_resize(width, height):
    glViewport(0, 0, width, height)
    return pyglet.event.EVENT_HANDLED

def redraw():
    dt = clock.tick()
    glClearColor(.3,.4,.5,1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    fps_display.draw()
    window.flip()

def nevermind(x):
    pass

#clock.set_fps_limit(60)
pyglet.clock.schedule_interval(nevermind, 1/59.0)
pyglet.app.run()






def main():
    #print(data.get_run_dir())
    pass
