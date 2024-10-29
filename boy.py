from pico2d import*
from state_machine import*

class Idle:
    @staticmethod
    def enter(boy, e):
        #현재 시간을 저장
        boy.start_time = get_time()
        if left_up(e) or left_down(e) or boy.dir == -1:
            boy.action = 2
            boy.face_dir = -1
        if right_up(e) or right_down(e) or boy.dir == 1 or start_event(e):
            boy.action = 3
            boy.face_dir = 1
        print('Boy Idle Enter')
    @staticmethod
    def exit(boy, e):
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
    def enter(boy, e):
        boy.frame = 3
        print('Boy Sleep Enter')
    @staticmethod
    def exit(boy, e):
        print('Boy Sleep Exit')
    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
    @staticmethod
    def draw(boy):  #''좌우 상하 반전 x 'v'좌우반전? 'h'상하반전?
        if boy.face_dir == -1:
            boy.image.clip_composite_draw(boy.frame * 100, boy.action * 100, 100, 100, -3.141592 / 2, '', boy.x + 25,
                                          boy.y - 25, 100, 100)
        else:
            boy.image.clip_composite_draw(boy.frame * 100, boy.action * 100, 100, 100, 3.141592 / 2, '', boy.x - 25, boy.y - 25,100,100)

class Run:
    @staticmethod
    def enter(boy,e):
        print('Boy Run Enter')
        if left_down(e) or left_up(e):
            boy.action = 0
            boy.dir = -1
        elif right_down(e) or right_up(e):
            boy.action = 1
            boy.dir = 1
        boy.frame = 0
    @staticmethod
    def exit(boy, e):
        print('Boy Run Exit')
    @staticmethod
    def do(boy):
        boy.x += boy.dir * 5
        if boy.x > 775:
            boy.x = 775
        elif boy.x < 25:
            boy.x = 25
        boy.frame = (boy.frame + 1) % 8
    @staticmethod
    def draw(boy):  # ''좌우 상하 반전 x 'v'좌우반전? 'h'상하반전?
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)

class AutoRun:
    @staticmethod
    def enter(boy,e):
        boy.start_time = get_time()
        print('Boy AutoRun Enter')
        if left_down(e) or left_up(e) or boy.face_dir == -1:
            boy.action = 0
            boy.dir = -1
        elif right_down(e) or right_up(e) or boy.face_dir == 1:
            boy.action = 1
            boy.dir = 1
        boy.frame = 0
    @staticmethod
    def exit(boy, e):
        print('Boy AutoRun Exit')
    @staticmethod
    def do(boy):
        boy.x += boy.dir * 10
        if (boy.x > 750 and boy.dir == 1) or (boy.x < 50 and boy.dir == -1):
            boy.dir *= -1
            boy.action = (boy.action + 1) % 2
            boy.x += boy.dir * 10
        boy.frame = (boy.frame + 1) % 8
        if get_time() - boy.start_time > 3:
            boy.state_machine.add_event(('TIME_OUT', 0))
    @staticmethod
    def draw(boy):  # ''좌우 상하 반전 x 'v'좌우반전? 'h'상하반전?
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y + 15, 150, 150)

class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 0
        self.action = 3
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Idle : { time_out : Sleep, right_down : Run, left_down : Run, a_down : AutoRun },
                Sleep: { space_down : Idle, right_down : Run, left_down : Run, a_down : AutoRun },
                Run : { right_up : Idle, left_up : Idle, a_down : AutoRun },
                AutoRun : { time_out : Idle, right_down : Run, left_down : Run }
            }
        )
    def update(self):
        self.state_machine.update()
        #self.frame = (self.frame + 1) % 8
    def handle_event(self, event):
        # event: 입력 이벤트 key mouse
        # 우리가 state machine 전달해줄껀 튜플
        if event.type ==SDL_KEYDOWN or event.type == SDL_KEYUP:
            self.state_machine.add_event(('INPUT', event))
    def draw(self):
        self.state_machine.draw()
        #self.image.clip_draw(self.frame * 100, self.action * 100, 100, 100, boy.x, boy.y)
