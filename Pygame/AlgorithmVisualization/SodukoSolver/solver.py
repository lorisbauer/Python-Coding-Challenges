class Solver:
    def __init__(self, board):
        self.board = board
        self.progress = []

    def solve(self):
        pos = self.find_empty()
        if pos is None:
            return True
        x, y = pos

        for i in range(1, 10):
            if self.validate(pos, i):
                self.board[x][y] = i
                self.progress.append([(x, y), i])

                if self.solve():
                    return True

                self.board[x][y] = 0
                self.progress.append([(x, y), 0])
        return False

    def validate(self, pos, value):
        x, y = pos
        square_x, square_y = (x // 3) * 3, (y // 3) * 3,

        for i, elements in enumerate(self.board):
            if i == x:
                for element in elements:
                    if element == value:
                        return False
            if elements[y] == value:
                return False

        for i in range(square_x, square_x + 3):
            for j in range(square_y, square_y + 3):
                if self.board[i][j] == value:
                    return False
        return True

    def find_empty(self):
        for i, elements in enumerate(self.board):
            for j, element in enumerate(elements):
                if element == 0:
                    return i, j
        return None
