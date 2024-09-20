import pygame as p
from pygame.locals import *
import pygame.gfxdraw
import math
import numpy as np
p.init()


class Ray:
    def __init__(self, x, y, angle, max_length, scene_rect, objects):
        self.x = x
        self.y = y
        self.angle = angle
        self.max_length = max_length
        self.scene_rect = scene_rect
        self.objects = objects
        self.marker_update = True
        self.points = []

    def marker_points(self):
        self.points.clear()
        for i in range(int(self.max_length)):
            y_comp = math.sin(self.angle) * i
            x_comp = math.cos(self.angle) * i
            self.points.append((self.x + x_comp, self.y + y_comp))

    def filter_points(self):
        for point in self.points:
            for obj in self.objects:
                if obj.collidepoint(point):
                    return obj, point
            if not self.scene_rect.collidepoint(point):
                return None, point
        return None, None

    def draw(self):
        if self.marker_update:
            self.marker_points()
        rect, point = self.filter_points()
        if point is not None:
            p.draw.line(SCREEN, p.Color('white'), (self.x, self.y), point)
            if rect is not None:
                return rect, point
        return None, None


class RayCasting:
    def __init__(self):
        self.running = True
        self.rays = []
        self.pos = (SIZE // 2, SIZE // 2)
        self.scene_rect = p.Rect(OUTLINE, OUTLINE, SIZE - 2 * OUTLINE, SIZE - 2 * OUTLINE)
        self.scene_objects = [p.Rect(400, 300, 250, 100), p.Rect(100, 200, 100, 250), p.Rect(350, 500, 100, 100)]

    @staticmethod
    def draw_rect_outline(surface, rect, color, width=1):
        x, y, w, h = rect
        width = max(width, 1)
        width = min(min(width, w // 2), h // 2)
        for i in range(width):
            p.gfxdraw.rectangle(surface, (x + i, y + i, w - i * 2, h - i * 2), color)

    def generate_rays(self, n, center):
        x, y = center
        angles = np.linspace(0, 2 * math.pi, n + 1)
        max_length = math.sqrt(2) * (SIZE - OUTLINE)
        for i in range(n):
            ray = Ray(x, y, angles[i], max_length, self.scene_rect, self.scene_objects)
            yield ray

    def draw_scene(self):
        for obj in self.scene_objects:
            p.draw.rect(SCREEN, SCENE_COLOR, obj)

    def draw(self):
        SCREEN.fill(p.Color('black'))
        self.draw_rect_outline(SCREEN, p.Rect(OUTLINE - OT, OUTLINE - OT,
                                              SIZE - 2 * OUTLINE + 2 * OT,
                                              SIZE - 2 * OUTLINE + 2 * OT), p.Color('white'), OT)
        self.draw_scene()
        objects = {tuple(k): [] for k in self.scene_objects}
        for ray in self.rays:
            if self.pos == (ray.x, ray.y):
                ray.marker_update = False
            ray.x, ray.y = self.pos
            rect, point = ray.draw()
            if rect is not None:
                objects[tuple(rect)].append(point)
            if ray.marker_update is False:
                ray.marker_update = True
        for points in list(objects.values()):
            if len(points) >= 2:
                p.draw.lines(SCREEN, p.Color('white'), False, points, 2)

    def main(self):
        clock = p.time.Clock()
        self.rays = list(self.generate_rays(450, self.pos))
        while self.running:
            clock.tick(FPS)
            mouse = p.mouse.get_pos()
            for event in p.event.get():
                if event.type == QUIT:
                    self.running = False
                    p.quit()
            if self.scene_rect.collidepoint(mouse):
                self.pos = mouse
            self.draw()
            p.display.flip()


if __name__ == '__main__':
    SIZE, OUTLINE, OT = 720, 50, 5
    SCENE_COLOR = (140, 140, 140)
    FPS = 100
    SCREEN = p.display.set_mode((SIZE, SIZE))

    win = RayCasting()
    win.main()
