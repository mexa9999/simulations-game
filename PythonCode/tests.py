import pygame as pg
from pygame.locals import *

class Text(pg.sprite.Sprite):
    
    def __init__(self, text, pos):
        pg.sprite.Sprite.__init__(self)
        
        self.text = text
        self.pos = pos
        
        self.fontname = None
        self.fontsize = 32
        self.fonccolor = Color("blue")
        self.set_font()
        self.render()
        
    def set_font(self):
        self.font = pg.font.Font(self.fontname, self.fontsize)
    
    def render(self):
        self.image = self.font.render(self.text, True, self.fonccolor)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)

class App:
    
    def __init__(self, size, Fps, flags):
        pg.init()
        pg.event.set_allowed([QUIT,KEYDOWN])
        
        self.Fps = Fps if Fps > 0 else -1
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode(size,flags)
        self.screen.set_alpha(None)
        self.vision = pg.rect.Rect(0,0,800,600)
        self.running = True
    
    def key_combinations(self, event):
        '''
        combinations = {
            (K_x, KMOD_ALT) : "print('!')"
        }
        key = event.key
        mod = event.mod
        if (key, mod) in combinations:
            exec(combinations[(key, mod)])
        '''
        pass
    
    def run(self, text_sprite_group = None, bacteria_sprite_group = None):
        Text("начать", (0,0)).draw(self.screen)
        while self.running:

            for event in pg.event.get():
                if event.type == QUIT:
                    self.running = False
                elif event.type == KEYDOWN:
                    self.key_combinations(event)
            pg.event.pump()
            
            if text_sprite_group: text_sprite_group.draw(self.screen)
            if text_sprite_group: bacteria_sprite_group.draw(self.screen)
            self.screen.scroll(1)
            pg.display.update(self.vision)
            
            self.clock.tick(self.Fps)
            
            #pg.display.set_caption(str(self.clock.get_fps()))

if __name__ == "__main__":
    
    j = App((800,800), 60, DOUBLEBUF)
    Text("начать", (0,700)).draw(j.screen)
    
    pg.display.update()
    j.run()