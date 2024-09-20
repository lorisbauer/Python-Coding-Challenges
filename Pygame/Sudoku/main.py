
def validate(game, pos, value):
    x, y = pos
    for i in range(len(game[x])):
        if i != y:
            if game[x][i] == value:
                return False

    square_size = len(game)//3
    square_x, square_y = square_size*(x//square_size), square_size*(y//square_size)
    for j in range(square_size):
        for k in range(square_size):
            if (j, k) != (x, y):
                x1, y1 = square_x + j, square_y + k          
                if game[x1][y1] == value:
                    return False
    return True


def find_empty(game, value=0):
    for i in range(len(game)):
        for j in range(len(game)):
            if game[i][j] == value:
                return (i, j)
    return False


def solve(game):
    if (pos:= find_empty(game)) is not False:
        x, y = pos
    else:
        return True

    for i in range(1, 10):
        if validate(game, (x, y), i):
            game[x][y] = i
            if solve(game):
                return True
            game[x][y] = 0
    return False


if __name__ == '__main__':
    main = [
        [0, 0, 5, 4, 8, 0, 0, 6, 7],
        [8, 3, 0, 0, 6, 9, 5, 0, 0],
        [7, 0, 6, 5, 0, 0, 4, 0, 8],
        [0, 7, 0, 9, 0, 6, 0, 5, 2],
        [6, 0, 3, 0, 7, 2, 1, 9, 0],
        [0, 2, 9, 1, 0, 0, 8, 0, 0],
        [3, 8, 0, 0, 5, 7, 0, 0, 9],
        [0, 0, 7, 3, 0, 4, 2, 8, 0],
        [5, 0, 2, 6, 0, 0, 7, 0, 3]
    ]  
    
    