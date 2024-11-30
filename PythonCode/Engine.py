import pygame as pg
from Player import Player, Cursor, Camera
from pygame.locals import *
import math

class Engine:
    
    def __init__(self, size:tuple[int,int], fps:int, map_size:tuple[int,int], flags) -> None:
        pg.init()
        pg.event.set_allowed([QUIT,KEYDOWN])
        
        self.fps = fps if fps > 0 else -1
        self.clock = pg.time.Clock()
        self.window = pg.display.set_mode(size,flags)
        self.screen = pg.surface.Surface(map_size)
        self.screen.set_alpha(None)
        self._scren_position = (map_size[0]-size[0])/-2

        self.player = Player(Camera(20, self._scren_position, size[0]), Cursor(50, self._scren_position, size[0]))
        self.vision = pg.rect.Rect(0,0,size[0],size[1])
        self.event_manager = EventManager(self, self.player.camera)
        self.scene_manager = SceneManager()
        self.button_manager = ButtonManager(self)

        self.running = True
        
    def end(self):
        self.running = False
        pg.quit()
        exit()

    def run(self):

        while self.running:
            pg.draw.rect(self.screen, pg.Color("black"), self.player.camera._screen_update)
            
            self.event_manager.quit_handler()
            self.event_manager.key_handler()
            self.button_manager.move()
            self.scene_manager.draw(self.screen)
            
            self.player.move(self.screen)
            self.window.blit(self.screen, (self._scren_position,self._scren_position), self.player.camera._screen_update)
            
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
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                pos = pg.mouse.get_pos()
                pos = [pos[0]+self.engine.player.cursor.x-500+self.engine.player.cursor.size/2, pos[1]+self.engine.player.cursor.y-500+self.engine.player.cursor.size/2]

                for command, button in self.engine.button_manager.get_items(self.engine.scene_manager.current_scene.name):
                    if button.rect.collidepoint(pos):
                        self.engine.button_manager.press_button(command) 
        pg.event.pump()
        
        
    def key_handler(self):
        keys = pg.key.get_pressed()
        
        self.camera.edit_speed(
            keys[pg.K_d]-keys[pg.K_a],
            keys[pg.K_s]-keys[pg.K_w])
        
        if keys[pg.K_9]:
            self.engine.scene_manager.change_scene("zero")
        elif keys[pg.K_0]:
            self.engine.scene_manager.change_scene("main")
        
class SceneManager:
    
    def __init__(self):
        self.current_scene:Scene = None
        self.scenes:dict[str,Scene] = {}
        
    def add_scene(self, scene):
        self.scenes[scene.name] = scene
        
    def change_scene(self, scene_name):
        if scene_name in self.scenes:
            self.current_scene = self.scenes[scene_name]
        
    def draw(self, screen):
        self.current_scene.draw(screen)

class Scene():
    
    def __init__(self, name, engine):
        self.name = name
        self.button_manager = engine.button_manager
        self.text_group = pg.sprite.Group()
        self.decor_group = pg.sprite.Group()
        self.button_group = pg.sprite.Group()
        
    def add_text(self, text):
        self.text_group.add(text)
        
    def add_decor(self, decor):
        self.decor_group.add(decor)
        
    def add_button(self, button):
        self.button_manager.add(self.name, button)
        self.button_group.add(button)
    
    def draw(self, screen:pg.surface.Surface):
        self.decor_group.draw(screen)
        self.button_group.draw(screen)
        self.text_group.draw(screen)

class ButtonManager:
    
    def __init__(self, engine:Engine):
        self.button_dict:dict = {}
        self.engine = engine
        
    def add(self, scene_name, button):
        self.button_dict.setdefault(scene_name, {}).update({button.command:button})
        
    def get(self, keys, defoult = {}):
        return self.button_dict.get(keys, defoult)
    
    def get_items(self, keys, defoult = {}):
        return self.button_dict.get(keys, defoult).items()
    
    def move(self):
        
        for button in self.button_dict[self.engine.scene_manager.current_scene.name].values():
            button.move(self.engine.player.camera.x_speed, self.engine.player.camera.y_speed)
    
    def press_button(self, command):
        print(command)
    
class Text(pg.sprite.Sprite):
    
    def __init__(self, text:str, color:pg.color.Color | tuple[int,int,int], position:tuple[int,int], size:int = 48, font=None):
        pg.sprite.Sprite.__init__(self)
        
        self.position = position
        
        self.edit_font(font, size)
        self.edit_text(text, color)
    
    def edit_font(self, font, size):
        self.font = pg.font.Font(font, size)
        
    def edit_text(self, text, color = None):
        self.color = color if color is not None else self.color
        self.image = self.font.render(text, True, self.color)
        self.rect = self.image.get_rect(center=self.position)
        
class Button(pg.sprite.Sprite):
    
    def __init__(self, position, command, size, color):
        pg.sprite.Sprite.__init__(self)
        
        self.command = command
        self.position = position
        
        self.edit_image(size, color)
        
    def edit_image(self, size, color):
        self.image = pg.surface.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect(center = self.position)

    def move(self, x_speed, y_speed):

        self.rect.move_ip(x_speed, y_speed)
        
class Sprite(pg.sprite.Sprite):
    
    def edit_image(self, image_path, position, size):
        self.position = position
        self.standart_image = pg.image.load(image_path).convert_alpha()
        self.resize_image = pg.transform.scale(self.image_i, size)
        self.rect = self.resize_image.get_rect(center=self.position)
    
    def update(self):
        '''
        self.image = pg.transform.rotate(self.image_i, round(math.degrees(x)-90))
        self.position[0] += 10*math.sin(x)
        self.position[1] += 10*math.cos(x)
        self.rect = self.image.get_rect(center=self.position)
        '''
        
