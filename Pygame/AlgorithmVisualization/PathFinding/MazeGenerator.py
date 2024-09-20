import random
import operator

class Maze:
    def __init__(self, dimensions: int):
        self.dimensions = dimensions
        self.directions = {'left': (-1, 0), 'right': (1,0), 'forwards': (0,1), 'backwards': (0,-1)}
        self.walls = []
        self.start = (random.randrange(1, self.dimensions - 1), random.randrange(1, self.dimensions - 1))
        self.maze = [['u' for _ in range(self.dimensions)] for _ in range(self.dimensions)]
        self.create_cell(self.start)
   
    def inside(self, pos: tuple):
        x, y = pos
        return 0 < x < self.dimensions - 1 and 0 < y < self.dimensions - 1

    def create_cell(self, pos: tuple, side=None):
        types = ['u', 'c']
        conditions = {
            'left': [self.maze[pos[0]][pos[1] - 1] in types, self.maze[pos[0]][pos[1] + 1] in types],
            'forwards': [self.maze[pos[0] - 1][pos[1]] in types,  self.maze[pos[0] + 1][pos[1]] in types],
            'backwards': [self.maze[pos[0] + 1][pos[1]] in types, self.maze[pos[0] - 1][pos[1]] in types],
            'right': [self.maze[pos[0]][pos[1] + 1] in types, self.maze[pos[0]][pos[1] - 1] in types]
        }
        if side is None or all(conditions.get(side)):
            x, y = pos
            self.maze[x][y] = 'c'
            for i in range(len(self.directions)):
                if self.inside((new := list(map(operator.add, (x,y), list(self.directions.values())[i])))):
                    if self.maze[new[0]][new[1]] != 'c':
                        self.maze[new[0]][new[1]] = 'w'
                        self.walls.append(new)
   
    def surrounding(self, pos, target=None):
        elements = {}
        for i in range(len(self.directions)):
            if self.inside((new := list(map(operator.add, pos, list(self.directions.values())[i])))):
                x,y = new
                if target is None:
                    elements[list(self.directions.keys())[i]] = new
                elif self.maze[x][y] == target:
                    elements[list(self.directions.keys())[i]] = {'object': self.maze[x][y], 'pos': new}
        return elements
    
    def surrounding_cells(self, pos):
        num = 0
        for i in range(len(self.directions)):
            if self.inside((new := list(map(operator.add, pos, list(self.directions.values())[i])))) and self.maze[new[0]][new[1]] == 'c':
               num += 1
        return num
        
    def all_elements(self, target: str):
        elements = []
        for i in range(len(self.maze)):
            for j in range(len(self.maze)):
                if self.maze[i][j] == target:
                    elements.append((i,j))
        return elements
    
    def build_connections(self):
        wall_list = self.all_elements('w')
        walls = random.sample(wall_list, k=len(wall_list))
        num = 0
        for i in range(len(walls)):
            if num < self.dimensions*2 and self.breaks(walls[i]) != [] and self.surrounding_cells(walls[i]) == 2:
                x, y = walls[i]
                num += 1
                self.maze[x][y] = 'c'

    def breaks(self, pos):
        x, y = pos
        paths, elements = [[(x + 1, y), (x - 1, y)], [(x, y + 1), (x, y - 1)]], []
        for i in range(len(paths)):
            for j in range(len(paths[i])):
                x, y = paths[i][j]
                if self.inside(paths[i][j]) is False or self.maze[x][y] != 'c':
                    break
                elif j == len(paths[i]) - 1:
                    elements.append(paths[i])
        return elements
    
    @staticmethod
    def translation(maze):
        elements = {'w': 'wall', 'c': 'empty'}
        for i in range(len(maze)):
            for j, element in enumerate(maze[i]):
                if element != 'u':
                    maze[i][j] = elements.get(element)
                else:
                    maze[i][j] = 'wall'
        return maze

    def path_generator(self):
        while self.walls:
            wall = self.walls[random.randint(0, len(self.walls) - 1)]
            surrounding = self.surrounding(wall)
            if self.inside(wall) and self.surrounding_cells(wall) < 2:
                for i in range(len(surrounding)):
                    self.create_cell(wall, list(surrounding.keys())[i])
            self.walls.remove(wall)
        self.build_connections()
        return self.translation(self.maze)