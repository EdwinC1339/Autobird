class Rect:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def collides(self, target):
        vertical_intersect_top = self.y < target.y + target.h
        vertical_intersect_bottom = self.y + self.h > target.y
        vertical_intersect = vertical_intersect_top and vertical_intersect_bottom

        horizontal_intersect_left = self.x < target.x + target.w
        horizontal_intersect_right = self.x + self.w > target.x
        horizontal_intersect = horizontal_intersect_left and horizontal_intersect_right

        return horizontal_intersect and vertical_intersect

    def transform(self, dx, dy):
        return Rect(self.x + dx, self.y + dy, self.w, self.h)

    @staticmethod
    def from_center(center_x, center_y, w, h):
        x = center_x - w / 2
        y = center_y - h / 2
        return Rect(x, y, w, h)
