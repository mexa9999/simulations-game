import pygame as pg
from pygame import Color

class Cursor():
    
    def __init__(self, size:int, offset:int, window_size):
        
        self.size = size

        self.x = window_size/2 - size/2 - offset
        self.y = window_size/2 - size/2 - offset
        
    def move(self, speed_x:int, speed_y:int):
        self.x += speed_x
        self.y += speed_y
    
    def draw(self, screen:pg.surface.Surface):
        pg.draw.line(screen, Color("white"), 
                    (self.x,self.size/2+self.y),
                    (self.size+self.x,self.size/2+self.y))
            
        pg.draw.line(screen, Color("white"), 
                    (self.size/2+self.x,self.y),
                    (self.size/2+self.x,self.size+self.y))
        

class Camera:
    
    def __init__(self, speed:int, offset, window_size):
        self.speed = speed
        self.offset = offset
        self.x_speed = 0
        self.y_speed = 0
        
        self._screen_update = pg.rect.Rect(0,0,window_size-offset,window_size-offset)
        
    def edit_speed(self,x,y):
        if self._screen_update.x-self.offset > 0 and x < 0 :
            self.x_speed = x*self.speed
        if self._screen_update.x+self.offset < 0 and x > 0:
            self.x_speed = x*self.speed
        if self._screen_update.y-self.offset > 0 or y > 0:
            self.y_speed = y*self.speed
        print(self._screen_update.x)
        
    def move(self):
        self._screen_update.move_ip(self.x_speed, self.y_speed)
        self.x_speed, self.y_speed = 0,0
        

class Player:
    
    def __init__(self, camera:Camera, cursor:Cursor):
        self.camera = camera
        self.cursor = cursor
        
    def move(self, screen:pg.surface.Surface):
        self.cursor.move(self.camera.x_speed,self.camera.y_speed)
        self.camera.move()
        self.cursor.draw(screen)