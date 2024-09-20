from colorama import init, Fore
import operator
import copy
import random

class BackTracking:
    def __init__(self, size, dimensions, maze, entrances):
        self.maze = maze
        self.entrances = {v:k for k,v in entrances.items()}
        self.size = size
        self.dimensions = dimensions
        self.directions = {'left': (-1, 0), 'right': (1,0), 'forwards': (0,1), 'backwards': (0,-1)}
        self.path = [self.entrances.get('start')]
        self.progress = []
    
    def inside(self, pos):
        x,y = pos
        return 0 <= x <= self.size//self.dimensions - 1 and 0 <= y <= self.size//self.dimensions - 1

    def surrounding(self, pos):
        elements = []
        for i in range(len(self.directions)):
            if self.inside((new := list(map(operator.add, pos, list(self.directions.values())[i])))):
                if self.maze[new[0]][new[1]] == 'c':
                    elements.append(new)
        return elements
    
    def algorithm(self):
        current_cell = self.path[-1]
        if current_cell == self.entrances.get('end'):
            return True

        operators = [(current_cell[0] + 1, current_cell[1]), (current_cell[0], current_cell[1] + 1), (current_cell[0] - 1, current_cell[1]), (current_cell[0], current_cell[1] - 1)]
        for i in range(len(operators)):
            x, y = operators[i]
            if self.inside((x,y)) and self.maze[x][y] == 'c':
                self.maze[x][y] = 'p'
                self.path.append((x, y))
                self.progress.append(copy.deepcopy(self.path))
                if self.algorithm():
                    return True
               
        current_cell = self.path[-1]
        if current_cell != self.entrances.get('end'):
            self.path.pop(-1)
            
    def solve(self):
        x, y = self.entrances.get('start')
        self.maze[x][y] = 'p'
        self.algorithm()
        return self.progress
