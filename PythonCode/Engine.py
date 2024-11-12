import pygame as pg
from Player import Player, Cursor, Camera
from pygame.locals import *
from abc import ABC, abstractmethod

class Engine:
    
    def __init__(self, size:tuple[int,int], fps:int, flags) -> None:
        pg.init()
        pg.event.set_allowed([QUIT,KEYDOWN])
        
        self.fps = fps if fps > 0 else -1
        self.clock = pg.time.Clock()
        self.window = pg.display.set_mode(size,flags)
        self.screen = pg.surface.Surface((2000,2000))
        self.screen.set_alpha(None)
        
        self.player = Player(Camera(5), Cursor(50))
        self.vision = pg.rect.Rect(0,0,1000,800)
        self.event_manager = EventManager(self, self.player.camera)
        self.scene_manager = SceneManager()

        self.running = True
        
    def end(self):
        self.engine.running = False
        pg.quit()
        exit()

    def run(self):
        j = Cursor(50)
        while self.running:
            pg.draw.rect(self.screen, pg.Color("black"), self.player.camera._screen_update)
            
            self.event_manager.quit_handler()
            self.event_manager.key_handler()
            j.draw(self.screen)
            self.player.move(self.screen)
            
            self.window.blit(self.screen, (-500,-500), self.player.camera._screen_update)
            
            pg.display.update()
            self.clock.tick(self.fps)
            
class EventManager:
    
    def __init__(self, engine:Engine, camera:Camera):
        self.engine = engine
        self.camera = camera
    
    def quit_handler(self):
        for event in pg.event.get():
            if event.type == QUIT:
                self.engine.end()
        pg.event.pump()
        
        
    def key_handler(self):
        keys = pg.key.get_pressed()
        
        self.camera.edit_speed(
            keys[pg.K_d]-keys[pg.K_a],
            keys[pg.K_s]-keys[pg.K_w])
        print(keys[pg.K_d]-keys[pg.K_a])
        
class SceneManager:
    
    def __init__(self):
        self.current_scene = None
        self.scenes = {}
        
    def add_scene(self, name, scene):
        self.scenes[name] = scene
        
    def change_scene(self, scene_name):
        if scene_name in self.scenes:
            self.current_scene = self.scenes[scene_name]
        
    def draw(self, screen):
        self.current_scene.draw(screen)

class Scene():
    
    def __init__(self):
        self.text_group = pg.sprite.Group()
        self.decor_group = pg.sprite.Group()
        self.button_group = pg.sprite.Group()
        
    def generate():
        pass
    
    def draw(self, screen:pg.surface.Surface):
        self.decor_group.draw(screen)
        self.button_group.draw(screen)
        self.text_group.draw(screen)
    