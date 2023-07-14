from gameobject import GameObject
from random import uniform
from pygame import Surface, image, transform, SRCALPHA
from rect import Rect

# Pipes will be at most this pct of the screen up or down from the previous position
MARGIN = 0.25


class Pipes(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y)

        top_pipe = Rect.from_center(0, -0.55, 0.18, 0.8)
        bottom_pipe = Rect.from_center(0, 0.48, 0.18, 0.8)

        self.colliders.append(top_pipe)
        self.colliders.append(bottom_pipe)
        self.sprite = None

    def initialize_sprite(self, scale):
        self.sprite = Surface([0.2 * scale, 1.9 * scale], SRCALPHA, 32)

        img1 = image.load('assets/bottom pipe.png')
        img1 = transform.scale(img1, [0.2 * scale, 0.8 * scale])
        self.sprite.blit(img1, (0, 0.95 * scale))

        img2 = image.load('assets/top pipe.png')
        img2 = transform.scale(img2, [0.2 * scale, 0.8 * scale])
        self.sprite.blit(img2, (0, 0))

    def update(self):
        if self.active:
            self.x -= 0.008

    def draw(self, surface, scale):
        surface.blit(self.sprite, ((self.x - 0.1) * scale, (self.y - 0.9) * scale))

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def reset_pos(self, prev_y):
        self.x = 1.6

        lowest = min(0.8, prev_y + MARGIN)
        highest = max(0.2, prev_y - MARGIN)

        self.y = uniform(lowest, highest)

    def off_edge(self):
        return self.x < -0.3
