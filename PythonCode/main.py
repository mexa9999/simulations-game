from Engine import Engine, Scene, Text, Button
from pygame.locals import *





if __name__ == "__main__":
    game = Engine((1000,1000), 60, (3000,3000), DOUBLEBUF)
    
    game.scene_manager.add_scene(Scene("main", game))
    game.scene_manager.add_scene(Scene("zero", game))
    game.scene_manager.change_scene("main")

    game.scene_manager.scenes["zero"].add_text(Text("пока", (0,0,180), (800,900)))
    game.scene_manager.scenes["main"].add_text(Text("привет", (0,0,180), (800,900)))
    game.scene_manager.scenes["main"].add_text(Text("привет", (0,0,180), (0,900)))
    game.scene_manager.scenes["main"].add_text(Text("привет", (0,0,180), (2980,900)))
    game.scene_manager.current_scene.add_button(Button([500,500], "hhh", (30,30), (0,0,255)))

    game.run()
    
    