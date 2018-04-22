import sys
import sdl2
import sdl2.ext

BLACK = sdl2.ext.Color(0, 0, 0)
WHITE = sdl2.ext.Color(255, 255, 255)
PLAYER_X = 20
PLAYER_START_Y = 400
PLAYER_SPEED = 5
SCROLL_SPEED = 2

class MovementSystem(sdl2.ext.Applicator):
    def __init__(self, minx, miny, maxx, maxy):
        super(MovementSystem, self).__init__()
        self.componenttypes = Velocity, sdl2.ext.Sprite
        self.minx = minx
        self.miny = miny
        self.maxx = maxx
        self.maxy = maxy

    def process(self, world, componentsets):
        for velocity, sprite in componentsets:
            swidth, sheight = sprite.size
            sprite.x += velocity.vx
            sprite.y += velocity.vy

            sprite.x = max(self.minx, sprite.x)
            sprite.y = max(self.miny, sprite.y)

            pmaxx = sprite.x + swidth
            pmaxy = sprite.y + sheight
            if pmaxx > self.maxx:
                sprite.x = self.maxx - swidth
            if pmaxy > self.maxy:
                sprite.y = self.maxy - sheight


class SoftwareRenderSystem(sdl2.ext.SoftwareSpriteRenderSystem):
    def __init__(self, window):
        super(SoftwareRenderSystem, self).__init__(window)

    def render(self, components):
        sdl2.ext.fill(self.surface, BLACK)
        super(SoftwareRenderSystem, self).render(components)


class Velocity(object):
    def __init__(self):
        super(Velocity, self).__init__()
        self.vx = 0
        self.vy = 0

class KeyInput():
    def __init__(self):
        self.up = False
        self.down = False
        self.left = False
        self.right = False

    def x(self):
        if self.left == self.right:
            return 0
        elif self.left == True:
            return -1
        elif self.right == True:
            return 1
        else:
            return None

    def y(self):
        if self.up == self.down:
            return 0
        elif self.up == True:
            return -1
        elif self.down == True:
            return 1
        else:
            return None


class Player(sdl2.ext.Entity):
    def __init__(self, world, sprite):
        self.sprite = sprite
        self.sprite.position = PLAYER_X, PLAYER_START_Y
        self.velocity = Velocity()


class Block(sdl2.ext.Entity):
    def __init__(self, world, sprite, posx = 0, posy = 0):
        self.sprite = sprite
        self.sprite.position = posx, posy
        self.velocity = Velocity()
        self.velocity.x = -SCROLL_SPEED

def main():
    sdl2.ext.init()
    window = sdl2.ext.Window("HoppingBird", size=(800, 600))
    window.show()
        
    factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
    world = sdl2.ext.World()
    spriteRendererSystem = SoftwareRenderSystem(window)
    movementSystem = MovementSystem(0, 0, 800, 600)
    world.add_system(spriteRendererSystem)
    world.add_system(movementSystem)

    player1 = Player(world, factory.from_color(WHITE, size=(20, 20)))

    running = True

    keyInput = KeyInput()

    while running:
        for event in sdl2.ext.get_events():
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
            if event.type == sdl2.SDL_KEYDOWN:
                if event.key.keysym.sym == sdl2.SDLK_UP:
                    keyInput.up = True
                if event.key.keysym.sym == sdl2.SDLK_DOWN:
                    keyInput.down = True
                if event.key.keysym.sym == sdl2.SDLK_LEFT:
                    keyInput.left = True
                if event.key.keysym.sym == sdl2.SDLK_RIGHT:
                    keyInput.right = True
                player1.velocity.vx = keyInput.x() * PLAYER_SPEED
                player1.velocity.vy = keyInput.y() * PLAYER_SPEED
            elif event.type == sdl2.SDL_KEYUP:
                if event.key.keysym.sym == sdl2.SDLK_UP:
                    keyInput.up = False
                if event.key.keysym.sym == sdl2.SDLK_DOWN:
                    keyInput.down = False
                if event.key.keysym.sym == sdl2.SDLK_LEFT:
                    keyInput.left = False
                if event.key.keysym.sym == sdl2.SDLK_RIGHT:
                    keyInput.right = False
                player1.velocity.vx = keyInput.x() * PLAYER_SPEED
                player1.velocity.vy = keyInput.y() * PLAYER_SPEED
        sdl2.SDL_Delay(10)
        world.process()


if __name__ == '__main__':
    main()