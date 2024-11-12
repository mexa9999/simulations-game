from Engine import Engine

from pygame.locals import *






if __name__ == "__main__":
    game = Engine((1000,1000), 60, DOUBLEBUF)
    game.run()
    