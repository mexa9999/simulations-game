import pygame as pg
from pygame.locals import *
from os import PathLike
from typing import Optional, IO

class Text(pg.sprite.Sprite):
    
    def __init__(
        self, 
        text: str, pos:tuple[int,int],
        textcolor:pg.color.Color = Color("blue"),
        fontsize:int = 32,
        fontname:Optional[str | bytes | PathLike[str] | PathLike[bytes] | IO[bytes] | IO[str]] = None,
    ) -> None:
        
        pg.sprite.Sprite.__init__(self)
        
        self.text = text

        self.set_font(fontname, fontsize)
        self.render(pos, textcolor)
        
    def set_font(
        self,
        fontname:Optional[str | bytes | PathLike[str] | PathLike[bytes] | IO[bytes] | IO[str]],
        fontsize:int
        ) -> None:
        self.font = pg.font.Font(fontname, fontsize)
    
    def render(self, pos:tuple[int,int], textcolor:pg.color.Color) -> None:
        self.image = self.font.render(self.text, True, textcolor)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        
    def draw(self, screen:pg.Surface) -> None:
        screen.blit(self.image, self.rect)

class App:
    
    def __init__(self, size:tuple[int,int], fps:int, flags) -> None:
        pg.init()
        pg.event.set_allowed([QUIT,KEYDOWN])
        
        self.fps = fps if fps > 0 else -1
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode(size,flags)
        self.screen.set_alpha(None)
        self.vision = pg.rect.Rect(0,0,800,600)
        self.running = True
    
    def run(
        self,
        text_sprite_group:pg.sprite.Group = pg.sprite.Group(),
        bacteria_sprite_group:pg.sprite.Group = pg.sprite.Group()
        ) -> None:
        
        Text("начать", (0,0)).draw(self.screen)
        
        while self.running:

            for event in pg.event.get():
                if event.type == QUIT:
                    self.running = False
                elif event.type == KEYDOWN:
                    self.key_combinations(event)
            pg.event.pump()
            
            text_sprite_group.draw(self.screen)
            bacteria_sprite_group.draw(self.screen)
            
            self.screen.scroll(1)
            pg.display.update(self.vision)
            
            self.clock.tick(self.fps)

if __name__ == "__main__":
    
    j = App((800,800), 60, DOUBLEBUF)
    Text("начать", (0,700),).draw(j.screen)
    
    pg.display.update()
    j.run()