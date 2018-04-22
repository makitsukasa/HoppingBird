import sys
import sdl2
import sdl2.ext
import random

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400

BLACK = sdl2.ext.Color(0, 0, 0)
WHITE = sdl2.ext.Color(255, 255, 255)
YELLOW = sdl2.ext.Color(255, 255, 0)
PLAYER_SIZE_X = 40
PLAYER_SIZE_Y = 80
BLOCK_SIZE = 40
SCROLL_SPEED = 2
PLAYER_X = 60
PLAYER_GROUND_Y = WINDOW_HEIGHT
PLAYER_JUMP_SPEED = 10
GRAVITY = 0.2

running = True

class MovementSystem(sdl2.ext.Applicator):
    def __init__(self, minx, miny, maxx, maxy, player):
        super(MovementSystem, self).__init__()
        self.componenttypes = Velocity, sdl2.ext.Sprite
        self.minx = minx
        self.miny = miny
        self.maxx = maxx
        self.maxy = maxy
        self.player = player

    def process(self, world, componentsets):
        for velocity, sprite in componentsets:
            swidth, sheight = sprite.size
            sprite.x += velocity.x
            sprite.y += velocity.y

            sprite.x = max(self.minx, sprite.x)
            sprite.y = max(self.miny, sprite.y)

            pmaxx = sprite.x + swidth
            pmaxy = sprite.y + sheight
            if pmaxx > self.maxx:
                sprite.x = self.maxx - swidth
            if pmaxy > self.maxy:
                sprite.y = self.maxy - sheight


class CollisionSystem(sdl2.ext.Applicator):
    def __init__(self, minx, miny, maxx, maxy, player):
        super(CollisionSystem, self).__init__()
        self.componenttypes = Velocity, sdl2.ext.Sprite
        self.minx = minx
        self.miny = miny
        self.maxx = maxx
        self.maxy = maxy
        self.player = player

    def _overlap(self, item):
        sprite = item[1]
        if sprite == self.player.sprite:
            return False

        left, top, right, bottom = sprite.area
        bleft, btop, bright, bbottom = self.player.sprite.area

        return (bleft < right and bright > left and
                btop < bottom and bbottom > top)

    def process(self, world, componentsets):
        collitems = [comp for comp in componentsets if self._overlap(comp)]
        if len(collitems) != 0:
            global running
            running = False


class SoftwareRenderSystem(sdl2.ext.SoftwareSpriteRenderSystem):
    def __init__(self, window):
        super(SoftwareRenderSystem, self).__init__(window)

    def render(self, components):
        sdl2.ext.fill(self.surface, BLACK)
        super(SoftwareRenderSystem, self).render(components)

class Velocity(object):
    def __init__(self, x = 0, y = 0):
        super(Velocity, self).__init__()
        self.x = x
        self.y = int(y)
        self.floaty = float(y)

# fuckin urgy
class PlayerIsGround(object):
    def __init__(self):
        super(PlayerIsGround, self).__init__()
        self.isGround = True

class Player(sdl2.ext.Entity):
    def __init__(self, world, sprite):
        self.sprite = sprite
        self.sprite.position = PLAYER_X, PLAYER_GROUND_Y
        self.velocity = Velocity()
        self.playerisground = PlayerIsGround()

    def jump(self):
        if self.playerisground.isGround == False:
            #print("jump failed")
            return

        #print("jump succeed")

        self.playerisground.isGround = False

        self.velocity.floaty = -PLAYER_JUMP_SPEED
        self.sprite.y += int(self.velocity.floaty)


class Block(sdl2.ext.Entity):
    def __init__(self, world, sprite, posx = WINDOW_WIDTH, posy = None):
        self.sprite = sprite
        self.sprite.position = posx, posy if posy is not None else random.randint(0, WINDOW_HEIGHT)
        self.velocity = Velocity(-SCROLL_SPEED, 0)
        

def main(randSeed, AICalculator, AIVariables, showGUI):
    random.seed(randSeed)

    sdl2.ext.init()
    if showGUI:
        window = sdl2.ext.Window("HoppingBird", size=(WINDOW_WIDTH, WINDOW_HEIGHT))
        window.show()
        
    factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
    world = sdl2.ext.World()

    player = Player(world, factory.from_color(YELLOW, size=(PLAYER_SIZE_X, PLAYER_SIZE_Y)))
    blocks = []

    if showGUI:
        spriteRendererSystem = SoftwareRenderSystem(window)
    movementSystem = MovementSystem(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, player)
    collisionSystem = CollisionSystem(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, player)
    if showGUI:
        world.add_system(spriteRendererSystem)
    world.add_system(movementSystem)
    world.add_system(collisionSystem)

    global running
    running = True

    blockInterval = 0
    score = -300

    while running:

        if blockInterval <= 0:
            newBlock = Block(world, factory.from_color(WHITE, size=(BLOCK_SIZE, BLOCK_SIZE)))
            blocks.append(newBlock)
            blockInterval = random.randint(150, 300)

        score += SCROLL_SPEED
        blockInterval -= SCROLL_SPEED

        scrollout_blocks = []
        for block in blocks:
            if block.sprite.x <= 0:
                blocks.remove(block)
                world.delete(block)

        if AICalculator is None:
            # a human is playing
            for event in sdl2.ext.get_events():
                if event.type == sdl2.SDL_QUIT:
                    running = False
                    break

                if event.type == sdl2.SDL_KEYDOWN:
                    if event.key.keysym.sym == sdl2.SDLK_SPACE:
                        player.jump()

        elif score > 0:
            # an AI is playing
            environmentVariables = [
                blocks[0].sprite.x - (PLAYER_X),
                blocks[0].sprite.y + BLOCK_SIZE - (PLAYER_GROUND_Y - PLAYER_SIZE_Y),
                100.0 / (blocks[0].sprite.x - PLAYER_X + 0.1),
                100.0 / (blocks[0].sprite.y + BLOCK_SIZE - (PLAYER_GROUND_Y - PLAYER_SIZE_Y) + 0.1),
            ]
            if blocks[0].sprite.x < PLAYER_X:
                environmentVariables = [
                    blocks[1].sprite.x - (PLAYER_X),
                    blocks[1].sprite.y + BLOCK_SIZE - (PLAYER_GROUND_Y - PLAYER_SIZE_Y),
                    100.0 / (blocks[1].sprite.x - PLAYER_X + 0.1),
                    100.0 / (blocks[1].sprite.y + BLOCK_SIZE - (PLAYER_GROUND_Y - PLAYER_SIZE_Y) + 0.1),
                ]

            if AICalculator(environmentVariables, AIVariables, showGUI) == True:
                player.jump()

        if player.playerisground.isGround == False:
            player.velocity.floaty += GRAVITY
            player.velocity.y = int(player.velocity.floaty)
            if player.sprite.y + player.sprite.size[1] >= PLAYER_GROUND_Y:
                #print("jump end")
                player.sprite.y = PLAYER_GROUND_Y
                player.velocity.y = 0
                player.velocity.floaty = 0.0
                player.playerisground.isGround = True

        if showGUI:
            sdl2.SDL_Delay(10)
        
        world.process()

    sdl2.ext.quit()

    if showGUI:
        print(score)
    return score

if __name__ == '__main__':
    main(None, None, None, True)