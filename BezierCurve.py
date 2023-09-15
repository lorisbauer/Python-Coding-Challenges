from math import factorial, dist
import pygame as p
from pygame import gfxdraw
from perlin_noise import PerlinNoise
from itertools import chain
import numpy as np
from time import perf_counter
p.init()

SIZE = 800
CELLS = 20
PATH_CELLS = 80
UPSCALE_FACTOR = 10
CELL_SIZE = SIZE // (CELLS * UPSCALE_FACTOR)
FPS = 40
RADIUS = 10
ORIGIN_RADIUS = RADIUS + 5
OCTAVES = 4
SCREEN = p.display.set_mode((SIZE, SIZE))


def draw_rect_outline(screen: p.Surface, color: tuple[int, int, int] | p.Color, rect: p.Rect, width: int = 1) -> None:
    x, y, w, h = rect
    width = min(min(max(width, 1), w // 2), h // 2)
    for i in range(width):
        gfxdraw.rectangle(screen, (x + i, y + i, w - i * 2, h - i * 2), color)


def draw_circle(screen: p.Surface, color: tuple[int, int, int] | p.Color, center: tuple, radius: int) -> None:
    if radius > 1:
        p.draw.circle(screen, (0, 0, 0), center, radius)
        p.draw.circle(screen, color, center, radius - 1)


def lerp(x: float, s1: float, e1: float, s2: float, e2: float) -> float:
    if x > e1:
        return e2
    if x < s1:
        return s2
    return s2 + (x - s1) * (e2 - s2) / (e1 - s1)


class Point:
    def __init__(self, pos: tuple[float, float], color: tuple = (255, 0, 0),
                 radius: int = RADIUS, ending: bool = False):
        self.pos = pos
        self.color = color
        self.radius = radius
        self.ending = ending
        self.x, self.y = self.pos
        self.selected = False

    def select(self):
        self.selected = True

    def unselect(self):
        self.selected = False

    def collide(self, mouse_pos: tuple) -> bool:
        return dist(self.pos, mouse_pos) < RADIUS

    def move(self, mouse_pos: tuple):
        if self.selected:
            self.pos = mouse_pos
            self.x, self.y = self.pos

    def draw(self):
        draw_circle(SCREEN, self.color, self.pos, self.radius)
        if self.selected:
            p.draw.circle(SCREEN, (255, 0, 0), self.pos, self.radius * 1.5, width=2)


class Square:
    def __init__(self, pos: tuple[int, int], size: int):
        self.pos = pos
        self.size = size
        self.x, self.y = self.pos
        self.x_transl, self.y_transl = self.x * self.size, self.y * self.size
        self.color = (0, 0, 0)
        self.rect = p.Rect(self.x_transl, self.y_transl, self.size, self.size)

    def draw(self) -> None:
        p.draw.rect(SCREEN, self.color, self.rect)
        draw_rect_outline(SCREEN, (255, 255, 255), self.rect)

    def get_center(self) -> tuple:
        return self.x_transl + self.size / 2, self.y_transl + self.size / 2

    def circle_collision(self, point: tuple, radius: int) -> bool:
        x, y = point
        rect_center_x, rect_center_y = self.get_center()

        distance_x = abs(x - rect_center_x)
        distance_y = abs(y - rect_center_y)

        if distance_x > (self.size / 2 + radius) or distance_y > (self.size / 2 + radius):
            return False

        if distance_x <= (self.size / 2) or distance_y <= (self.size / 2):
            return True

        corner_distance_sq = (distance_x - self.size / 2) ** 2 + (distance_y - self.size / 2) ** 2
        return corner_distance_sq <= radius ** 2


class Curve:
    def __init__(self, points: list, n_elements: int):
        self.points = points
        self.n_elements = n_elements
        self.length = len(self.points)
        self.curve = self.linear_interpolation_for_lines()

    def evaluate(self, t: float, points: list) -> tuple[float, float]:
        x = y = 0
        length = len(points)
        n = self.length - 1
        for k, point in enumerate(points):
            coeff = factorial(n) / (factorial(n - k) * factorial(k))
            factor = coeff * (1 - t) ** (length - k - 1) * t ** k
            x += factor * point.x
            y += factor * point.y
        pos = (x, y)
        return pos

    def linear_interpolation_for_lines(self) -> list:
        inc = 1 / self.n_elements
        t = 0
        curve = []
        i = 0
        while i <= self.n_elements:
            pos = self.evaluate(t, self.points)
            curve.append(Point(pos))
            t += inc
            i += 1
        return curve

    def get_curve(self) -> list:
        return [elem.pos for elem in self.curve]

    def __str__(self):
        return f"{[elem.pos for elem in self.curve]}"


class Background:
    def __init__(self, width: int, height: int, octaves: int):
        self.width, self.height = width, height
        self.depth = 0
        self.grid = np.zeros((self.width, self.height))
        self.noise = PerlinNoise(octaves=octaves)
        self.scale = 0.01
        self.inc = 0.5
        self.steps = 400
        self.mixed_colors = self.interpolate_colors([(100, 100, 100), (150, 150, 150)], self.steps)

    @staticmethod
    def interpolate_colors(colors: list, steps: int) -> list:
        mixed_colors = []

        for i in range(len(colors) - 1):
            c1 = colors[i]
            c2 = colors[i + 1]

            step_size = 1 / steps

            for j in range(steps):
                t = j * step_size
                mixed_color = tuple(
                    int((1 - t) * c1[k] + t * c2[k])
                    for k in range(3)
                )
                mixed_colors.append(mixed_color)

        return mixed_colors

    def regenerate(self):
        self.generate_layer()
        self.translate()
        self.upscale()

    def upscale(self):
        input_height, input_width = self.grid.shape

        output_height = input_height * UPSCALE_FACTOR
        output_width = input_width * UPSCALE_FACTOR
        output_array = np.zeros((output_height, output_width))

        for y in range(output_height):
            for x in range(output_width):
                x_input = x / UPSCALE_FACTOR
                y_input = y / UPSCALE_FACTOR

                x0 = int(x_input)
                x1 = min(x0 + 1, input_width - 1)
                y0 = int(y_input)
                y1 = min(y0 + 1, input_height - 1)

                dx = x_input - x0
                dy = y_input - y0

                interpolated_value = (
                        self.grid[y0, x0] * (1 - dx) * (1 - dy) +
                        self.grid[y0, x1] * dx * (1 - dy) +
                        self.grid[y1, x0] * (1 - dx) * dy +
                        self.grid[y1, x1] * dx * dy
                )

                output_array[y, x] = interpolated_value
        self.grid = output_array

    def generate_layer(self) -> None:
        for x in range(self.width):
            for y in range(self.height):
                self.grid[x][y] = self.noise([x * self.scale, y * self.scale, self.depth * self.scale])
        self.depth += self.inc

    def translate(self) -> None:
        unpacked = list(chain.from_iterable(self.grid))
        low, high = min(unpacked), max(unpacked)
        for i, row in enumerate(self.grid):
            for j, val in enumerate(row):
                k = lerp(val, low, high, 0, len(self.mixed_colors) - 1)
                self.grid[i][j] = k

    def draw_bg(self) -> None:
        self.regenerate()
        for i, row in enumerate(self.grid):
            for j, k in enumerate(row):
                color = self.mixed_colors[int(k)]
                p.draw.rect(SCREEN, color, p.Rect(i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        self.grid = np.zeros((self.width, self.height))


class Display:
    def __init__(self):
        self.n = 150
        self.path_radius = 20
        self.max_points = 100
        self.points = self.set_start_points()
        self.curve = self.generate_curve()
        self.running = True
        self.selected = False
        self.draw_path = False
        self.bg = Background(CELLS, CELLS, OCTAVES)
        self.squares = [Square((i, j), SIZE // PATH_CELLS) for i in range(PATH_CELLS) for j in range(PATH_CELLS)]

    @staticmethod
    def set_start_points() -> list:
        return [Point((SIZE // 4, SIZE // 2), (70, 140, 0), ORIGIN_RADIUS, True),
                Point((3 * SIZE // 4, SIZE // 2), (0, 70, 140), ORIGIN_RADIUS, True)]

    def generate_curve(self) -> list:
        return Curve(self.points, self.n).get_curve()

    def spawn_new_point(self, mouse_pos: tuple) -> None:
        if len(self.points) < self.max_points:
            point = Point(mouse_pos)
            self.points.insert(1, point)
            self.sort_points()

    def sort_points(self) -> None:
        anchor = self.points[0]
        self.points[1:len(self.points) - 1] =\
            sorted(self.points[1:len(self.points) - 1], key=lambda x: dist(anchor.pos, x.pos))

    def draw_curve(self) -> None:
        p.draw.aalines(SCREEN, (255, 255, 255), False, self.curve)

    def draw_points(self):
        for point in self.points:
            point.draw()

    def pathing(self):
        for i, point in enumerate(self.curve):
            if i not in [0, len(self.curve) - 1]:
                for square in self.squares:
                    if square.circle_collision(point, self.path_radius):
                        square.draw()

    def draw(self) -> None:
        SCREEN.fill((150, 150, 150))
        self.bg.draw_bg()
        if self.draw_path:
            self.pathing()
        else:
            self.draw_curve()
        self.draw_points()
        p.display.update()

    def main(self) -> None:
        clock = p.time.Clock()
        while self.running:
            clock.tick(FPS)
            mouse = p.mouse.get_pos()
            for event in p.event.get():
                if event.type == p.QUIT:
                    self.running = False
                if event.type == p.MOUSEBUTTONDOWN:
                    for point in self.points:
                        if point.collide(mouse):
                            if self.selected is not False and point == self.selected:
                                self.selected.unselect()
                                self.selected = False
                            else:
                                if self.selected is not False:
                                    self.selected.unselect()
                                point.select()
                                self.selected = point
                            break
                if event.type == p.KEYDOWN:
                    if event.key == p.K_s:
                        self.spawn_new_point(mouse)
                    elif event.key == p.K_BACKSPACE:
                        if self.selected is not False and\
                                self.points.index(self.selected) not in [0, len(self.points) - 1]:
                            self.points.remove(self.selected)
                            self.selected = False
                    elif event.key == p.K_TAB:
                        self.draw_path = bool(int(self.draw_path) - 1)
            if self.selected is not False:
                self.selected.move(mouse)
            self.draw()
            self.sort_points()
            self.curve = self.generate_curve()


if __name__ == '__main__':
    display = Display()
    display.main()
