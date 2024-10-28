from pico2d import*
import random
from boy import*

# 모양없는 납작한 붕어빵의 납작한 초기 모습
class Grass:
    def __init__(self):
        self.image = load_image('grass.png')
    def update(self):
        pass
    def draw(self):
        self.image.draw(400,30)

def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

def reset_world():
    global running
    global grass
    global team
    global world

    running = True
    world = []
    grass = Grass()
    world.append(grass)
    character = Boy()
    world.append(character)
#    team = [Boy() for i in range(11)]
#    world += team
#    num = random.randint(1,19)

def update_world():
    for o in world:
        o.update()
    pass

def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()

open_canvas()

reset_world()

while running:
    handle_events()
    update_world()
    render_world()
    delay(0.05)

close_canvas()