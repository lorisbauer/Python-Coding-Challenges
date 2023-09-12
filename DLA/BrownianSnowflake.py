import pygame as p
from pygame.locals import *
import math
import random
p.init()

SIZE = 640
FPS = 60
VEL = 2
SEGMENT = 4 * (SIZE // 2) // 5
WIDTH, THICKNESS, RADIUS, GAP = 35, 50, 1, 20
STARTS = 2 * SEGMENT // 5
NUMBER = STARTS * 9
SCREEN = p.display.set_mode((SIZE, SIZE))


class Walker:
    def __init__(self, x, y, color, radius, limit):
        self.x = x
        self.y = y
        self.x_min, self.y_min = limit
        self.color = color
        self.radius = radius
        self.stuck = False

    def restriction(self, x, y):
        return self.x_min + self.radius < self.x + x < self.x_min + WIDTH \
               and self.y_min + self.radius < self.y + y < self.y_min + SEGMENT - GAP // 2

    def checkStuck(self, walkers):
        for walker in walkers:
            if math.dist((walker.x, walker.y), (self.x, self.y)) <= self.radius * 2:
                self.stuck = True
                break

    def update(self):
        if self.stuck is False:
            x, y = random.randrange(-VEL, VEL + 1), random.randrange(-VEL, VEL + 1)
            if self.restriction(x, y):
                self.x += x
                self.y += y

    def draw(self):
        p.draw.circle(SCREEN, self.color, (self.x, self.y), self.radius)


class Snowflake:
    def __init__(self, n):
        self.n = n
        self.base = 2 * math.pi / self.n
        self.run = True
        self.start_points = sorted(random.sample(range(GAP // 2, SEGMENT - GAP, 2), STARTS))
        self.limit = (SIZE // 2 - WIDTH, SIZE // 2 - SEGMENT)
        self.tree = []
        self.side = []
        self.counter = 0
        self.line_vectors = self.get_vectors((0, -(SEGMENT - GAP)), 0, self.n)

    @staticmethod
    def mirror(line_x, tree):
        mirrored_tree = [*tree]
        for obj in tree:
            x1, y1 = obj.x, obj.y
            distance = math.dist((x1, y1), (line_x, y1))
            x1 += 2 * distance
            mirrored_tree.append(Walker(x1, y1, obj.color, obj.radius, (obj.x_min, obj.y_min)))
        return mirrored_tree

    def duplicate(self, combined):
        result = [*combined]
        for point in combined:
            x, y = point.x, point.y
            x1, y1 = (SIZE // 2, SIZE // 2)
            vectors = self.get_vectors((x - x1, y - y1), 1, self.n)
            for (x2, y2) in vectors:
                result.append((Walker(x2, y2, point.color, point.radius, (point.x_min, point.y_min))))
        return result

    def get_vectors(self, line, start, end):
        x, y = line
        vectors = []
        for i in range(start, end):
            angle = i * self.base
            x1 = x * math.cos(angle) - y * math.sin(angle)
            y1 = x * math.sin(angle) + y * math.cos(angle)
            vectors.append((SIZE // 2 + x1, SIZE // 2 + y1))
        return vectors

    def setup(self):
        for y in self.start_points:
            start = Walker(SIZE // 2 - RADIUS, SIZE // 2 - y, p.Color('white'), RADIUS, self.limit)
            start.stuck = True
            self.tree.append(start)

        for _ in range(NUMBER):
            walker = Walker(random.randint(self.limit[0] + RADIUS, self.limit[0] + WIDTH - RADIUS),
                            random.randint(self.limit[1] + RADIUS, self.limit[1] + SEGMENT - RADIUS),
                            p.Color('white'), RADIUS, self.limit)
            self.side.append(walker)

    def update_main_tree(self):
        if len(self.side) > 1 * NUMBER // 3:
            for walker in self.side:
                if walker.stuck:
                    self.tree.append(walker)
                    self.side.remove(walker)
                else:
                    walker.checkStuck(self.tree)
                    walker.update()

        result = self.duplicate(self.mirror(SIZE // 2, self.tree))
        for element in result:
            element.draw()

    def draw(self):
        SCREEN.fill((0, 70, 140))
        for vector in self.line_vectors:
            p.draw.line(SCREEN, p.Color('white'), vector, (SIZE // 2, SIZE // 2), 3)
        self.update_main_tree()
        p.display.update()

    def main(self):
        clock = p.time.Clock()
        self.setup()
        while self.run:
            clock.tick(FPS)
            for event in p.event.get():
                if event.type == QUIT:
                    self.run = False
            self.draw()


if __name__ == '__main__':
    snowflake = Snowflake(6)
    snowflake.main()
