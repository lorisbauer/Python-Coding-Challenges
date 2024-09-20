from main import Board, Methods
import copy


class Evaluation:
    def __init__(self, color, board):
        self.color = color
        self.board = board
        self.chess_board = Board(self.board)
        self.pieces = {11: 'wP', 12: 'wR', 13: 'wN', 14: 'wB', 15: 'wQ', 16: 'wK',
                       21: 'bP', 22: 'bR', 23: 'bN', 24: 'bB', 25: 'bQ', 26: 'bK'}
        self.main_pieces = {k: v for k, v in self.pieces.items() if k != 11 and k != 21}
        self.pieces_color = {'white': {11: 'wP', 12: 'wR', 13: 'wN', 14: 'wB', 15: 'wQ', 16: 'wK'},
                             'black': {21: 'bP', 22: 'bR', 23: 'bN', 24: 'bB', 25: 'bQ', 26: 'bK'}}
        self.pieces_swap = {v: k for k, v in self.pieces.items()}
        self.color_change = {'white': 'w', 'black': 'b'}
        self.values = {self.pieces_swap[self.color_change[self.color] + 'P']: 1,
                       self.pieces_swap[self.color_change[self.color] + 'R']: 5,
                       self.pieces_swap[self.color_change[self.color] + 'N']: 3,
                       self.pieces_swap[self.color_change[self.color] + 'B']: 3,
                       self.pieces_swap[self.color_change[self.color] + 'Q']: 9,
                       self.pieces_swap[self.color_change[self.color] + 'K']: .5}
        self.piece_values = {'P': 1, 'R': 5, 'N': 3, 'B': 3.125, 'Q': 9, 'K': .5}

    def material(self):
        m = 0
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] in self.values:
                    m += int(self.values[self.board[i][j]])
        return m

    def find_weak_squares(self):
        pass

    def pawn_structures(self):
        piece = self.color_change[self.color] + 'P'
        piece_num = self.pieces_swap[piece]
        elements = []
        element = []

        def defending_V1(start, surrounding):
            defending_list = []
            for x in range(len(surrounding)):
                if surrounding[x][1] != start[1]:
                    defending_list.append(surrounding[x])
            return defending_list

        def defending_V2(start, surrounding, color):
            defending_list = []
            for x in range(len(surrounding)):
                if surrounding[x][0] != start[0] and surrounding[x][1] != start[1]:
                    defending_list.append(surrounding[x])
            if color == 'white':
                return defending_list[:len(defending_list)//2]
            elif color == 'black':
                return defending_list[len(defending_list)//2:]

        def evaluate_structure(pos: tuple, board):
            surrounding = defending_V1(pos, Methods.surrounding_3x3(pos))
            for k in range(len(surrounding)):
                r, c = surrounding[k]
                if (r, c) not in element:
                    if board[r][c] == piece_num and (r, c) not in element \
                            and (r, c) not in Methods.merge_lists(*elements):
                        element.append((r, c))
                        if evaluate_structure(surrounding[k], board) is False:
                            return False
                    else:
                        for m in range(len(elements)):
                            if (r, c) in elements[m] and pos not in elements[m]:
                                element.remove(pos)
                                elements[m].append(pos)
            return False

        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if self.board[i][j] == piece_num:
                    if (i, j) not in Methods.merge_lists(elements):
                        element.append((i, j))
                    if evaluate_structure((i, j), self.board) is False:
                        if list(reversed(element)) not in elements and element is not []:
                            for k in range(len(element)):
                                if element[k] in Methods.merge_lists(*elements):
                                    element.clear()
                            if len(element) >= 1:
                                elements.append(copy.deepcopy(element))
                                element.clear()
        if len(elements) > 0:
            weakness = []
            for k in range(len(elements)):
                for m in range(len(elements[k])):
                    start = elements[k][m]
                    if len(elements[k]) == 1:
                        weakness.append(start)
                    else:
                        valid_surrounding = defending_V2(start, Methods.surrounding_3x3(start), self.color)
                        defended = False
                        for n in range(len(valid_surrounding)):
                            row, col = valid_surrounding[n]
                            if self.board[row][col] == self.pieces_swap[self.color_change[self.color] + 'P']:
                                defended = True
                                break
                        if defended is False:
                            weakness.append(start)

            return {'structure': sorted(elements, key=len),
                    'weakness': sorted(list(dict.fromkeys(weakness)), key=lambda x: (x[0:2]))}

    def king_safety(self):
        king_pos = tuple(*self.chess_board.get_pos(self.pieces_swap[self.color_change[self.color] + 'K']))
        row, col = king_pos

        king_area_3x3 = Methods.surrounding_3x3(king_pos)
        king_area_5x5 = Methods.surrounding_5x5(king_pos)

        king_pawns = 0
        empty_squares = 0
        defending_pieces = 0

        for i in range(len(king_area_5x5)):
            r, c = king_area_5x5[i]
            if (r, c) != (row, col):
                if (r, c) in king_area_3x3:
                    if self.board[r][c] == self.pieces_swap[self.color_change[self.color] + 'P'] and r <= row - 1:
                        king_pawns += 1
                    elif self.board[r][c] == 0 and r == row - 1:
                        empty_squares += 1
                if self.board[r][c] in self.pieces_color[self.color] and self.board[r][c] != self.pieces_swap[self.color_change[self.color] + 'P']:
                    defending_pieces += 1

    def pawn_space(self, board_control_pawns):
        space = 0
        board_squares = [(i, j) for i in range(8) for j in range(8)]
        black_side = board_squares[:len(board_squares)//2]

        for i in range(len(board_control_pawns)):
            r, c = list(board_control_pawns.keys())[i]
            if self.board[r][c] == self.pieces_swap[self.color_change[self.color] + 'P']:
                if len(list(board_control_pawns.values())[i]) == 3 and\
                        1 <= list(board_control_pawns.keys())[i][1] < len(self.board) - 1:
                    list(board_control_pawns.values())[i].pop(1)

                elif len(list(board_control_pawns.values())[i]) == 4 or\
                        1 > list(board_control_pawns.keys())[i][1] == len(self.board) - 1:
                    element_remove = []
                    for j in range(len(list(board_control_pawns.values())[i]) // 2):
                        r, c = list(board_control_pawns.keys())[i]
                        for k in range(len(list(board_control_pawns.values())[j])):
                            r1, c1 = list(board_control_pawns.values())[j][k]
                            if c1 == c:
                                element_remove.append(list(board_control_pawns.values())[j][k])
                    for m in range(len(element_remove)):
                        list(board_control_pawns.values())[i].remove(element_remove[m])

        for i in range(len(board_control_pawns)):
            for j in range(len(list(board_control_pawns.values())[i])):
                if list(board_control_pawns.values())[i][j] in black_side:
                    space += 1
        return space

    @staticmethod
    def board_control(all_valid_moves):
        all_moves_united = {}
        board_squares = [(i, j) for i in range(8) for j in range(8)]
        squares_control = {}

        for i in range(len(all_valid_moves)):
            element = []
            for j in range(len(list(all_valid_moves.values())[i])):
                if type(list(all_valid_moves.values())[i][j]) is list:
                    elements = []
                    for k in range(len(list(all_valid_moves.values())[i])):
                        elements += list(all_valid_moves.values())[i][k]
                    if type(elements[0]) is not list:
                        all_moves_united[list(all_valid_moves.keys())[i]] = elements
                    else:
                        special_elements = []
                        for l in range(len(list(elements))):
                            special_elements += elements[l]
                        all_moves_united[list(all_valid_moves.keys())[i]] = special_elements
                    break
                else:
                    element.append(list(all_valid_moves.values())[i][j])
            if type(list(all_valid_moves.values())[i][0]) is not list:
                all_moves_united[list(all_valid_moves.keys())[i]] = element

        for a in range(len(board_squares)):
            looked = []
            pieces = []
            for i in range(len(all_moves_united)):
                r, c = list(all_moves_united.keys())[i]
                for j in range(len(list(all_moves_united.values())[i])):
                    row, col = list(all_moves_united.values())[i][j]
                    if (row, col) == board_squares[a] and [(r, c), (row, col)] not in looked:
                        looked.append([(r, c), (row, col)])
                        pieces.append((r, c))
            squares_control[board_squares[a]] = {'positions': pieces}
        return squares_control

    def developed_pieces(self):
        back_rank = {'white': 7, 'black': 0}
        developed = []
        for i in range(len(self.main_pieces)):
            if list(self.main_pieces.values())[i][0] == self.color_change[self.color]:
                pos = self.chess_board.get_pos(list(self.main_pieces.keys())[i])
                if list(self.main_pieces.values())[i][1] != 'R':
                    for j in range(len(pos)):
                        if pos[j][0] != back_rank[self.color]:
                            developed.append(pos[j])
                else:
                    start_pos = self.chess_board.get_start_pos(list(self.main_pieces.keys())[i])
                    for j in range(len(pos)):
                        if pos[j] not in start_pos:
                            developed.append(pos[j])
        return developed

    def valid_capture_sequence(self, pieces: list, attacked: list):
        pieces_list = []
        attacked_list = []
        for i in range(len(pieces)):
            row, col = pieces[i]
            pieces_list.append(self.piece_values[self.pieces[self.board[row][col]][1]])
        for j in range(len(attacked)):
            row, col = attacked[j]
            attacked_list.append(self.piece_values[self.pieces[self.board[row][col]][1]])

        for k in range(len(pieces_list)):
            if k != len(attacked_list) and k != len(pieces_list) - 1 or len(attacked_list) == len(pieces_list):
                if pieces_list[k] == .5:
                    return False
                if attacked_list[k] == .5:
                    if k == len(attacked_list) - 1 and len(attacked_list) == len(pieces_list):
                        return False
                    else:
                        return True
                if pieces_list[k] <= attacked_list[k] and len(pieces) >= len(attacked):
                    if k == len(pieces_list) - 1:
                        return True
                    else:
                        pass
                elif pieces_list[k] > attacked_list[k] and k == len(attacked_list) - 1:
                    return True
                else:
                    return False
            elif k == len(attacked_list) and k == len(pieces_list) - 1:
                return True

    def connected_rooks(self):
        pos = self.chess_board.get_pos(self.pieces_swap[self.color_change[self.color] + 'R'])
        status = False
        if len(pos) > 1:
            other = None
            for i in range(len(pos)):
                if other is None:
                    other = pos[i]
                else:
                    if pos[i][0] == other[0]:
                        for j in range(len(self.board[other[0]])):
                            if (other[0], j) == other:
                                for k in range(j + 1, len(self.board[other[0]])):
                                    row, col = (other[0], k)
                                    if (row, col) != pos[i] and self.board[row][col] != 0:
                                        break
                                    elif (row, col) == pos[i]:
                                        status = True
        return status

    def activity(self, piece):
        pass

    def square_control(self, pos, board):
        funcs = {'white': {'valid': Methods.prep_moves(board)['valid'][0],
                 'black': {'valid': Methods.prep_moves(board)['valid'][1]}}}
        valid = funcs[self.color]['valid']
        for i in range(valid):
            if list(valid.keys())[i] == pos:
                return len(list(valid.values())[i])

    def attacked(self, pos):
        valid_moves_white, valid_moves_black = Methods.prep_moves(self.board)['valid']
        if self.color == 'white':
            for i in range(len(valid_moves_white)):
                if pos in list(valid_moves_white.values())[i]:
                    return True
            return False

        elif self.color == 'black':
            for i in range(len(valid_moves_black)):
                if pos in list(valid_moves_black.values())[i]:
                    return True
            return False
