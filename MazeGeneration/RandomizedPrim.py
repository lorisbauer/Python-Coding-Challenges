import pygame as p
from pygame import gfxdraw
import random
from itertools import permutations

p.init()

SIZE = 660
FPS = 60
VISITED = (86, 192, 245)
WALL = (0, 0, 0)
CURRENT = (255, 0, 0)
DIMENSION = SIZE // 15
DELAY = 0
SCREEN = p.display.set_mode((SIZE, SIZE))


class Point:
    def __init__(self, x, y, color, square):
        self.x = x
        self.y = y
        self.color = color
        self.square = square
        self.unvisited = True

    def draw(self):
        p.draw.rect(SCREEN, self.color,
                    (rect := p.Rect(self.x * self.square, self.y * self.square, self.square, self.square)))


class RP:
    def __init__(self, square, dimension):
        self.square = square
        self.dimension = dimension
        self.maze = [[Point(i, j, WALL, self.square) for j in range(self.dimension)] for i in range(self.dimension)]
        self.walls = []
        self.start = self.start_point()
        self.current = self.start

    @staticmethod
    def draw_rect_outline(surface, color, rect, width=1):
        x, y, w, h = rect
        width = min(min(max(width, 1), w // 2), h // 2)
        for i in range(width):
            gfxdraw.rectangle(surface, (x + i, y + i, w - i * 2, h - i * 2), color)

    def start_generation(self):
        self.generate()
        self.current = None

    def surrounding(self, element):
        directions = list(permutations([0, -1], 2)) + list(permutations([1, 0], 2))
        surrounding = []
        for (x, y) in directions:
            if 0 <= element.x + x < self.dimension and 0 <= element.y + y < self.dimension and \
                    self.maze[element.x + x][element.y + y].unvisited:
                surrounding.append(self.maze[element.x + x][element.y + y])
        return surrounding

    def divided(self, obj):
        pairs = [[(-1, 0), (1, 0)], [(0, -1), (0, 1)]]
        result = []
        for element in pairs:
            unvis = []
            vis = []
            for (x, y) in element:
                if 0 <= obj.x + x < self.dimension and 0 <= obj.y + y < self.dimension:
                    if self.maze[obj.x + x][obj.y + y].unvisited:
                        unvis.append(self.maze[obj.x + x][obj.y + y])
                    else:
                        vis.append(self.maze[obj.x + x][obj.y + y])
            if len(unvis) == 1 and len(vis) == 1:
                result.append(*unvis)
        return result

    def start_point(self):
        x = random.randrange(1, self.dimension)
        y = random.randrange(1, self.dimension)
        self.maze[x][y].color = VISITED
        self.maze[x][y].unvisited = False
        if surrounding := self.surrounding(self.maze[x][y]):
            for wall in surrounding:
                self.walls.append(wall)
        return self.maze[x][y]

    def generate(self):
        if not self.walls:
            return True
        wall = random.choice(self.walls)
        if array := self.divided(wall):
            cell = random.choice(array)
            self.current = cell
            wall.color = VISITED
            wall.unvisited = False
            cell.color = VISITED
            cell.unvisited = False
            if surrounding := self.surrounding(cell):
                for point in surrounding:
                    if point not in self.walls:
                        self.walls.append(point)
        self.walls.remove(wall)
        self.draw()
        self.generate()

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
        p.display.update()
        p.time.delay(DELAY)


class Display:
    def __init__(self, dimension):
        self.dimension = dimension
        self.run = True
        self.square = SIZE // self.dimension
        self.generator = RP(self.square, self.dimension)

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
