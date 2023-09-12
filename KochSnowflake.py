import pygame as p
from pygame.locals import *
from itertools import pairwise
import math
import operator
p.init()

SIZE = 700
FPS = 60
SCREEN = p.display.set_mode((SIZE, SIZE))


class Snowflake:
    def __init__(self, bg, n, side_length=(2 * SIZE // 3)):
        self.bg = bg
        self.n = n
        self.side_length = side_length
        self.length = math.sqrt(self.side_length ** 2 - (self.side_length // 2) ** 2)
        self.line = self.get_start_points()
        self.run = True
        self.count = 0
        self.draw_sf = False

    def get_start_points(self):
        start = (int((SIZE - self.length) / 2), int((SIZE - self.length) / 2 - (SIZE - 2 * self.length) // 2))
        line = [start]
        for a in [(self.length, 0), (self.length // 2, self.length)]:
            line.append(tuple(map(operator.add, start, a)))
        line.append(start)
        return [list(pairwise(line))]

    def edge_division(self, cord):
        start, end = cord
        line = []
        x1, y1 = start
        x2, y2 = end
        distance = (x2 - x1, y2 - y1)
        for i in range(3):
            vector = [element / 3 * (i + 1) for element in distance]
            point = (start if not line else line[-1][1], tuple(map(operator.add, start, vector)))
            line.append(point)
        return self.extrusion(line, [element / 3 for element in distance])

    @staticmethod
    def extrusion(line, vector):
        line.pop(1)
        x, y = vector
        x1 = x * math.cos(5 * math.pi / 3) - y * math.sin(5 * math.pi / 3)
        y1 = x * math.sin(5 * math.pi / 3) + y * math.cos(5 * math.pi / 3)
        anchor = line[0][1]
        point = tuple(map(operator.add, anchor, [x1, y1]))
        line.insert(1, (anchor, point))
        line.insert(2, (point, line[2][0]))
        return line

    def draw_snowflake(self, line):
        lines = []
        for element in line:
            lines.append(self.edge_division(element))
        for line in lines:
            for (start, end) in line:
                p.draw.line(SCREEN, p.Color('white'), start, end)
        return lines

    def draw(self):
        SCREEN.fill(self.bg)
        lines = []
        if self.draw_sf:
            for line in self.line:
                if len(self.line) != 1:
                    for element in self.draw_snowflake(line):
                        lines.append(element)
                else:
                    lines = self.draw_snowflake(line)
            if self.n > self.count + 1:
                self.count += 1
                self.line = lines
                p.time.delay(1000)
        else:
            for (start, end) in self.line[0]:
                p.draw.line(SCREEN, p.Color('white'), start, end)
        p.display.update()

    def main(self):
        clock = p.time.Clock()
        while self.run:
            clock.tick(FPS)
            for event in p.event.get():
                if event.type == QUIT:
                    self.run = False
                    p.quit()
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        self.draw_sf = True
            self.draw()


if __name__ == '__main__':
    snowflake = Snowflake((0, 70, 140), 8)
    snowflake.main()
