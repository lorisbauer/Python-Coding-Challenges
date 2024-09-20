def moon_angle(t):
    return np.linspace(0, 2 * math.pi, t + 1)


def get_angle(pos1, pos2):
    distance_x, distance_y = pos1[0] - pos2[0], pos1[1] - pos2[1]
    return math.atan2(distance_y, distance_x)


def asteroid_belt(n):
    belt = []
    n1 = int(3 * n / 8)
    for _ in range(n1):
        distance = random.random() * 1.4 * Planet.AU + 2.2*Planet.AU
        angle = random.random() * 2 * math.pi
        x_distance = math.cos(angle) * distance
        y_distance = math.sin(angle) * distance
        belt.append(((SIZE / 2 + x_distance * Planet.SCALE, SIZE / 2 + y_distance * Planet.SCALE), random.randrange(1, 2)))
    return belt


class Moon:
    def __init__(self, distance, radius, color, t):
        self.distance = distance
        self.radius = radius
        self.color = color
        self.t = t
        self.pos = (0, 0)
        self.angles = moon_angle(self.t)
        self.orbit = []


class Planet:
    AU = 149.6 * 10 ** 6 * 1000
    G = 6.67428 * 10 ** -11
    SCALE = 85 / AU
    TIME_STEP = 3600 * 24

    def __init__(self, x, y, radius, color, mass, moon=None):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.moon = moon
        self.moon_time = 0
        self.paused = False

        self.x_vel = 0
        self.y_vel = 0

    def draw_obj(self):
        x = self.x * self.SCALE + SIZE / 2
        y = self.y * self.SCALE + SIZE / 2

        if len(self.orbit) > 2:
            p.draw.lines(SCREEN, self.color, False, self.orbit)
        p.draw.circle(SCREEN, self.color, (x, y), self.radius)
        if self.moon is not None:
            for moon in self.moon:
                self.draw_moon(moon)

    def draw_moon(self, moon):
        if self.paused is False:
            angle = moon.angles[self.moon_time]
            x_distance = math.cos(angle) * moon.distance
            y_distance = math.sin(angle) * moon.distance
            moon.pos = ((self.x + x_distance) * self.SCALE + SIZE / 2, (self.y + y_distance) * self.SCALE + SIZE / 2)
            moon.orbit.append(moon.pos)
            if self.moon_time < moon.t:
                self.moon_time += 1
            else:
                self.moon_time = 1
        p.draw.circle(SCREEN, moon.color, moon.pos, moon.radius)
        if len(moon.orbit) > 2:
            p.draw.lines(SCREEN, moon.color, False, moon.orbit)

    def attraction(self, obj):
        distance_x, distance_y = obj.x - self.x, obj.y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        force = self.G * self.mass * obj.mass / distance ** 2
        angle = math.atan2(distance_y, distance_x)
        force_x = math.cos(angle) * force
        force_y = math.sin(angle) * force
        return force_x, force_y

    def update_position(self, objects):
        fx_tot = fy_tot = 0
        for obj in objects:
            if self == obj:
                continue
            fx, fy = self.attraction(obj)
            fx_tot += fx
            fy_tot += fy
        self.x_vel += fx_tot / self.mass * self.TIME_STEP
        self.y_vel += fy_tot / self.mass * self.TIME_STEP

        self.x += self.x_vel * self.TIME_STEP
        self.y += self.y_vel * self.TIME_STEP
        self.orbit.append((self.x * self.SCALE + SIZE / 2, self.y * self.SCALE + SIZE / 2))


class Simulation:
    def __init__(self):
        self.objects = []
        self.belt = asteroid_belt(5000)
        self.paused = False
        self.running = True

    def draw(self):
        SCREEN.blit(BACKGROUND, (0, 0))
        for obj in self.objects:
            if obj.moon is not None and self.paused:
                obj.paused = True
            elif self.paused is False and obj.paused:
                obj.paused = False

            obj.draw_obj()
            if self.paused is False:
                obj.update_position(self.objects)
        if self.paused:
            SCREEN.blit(PLAY_BUTTON, (10, 10))
        for point in self.belt:
            pos, radius = point
            p.draw.circle(SCREEN, (107, 102, 102), pos, radius)
        p.display.update()

    def main(self):
        clock = p.time.Clock()
        sun = Planet(0, 0, 18, p.Color('yellow'), 1.98892 * 10 ** 30)

        earth = Planet(Planet.AU, 0, 8, (100, 149, 237), 5.9742 * 10 ** 24, [Moon(2 * 10 ** 10, 2, (213, 212, 205), 28)])
        earth.y_vel = -29.783 * 1000
        mars = Planet(1.524 * Planet.AU, 0, 6, (188, 39, 50), 6.29 * 10 ** 23)
        mars.y_vel = -24.077 * 1000
        mercury = Planet(0.387 * Planet.AU, 0, 4, (80, 78, 81), 3.3 * 10 ** 23)
        mercury.y_vel = -47.4 * 1000
        venus = Planet(0.723 * Planet.AU, 0, 8, (226, 223, 201), 4.8685 * 10 ** 24)
        venus.y_vel = -35.02 * 1000
        jupiter = Planet(5.2 * Planet.AU, 0, 12, (246, 232, 142), 1.898 * 10 ** 27)
        jupiter.y_vel = -13.06 * 1000
        self.objects = [sun, earth, mars, mercury, venus, jupiter]

        while self.running:
            clock.tick(FPS)
            for event in p.event.get():
                if event.type == QUIT:
                    self.running = False
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.paused = bool(self.paused - 1)
            self.draw()


if __name__ == '__main__':
    import pygame as p
    from pygame.locals import *
    import os
    import math
    import numpy as np
    import random
    p.init()

    SIZE = p.display.Info().current_h - 100
    FPS = 60
    BUTTON_SIZE = 150
    BACKGROUND = p.transform.scale(p.image.load(os.path.join('8k_stars_milky_way.jpg')), (SIZE*1.5, SIZE))
    PLAY_BUTTON = p.transform.scale(p.image.load(os.path.join('play-button.png')), (BUTTON_SIZE, BUTTON_SIZE))
    SCREEN = p.display.set_mode((SIZE, SIZE))

    simulation = Simulation()
    simulation.main()
