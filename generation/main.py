import collections
import enum
import itertools
import json
import math
import random
import tkinter
from typing import Iterable

import png

import ffmpeg_utils
from circle import Circle
from custom_types import Point, Numeric


WWW_DATA = './www/data'


class CornerKind(str, enum.Enum):
    TOP_LEFT = 'top_left'
    TOP_RIGHT = 'top_right'
    BOTTOM_LEFT = 'bottom_left'
    BOTTOM_RIGHT = 'bottom_right'


class Settings:
    def __init__(
            self,
            input_file: str,
            radius: int = 20,
    ):
        self.radius = radius
        self.input_file = input_file


class Line:
    def __init__(self, points: set[Point]):
        self.points = {(int(x), int(y)) for x, y in points}

    @classmethod
    def empty(cls):
        return Line(set())

    def draw(self, width: int, height: int):
        root = tkinter.Tk()
        canvas = tkinter.Canvas(
            root,
            bg='white',
            width=width,
            height=height,
        )
        for x, y in self.points:
            canvas.create_line(x, y, x + 1, y + 1, fill='black')
        canvas.pack()
        root.mainloop()

    def reversed(self) -> 'Line':
        points = set()
        for x, y in self.points:
            points.add((y, x))
        return Line(points)

    def __ior__(self, other: 'Line|None'):
        if other:
            self.points |= other.points
        return self

    def add(self, x: Numeric, y: Numeric):
        self.points.add((int(x), int(y)))

    def max_x(self) -> Numeric:
        return max(self.points, key=lambda point: point[0])[0]

    def min_x(self) -> Numeric:
        return min(self.points, key=lambda point: point[0])[0]

    def max_y(self) -> Numeric:
        return max(self.points, key=lambda point: point[1])[1]

    def min_y(self) -> Numeric:
        return min(self.points, key=lambda point: point[1])[1]


class MaskAlgo:
    def __init__(
            self,
            width: int,
            height: int,
            parts_x: int,
            parts_y: int,
            settings: Settings,
    ):
        self.width = width
        self.height = height
        self.parts_x = parts_x
        self.parts_y = parts_y
        self.settings = settings

        self.puzzle_width = self.width // self.parts_x
        self.puzzle_height = self.height // self.parts_y

    @classmethod
    def create(cls) -> 'MaskAlgo':
        return MaskAlgo(
            width=1280,
            height=720,
            parts_x=8,
            parts_y=4,
            settings=Settings(
                input_file='./1.mp4',
                radius=20,
            ),
        )

    def reversed(self) -> 'MaskAlgo':
        return MaskAlgo(
            width=self.height,
            height=self.width,
            parts_x=self.parts_y,
            parts_y=self.parts_x,
            settings=self.settings,
        )

    def generate_vertical_lines(self) -> list[list[Line]]:
        result = []

        print(f'{self.puzzle_width=} {self.puzzle_height=}')

        for x0 in range(self.puzzle_width, self.width, self.puzzle_width):
            result.append([])

            for y0 in range(0, self.height, self.puzzle_height):
                pre_line = Line.empty()

                y_high_half = int(y0 + self.puzzle_height / 2 - self.settings.radius / 2)
                y_low_half = int(y0 + self.puzzle_height / 2 + self.settings.radius / 2)

                x_circle = x0 + self.settings.radius
                y_circle = y0 + self.puzzle_height / 2

                x_start_circle = x_circle - math.sqrt(self.settings.radius ** 2 - (y_high_half - y_circle) ** 2)

                for y in range(y0, y_high_half + 1):
                    pre_line.add(x0, y)

                for x in range(x0, int(x_start_circle) + 1):
                    pre_line.add(x, y_high_half)
                    pre_line.add(x, y_low_half)

                for x, y in Circle(
                        x0=x_circle,
                        y0=y_circle,
                        radius=self.settings.radius,
                ).points():
                    if x >= x_start_circle:
                        pre_line.add(x, y)

                for y in range(y_low_half, y0 + self.puzzle_height + 1):
                    pre_line.add(x0, y)

                line = Line(set())
                if random.choice([False, True]):  # False - >; True - <
                    for x, y in pre_line.points:
                        line.add(2 * x0 - x, y)
                else:
                    line |= pre_line
                result[-1].append(line)

        return result


def draw_masks_in_tk():  # for debugging
    algo = MaskAlgo.create()
    result_line = Line.empty()

    for lines in algo.generate_vertical_lines():
        for line in lines:
            result_line |= line

    for lines in algo.reversed().generate_vertical_lines():
        for line in lines:
            result_line |= line.reversed()

    result_line.draw(algo.width, algo.height)


class Border:
    def __init__(
            self,
            ident: str,
            number: int,
            left: Line | None,
            right: Line | None,
            top: Line | None,
            bottom: Line | None,
            top_left_corner: Point,
            puzzle_width: int,
            puzzle_height: int,
    ):
        self.ident = ident
        self.number = number
        self._left = left
        self._right = right
        self._top = top
        self._bottom = bottom
        self._top_left_corner = top_left_corner
        self._puzzle_width = puzzle_width
        self._puzzle_height = puzzle_height

        self._max_x = max(line.max_x() for line in self.iteratee())
        self._min_x = min(line.min_x() for line in self.iteratee())
        self._max_y = max(line.max_y() for line in self.iteratee())
        self._min_y = min(line.min_y() for line in self.iteratee())

        self.height = self._max_y - self._min_y
        self.width = self._max_x - self._min_x
        self.left = self._min_x
        self.top = self._min_y

        self._corners: dict[CornerKind, Point] = {
            CornerKind.TOP_LEFT: self._top_left_corner,
            CornerKind.TOP_RIGHT: self._top_right_corner,
            CornerKind.BOTTOM_LEFT: self._bottom_left_corner,
            CornerKind.BOTTOM_RIGHT: self._bottom_right_corner
        }

    @property
    def _top_right_corner(self):
        return self._top_left_corner[0] + self._puzzle_width, self._top_left_corner[1]

    @property
    def _bottom_left_corner(self):
        return self._top_left_corner[0], self._top_left_corner[1] + self._puzzle_height

    @property
    def _bottom_right_corner(self):
        return self._top_left_corner[0] + self._puzzle_width, self._top_left_corner[1] + self._puzzle_height

    def iteratee(self) -> Iterable[Line]:
        for side in [self._left, self._right, self._top, self._bottom]:
            if side:
                yield side

    def has(self, x: Numeric, y: Numeric, with_offset: bool = False) -> bool:
        point = (x, y) if with_offset else (x + self._min_x, y + self._min_y)
        return any(point in line.points for line in self.iteratee())

    @property
    def relative_corners(self) -> dict[CornerKind, Point]:
        result = {}
        for corner_kind, absolute_point in self._corners.items():
            if absolute_point:
                result[corner_kind] = absolute_point[0] - self.left, absolute_point[1] - self.top
        return result


def save_mask(border: Border) -> str:
    height = border.height
    width = border.width

    pixels = [[[255, 255, 255, 0] for _i in range(width)] for _j in range(height)]

    stack = collections.deque()
    stack.append((int(height / 2), int(width / 2)))

    while len(stack):
        x, y = stack.popleft()
        if border.has(x, y, with_offset=False):
            continue
        for dx, dy in [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1),
        ]:
            nx, ny = x + dx, y + dy
            if nx < 0 or ny < 0:
                continue
            if nx >= width or ny >= height:
                continue
            if border.has(nx, ny, with_offset=False):
                continue
            if pixels[ny][nx][3] == 0:
                stack.append((nx, ny))
                pixels[ny][nx][3] = 255

    mask_file = f'{WWW_DATA}/2/masks/{border.ident}.png'
    with open(mask_file, 'wb') as f:
        w = png.Writer(width, height, greyscale=False, alpha=True)
        w.write(f, [itertools.chain(*row) for row in pixels])
    return mask_file


def save_cropped(border: Border, input_file: str) -> str:
    output_file = f'{WWW_DATA}/2/cropped/{border.ident}.mp4'
    ffmpeg_utils.crop(
        width=border.width,
        height=border.height,
        left=border.left,
        top=border.top,
        input_file=input_file,
        output_file=output_file,
    )
    return output_file


def save_masked(mask_file: str, cropped_video: str, border: Border):
    ffmpeg_utils.apply_mask(
        video_file=cropped_video,
        mask_file=mask_file,
        output_file=f'{WWW_DATA}/2/masked/out-{border.number}.webm'
    )


def generate_borders():
    algo = MaskAlgo.create()

    vertical_lines = algo.generate_vertical_lines()
    horizontal_lines = algo.reversed().generate_vertical_lines()

    metadata = {
        'relative_corners': {},
    }

    for i in range(algo.parts_x):
        for j in range(algo.parts_y):
            border = Border(
                ident=f'{i}-{j}',
                number=i * algo.parts_y + j + 1,
                left=None if i == 0 else vertical_lines[i - 1][j],
                right=None if i == algo.parts_x - 1 else vertical_lines[i][j],
                top=None if j == 0 else horizontal_lines[j - 1][i].reversed(),
                bottom=None if j == algo.parts_y - 1 else horizontal_lines[j][i].reversed(),
                top_left_corner=(i * algo.puzzle_width, j * algo.puzzle_height),
                puzzle_width=algo.puzzle_width,
                puzzle_height=algo.puzzle_height,
            )
            mask_file = save_mask(border)
            cropped_video = save_cropped(border, algo.settings.input_file)
            save_masked(mask_file, cropped_video, border)
            metadata['relative_corners'][border.number] = border.relative_corners

    with open(f'{WWW_DATA}/2/puzzle-metadata.js', 'w') as fp:
        fp.write('const PUZZLE_METADATA = ')
        fp.write(json.dumps(metadata, indent=2))


if __name__ == '__main__':
    generate_borders()
