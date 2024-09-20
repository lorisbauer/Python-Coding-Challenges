from main import Board


class MoveLogBlack:
    def __init__(self, board):
        self.board = board
        self.pieces = {'white': {11: 'wP', 12: 'wR', 13: 'wN', 14: 'wB', 15: 'wQ', 16: 'wK'},
                       'black': {21: 'bP', 22: 'bR', 23: 'bN', 24: 'bB', 25: 'bQ', 26: 'bK'}}
        self.chess_board = Board(self.board)
        self.dimension = 8
        self.board_square = [(i, j) for i in range(self.dimension) for j in range(self.dimension)]

    # validates all moves from all pieces of one sort
    def board_control(self, piece, surrounding):
        if piece == 'bP' and surrounding is not None:
            valid_surrounding_pawn = {}
            for i in range(len(surrounding)):
                elements = []
                for j in range(len(list(surrounding.values())[i])):
                    r, c = list(surrounding.keys())[i]
                    row, col = list(surrounding.values())[i][j]
                    if self.board[row][col] in self.pieces['white'] and col != c:
                        elements.append((row, col))
                    elif self.board[row][col] in self.pieces['black'] and col != c:
                        elements.append((row, col))
                    elif self.board[row][col] == 0 and col != c:
                        elements.append((row, col))
                if len(elements) > 0:
                    valid_surrounding_pawn[list(surrounding.keys())[i]] = elements
            return valid_surrounding_pawn

        elif piece == 'bR' and surrounding is not None:
            valid_surrounding_rook = {}
            for i in range(len(list(surrounding.values()))):
                elements = []
                for j in range(len(list(surrounding.values())[i])):
                    for k in range(len(list(surrounding.values())[i][j])):
                        row, col = list(surrounding.values())[i][j][k]
                        if self.board[row][col] == 0:
                            elements.append((row, col))
                        elif self.board[row][col] in self.pieces['white']:
                            elements.append((row, col))
                            break
                        elif self.board[row][col] in self.pieces['black']:
                            if self.board[row][col] == 25:
                                elements.append((row, col))
                            if self.board[row][col] == 22:
                                elements.append((row, col))
                            if self.board[row][col] == 23 or self.board[row][col] == 24 or self.board[row][col] == 26 or self.board[row][col] == 21:
                                elements.append((row, col))
                                break
                valid_surrounding_rook[list(surrounding.keys())[i]] = list(set(elements))
            return valid_surrounding_rook

        elif piece == 'bB' and surrounding is not None:
            valid_surrounding_bishop = {}
            for i in range(len(list(surrounding.values()))):
                r, c = list(surrounding.keys())[i]
                elements = []
                for j in range(len(list(surrounding.values())[i])):
                    for k in range(len(list(surrounding.values())[i][j])):
                        row, col = list(surrounding.values())[i][j][k]
                        if self.board[row][col] == 0:
                            elements.append((row, col))
                        elif self.board[row][col] in self.pieces['white']:
                            elements.append((row, col))
                            break
                        elif self.board[row][col] in self.pieces['black']:
                            if self.board[row][col] == 21:
                                for m in range(len(self.board)):
                                    if (row - m, col - m) == (r, c):
                                        if (row, col) not in elements:
                                            elements.append((row, col))
                                        if (row + 1, col + 1) in self.board_square:
                                            elements.append((row + 1, col + 1))
                                        break
                                    if (row - m, col + m) == (r, c):
                                        if (row, col) not in elements:
                                            elements.append((row, col))
                                        if (row + 1, col - 1) in self.board_square:
                                            elements.append((row + 1, col - 1))
                                        break
                                    if (row, col) not in elements:
                                        elements.append((row, col))
                                break
                            if self.board[row][col] == 25:
                                elements.append((row, col))
                            if self.board[row][col] == 24:
                                elements.append((row, col))
                            if self.board[row][col] == 23 or self.board[row][col] == 26 or self.board[row][col] == 22:
                                elements.append((row, col))
                                break

                valid_surrounding_bishop[list(surrounding.keys())[i]] = list(set(elements))
            return valid_surrounding_bishop

        elif piece == 'bQ' and surrounding is not None:
            valid_surrounding_queen = {}
            for x in range(len(surrounding)):
                r, c = list(surrounding.keys())[x]
                elements = []
                for i in range(len(list(surrounding.values())[x])):
                    for j in range(len(list(surrounding.values())[x][i])):
                        for k in range(len(list(surrounding.values())[x][i][j])):
                            row, col = list(surrounding.values())[x][i][j][k]
                            if self.board[row][col] == 0:
                                elements.append((row, col))
                            elif self.board[row][col] in self.pieces['white']:
                                elements.append((row, col))
                                break
                            elif self.board[row][col] in self.pieces['black']:
                                if self.board[row][col] == 21:
                                    for m in range(len(self.board)):
                                        if (row - m, col - m) == (r, c):
                                            if (row, col) not in elements:
                                                elements.append((row, col))
                                            if (row - 1, col + 1) in self.board_square:
                                                elements.append((row + 1, col + 1))
                                            break
                                        if (row + m, col + m) == (r, c):
                                            if (row, col) not in elements:
                                                elements.append((row, col))
                                            if (row + 1, col - 1) in self.board_square:
                                                elements.append((row + 1, col - 1))
                                            break
                                        if (row, col) not in elements:
                                            elements.append((row, col))
                                    break
                                if self.board[row][col] == 22:
                                    elements.append((row, col))
                                if self.board[row][col] == 24:
                                    elements.append((row, col))
                                if self.board[row][col] == 25:
                                    elements.append((row, col))
                                if self.board[row][col] == 23 or self.board[row][col] == 26:
                                    elements.append((row, col))
                                    break

                valid_surrounding_queen[list(surrounding.keys())[x]] = list(set(elements))
            return valid_surrounding_queen

        elif piece == 'bN' and surrounding is not None:
            valid_surrounding_knight = {}
            for i in range(len(list(surrounding.values()))):
                elements = []
                for j in range(len(list(surrounding.values())[i])):
                    for k in range(len(list(surrounding.values())[i][j])):
                        row, col = list(surrounding.values())[i][j][k]
                        if self.board[row][col] == 0:
                            elements.append((row, col))
                        elif self.board[row][col] in self.pieces['white']:
                            elements.append((row, col))
                        elif self.board[row][col] in self.pieces['black']:
                            elements.append((row, col))
                valid_surrounding_knight[list(surrounding.keys())[i]] = elements

            return valid_surrounding_knight
        elif piece == 'bK' and surrounding is not None:
            valid_surrounding_king = {}
            for i in range(len(list(surrounding.values()))):
                elements = []
                for j in range(len(list(surrounding.values())[i])):
                    row, col = list(surrounding.values())[i][j]
                    if self.board[row][col] == 0:
                        elements.append((row, col))
                    elif self.board[row][col] in self.pieces['white']:
                        elements.append((row, col))
                    elif self.board[row][col] in self.pieces['black']:
                        elements.append((row, col))
                valid_surrounding_king[list(surrounding.keys())[i]] = elements
            return valid_surrounding_king

        elif surrounding is None:
            return None
        else:
            raise ValueError

    def valid_moves(self, piece, surrounding):
        if piece == 'bP' and surrounding is not None:
            valid_surrounding_pawn = {}
            for i in range(len(surrounding)):
                elements = []
                for j in range(len(list(surrounding.values())[i])):
                    row, col = list(surrounding.values())[i][j]
                    if tuple(list(surrounding.keys())[i]) == (row - 1, col) or \
                            tuple(list(surrounding.keys())[i]) == (row - 2, col):
                        if self.board[row][col] == 0:
                            if self.board[row][col] == 0:
                                if tuple(list(surrounding.keys())[i]) == (row - 2, col):
                                    if self.board[row - 1][col] == 0:
                                        elements.append((row, col))
                                elif tuple(list(surrounding.keys())[i]) == (row - 1, col):
                                    elements.append((row, col))
                    else:
                        if self.board[row][col] in self.pieces['white']:
                            elements.append((row, col))
                        elif self.board[row][col] in self.pieces['black']:
                            elements.append((row, col))
                if len(elements) > 0:
                    valid_surrounding_pawn[list(surrounding.keys())[i]] = elements
                else:
                    continue
            return valid_surrounding_pawn

        elif piece == 'bR' and surrounding is not None:
            valid_surrounding_rook = {}
            for i in range(len(list(surrounding.values()))):
                elements = []
                for j in range(len(list(surrounding.values())[i])):
                    for k in range(len(list(surrounding.values())[i][j])):
                        row, col = list(surrounding.values())[i][j][k]
                        if self.board[row][col] == 0:
                            elements.append((row, col))
                        elif self.board[row][col] in self.pieces['white']:
                            elements.append((row, col))
                            break
                        elif self.board[row][col] in self.pieces['black']:
                            elements.append((row, col))
                            break
                valid_surrounding_rook[list(surrounding.keys())[i]] = elements
            return valid_surrounding_rook

        elif piece == 'bB' and surrounding is not None:
            valid_surrounding_bishop = {}
            for i in range(len(list(surrounding.values()))):
                elements = []
                for j in range(len(list(surrounding.values())[i])):
                    for k in range(len(list(surrounding.values())[i][j])):
                        row, col = list(surrounding.values())[i][j][k]
                        if self.board[row][col] == 0:
                            elements.append((row, col))
                        elif self.board[row][col] in self.pieces['white']:
                            elements.append((row, col))
                            break
                        elif self.board[row][col] in self.pieces['black']:
                            elements.append((row, col))
                            break
                valid_surrounding_bishop[list(surrounding.keys())[i]] = elements
            return valid_surrounding_bishop

        elif piece == 'bQ' and surrounding is not None:
            valid_surrounding_queen = {}
            for i in range(len(list(surrounding.values()))):
                elements = []
                for j in range(len(list(surrounding.values())[i])):
                    for k in range(len(list(surrounding.values())[i][j])):
                        for l in range(len(list(surrounding.values())[i][j][k])):
                            row, col = list(surrounding.values())[i][j][k][l]
                            if self.board[row][col] == 0:
                                elements.append((row, col))
                            elif self.board[row][col] in self.pieces['white']:
                                elements.append((row, col))
                                break
                            elif self.board[row][col] in self.pieces['black']:
                                elements.append((row, col))
                                break
                valid_surrounding_queen[list(surrounding.keys())[i]] = elements
            return valid_surrounding_queen

        elif piece == 'bN' and surrounding is not None:
            valid_surrounding_knight = {}
            for i in range(len(list(surrounding.values()))):
                elements = []
                for j in range(len(list(surrounding.values())[i])):
                    for k in range(len(list(surrounding.values())[i][j])):
                        row, col = list(surrounding.values())[i][j][k]
                        if self.board[row][col] == 0:
                            elements.append((row, col))
                        elif self.board[row][col] in self.pieces['white']:
                            elements.append((row, col))
                        elif self.board[row][col] in self.pieces['black']:
                            elements.append((row, col))
                valid_surrounding_knight[list(surrounding.keys())[i]] = elements

            return valid_surrounding_knight
        elif piece == 'bK' and surrounding is not None:
            valid_surrounding_king = {}
            for i in range(len(list(surrounding.values()))):
                elements = []
                for j in range(len(list(surrounding.values())[i])):
                    row, col = list(surrounding.values())[i][j]
                    if self.board[row][col] == 0:
                        elements.append((row, col))
                    elif self.board[row][col] in self.pieces['white']:
                        elements.append((row, col))
                    elif self.board[row][col] in self.pieces['black']:
                        elements.append((row, col))
                valid_surrounding_king[list(surrounding.keys())[i]] = elements
            return valid_surrounding_king

        elif surrounding is None:
            return None
        else:
            raise ValueError

    # all moves white pawns
    def all_moves_pawn(self):
        positions = self.chess_board.get_pos(21)
        surrounding_pawn = {}
        if positions is not None:
            for i in range(len(positions)):
                row, col = positions[i]
                if row != 1:
                    if col - 1 >= 0 and col + 1 <= len(self.board) - 1:
                        surrounding_pawn[(row, col)] = [(row + 1, col - 1),
                                                   (row + 1, col),
                                                   (row + 1, col + 1)]
                    elif col - 1 >= 0 and col + 1 > len(self.board) - 1:
                        surrounding_pawn[(row, col)] = [(row + 1, col - 1),
                                                   (row + 1, col)]
                    elif col - 1 < 0 and col + 1 <= len(self.board) - 1:
                        surrounding_pawn[(row, col)] = [(row + 1, col),
                                                   (row + 1, col + 1)]
                elif row == 1:
                    if col - 1 >= 0 and col + 1 <= len(self.board) - 1:
                        surrounding_pawn[(row, col)] = [(row + 1, col - 1),
                                                   (row + 1, col),
                                                   (row + 1, col + 1),
                                                   (row + 2, col)]
                    elif col - 1 >= 0 and col + 1 > len(self.board) - 1:
                        surrounding_pawn[(row, col)] = [(row + 1, col - 1),
                                                   (row + 1, col),
                                                   (row + 2, col)]
                    elif col - 1 < 0 and col + 1 <= len(self.board) - 1:
                        surrounding_pawn[(row, col)] = [(row + 1, col),
                                                   (row + 1, col + 1),
                                                   (row + 2, col)]
            return surrounding_pawn
        else:
            return None

    def all_moves_rook(self):
        positions = self.chess_board.get_pos(22)
        surrounding_rook = {}
        if positions is not None:
            for i in range(len(positions)):
                row, col = positions[i]
                elements_right = []
                elements_left = []
                elements_up = []
                elements_down = []
                for j in range(len(self.board[i])):
                    if col + j <= len(self.board) - 1:
                        elements_right.append((row, col + j))
                for j in range(len(self.board[i])):
                    if row + j <= len(self.board) - 1:
                        elements_down.append((row + j, col))
                for j in range(len(self.board[i])):
                    if col - j >= 0:
                        elements_left.append((row, col - j))
                for j in range(len(self.board[i])):
                    if row - j >= 0:
                        elements_up.append((row - j, col))
                elements = [list(filter(lambda x: x != (row, col), elements_right)),
                            list(filter(lambda x: x != (row, col), elements_left)),
                            list(filter(lambda x: x != (row, col), elements_up)),
                            list(filter(lambda x: x != (row, col), elements_down))]
                surrounding_rook[(row, col)] = list(filter(lambda x: x != [], elements))
            return surrounding_rook
        else:
            return None

    def all_moves_bishop(self):
        positions = self.chess_board.get_pos(24)
        surrounding_bishop = {}
        if positions is not None:
            for i in range(len(positions)):
                row, col = positions[i]
                elements_00 = []
                elements_07 = []
                elements_70 = []
                elements_77 = []
                for j in range(len(self.board)):
                    if row - j >= 0 and col - j >= 0:
                        elements_00.append((row - j, col - j))
                for j in range(len(self.board)):
                    if row - j >= 0 and col + j <= len(self.board) - 1:
                        elements_07.append((row - j, col + j))
                for j in range(len(self.board)):
                    if row + j <= len(self.board) - 1 and col - j >= 0:
                        elements_70.append((row + j, col - j))
                for j in range(len(self.board)):
                    if row + j <= len(self.board) - 1 and col + j <= len(self.board) - 1:
                        elements_77.append((row + j, col + j))
                elements = [list(filter(lambda x: x != (row, col), elements_00)),
                            list(filter(lambda x: x != (row, col), elements_07)),
                            list(filter(lambda x: x != (row, col), elements_70)),
                            list(filter(lambda x: x != (row, col), elements_77))]
                surrounding_bishop[(row, col)] = list(filter(lambda x: x != [], elements))

            return surrounding_bishop
        else:
            return None

    def all_moves_queen(self):
        positions = self.chess_board.get_pos(25)
        surrounding_queen = {}
        if positions is not None:
            for i in range(len(positions)):
                between_list = []
                row, col = positions[i]
                elements_00 = []
                elements_07 = []
                elements_70 = []
                elements_77 = []
                for j in range(len(self.board)):
                    if row - j >= 0 and col - j >= 0:
                        elements_00.append((row - j, col - j))
                    if row - j >= 0 and col + j <= len(self.board) - 1:
                        elements_07.append((row - j, col + j))
                    if row + j <= len(self.board) - 1 and col - j >= 0:
                        elements_70.append((row + j, col - j))
                    if row + j <= len(self.board) - 1 and col + j <= len(self.board) - 1:
                        elements_77.append((row + j, col + j))
                elements = [list(filter(lambda x: x != (row, col), elements_00)),
                            list(filter(lambda x: x != (row, col), elements_07)),
                            list(filter(lambda x: x != (row, col), elements_70)),
                            list(filter(lambda x: x != (row, col), elements_77))]
                between_list.append(list(filter(lambda x: x != [], elements)))
                elements_right = []
                elements_left = []
                elements_up = []
                elements_down = []
                for j in range(len(self.board)):
                    if col + j <= len(self.board) - 1:
                        elements_right.append((row, col + j))
                    if row + j <= len(self.board) - 1:
                        elements_down.append((row + j, col))
                    if col - j >= 0:
                        elements_left.append((row, col - j))
                    if row - j >= 0:
                        elements_up.append((row - j, col))
                elements = [list(filter(lambda x: x != (row, col), elements_right)),
                            list(filter(lambda x: x != (row, col), elements_left)),
                            list(filter(lambda x: x != (row, col), elements_up)),
                            list(filter(lambda x: x != (row, col), elements_down))]
                between_list.append(list(filter(lambda x: x != [], elements)))
                surrounding_queen[(positions[i])] = between_list
            return surrounding_queen
        else:
            return None

    def all_moves_knight(self):
        positions = self.chess_board.get_pos(23)
        surrounding_knight = {}
        if positions is not None:
            for i in range(len(positions)):
                row, col = positions[i]
                elements_right = []
                elements_left = []
                elements_up = []
                elements_down = []
                if col + 2 <= len(self.board) - 1:
                    if row + 1 <= len(self.board) - 1:
                        elements_right.append((row + 1, col + 2))
                    if row - 1 >= 0:
                        elements_right.append((row - 1, col + 2))
                if col - 2 >= 0:
                    if row + 1 <= len(self.board) - 1:
                        elements_left.append((row + 1, col - 2))
                    if row - 1 >= 0:
                        elements_left.append((row - 1, col - 2))
                if row + 2 <= len(self.board) - 1:
                    if col + 1 <= len(self.board) - 1:
                        elements_up.append((row + 2, col + 1))
                    if col - 1 >= 0:
                        elements_up.append((row + 2, col - 1))
                if row - 2 >= 0:
                    if col + 1 <= len(self.board) - 1:
                        elements_left.append((row - 2, col + 1))
                    if col - 1 >= 0:
                        elements_left.append((row - 2, col - 1))
                elements = [list(filter(lambda x: x != (row, col), elements_right)),
                            list(filter(lambda x: x != (row, col), elements_left)),
                            list(filter(lambda x: x != (row, col), elements_up)),
                            list(filter(lambda x: x != (row, col), elements_down))]
                surrounding_knight[(row, col)] = list(filter(lambda x: x != [], elements))
            return surrounding_knight
        else:
            return None

    def all_moves_king(self):
        positions = self.chess_board.get_pos(26)
        surrounding_king = {}
        if positions is not None:
            row, col = positions[0]
            elements = []
            for j in range(3):
                for k in range(3):
                    if 0 <= (row + 1) - j <= len(self.board) - 1 and 0 <= (col - 1) + k <= len(self.board) - 1:
                        elements.append(((row + 1) - j, (col - 1) + k))
            elements = list(filter(lambda x: x != (row, col), elements))
            surrounding_king[(row, col)] = list(filter(lambda x: x != [], elements))
            return surrounding_king
        else:
            return None