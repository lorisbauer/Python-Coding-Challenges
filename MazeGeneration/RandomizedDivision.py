import pygame as p
import random
from itertools import permutations
p.init()

SIZE = 660
FPS = 30
DIMENSION = SIZE // 6
DELAY = 0
WALL = p.Color(0, 0, 0)
PATH = p.Color(180, 180, 180)
MIN = 3
SCREEN = p.display.set_mode((SIZE, SIZE))


class Point:
    def __init__(self, x, y, color, square):
        self.x = x
        self.y = y
        self.color = color
        self.square = square
        self.hole = False

    def draw(self):
        p.draw.rect(SCREEN, self.color, p.Rect(self.x * self.square, self.y * self.square,
                                               self.square, self.square))


class RD:
    def __init__(self, dimension):
        self.dimension = dimension
        self.square = SIZE // self.dimension
        self.maze = [[Point(i, j, WALL, self.square) for j in range(self.dimension)] for i in range(self.dimension)]
        self.maze = self.border(self.maze, PATH)

    def start_generation(self):
        self.generate(1, 1, self.dimension - 2, self.dimension - 2)

    def border(self, maze, color):
        for i in range(self.dimension - 2):
            for j in range(self.dimension - 2):
                maze[1 + i][1 + j].color = color
        return maze

    def surrounding(self, element):
        directions = list(permutations([0, -1], 2)) + list(permutations([1, 0], 2))
        for (x, y) in directions:
            if 0 <= element.x + x < self.dimension and 0 <= element.y + y < self.dimension and \
                    self.maze[element.x + x][element.y + y].hole:
                return False
        return True

    def vertical_limit(self, x, y, width, height):
        elements = []
        for j in range(1, width - 1):
            if self.surrounding(self.maze[x + j][y]) and self.surrounding(self.maze[x + j][y + height - 1]):
                elements.append(j)
        return elements

    def horizontal_limit(self, x, y, width, height):
        elements = []
        for j in range(1, height - 1):
            if self.surrounding(self.maze[x][y + j]) and self.surrounding(self.maze[x + width - 1][y + j]):
                elements.append(j)
        return elements

    def vertical(self, x, y, width, height, selection):
        if selection:
            x_wall = random.choice(selection)
            holes = []
            if height >= self.dimension // 2:
                for value in random.sample(range(height), *random.choices([1, 2, 3], weights=[1, 3, 1])):
                    if value + 1 not in holes and value - 1 not in holes:
                        self.maze[x + x_wall][y + value].hole = True
                        holes.append(value)
            else:
                hole = random.randint(0, height - 1)
                self.maze[x + x_wall][y + hole].hole = True
                holes.append(hole)
            for i in range(height):
                if i not in holes:
                    self.maze[x + x_wall][y + i].color = WALL
            return [(x, y, x_wall, height), (x + x_wall + 1, y, width - x_wall - 1, height)]
        return False

    def horizontal(self, x, y, width, height, selection):
        if selection:
            y_wall = random.choice(selection)
            holes = []
            if width >= self.dimension // 2:
                for value in random.sample(range(width), *random.choices([1, 2, 3], weights=[1, 3, 1])):
                    if value + 1 not in holes and value - 1 not in holes:
                        self.maze[x + value][y + y_wall].hole = True
                        holes.append(value)
            else:
                hole = random.randint(0, width - 1)
                self.maze[x + hole][y + y_wall].hole = True
                holes.append(hole)
            for i in range(width):
                if i not in holes:
                    self.maze[x + i][y + y_wall].color = WALL
            return [(x, y, width, y_wall), (x, y + y_wall + 1, width, height - y_wall - 1)]
        return False

    def axis(self, x, y, width, height):
        filtered = list(filter(lambda a: a >= 3, [width, height]))
        if len(filtered) < 2:
            elements = self.vertical(x, y, width, height, self.vertical_limit(x, y, width, height)) if filtered[0] == width \
                else self.horizontal(x, y, width, height, self.horizontal_limit(x, y, width, height))
            return elements
        else:
            v_lim = self.vertical_limit(x, y, width, height)
            h_lim = self.horizontal_limit(x, y, width, height)

            if len(v_lim) > len(h_lim):
                return self.vertical(x, y, width, height, v_lim)
            elif len(v_lim) < len(h_lim):
                return self.horizontal(x, y, width, height, h_lim)
            else:
                vertical = random.choice([True, False])
                if vertical:
                    return self.vertical(x, y, width, height, v_lim)
                else:
                    return self.horizontal(x, y, width, height, h_lim)

    def generate(self, x, y, width, height):
        if width * height < MIN * (MIN - 1):
            return True
        elements = self.axis(x, y, width, height)
        if elements is False:
            return True
        self.draw()
        for element in elements:
            x1, y1, w, h = element
            self.generate(x1, y1, w, h)

    def draw(self):
        SCREEN.fill((0, 70, 140))
        for i, elements in enumerate(self.maze):
            for j, element in enumerate(self.maze[i]):
                element.draw()
        p.display.update()
        p.time.delay(DELAY)


class Display:
    def __init__(self, dimension):
        self.dimension = dimension
        self.run = True
        self.generator = RD(self.dimension)

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
            self.generator.draw()


if __name__ == '__main__':
    display = Display(DIMENSION)
    display.main()
