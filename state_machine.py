class StateMachine:
    def __init__(self, obj):
        self.obj = obj
    def start(self, state):
        self.cur_state = state  #시작 상태를 받아서, 그걸로 현재 상태를 정의
        self.cur_state.enter(self.obj)
    def update(self):
        self.cur_state.do(self.obj)
    def draw(self):
        self.cur_state.draw(self.obj)
