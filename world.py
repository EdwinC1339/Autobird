from bird import Bird
from pipes import Pipes
from numpy import array
from soundplayer import SoundPlayer


class World:
    def __init__(self, bird: Bird, active_pipes: Pipes, inactive_pipes: Pipes, sound_player: SoundPlayer):
        self.bird = bird
        self.active_pipes = active_pipes
        self.inactive_pipes = inactive_pipes
        self.sound_player = sound_player
        self.active = False

        self.score_flag = False

        self.time = 0

    def reset(self):
        self.bird.reset()
        self.active_pipes.x = 0.7
        self.active_pipes.y = 0.5
        self.inactive_pipes.reset_pos(0.5)
        self.time = 0
        self.reset_score()
        self.deactivate()

    def draw(self, surface, scale):
        self.bird.draw(surface, scale)
        self.active_pipes.draw(surface, scale)
        self.inactive_pipes.draw(surface, scale)

    def draw_debug(self, surface, scale):
        self.bird.draw_colliders(surface, scale)
        self.active_pipes.draw_colliders(surface, scale)

    def update(self):
        self.bird.update()
        self.active_pipes.update()
        self.inactive_pipes.update()

        if self.active and self.bird.collides(self.active_pipes) or self.bird.oob():
            self.bird.die()
            self.sound_player.die()
            self.deactivate()
            return True, False

        if self.active_pipes.off_edge():
            # Reset the pipes that went off the edge
            prev_y = self.inactive_pipes.y
            self.active_pipes.reset_pos(prev_y)

            # Swap active pipes with inactive
            self.active_pipes, self.inactive_pipes = self.inactive_pipes, self.active_pipes

            # Disable score flag (enables scoring again)
            self.reset_score()

        if self.active_pipes.x < 0.2 and not self.score_flag:
            self.score()
            return False, True

        if self.active:
            self.time += 1

        return False, False

    def activate(self):
        self.bird.activate()
        self.active_pipes.activate()
        self.inactive_pipes.activate()
        self.active = True

    def deactivate(self):
        self.bird.deactivate()
        self.active_pipes.deactivate()
        self.inactive_pipes.deactivate()
        self.active = False

    def jump(self):
        self.bird.jump()
        self.sound_player.jump()

    def score(self):
        self.score_flag = True

    def reset_score(self):
        self.score_flag = False

    def get_state(self):
        state = array([self.time,
                       self.bird.y, self.bird.vy,
                       self.active_pipes.x, self.active_pipes.y,
                       self.inactive_pipes.x, self.inactive_pipes.y])

        return state
