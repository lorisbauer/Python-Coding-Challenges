import pygame as p
from pygame.locals import *
import pygame.gfxdraw
p.init()


class lightLevel:
    def __init__(self):
        self.run = True

    @staticmethod
    def draw_rect_outline(surface, rect, color, width=1):
        x, y, w, h = rect
        width = min(min(max(width, 1), w // 2), h // 2)
        for i in range(width):
            p.gfxdraw.rectangle(surface, (x + i, y + i, w - i * 2, h - i * 2), color)

    def draw(self):
        SCREEN.blit(BG, (0, 0))
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
    SIZE = 720
    FPS = 100
    SCREEN = p.display.set_mode((SIZE, SIZE))
    BG = p.transform.scale(p.image.load('wall.jpg'), (SIZE, SIZE))

    level = lightLevel()
    level.main()
