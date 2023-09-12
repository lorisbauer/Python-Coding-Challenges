import pygame as p
from pygame.locals import *
from PIL import ImageColor
from colour import Color
import random
import math
p.init()

SIZE = 600
RADIUS = 8
LENGTH = (SIZE - SIZE // 7) // 2
NUMBER = 1800
COLOR_RANGE = NUMBER // 180
VEL = 5
FPS = 60
SCREEN = p.display.set_mode((SIZE, SIZE))


class Walker:
    def __init__(self, x, y, color, radius):
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius
        self.stuck = False

    def restriction(self, x, y):
        return self.radius < self.x + x < SIZE - self.radius and self.radius < self.y + y < SIZE - self.radius

    def checkStuck(self, walkers):
        for walker in walkers:
            if math.dist((walker.x, walker.y), (self.x, self.y)) < self.radius + walker.radius:
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


class DLA:
    def __init__(self):
        self.run = True
        self.walkers = []
        self.tree = []
        self.counter = 0
        self.gradient = self.get_gradient()

    @staticmethod
    def get_gradient():
        gradient = {}
        red = Color("blue")
        colors = list(red.range_to(Color("red"), NUMBER // COLOR_RANGE + 1))
        for i, value in enumerate(colors):
            rgb = ImageColor.getcolor(str(value), "RGB")
            gradient[i + 1] = rgb
        return gradient

    def draw(self):
        SCREEN.fill((30, 30, 30))
        if len(self.walkers) > 15:
            for walker in self.walkers:
                if walker.stuck:
                    if walker.radius > 2:
                        index = self.tree.index(self.tree[-1]) + 1
                        color = self.gradient[index // COLOR_RANGE + 1]
                        walker.color = color
                        self.tree.append(walker)
                        self.walkers.remove(walker)
                else:
                    walker.radius -= self.counter
                    walker.checkStuck(self.tree)
                    walker.update()
                    self.counter += 3.9 * 10 ** -7

        for element in self.tree[1:]:
            element.draw()
        self.tree[0].draw()
        p.display.update()

    def main(self):
        clock = p.time.Clock()
        center = Walker(SIZE // 2, SIZE // 2, p.Color('white'), RADIUS)
        center.stuck = True
        self.tree.append(center)

        for _ in range(NUMBER):
            obj = Walker(random.randint(RADIUS, SIZE - RADIUS), random.randint(RADIUS, SIZE - RADIUS), p.Color('white'),
                         RADIUS)
            self.walkers.append(obj)

        while self.run:
            clock.tick(FPS)
            for event in p.event.get():
                if event.type == QUIT:
                    self.run = False
                    p.quit()
            self.draw()


if __name__ == '__main__':
    dla = DLA()
    dla.main()
