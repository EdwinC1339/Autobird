from gameobject import GameObject
from pygame import Surface, image, transform, SRCALPHA
from rect import Rect


class Bird(GameObject):
    def __init__(self):
        super().__init__(0.2, 0.5)
        self.vy = 0
        self.gravity = 0.00061
        self.sprite = None
        self.sprite_flap = None

        collider = Rect.from_center(0, 0, 0.085, 0.082)
        self.colliders.append(collider)

        self.flap_cd = 0
        self.flap_active = False

    def reset(self):
        self.y = 0.5
        self.vy = 0
        self.flap_cd = 0
        self.flap_active = False

    def initialize_sprite(self, scale):
        self.sprite = Surface([0.1 * scale, 0.1 * scale], SRCALPHA, 32)
        img = image.load('assets/bird1.png')
        img = transform.scale(img, [0.1 * scale, 0.1 * scale])
        self.sprite.blit(img, (0, 0))

        self.sprite_flap = Surface([0.1 * scale, 0.1 * scale], SRCALPHA, 32)
        img = image.load('assets/bird2.png')
        img = transform.scale(img, [0.1 * scale, 0.1 * scale])
        self.sprite_flap.blit(img, (0, 0))

    def update(self):
        if self.active:
            self.vy += self.gravity
            self.y += self.vy

        if self.y < 0:
            self.y = 0
            self.vy = 0

        if self.y > 0.9:
            self.y = 0.9

        if self.flap_active:
            self.flap_cd -= 1

        if self.flap_cd == 0:
            self.flap_active = False

    def draw(self, surface, scale):
        if self.flap_active and self.flap_cd % 8 < 6:
            surface.blit(self.sprite_flap, ((self.x - 0.05) * scale, (self.y - 0.05) * scale))
        else:
            surface.blit(self.sprite, ((self.x - 0.05) * scale, (self.y - 0.05) * scale))

    def jump(self):
        self.vy = min(-0.011, self.vy - 0.0085)
        self.flap_cd = 18
        self.flap_active = True

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False
        self.flap_active = False
        self.flap_cd = 0
        self.vy = 0

    def die(self):
        self.deactivate()

    def oob(self):
        return self.y > 1 or self.y < 0
