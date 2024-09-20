
class Map:
    def __init__(self):
        self.maze = Maze(SIZE, TILE)
        self.entrances = {v:k for k,v in self.maze.path_generator().items()}
        self.map = self.maze.maze
        self.origin = (0, 0)
        self.pos = self.entrances.get('start')
        self.x_shift, self.y_shift = self.shift()
        self.movement_log = [self.pos]
        self.colors = {'w': p.Color('brown'), 'c': p.Color('white')}
        self.tiles = {((i + self.x_shift)*TILE, (j + self.y_shift)*TILE, TILE, TILE): self.colors.get(self.map[i][j]) if (i,j) not in list(self.entrances.values()) else p.Color('blue') if (i,j) == self.pos else p.Color('green') for i in range(SIZE//TILE) for j in range(SIZE//TILE)}
        self.images = {tuple(p.Color('brown')): WALL, tuple(p.Color('white')): FLOOR, tuple(p.Color('blue')): START, tuple(p.Color('green')): END}
        self.walls = self.get_walls()
    
    @staticmethod
    def draw_rect_outline(surface, rect, color, width=1):
        x, y, w, h = rect
        width = min(min(max(width, 1), w//2), h//2)
        for i in range(width):
            p.gfxdraw.rectangle(surface, (x+i, y+i, w-i*2, h-i*2), color)
    
    def get_walls(self):
        walls = []
        for i in range(len((element:=list(self.tiles.values())))):
            if element[i] == p.Color('brown'):
                walls.append(list(self.tiles.keys())[i])
        return walls
    
    def get_passages(self):
        passages = {}
        for i in range(len((element:=list(self.tiles.values())))):
            if element[i] == p.Color('blue'):
                passages['start'] = list(self.tiles.keys())[i][:2]
            elif element[i] == p.Color('green'):
                passages['end'] = list(self.tiles.keys())[i][:2]
        return passages
    
    def end_line(self):
        passages = self.get_passages()
        x, y = passages.get('end')
        return ((x + TILE, y), (x + TILE, y + TILE))
    
    def outlines(self, rect):
        x, y, w, h = rect
        num = 2
        return {'top': p.Rect(x, y - num, w, num), 'right': p.Rect(x + w, y, num, h), 
                'left':p.Rect(x - num, y, num, h), 'bottom':p.Rect(x, y + h, w, num)}
        
    def shift(self):
        x_shift, y_shift = tuple(np.subtract(self.origin, self.pos))
        return (x_shift + WIDTH//2/TILE - .5, y_shift + HEIGHT//2/TILE - .5)
    
    def movement(self):
        if self.movement_log[-1] != self.pos and (element:= tuple(np.subtract(self.movement_log[-1], self.pos))) != (0,0):
            self.movement_log.append(self.pos)
            x, y = element
            elements = {}
            for i in range(len(self.tiles)):
                x1, y1 = list(list(self.tiles.keys())[i])[:2]
                x1, y1 = x1 + x*MOVEMENT, y1 + y*MOVEMENT
                elements[(x1, y1, TILE, TILE)] = self.tiles.get(list(self.tiles.keys())[i])
            return elements
        return self.tiles
                              
    def draw(self):
        SCREEN.fill(p.Color('gray'))
        passages = self.get_passages()
        for i in range(len(self.tiles)):
            element = list(self.tiles.keys())[i]
            if p.Rect(element).colliderect(p.Rect(0, 0, WIDTH, HEIGHT)):
                x, y = element[:2]
                SCREEN.blit(self.images.get(tuple(list(self.tiles.values())[i])), (x, y))
                if (x, y) in list(passages.values()):
                    Map.draw_rect_outline(SCREEN, p.Rect(x, y, TILE, TILE), p.Color('black'), 4)
        p.draw.line(SCREEN, p.Color('black'), *self.end_line(), 8)
        p.draw.circle(SCREEN, p.Color('black'), (WIDTH//2, HEIGHT//2), PLAYER_SIZE)
        p.display.update()
    
    def main(self):
        run = True
        clock = p.time.Clock()
        while run:
            hitbox = p.Rect(WIDTH//2 - PLAYER_SIZE, HEIGHT//2 - PLAYER_SIZE, PLAYER_SIZE*2, PLAYER_SIZE*2)
            outlines = self.outlines(hitbox)
            clock.tick(FPS)
            keys = p.key.get_pressed()
            for event in p.event.get():
                if event.type == QUIT:
                    run = False
                    p.quit()
            if hitbox.clipline(self.end_line()):
                p.time.delay(2000)
                run = False
                map = Map()
                map.main()

            walls = self.get_walls()
            x, y = self.pos
            if keys[K_RIGHT] and not outlines.get('right').collidelistall(walls):
                x+=1
            if keys[K_LEFT] and not outlines.get('left').collidelistall(walls):
                x-=1
            if keys[K_DOWN] and not outlines.get('bottom').collidelistall(walls):
                y+=1
            if keys[K_UP] and not outlines.get('top').collidelistall(walls):
                y-=1
            self.pos = (x, y)
            
            self.tiles = self.movement()
            p.display.flip()
            self.draw()


if __name__ == '__main__':
    import pygame as p
    from pygame.locals import *
    import pygame.gfxdraw
    import numpy as np
    from generator import Maze
    import os

    WIDTH = HEIGHT = 660
    SIZE = 8000
    TILE = SIZE//25
    PLAYER_SIZE = 20
    MOVEMENT = 20
    FPS = 30
    SCREEN = p.display.set_mode((WIDTH, HEIGHT))
    FLOOR = p.transform.scale(p.image.load(os.path.join('images', 'floor.jpg')), (TILE, TILE))
    WALL = p.transform.scale(p.image.load(os.path.join('images', 'wall.png')), (TILE, TILE))
    END = p.transform.scale(p.image.load(os.path.join('images', 'end.png')), (TILE, TILE))
    START = p.transform.scale(p.image.load(os.path.join('images', 'start.jpg')), (TILE, TILE))
    PLAYER = p.transform.scale(p.image.load(os.path.join('images', 'blue_tank.png')), (PLAYER_SIZE, PLAYER_SIZE))

    map = Map()
    map.main()