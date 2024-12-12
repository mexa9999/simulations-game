import pyglet as pg
from pyglet import shapes,clock
from pyglet.window import key
from functools import partial
import random
import math

class Engine(pg.window.Window):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.batch = pg.graphics.Batch()
        self.keys = {"w":False, "s":False, "a":False, "d":False}
        self.zoom_vector = pg.math.Vec3(1, 1, 1)
        self.move_vector = pg.math.Vec3(0, 0, 0)
        
        self.circle = shapes.Circle(100,100,50,color=(0,0,255), batch=self.batch)
        self.fps = pg.window.FPSDisplay(self)
        
        clock.schedule_interval(self.update, 1/60)
        
    def on_key_press(self, symbol, modifiers):
        if symbol == key.W:self.keys["w"] = True
        elif symbol == key.S:self.keys["s"] = True
        elif symbol == key.A:self.keys["a"] = True
        elif symbol == key.D:self.keys["d"] = True
        else: return
            
    def on_key_release(self, symbol, modifiers):
        if symbol == key.W:self.keys["w"] = False
        elif symbol == key.S:self.keys["s"] = False
        elif symbol == key.A:self.keys["a"] = False
        elif symbol == key.D:self.keys["d"] = False
        else: return
            
    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        self.zoom_vector.x += scroll_y/30
        self.zoom_vector.y += scroll_y/30
        
    def on_draw(self):
        self.clear()
        self.batch.draw()
        self.fps.draw()
    
    def update(self, dt):
        self.move_vector.x += (self.keys["a"]-self.keys["d"])*600*dt
        self.move_vector.y  += (self.keys["s"]-self.keys["w"])*600*dt
        self.view = self.view.from_scale(window.zoom_vector).from_translation(self.move_vector)
        
window = Engine(width=800, height=600, caption="game", resizable= True, vsync=False)
pg.app.run(1/1000000)