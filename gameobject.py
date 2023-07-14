from abc import ABC, abstractmethod
from rect import Rect
from pygame import Rect as PGRect
from pygame import draw

RectList = list[Rect]


class GameObject(ABC):
    def __init__(self, x, y):
        self._x = x
        self._y = y
        self.active = False
        self.colliders = RectList()

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self, surface, scale):
        pass

    @abstractmethod
    def activate(self):
        pass

    @abstractmethod
    def deactivate(self):
        pass

    def collides(self, target):
        for self_rect in self.colliders:
            for target_rect in target.colliders:
                x_adjust = target.x - self.x
                y_adjust = target.y - self.y
                if self_rect.collides(target_rect.transform(x_adjust, y_adjust)):
                    return True

        return False

    def draw_colliders(self, surface, scale):
        for rect in self.colliders:
            self.draw_collider(rect, surface, scale)

    def draw_collider(self, rect, surface, scale):
        top_left_x = (rect.x + self.x) * scale
        top_left_y = (rect.y + self.y) * scale
        w = rect.w * scale
        h = rect.h * scale

        render_rect = PGRect(top_left_x, top_left_y, w, h)
        draw.rect(surface, "white", render_rect, 3)
