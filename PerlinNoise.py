import pygame as p
from perlin_noise import PerlinNoise
from itertools import chain
import numpy as np
p.init()

SIZE = 800
CELLS = 20
UPSCALE_FACTOR = 8
CELL_SIZE = SIZE // (CELLS * UPSCALE_FACTOR)
FPS = 60
OCTAVES = 10
SCREEN = p.display.set_mode((SIZE, SIZE))


def lerp(x: float, s1: float, e1: float, s2: float, e2: float) -> float:
    if x > e1:
        return e2
    if x < s1:
        return s2
    return s2 + (x - s1) * (e2 - s2) / (e1 - s1)


class Background:
    def __init__(self, width: int, height: int, octaves: int):
        self.width, self.height = width, height
        self.depth = 0
        self.grid = np.zeros((self.width, self.height))
        self.noise = PerlinNoise(octaves=octaves)
        self.scale = 0.01
        self.inc = 0.5
        self.steps = 200
        self.mixed_colors = self.interpolate_colors([(150, 0, 0), (255, 0, 0), (0, 255, 255), (0, 0, 255), (0, 0, 0)], self.steps)

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

    def upscale(self) -> None:
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
                k = int(lerp(val, low, high, 0, len(self.mixed_colors) - 1))
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
        self.running = True
        self.bg = Background(CELLS, CELLS, OCTAVES)

    def draw(self) -> None:
        SCREEN.fill((255, 255, 255))
        self.bg.draw_bg()
        p.display.update()

    def main(self) -> None:
        clock = p.time.Clock()
        while self.running:
            clock.tick(FPS)
            for event in p.event.get():
                if event.type == p.QUIT:
                    self.running = False
            self.draw()


if __name__ == '__main__':
    display = Display()
    display.main()
