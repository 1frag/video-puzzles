import math
from typing import Iterable

from custom_types import Numeric, Point


class Circle:
    def __init__(self, x0: Numeric, y0: Numeric, radius: Numeric):
        self.x0 = int(x0)
        self.y0 = int(y0)
        self.radius = int(radius)

    def points(self) -> Iterable[Point]:
        for x in range(self.x0 - self.radius, self.x0 + self.radius + 1):
            module_dy = math.sqrt(self.radius ** 2 - (x - self.x0) ** 2)  # |y-y0|
            yield x, self.y0 + module_dy
            yield x, self.y0 - module_dy

        for y in range(self.y0 - self.radius, self.y0 + self.radius + 1):
            module_dx = math.sqrt(self.radius ** 2 - (y - self.y0) ** 2)  # |x-x0|
            yield self.x0 + module_dx, y
            yield self.x0 - module_dx, y
