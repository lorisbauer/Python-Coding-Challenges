import pygame as p
from pygame import gfxdraw
import random
from itertools import permutations
p.init()

SIZE = 630
FPS = 60
DIMENSION = SIZE // 15
UNVISITED = (0, 0, 0)
VISITED = (100, 202, 253)
WALL = (0, 0, 0)
CURRENT = (255, 0, 0)
OFFSET = 1.5
DELAY = 10
SCREEN = p.display.set_mode((SIZE, SIZE))


class Point:
    def __init__(self, x, y, color, square):
        self.x = x
        self.y = y
        self.color = color
        self.square = square
        self.visited = False
        self.walls = self.gen_walls()

    def gen_walls(self):
        walls = {
            'N': [(self.x, self.y), (self.x + 1, self.y)],
            'W': [(self.x, self.y), (self.x, self.y + 1)],
            'E': [(self.x + 1, self.y), (self.x + 1, self.y + 1)],
            'S': [(self.x, self.y + 1), (self.x + 1, self.y + 1)]

        }
        return walls

    def draw(self):
        p.draw.rect(SCREEN, self.color, p.Rect(self.x * self.square + OFFSET, self.y * self.square + OFFSET,
                                               self.square - OFFSET // 2, self.square - OFFSET // 2))
        if self.visited:
            for (start, end) in self.walls.values():
                x, y = start[0] * self.square, start[1] * self.square
                x1, y1 = end[0] * self.square, end[1] * self.square
                p.draw.line(SCREEN, WALL, (x, y), (x1, y1), 2)


class DFS:
    def __init__(self, square, dimension):
        self.square = square
        self.dimension = dimension
        self.maze = [[Point(i, j, UNVISITED, self.square) for j in range(self.dimension)] for i in range(self.dimension)]
        self.start = self.start_point()
        self.current = self.start
        self.swap = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}

    def start_generation(self):
        self.generate(self.start)
        self.current = None

    @staticmethod
    def draw_rect_outline(surface, color, rect, width=1):
        x, y, w, h = rect
        width = min(min(max(width, 1), w // 2), h // 2)
        for i in range(width):
            gfxdraw.rectangle(surface, (x + i, y + i, w - i * 2, h - i * 2), color)

    def start_point(self):
        x = random.randrange(0, self.dimension)
        y = random.randrange(0, self.dimension)
        self.maze[x][y].visited = True
        self.maze[x][y].color = VISITED
        return self.maze[x][y]

    def surrounding(self, element):
        directions = list(permutations([0, -1], 2)) + list(permutations([1, 0], 2))
        names = ['N', 'W', 'E', 'S']
        combined = {k: v for k, v in zip(directions, names)}
        surrounding = []
        for (a, b) in combined.keys():
            if 0 <= element.x + a < self.dimension and 0 <= element.y + b < self.dimension and \
                    self.maze[element.x + a][element.y + b].visited is False:
                d = combined[(a, b)]
                surrounding.append([d, self.maze[element.x + a][element.y + b]])
        return surrounding

    def generate(self, element):
        if not (surrounding := self.surrounding(element)):
            return True
        self.draw()
        random.shuffle(surrounding)
        for collection in surrounding:
            direction, obj = collection
            if obj.visited is False:
                element.walls.pop(direction)
                obj.walls.pop(self.swap[direction])
                obj.visited = True
                obj.color = VISITED
                self.current = obj
                self.generate(obj)

    def draw(self):
        SCREEN.fill(p.Color('white'))
        for i, elements in enumerate(self.maze):
            for j, element in enumerate(self.maze[i]):
                element.draw()
        if self.current is not None:
            color = self.current.color
            self.current.color = CURRENT
            self.current.draw()
            self.current.color = color
            self.draw_rect_outline(SCREEN, p.Color('white'), p.Rect(self.current.x * self.square + OFFSET,
                                                                    self.current.y * self.square + OFFSET,
                                                                    self.square - OFFSET // 2,
                                                                    self.square - OFFSET // 2))

        self.draw_rect_outline(SCREEN, WALL,
                               p.Rect(0, 0, self.dimension * self.square, self.dimension * self.square), 4)
        p.display.update()
        p.time.delay(DELAY)


class Display:
    def __init__(self, dimension):
        self.dimension = dimension
        self.run = True
        self.square = SIZE // self.dimension
        self.generator = DFS(self.square, self.dimension)

    def draw(self):
        self.generator.draw()

    def main(self):
        clock = p.time.Clock()
        while self.run:
            clock.tick(FPS)
            for event in p.event.get():
                if event.type == p.QUIT:
                    self.run = False
                if event.type == p.KEYDOWN:
                    if event.key == p.K_SPACE:
                        self.generator.start_generation()
            self.draw()


if __name__ == '__main__':
    display = Display(DIMENSION)
    display.main()
