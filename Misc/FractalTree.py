import pygame as p
from pygame.locals import *
import numpy as np
import math
p.init()

SIZE = 600
FPS = 60
ANGLE = math.pi / 7
OFF = 80
CENTER = (SIZE // 2, SIZE // 2 + OFF)
TRUNK = 150
LENGTH = 200
RATE = 0.65
MIN = 12
N = 11
SCREEN = p.display.set_mode((SIZE, SIZE))


def rotate(x, y, angle):
    x1 = x * math.cos(angle) - y * math.sin(angle)
    y1 = x * math.sin(angle) + y * math.cos(angle)
    return x1, y1


def generate_branches(n, last, point, length):
    if n == 0:
        return True
    if length > MIN:
        length = int(length * RATE)
    scaled = last / np.linalg.norm(last) * length
    a, b = point
    x, y = scaled

    x1, y1 = rotate(x, y, ANGLE)
    x1, y1 = a + x1, b + y1
    x2, y2 = rotate(x, y, math.pi * 2 - ANGLE)
    x2, y2 = a + x2, b + y2
    p.draw.aaline(SCREEN, p.Color('white'), (a, b), (x1, y1))
    p.draw.aaline(SCREEN, p.Color('white'), (a, b), (x2, y2))
    p.display.update()
    p.time.delay(25)
    for (x, y) in [(x1, y1), (x2, y2)]:
        vector = np.subtract(np.array((x, y)), np.array(point))
        generate_branches(n - 1, vector, (x, y), length)
    return True


class Tree:
    def __init__(self, n):
        self.n = n
        self.run = True

    def draw(self):
        SCREEN.fill((0, 70, 140))
        x, y = CENTER
        p.draw.aaline(SCREEN, p.Color('white'), CENTER, (x, y + TRUNK))
        generate_branches(self.n, np.array(np.subtract(np.array(CENTER), np.array((x, y + TRUNK)))), CENTER, LENGTH)
        p.time.delay(2000)
        self.run = False

    def main(self):
        clock = p.time.Clock()
        while self.run:
            clock.tick(FPS)
            for event in p.event.get():
                if event.type == QUIT:
                    self.run = False
            self.draw()


if __name__ == '__main__':
    tree = Tree(N)
    tree.main()
