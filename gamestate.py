from enum import Enum


class SubState(Enum):
    PREGAME = 1
    GAME = 2
    POSTGAME = 3


class GameState:
    def __init__(self, screen, clock, font1, font2):
        self.running = False
        self.screen = screen
        self.clock = clock
        self.sub_state = SubState.PREGAME
        self.score = 0

        self.font1 = font1
        self.font2 = font2

    def get_screen(self):
        return self.screen

    def get_clock(self):
        return self.clock

    def get_sub_state(self):
        return self.sub_state

    def start_game(self):
        self.sub_state = SubState.GAME

    def end_game(self):
        self.sub_state = SubState.POSTGAME

    def start_pre_game(self):
        self.sub_state = SubState.PREGAME

    def is_running(self):
        return self.running

    def stop(self):
        self.running = False

    def run(self):
        self.running = True

    def get_score(self):
        return self.score

    def inc_score(self):
        self.score += 1

    def reset_score(self):
        self.score = 0
