from pico2d import*
from state_machine import*

class Idle:
    @staticmethod
    def enter(boy):
        print('Boy Idle Enter')
    @staticmethod
    def exit(boy):
        print('Boy Idle Exit')
    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)

class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.action = 3
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
    def update(self):
        self.state_machine.update()
        #self.frame = (self.frame + 1) % 8
    def handle_event(self, event):
        pass
    def draw(self):
        self.state_machine.draw()
        #self.image.clip_draw(self.frame * 100, self.action * 100, 100, 100, boy.x, boy.y)
