from pico2d import*
from state_machine import*

class Idle:
    @staticmethod
    def enter(boy):
        #현재 시간을 저장
        boy.start_time = get_time()
        boy.action = 3
        print('Boy Idle Enter')
    @staticmethod
    def exit(boy):
        print('Boy Idle Exit')
    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        if get_time() - boy.start_time > 3:
            boy.state_machine.add_event(('TIME_OUT', 0))
    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)

class Sleep:
    @staticmethod
    def enter(boy):
        boy.frame = 3
        print('Boy Sleep Enter')
    @staticmethod
    def exit(boy):
        print('Boy Sleep Exit')
    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
    @staticmethod
    def draw(boy):  #''좌우 상하 반전 x 'v'좌우반전? 'h'상하반전?
        boy.image.clip_composite_draw(boy.frame * 100, boy.action * 100, 100, 100, 3.141592/2, '', boy.x-25, boy.y-25,100,100)

class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 0
        self.action = 3
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Sleep)
        self.state_machine.set_transitions(
            {
                Idle : { time_out : Sleep },
                Sleep: { space_down : Idle}
            }
        )
    def update(self):
        self.state_machine.update()
        #self.frame = (self.frame + 1) % 8
    def handle_event(self, event):
        # event: 입력 이벤트 key mouse
        # 우리가 state machine 전달해줄껀 튜플
        self.state_machine.add_event(('INPUT', event))
    def draw(self):
        self.state_machine.draw()
        #self.image.clip_draw(self.frame * 100, self.action * 100, 100, 100, boy.x, boy.y)
