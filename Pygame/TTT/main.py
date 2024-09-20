import pygame as p
from copy import deepcopy
from pygame.locals import *
from pygame.gfxdraw import *

def rotate(l):
    rotated = [[0 for _ in range(len(l))] for _ in range(len(l))]
    for i in range(len(l)):
        for j in range(len(l[i])):
            x, y = j, len(l) - i - 1
            rotated[x][y] = l[i][j]
    return rotated

def winner(game, target):
    diagonal = [(i, i) for i in range(len(game))]
    rotations = 2
    for i in range(rotations):
        if i == rotations//2:
            game = rotate(game)
        for j in range(len(game)):
            if len(element := list(set(game[j]))) == 1 and element[-1] is not None and element[-1] == target:
                return True
        if len(element := list(set([game[x][y] for (x, y) in diagonal]))) == 1 and element[-1] is not None and element[-1] == target:
            return True
    return False

def find_empty(game, value=None):
    return [(i, j) for i, sub in enumerate(game) for j, val in enumerate(sub) if val == value]

def evaluation(game, target):
    empty = find_empty(game)
    num = 0
    if empty:
        for (x, y) in empty:
            game[x][y] = target
            if winner(game, target):
                num += 1
            game[x][y] = None
    return num

def convert(game, empty, target):
    childs = []
    for (x, y) in empty:
        child = deepcopy(game)
        child[x][y] = target
        childs.append(child)
    return childs
        
class Interface:
    def __init__(self):
        self.screen = p.display.set_mode((WIDTH, HEIGHT))
        self.background = [p.Rect(i*TILE, j*TILE, TILE, TILE) for i in range(LENGTH) for j in range(LENGTH)]
        self.game = [[None for _ in range(LENGTH)] for _ in range(LENGTH)]
    
    @staticmethod
    def draw_rect_outline(surface, color, rect, width=1):
        x, y, w, h = rect
        width = min(min(max(width, 1), w//2), h//2)
        for i in range(width):
            p.gfxdraw.rectangle(surface, (x+i, y+i, w-i*2, h-i*2), color)
    
    @staticmethod
    def rect_to_pos(rect):
        x, y = list(rect)[:2]
        return (x//TILE, y//TILE)
    
    def draw(self):
        for _,element in enumerate(self.background):
            p.draw.rect(self.screen, BACKGROUND_COLOR, element)
            Interface.draw_rect_outline(self.screen, p.Color('black'), element, 3)
        p.display.update()
    
    def main(self):
        run = True
        clock = p.time.Clock()
        while run:
            clock.tick(FPS)
            for event in p.event.get():
                if event.type == QUIT:
                    run = False
                    p.quit()
            p.display.flip()
            self.draw()

if __name__ == '__main__':
    WIDTH, HEIGHT = 600, 600
    LENGTH = 3
    TILE = WIDTH//LENGTH
    BACKGROUND_COLOR = (0,34,102)
    FPS = 30
    
    # interface = Interface()
    # interface.main()

    game = [
        [None, None, None],
        [None, 2, None],
        [None, None, None]
    ]