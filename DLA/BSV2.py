import pygame as p
from pygame.locals import *
import math
import random
p.init()

SIZE = 640
FPS = 60
ANGLE = -math.pi / 6
RADIUS = 2
HEIGHT = 300
NUMBER = 600
DUP = 6
X_VEL, Y_VEL = 2.5, 1
X, Y = (SIZE // 2, SIZE // 2)
SCREEN = p.display.set_mode((SIZE, SIZE))


class Walker:
    def __init__(self, x, y, color, radius):
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius
        self.stuck = False

    def vector_angle(self):
        x_comp, y_comp = self.x - X, self.y - Y
        return math.atan(y_comp / x_comp)

    def restriction(self, x, y):
        x_comp, y_comp = X - (self.x + x), Y - (self.y + y)
        return (self.x + x) <= X - self.radius and \
               x_comp != 0 and math.pi / 2 + ANGLE < abs(math.atan(y_comp / x_comp)) < math.pi / 2

    def checkStuck(self, walkers):
        if self.y + self.radius * 2 >= Y:
            self.stuck = True
        else:
            for walker in walkers:
                if math.dist((walker.x, walker.y), (self.x, self.y)) <= self.radius * 2:
                    self.stuck = True
                    break

    def update(self):
        if self.stuck is False:
            x, y = random.uniform(-X_VEL, X_VEL), Y_VEL
            if self.restriction(x, y):
                self.x += x
                self.y += y

    def draw(self):
        p.draw.circle(SCREEN, self.color, (self.x, self.y), self.radius)


class Flake:
    def __init__(self, n, dup):
        self.n = n
        self.dup = dup
        self.base = 2 * math.pi / self.dup
        self.run = True
        self.walker = self.generate_walker()
        self.tree = []

    @staticmethod
    def mirror(line_x, tree):
        mirrored_tree = [*tree]
        for obj in tree:
            x1, y1 = obj.x, obj.y
            distance = math.dist((x1, y1), (line_x, y1))
            x1 += 2 * distance
            mirrored_tree.append(Walker(x1, y1, obj.color, obj.radius))
        return mirrored_tree

    def duplicate(self, combined):
        result = [*combined]
        for point in combined:
            x, y = point.x, point.y
            x1, y1 = (SIZE // 2, SIZE // 2)
            vectors = self.get_vectors((x - x1, y - y1))
            for (x2, y2) in vectors:
                result.append((Walker(x2, y2, point.color, point.radius)))
        return result

    def get_vectors(self, line):
        x, y = line
        vectors = []
        for i in range(1, self.dup):
            angle = i * self.base
            x1 = x * math.cos(angle) - y * math.sin(angle)
            y1 = x * math.sin(angle) + y * math.cos(angle)
            vectors.append((SIZE // 2 + x1, SIZE // 2 + y1))
        return vectors

    def generate_walker(self):
        self.n -= 1
        return Walker(X - RADIUS, Y - HEIGHT + RADIUS, p.Color('white'), RADIUS)

    def update(self):
        while self.walker.stuck is False and self.n > 0:
            self.walker.update()
            self.walker.checkStuck(self.tree)
        else:
            self.tree.append(self.walker)
            self.walker = self.generate_walker()

        result = self.duplicate(self.mirror(SIZE // 2, self.tree))
        for element in result:
            element.draw()

    def draw(self):
        SCREEN.fill((0, 70, 140))
        self.update()
        p.display.update()

    def main(self):
        clock = p.time.Clock()
        while self.run:
            clock.tick(FPS)
            for event in p.event.get():
                if event.type == QUIT:
                    self.run = False
            self.draw()


if __name__ == '__main__':
    snowflake = Flake(NUMBER, DUP)
    snowflake.main()
