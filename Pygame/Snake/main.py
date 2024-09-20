
class Cell:
    def __init__(self, pos):
        self.pos = pos
        self.state = 'empty'
        self.color = (63, 182, 39)
    
    def make_empty(self):
        self.state = 'empty'
        self.color = (63, 182, 39)
    
    def make_target(self):
        self.state = 'target'
        self.color = p.Color('blue')
    
class Snake:
    def __init__(self, pos):
        self.pos = pos
        self.head = self.pos
        self.elements = [self.pos]
        self.positions = [self.pos]
        self.current_direction = None
        self.break_point = False
    
    def update_snake(self, direction):
        head = deepcopy(tuple(self.elements[0]))
        new = tuple(map(operator.add, head, direction))
        x, y = new
        self.current_direction = direction
        if 0 > x or x >= DIMENSION or 0 > y or y >= DIMENSION:
            if 0 > x:
                new = (DIMENSION, y)
            elif x >= DIMENSION:
                new = (0, y)
            elif 0 > y:
                new = (x, DIMENSION)
            elif y >= DIMENSION:
                new = (x, 0)
        if (sample:= self.elements[1:]):
            for i in range(len(sample) + 1):
                if self.elements[i] == new:
                    self.break_point = True
                self.elements[i] = self.positions[-i]
        self.elements[0] = new
        self.head = new
        self.positions.append(self.head)

    def add(self):
        self.elements.append(self.positions[-(len(self.elements) + 1)])

class Game:
    def __init__(self):
        self.running = True
        self.board = [[Cell((i, j)) for j in range(DIMENSION)] for i in range(DIMENSION)]
        self.snake = Snake((DIMENSION//2, DIMENSION//2))
        self.target = None

    @staticmethod
    def draw_rect_outline(surface, rect, color, width=1):
        x, y, w, h = rect
        width = min(min(max(width, 1), w//2), h//2)
        for i in range(width):
            p.gfxdraw.rectangle(surface, (x+i, y+i, w-i*2, h-i*2), color)

    def generate_target(self):
        possiblities = [(i, j) for i in range(DIMENSION) for j in range(DIMENSION) if (i, j) not in self.snake.elements]
        x, y = random.choice(possiblities)
        self.board[x][y].make_target()
        self.target = (x, y)

    def draw_board(self):
        for element in self.board:
            for cell in element:
                x, y = cell.pos
                p.draw.rect(SCREEN, cell.color, (rect:= p.Rect(x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE)))
                self.draw_rect_outline(SCREEN, rect, p.Color('black'))
    
    def draw_snake(self):
        for (x, y) in self.snake.elements[1:]:
            p.draw.rect(SCREEN, p.Color('red'), p.Rect(x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        x, y = self.snake.head
        p.draw.rect(SCREEN, p.Color('dark red'), p.Rect(x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def draw(self):
        self.draw_board()
        self.draw_snake()
        p.display.update()

    def main(self):
        clock = p.time.Clock()
        while self.running:
            clock.tick(FPS)
            direction = None
            for event in p.event.get():
                if event.type == QUIT:
                    self.running = False
                    p.quit()
                if event.type == KEYDOWN:
                    if event.key == K_w:
                        direction = (0, -1)
                    elif event.key == K_a:
                        direction = (-1, 0)
                    elif event.key == K_s:
                        direction = (0, 1)
                    elif event.key == p.K_d:
                        direction = (1, 0)
            if self.target is None:
                self.generate_target()

            if direction:
                self.snake.update_snake(direction)
            elif self.snake.current_direction is not None:
                self.snake.update_snake(self.snake.current_direction)
            if self.snake.head == self.target:
                self.snake.add()
                x, y = self.target
                self.board[x][y].make_empty()
                self.target = None

            self.draw()
            p.time.delay(150)
            
            if self.snake.break_point:
                self.running = False
                p.time.delay(1000)
                self.__init__()


if __name__ == '__main__':
    import pygame as p
    from pygame.gfxdraw import *
    from pygame.locals import *
    import random
    import operator
    from copy import deepcopy
    p.init()

    SIZE = 720
    DIMENSION = 30
    FPS = 60
    CELL_SIZE = SIZE//DIMENSION
    SCREEN = p.display.set_mode((SIZE, SIZE))

    game = Game()
    game.main()
