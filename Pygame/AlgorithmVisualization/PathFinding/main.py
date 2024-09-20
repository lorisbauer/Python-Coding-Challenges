import pygame as p
from pygame import gfxdraw
from pygame.locals import *
from queue import PriorityQueue
from MazeGenerator import Maze
from helper import gradient, get_surrounding

SIZE = 680
p.init()

OUTLINE, EDGE = 30, 10
DIMENSION = int((SIZE - 2*OUTLINE)//20)
FPS = 60
TILE_SIZE = (SIZE - 2*OUTLINE)//DIMENSION
SCREEN = p.display.set_mode((SIZE, SIZE), SHOWN, 64, vsync=1)


class Tile:
    def __init__(self, pos, state='empty'):
        self.pos = pos
        self.state = state


class Main:
    def __init__(self):
        self.run = True
        self.selected = False
        self.colors = {
            'empty': tuple(p.Color('white')),
            'wall': (77, 77, 77), 
            'src': tuple(p.Color('red')), 
            'path': tuple(p.Color('red'))
            }
        self.start, self.end = None, None
        self.mapped = False
        self.mouse_rect = p.Rect(SIZE//2, SIZE//2, TILE_SIZE, TILE_SIZE)
        self.map = [[Tile((i, j)) for j in range(DIMENSION)] for i in range(DIMENSION)]
        self.translated = self.translate_map()
        self.gradient_length = self.counter(self.map)
        self.gradient = gradient(self.gradient_length, (2, 1, 0), mixture=False)

    @staticmethod
    def draw_rect_outline(surface, rect, color, width=1):
        x, y, w, h = rect
        width = min(min(max(width, 1), w//2), h//2)
        for i in range(width):
            gfxdraw.rectangle(surface, (x+i, y+i, w-i*2, h-i*2), color)
       
    @staticmethod
    def translate_coordinate(pos):
        x, y = pos
        return (x*TILE_SIZE + OUTLINE, y*TILE_SIZE + OUTLINE)
    
    def get_surroundings(self, pos, looked):
        x, y = pos
        elements = []
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        for (a, b) in directions:
            x1, y1 = (x + a, y + b)
            if 0 <= x1 < DIMENSION and 0 <= y1 < DIMENSION and (x1, y1) not in looked and self.map[x1][y1].state != 'wall':
                elements.append((x1, y1))
        return elements
    
    def counter(self, map, target='empty', listed=False):
        count = 0
        positions = []
        for i in range(len(map)):
            for _, element in enumerate(map[i]):
                if element.state == target:
                    count += 1
                    if listed:
                        positions.append(element.pos)
        if listed:
            return positions
        return count
    
    def draw_tiles(self):
        for i in range(DIMENSION):
            for j, tile in enumerate(self.map[i]):
                if type(tile.state) != int:
                    p.draw.rect(SCREEN, self.colors.get(tile.state), p.Rect(i*TILE_SIZE + OUTLINE, j*TILE_SIZE + OUTLINE, TILE_SIZE, TILE_SIZE))
                else:
                    p.draw.rect(SCREEN, self.gradient.get(tile.state), p.Rect(i*TILE_SIZE + OUTLINE, j*TILE_SIZE + OUTLINE, TILE_SIZE, TILE_SIZE))

    def draw_map_raster(self, target):
        elements = self.counter(self.map, target, listed=True)
        for pos in elements:
            self.draw_outline(pos, target)
    
    def draw_outline(self, pos, target):
        surrounding = get_surrounding(self.map, pos, target)
        x, y = pos
        for (a, b) in surrounding:
            start_offset_x = a - x if a - x >= 0 else 0
            start_offset_y = b - y if b - y >= 0 else 0
            end_offset_x = a - x + 1 if a - x <= 0 else 1
            end_offset_y = b - y + 1 if b - y <= 0 else 1

            start_x, start_y = self.translate_coordinate((x + start_offset_x, y + start_offset_y))
            end_x, end_y = self.translate_coordinate((x + end_offset_x, y + end_offset_y))
            p.draw.line(SCREEN, p.Color('black'), (start_x, start_y), (end_x, end_y), 2)
    
    def draw_default_raster(self):
        for _, elements in enumerate(self.translated):
            for rect in elements:
                x, y, _, _ = rect
                for pos in [(x, y + TILE_SIZE), (x + TILE_SIZE, y)]:
                    p.draw.line(SCREEN, p.Color('black'), (x, y), pos)

    def draw(self):
        SCREEN.fill((0, 70, 140))
        p.draw.rect(SCREEN, p.Color('white'), p.Rect(OUTLINE, OUTLINE, SIZE - 2*OUTLINE, SIZE - 2*OUTLINE))
        self.draw_rect_outline(SCREEN, p.Rect(OUTLINE - EDGE//2, OUTLINE - EDGE//2, SIZE - 2*(OUTLINE - EDGE//2), SIZE - 2*(OUTLINE - EDGE//2)), p.Color('black'), EDGE)
        self.draw_tiles()
        if self.mapped:
            self.draw_map_raster('wall')
        else:
            self.draw_default_raster()
        if self.selected is False:
            self.draw_rect_outline(SCREEN, self.mouse_rect, p.Color('black'), 2)
        p.display.update()
    
    def translate_map(self):
        elements = [[None for _ in range(DIMENSION)] for _ in range(DIMENSION)]
        for i in range(DIMENSION):
            for j, element in enumerate(self.map[i]):
                x, y = element.pos
                elements[i][j] = p.Rect(x*TILE_SIZE + OUTLINE, y*TILE_SIZE + OUTLINE, TILE_SIZE, TILE_SIZE)
        return elements
    
    def update_state_count(self, pos):
        x, y = pos
        if self.map[x][y].state != 'src':
            for i in range(len(self.map)):
                for _, element in enumerate(self.map[i]):
                    if type(element.state) != str and element.state < self.gradient_length - 1:
                        if element.state > 100:
                            element.state += 1
                        else:
                            element.state += 50
            self.map[x][y].state = 1
    
    def reconstruct_path(self, came_from, current):
        while current in came_from:
            current = came_from[current]
            x, y = current
            self.map[x][y].state = 'path'
            self.draw()
            p.time.delay(25)

    def dijkstra(self, start, end):
        for (x, y) in [start, end]:
            self.map[x][y].state = 'src'

        q = PriorityQueue()
        came_from = {}
        solved = False
        looked = {start}
        q.put((0, start))
        
        while not q.empty():
            value, pos = q.get()
            if pos == end:
                solved = True
                break

            self.update_state_count(pos)
            self.draw()
            for (x, y) in self.get_surroundings(pos, looked):
                came_from[(x, y)] = pos
                if self.map[x][y].state != 'src':
                    self.map[x][y].state = 1
                self.draw()                       
                q.put((value + 1, (x, y)))
                looked.add((x, y))
                if (x, y) == end:
                    break

        if solved: 
            self.reconstruct_path(came_from, end)
            p.time.delay(5000)
            self.__init__()
        else:
            p.time.delay(1000)
            self.run = False
    
    def a_star(self, start, end):
        for (x, y) in [start, end]:
            self.map[x][y].state = 'src'

        def h(p1):
            x1, y1 = p1
            x2, y2 = end
            return abs(x1 - x2) + abs(y1 - y2)

        open_set = PriorityQueue()
        solved = False
        count = 0
        open_set.put((0, count, start))
        looked = {start}
        g_score = {(i, j): float('inf') for i in range(DIMENSION) for j in range(DIMENSION)}
        g_score[start] = 0
        f_score = {(i, j): float('inf') for i in range(DIMENSION) for j in range(DIMENSION)}
        f_score[start] = h(start)
        came_from = {}

        while not open_set.empty():
            pos = open_set.get()[-1]
            looked.remove(pos)

            if pos == end:
                solved = True
                break

            self.update_state_count(pos)
            self.draw()
            for (x, y) in self.get_surroundings(pos, looked):
                temp_g_score = g_score[pos] + 1
                if temp_g_score < g_score[(x, y)]:
                    came_from[(x, y)] = pos
                    g_score[(x, y)] = temp_g_score
                    f_score[(x, y)] = temp_g_score + h((x, y))
                    if self.map[x][y].state != 'src':
                        self.map[x][y].state = 1
                    self.draw()
                    if (x, y) not in looked:
                        count += 1
                        open_set.put((f_score[(x, y)], count, (x, y)))
                        looked.add((x, y))
        if solved:
            self.reconstruct_path(came_from, end)
            p.time.delay(3000)
            self.__init__()
        else:
            p.time.delay(1000)
            self.run = False
 
    def main(self):
        clock = p.time.Clock()
        while self.run:
            clock.tick(FPS)
            for event in p.event.get():
                if event.type == QUIT:
                    self.run = False
                    p.quit()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 3:
                        for i in range(DIMENSION):
                            for _, rect in enumerate(self.translated[i]):
                                if rect.collidepoint(p.mouse.get_pos()):
                                    x, y, _, _ = rect
                                    x, y = (x - OUTLINE)//TILE_SIZE, (y - OUTLINE)//TILE_SIZE
                                    if self.map[x][y].state != 'wall':
                                        if self.map[x][y].state != 'src':
                                            self.map[x][y].state = 'src'
                                            if self.start is None:
                                                self.start = (x, y)
                                            elif self.end is None:
                                                self.end = (x, y)
                                        else:
                                            self.map[x][y].state = 'empty'
                                            if self.start is not None and self.end is None:
                                                self.start = None
                                            else:
                                                x1, y1 = self.end
                                                self.map[x1][y1].state = 'empty'
                                                self.end = None
                                        break
                if event.type == KEYDOWN:
                    if event.key == K_RETURN and self.end is not None:
                        self.selected = True
                    if event.key == K_g and self.selected is False and all((self.start is None, self.end is None)):
                        self.mapped = True
                        obj = Maze(DIMENSION)
                        mapped = obj.path_generator()
                        self.map = [[Tile((i, j), state) for j, state in enumerate(mapped[i])] for i in range(DIMENSION)]

            if self.selected is False:
                for i in range(DIMENSION):
                    for _, rect in enumerate(self.translated[i]):
                        if rect.collidepoint(p.mouse.get_pos()):
                            self.mouse_rect = rect
                self.draw()
            elif self.selected:
                self.a_star(self.start, self.end)


if __name__ == '__main__':
    main = Main()
    main.main()
