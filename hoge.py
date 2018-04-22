import sys
import sdl2
import sdl2.ext

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 300

BLACK = sdl2.ext.Color(0, 0, 0)
YELLOW = sdl2.ext.Color(255, 255, 0)
PLAYER_SIZE = 40
PLAYER_X = 60
PLAYER_GROUND_Y = WINDOW_HEIGHT
PLAYER_JUMP_SPEED = 5

class Player(sdl2.ext.Entity):
    def __init__(self, world, sprite, posx=0, posy=0, ai=False):
        self.sprite = sprite
        self.sprite.position = posx, posy
        self.velocity = None
        self.playerdata = None

def main():
    sdl2.ext.init()
    window = sdl2.ext.Window("HoppingBird", size=(WINDOW_WIDTH, WINDOW_HEIGHT))
    window.show()
        
    factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
    world = sdl2.ext.World()

    player = Player(world, factory.from_color(YELLOW, size=(PLAYER_SIZE, PLAYER_SIZE)))

    dummyEntity = sdl2.ext.Entity(world)

    for i in dir(dummyEntity):
        print(i)

    for i in dir(player):
        print(i)

    if player.velocity is not None:
        print("hoge")


    #player.jump()

if __name__ == '__main__':
    main()