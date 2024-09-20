import time
import pygame as p
import pygame.gfxdraw
import math
from pygame.locals import *


class Clock:
    def __init__(self):
        self.run = True
        self.combined = self.get_attr()

    @staticmethod
    def get_attr():
        sizes = {
            'hour': int((HEIGHT // 2) * .3),
            'minute': int((HEIGHT // 2) * .55),
            'second': int((HEIGHT // 2) * .7)
        }
        colors = {
            'hour': (255, 255, 255),
            'minute': (255, 0, 0),
            'second': (0, 0, 255)
        }
        values = zip(sizes.values(), colors.values())
        return dict(zip(['hour', 'minute', 'second'], values))

    @staticmethod
    def draw_rect_outline(surface, rect, color, width=1):
        x, y, w, h = rect
        width = min(min(max(width, 1), w // 2), h // 2)
        for i in range(width):
            p.gfxdraw.rectangle(surface, (x + i, y + i, w - i * 2, h - i * 2), color)

    @staticmethod
    def get_time():
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        return [int(value) for value in current_time.split(':')]

    @staticmethod
    def get_angles(t):
        h, m, s = t
        return (math.radians(h / 24 * 360) - math.pi / 2,
                math.radians(m / 60 * 360) - math.pi / 2,
                math.radians(s / 60 * 360) - math.pi / 2)

    @staticmethod
    def calculate_point(angle, size):
        x, y = CENTER
        x_comp = math.cos(angle) * size
        y_comp = math.sin(angle) * size
        return x + x_comp, y + y_comp

    def draw(self):
        SCREEN.fill((0, 70, 140))
        SCREEN.blit(CLOCK, (WIDTH // 2 - IMG // 2, HEIGHT // 2 - IMG // 2))
        current_time = self.get_time()
        angles = self.get_angles(current_time)
        for i in range(len(angles)):
            angle = angles[-i]
            size, color = list(self.combined.values())[-i]
            end_point = self.calculate_point(angle, size)
            p.draw.line(SCREEN, color, CENTER, end_point, 5)
        p.draw.circle(SCREEN, p.Color('black'), CENTER, 20)
        p.display.update()

    def main(self):
        clock = p.time.Clock()
        while self.run:
            clock.tick(FPS)
            for event in p.event.get():
                if event.type == QUIT:
                    self.run = False
                    p.quit()
            self.draw()


if __name__ == '__main__':
    WIDTH = HEIGHT = 720
    FPS = 60
    IMG = 600
    SCREEN = p.display.set_mode((WIDTH, HEIGHT))
    CENTER = (WIDTH // 2, HEIGHT // 2)
    CLOCK = p.transform.scale(p.image.load('clock.png'), (IMG, IMG))
    cl = Clock()
    cl.main()
