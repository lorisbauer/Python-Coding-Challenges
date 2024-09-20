
class Player:
    def __init__(self, pos: tuple, color):
        self.x, self.y = pos
        self.color = color

class GUI:
    def __init__(self):
        self.maze = Maze(STANDARD_SIZE, DIMENSIONS)
        self.entrances = self.maze.path_generator()
        self.setting = self.maze.maze
        self.astar = Algorithm(Maze.translation(copy.deepcopy(self.setting)), list(self.entrances.keys())[0], list(self.entrances.keys())[1])
        self.path = self.astar.main()
        self.progress = self.astar.progress
        self.directions = {'left': (-1, 0), 'right': (1,0), 'forwards': (0,1), 'backwards': (0,-1)}
        self.maze_setting = {(i, j): 90*random.randint(0, 3) for i in range(len(self.setting)) for j in range(len(self.setting))}
        self.mouse = (0,0)
        self.time = 0
        self.start_time = 0
        self.solve = False
        self.rects = {}
        self.search = []
        p.display.set_caption('Maze')
    
    @staticmethod
    def draw_rect_outline(surface, rect, color, width=1):
        x, y, w, h = rect
        width = max(width, 1)
        width = min(min(width, w//2), h//2)
        for i in range(width):
            p.gfxdraw.rectangle(surface, (x+i, y+i, w-i*2, h-i*2), color)
    
    def draw(self, player):
        SCREEN.fill(p.Color('brown'))

        self.draw_maze()
        self.maze_outline()

        time_text = FONT.render(f'Time: {self.time//1000}', True, p.Color('white'))

        if button.collidepoint(self.mouse[0], self.mouse[1]):
            p.draw.rect(SCREEN, p.Color('gray'), button)
        else:
            p.draw.rect(SCREEN, (100,100,100), button)
        GUI.draw_rect_outline(SCREEN, button, p.Color('black'))

        SCREEN.blit(solve_text, (STANDARD_SIZE - solve_text.get_width() - THICKNESS*4, 10 + THICKNESS))
        SCREEN.blit(time_text, (10, 10))

        if self.solve:
            t = int(self.time//SEARCH_SPEED - self.start_time)
            self.astar_algorithm(t)

        p.draw.circle(SCREEN, player.color, (player.x, player.y), DIMENSIONS//3)
        p.display.update()
    
    def astar_algorithm(self, t):
        shortest = FONT.render(f'Length: {len(self.path) - 2}', True, p.Color('white'))
        SCREEN.blit(shortest, (STANDARD_SIZE/2 - shortest.get_width()/2, 10 + THICKNESS))
        
        if t < len(self.progress):
            x, y = self.progress[t][0]
            value, colors = self.progress[t][1], {1: p.Color('red'), 0: p.Color('green')}
            self.search.append([SCREEN, colors[value], p.Rect(x*DIMENSIONS, y*DIMENSIONS + OUTLINE, DIMENSIONS, DIMENSIONS)])         
            for i in range(len(self.search)):
                p.draw.rect(*self.search[i])
                GUI.draw_rect_outline(SCREEN, self.search[i][-1], p.Color('black'))
        else:
            for j in range(len(self.path)):
                x, y = self.path[j]
                rect = p.Rect(x*DIMENSIONS, y*DIMENSIONS + OUTLINE, DIMENSIONS, DIMENSIONS)
                p.draw.rect(SCREEN, p.Color('white'), rect)
                GUI.draw_rect_outline(SCREEN, rect, p.Color('black'))
    
    @staticmethod
    def inside(pos: tuple):
        x, y = pos
        return 0 <= x <= STANDARD_SIZE//DIMENSIONS - 1 and 0 <= y <= STANDARD_SIZE//DIMENSIONS - 1
    
    def surrounding(self, pos, target: str):
        elements = []
        for i in range(len(self.directions)):
            x, y = list(map(operator.add, pos, list(self.directions.values())[i]))
            if GUI.inside((x,y)):
                if self.setting[x][y] == target:
                    elements.append(list(self.directions.keys())[i])
        return elements

    def maze_outline(self):
        walls, _ = self.types()
        for i in range(len(walls)):
            x, y = walls[i]
            surrounding = self.surrounding((x, y), 'c')
            if len(surrounding) > 0:
                x1 , y1 = (x*DIMENSIONS, y*DIMENSIONS + OUTLINE)
                for j in range(len(surrounding)):
                    direction = surrounding[j]
                    if direction == 'left':
                        p.draw.line(SCREEN, p.Color('black'), (x1,y1), (x1, y1 + DIMENSIONS), 3)
                    elif direction == 'right':
                        p.draw.line(SCREEN, p.Color('black'), (x1 + DIMENSIONS, y1), (x1 + DIMENSIONS, y1 + DIMENSIONS), 2)
                    elif direction == 'forwards':
                        p.draw.line(SCREEN, p.Color('black'), (x1, y1 + DIMENSIONS), (x1 + DIMENSIONS, y1 + DIMENSIONS), 2)
                    elif direction == 'backwards':
                        p.draw.line(SCREEN, p.Color('black'), (x1,y1), (x1 + DIMENSIONS, y1), 2)
                                       
    def draw_maze(self):
        for k in range(len(self.maze_setting)):
            i, j = list(self.maze_setting.keys())[k]
            rect = p.Rect(i*DIMENSIONS, j*DIMENSIONS + OUTLINE, DIMENSIONS, DIMENSIONS)
            p.draw.rect(SCREEN, p.Color('white'), rect)
            if (i,j) not in list(self.entrances.keys()):
                SCREEN.blit(p.transform.rotate(ASSIGNMENT[self.maze.symbols.get(self.setting[i][j])], self.maze_setting[(i,j)]), (i*DIMENSIONS, j*DIMENSIONS + OUTLINE))
            else:
                SCREEN.blit(p.transform.rotate(ASSIGNMENT[self.entrances[(i,j)]], self.maze_setting[(i,j)]), (i*DIMENSIONS, j*DIMENSIONS + OUTLINE))           
            self.rects[(i,j)] = {'rect': rect, 'center': (i*DIMENSIONS + DIMENSIONS/2, j*DIMENSIONS + DIMENSIONS/2 + OUTLINE)}
        GUI.draw_rect_outline(SCREEN, p.Rect(0, 0, STANDARD_SIZE, OUTLINE), p.Color('black'), THICKNESS)
        GUI.draw_rect_outline(SCREEN, p.Rect(0, OUTLINE, STANDARD_SIZE, STANDARD_SIZE), p.Color('black'), THICKNESS)
  
    def draw_path(self, path, color: str):
        for i in range(1, len(path)):
            x1, y1 = path[i - 1]
            x2, y2 = path[i]
            p.draw.line(SCREEN, p.Color(color), self.rects[(x1, y1)]['center'], self.rects[(x2, y2)]['center'], 2)
    
    def types(self):
        walls, paths = [], []
        for i in range(len(self.setting)):
            for j in range(len(self.setting)):
                if self.setting[i][j] == 'w':
                    walls.append((i, j))
                else:
                    paths.append((i, j))
        return walls, paths

    def main(self):
        run = True
        clock = p.time.Clock()
        startx, starty = list(self.entrances.keys())[0]
        player = Player((startx*DIMENSIONS + DIMENSIONS/2, starty*DIMENSIONS + DIMENSIONS/2 + OUTLINE), p.Color('blue'))
        while run:
            clock.tick(FPS)
            self.mouse = p.mouse.get_pos()
            self.time = p.time.get_ticks()
            for event in p.event.get():
                if event.type == QUIT:
                    run = False
                    p.quit()
                if event.type == MOUSEBUTTONDOWN:
                    if button.collidepoint(self.mouse[0], self.mouse[1]):
                        if self.solve is False:
                            self.solve = True
                            self.start_time = self.time//SEARCH_SPEED
                        else:
                            self.solve = False
                            self.search.clear()
            p.display.flip()
            self.draw(player)


if __name__ == '__main__':
    import pygame as p
    from pygame.locals import *
    from pygame.gfxdraw import *
    from generator import Maze
    from backtracking import BackTracking
    from Astar import Algorithm
    import operator
    import random
    import os
    import copy
    p.init()
    p.font.init()


    STANDARD_SIZE = 600
    FPS = 60
    DIMENSIONS = 20
    TEXT_SIZE = 50
    OUTLINE = 100
    THICKNESS = 4
    SEARCH_SPEED = 60

    FONT = p.font.SysFont('comicsans', TEXT_SIZE)
    SCREEN = p.display.set_mode((STANDARD_SIZE, STANDARD_SIZE + OUTLINE))
    FLOOR = p.transform.scale(p.image.load(os.path.join('images', 'floor.jpg')), (DIMENSIONS, DIMENSIONS))
    WALL = p.transform.scale(p.image.load(os.path.join('images', 'wall.png')), (DIMENSIONS, DIMENSIONS))
    END = p.transform.scale(p.image.load(os.path.join('images', 'end.png')), (DIMENSIONS, DIMENSIONS))
    START = p.transform.scale(p.image.load(os.path.join('images', 'start.jpg')), (DIMENSIONS, DIMENSIONS))
    ASSIGNMENT = {'path': FLOOR, 'wall': WALL, 'start': START, 'end': END}

    solve_text = FONT.render('Solve',  True, p.Color('white'))
    button = p.Rect(STANDARD_SIZE - solve_text.get_width() - THICKNESS*5, 10, solve_text.get_width() + THICKNESS*2, solve_text.get_height() + THICKNESS*2)
    
    gui = GUI()
    gui.main()
