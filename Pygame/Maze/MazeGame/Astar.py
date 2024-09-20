from queue import PriorityQueue
import operator

class Algorithm:
    def __init__(self, maze, start, end):
        self.maze = maze
        self.start = start
        self.end = end
        self.q = PriorityQueue()
        self.directions = {'left': (-1, 0), 'right': (1,0), 'forwards': (0,1), 'backwards': (0,-1)}
        self.g_score = {(i,j): float('inf') for i in range(len(self.maze)) for j in range(len(self.maze))}
        self.g_score[self.start] = 0
        self.f_score = {(i,j): float('inf') for i in range(len(self.maze)) for j in range(len(self.maze))}
        self.f_score[self.start] = Algorithm.h(self.start, self.end)
        self.came_from = {}
        self.open_set = {self.start}
        self.progress = []
    
    def inside(self, pos: tuple):
        x, y = pos
        return 0 <= x <= len(self.maze) - 1 and 0 <= y <= len(self.maze) - 1
    
    @staticmethod
    def h(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        return abs(x1 - x2) + abs(y1 - y2)
    
    def surrounding(self, pos, target=None):
        elements = []
        for i in range(len(self.directions)):
            if self.inside((new := list(map(operator.add, pos, list(self.directions.values())[i])))):
                x, y = new
                if target is None:
                    elements.append(tuple(new))
                elif self.maze[x][y] == target:
                    elements.append(tuple(new))
        return elements
    
    def path(self, current):
        path = [self.end]
        while current in self.came_from:
            current = self.came_from[current]
            path.append(current)
        return path
    
    def main(self):
        count = 0
        self.q.put((0, count, self.start))

        while not self.q.empty():
            current = self.q.get()[2]
            self.open_set.remove(current)

            if current == self.end:
                return self.path(self.end)

            for neighbor in self.surrounding(current, 0):
                temp_g_score = self.g_score[current] + 1
                if temp_g_score < self.g_score[neighbor]:
                    self.came_from[neighbor] = current
                    self.g_score[neighbor] = temp_g_score
                    self.f_score[neighbor] = temp_g_score + Algorithm.h(neighbor, self.end)

                    if neighbor not in self.open_set:
                        count += 1
                        self.q.put((self.f_score[neighbor], count, neighbor))
                        self.open_set.add(neighbor)
                        x, y = neighbor
                        self.maze[x][y] = 0
                        self.progress.append([(x,y), 0])

            if current != self.start:
                x, y = current
                self.maze[x][y] = 1
                self.progress.append([(x,y), 1])
        return False