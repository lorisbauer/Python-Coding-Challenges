import pygame as p
from pygame import gfxdraw
import random
from math import dist
p.init()

SIZE = 800
FPS = 60
RADIUS = 2
SCREEN = p.display.set_mode((SIZE, SIZE))


def draw_rect_outline(screen: p.Surface, color: tuple[int, int, int] | p.Color, rect: p.Rect, width: int = 1) -> None:
    x, y, w, h = rect
    width = min(min(max(width, 1), w // 2), h // 2)
    for i in range(width):
        gfxdraw.rectangle(screen, (x + i, y + i, w - i * 2, h - i * 2), color)


class Point:
    def __init__(self, pos: tuple):
        self.pos = pos
        self.x, self.y = self.pos
        self.color = (255, 0, 0)

    def draw(self):
        p.draw.circle(SCREEN, self.color, self.pos, RADIUS)


class Circle:
    def __init__(self, pos: tuple, radius: int):
        self.pos = pos
        self.x, self.y = self.pos
        self.radius = radius

    def contains(self, point: Point) -> bool:
        return dist(self.pos, point.pos) < self.radius

    def draw(self):
        p.draw.circle(SCREEN, (0, 255, 0), self.pos, self.radius, 2)


class Rectangle:
    def __init__(self, x: int, y: int, w: int, h: int):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.rect = p.Rect(self.x - self.w, self.y - self.h, self.w * 2, self.h * 2)

    def get_attr(self):
        return self.x, self.y, self.w, self.h

    def contains(self, point: Point):
        return self.x - self.w <= point.x <= self.x + self.w and self.y - self.h <= point.y <= self.y + self.h

    def intersects_rect(self, area) -> bool:
        return not (area.x - area.w > self.x + self.w or area.x + area.w < self.x - self.w or
                    area.y - area.h > self.y + self.h or area.y + area.h < self.y - self.h)

    def intersects_circle(self, area) -> bool:
        x, y = area.pos
        rect_center_x, rect_center_y = self.x, self.y
        w, h = self.w * 2, self.h * 2

        distance_x = abs(x - rect_center_x)
        distance_y = abs(y - rect_center_y)

        if distance_x > (w / 2 + area.radius) or distance_y > (h / 2 + area.radius):
            return False

        if distance_x <= (w / 2) or distance_y <= (h / 2):
            return True

        corner_distance_sq = (distance_x - w / 2) ** 2 + (distance_y - h / 2) ** 2
        return corner_distance_sq <= area.radius ** 2

    def draw(self):
        draw_rect_outline(SCREEN, (0, 0, 0), self.rect)


class QuadTree:
    def __init__(self, boundary: Rectangle, n: int):
        self.boundary = boundary
        self.capacity = n
        self.points = []
        self.northwest = self.northeast = self.southwest = self.southeast = None
        self.divided = False

    def subdivide(self):
        x, y, w, h = self.boundary.get_attr()
        nw = Rectangle(x + w // 2, y - h // 2, w // 2, h // 2)
        ne = Rectangle(x - w // 2, y - h // 2, w // 2, h // 2)
        sw = Rectangle(x + w // 2, y + h // 2, w // 2, h // 2)
        se = Rectangle(x - w // 2, y + h // 2, w // 2, h // 2)

        self.northwest = QuadTree(nw, self.capacity)
        self.northeast = QuadTree(ne, self.capacity)
        self.southwest = QuadTree(sw, self.capacity)
        self.southeast = QuadTree(se, self.capacity)
        self.divided = True

    def insert(self, point: Point):
        if not self.boundary.contains(point):
            return False
        if len(self.points) < self.capacity:
            self.points.append(point)
            return True
        else:
            if not self.divided:
                self.subdivide()
            if self.northwest.insert(point):
                return True
            elif self.northeast.insert(point):
                return True
            elif self.southwest.insert(point):
                return True
            elif self.southeast.insert(point):
                return True

    def query(self, area: Rectangle | Circle, found: list):
        if type(area) == Rectangle and not self.boundary.intersects_rect(area) or \
                type(area) == Circle and not self.boundary.intersects_circle(area):
            return
        else:
            for point in self.points:
                if type(area) == Rectangle and area.contains(point) \
                        or type(area) == Circle and area.contains(point):
                    found.append(point)
            if self.divided:
                self.northwest.query(area, found)
                self.northeast.query(area, found)
                self.southwest.query(area, found)
                self.southeast.query(area, found)
        return found

    def show(self):
        self.boundary.draw()
        for point in self.points:
            point.draw()
        if self.divided:
            self.northwest.show()
            self.northeast.show()
            self.southwest.show()
            self.southeast.show()


class Display:
    def __init__(self):
        self.running = True
        self.qt = QuadTree(Rectangle(SIZE // 2, SIZE // 2, SIZE // 2, SIZE // 2), 4)

    def insert_qt(self):
        for _ in range(2000):
            point = Point((random.uniform(0, SIZE), random.uniform(0, SIZE)))
            self.qt.insert(point)

    def test_qt(self):
        x, y = p.mouse.get_pos()
        # area = Rectangle(x, y, 100, 100)
        # draw_rect_outline(SCREEN, (0, 255, 0), area.rect)
        area = Circle((x, y), 100)
        area.draw()
        points = self.qt.query(area, [])
        for point in points:
            p.draw.circle(SCREEN, (0, 255, 0), point.pos, RADIUS)

    def draw(self) -> None:
        SCREEN.fill((150, 150, 150))
        self.qt.show()
        self.test_qt()
        p.display.update()

    def main(self) -> None:
        clock = p.time.Clock()
        self.insert_qt()
        while self.running:
            clock.tick(FPS)
            for event in p.event.get():
                if event.type == p.QUIT:
                    self.running = False
            self.draw()


if __name__ == '__main__':
    display = Display()
    display.main()
