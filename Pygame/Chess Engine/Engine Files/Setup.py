from main import *
from MLB import MoveLogBlack
from MLW import MoveLogWhite
import copy

class SetupGame:
    ranks_to_rows = {'1': 7, '2': 6, '3': 5, '4': 4,
                     '5': 3, '6': 2, '7': 1, '8': 0}
    files_to_cols = {'a': 0, 'b': 1, 'c': 2, 'd': 3,
                     'e': 4, 'f': 5, 'g': 6, 'h': 7}

    def __init__(self, moves):
        self.moves = moves
        self.pieces = {12: 'R', 13: 'N', 14: 'B', 15: 'Q', 16: 'K',
                       22: 'R', 23: 'N', 24: 'B', 25: 'Q', 26: 'K'}
        self.pieces_swap = {v: k for k, v in self.pieces.items()}
        self.pieces_color = {11: 'wP', 12: 'wR', 13: 'wN', 14: 'wB', 15: 'wQ', 16: 'wK',
                             21: 'bP', 22: 'bR', 23: 'bN', 24: 'bB', 25: 'bQ', 26: 'bK', 0: '--'}
        self.pieces_color_swap = {v: k for k, v in self.pieces_color.items()}
        self.operations = {'x': 'capture', '+': 'check', 'O': 'castle element', '-': 'castle element'}
        self.white_turn = True
        self.board = [[22, 23, 24, 25, 26, 24, 23, 22],
                      [21, 21, 21, 21, 21, 21, 21, 21],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [11, 11, 11, 11, 11, 11, 11, 11],
                      [12, 13, 14, 15, 16, 14, 13, 12]]
        self.board_list = [self.board]
        self.standard_board = self.board_list[-1]
        self.completed = False
        self.pregame = self.preparation(moves)
        self.main_board = Board(self.standard_board)

    def display_board(self):
        standard_board = self.board_list[-1]
        for i in range(len(self.standard_board)):
            for j in range(len(standard_board[0])):
                if j == 7:
                    print(self.pieces_color[standard_board[i][j]])
                else:
                    print(self.pieces_color[standard_board[i][j]] + " ", end="")
        print()

    def preparation(self, move_list: str):
        if move_list == '':
            return False
        move_list += '/'
        translated = {}
        str_num = [f'{i}' for i in range(0, 10)]
        elements = []
        element = []

        s = ''
        for i in range(len(move_list)):
            if move_list[i] in str_num and move_list[i - 1] not in self.files_to_cols \
                    and move_list[i + 1] not in str_num and move_list[i + 2] not in str_num:
                index = i
                while True:
                    if move_list[index + 1] in str_num:
                        index += 1
                    elif move_list[index + 1] == '.':
                        index += 1
                        break
                for j in range(index, len(move_list)):
                    if move_list[j] in str_num and move_list[j - 1] not in self.files_to_cols or move_list[j] == '/':
                        for k in range(index + 2, j):
                            s += move_list[k]
                        break

        s += '/'
        for m in range(len(s)):
            if s[m] in self.files_to_cols or s[m] in self.ranks_to_rows or s[m] in self.operations \
                    or s[m] in self.pieces_swap:
                element.append(s[m])
            else:
                var = ''
                for n in range(len(element.copy())):
                    var += str(list(element.copy())[n])
                elements.append(var)
                element.clear()

        def divide_chunks(length, num: int):
            for i in range(0, len(length), num):
                yield length[i:i + num]
        paired_elements = list(divide_chunks(elements, 2))

        for e in paired_elements:
            translated[paired_elements.index(e) + 1] = e
        return translated

    def search_start(self):
        if self.pregame is False:
            return False
        for i in range(len(self.pregame)):
            for j in range(len(list(self.pregame.values())[i])):
                move_log_white = MoveLogWhite(self.standard_board)
                move_log_black = MoveLogBlack(self.standard_board)
                pieces_surrounding = {'wP': move_log_white.all_moves_pawn(), 'wR': move_log_white.all_moves_rook(),
                                      'wN': move_log_white.all_moves_knight(), 'wB': move_log_white.all_moves_bishop(),
                                      'wQ': move_log_white.all_moves_queen(), 'wK': move_log_white.all_moves_king(),
                                      'bP': move_log_black.all_moves_pawn(), 'bR': move_log_black.all_moves_rook(),
                                      'bN': move_log_black.all_moves_knight(), 'bB': move_log_black.all_moves_bishop(),
                                      'bQ': move_log_black.all_moves_queen(), 'bK': move_log_black.all_moves_king()}
                color_class = {'w': move_log_white, 'b': move_log_black}
                move = list(self.pregame.values())[i][j]
                enc = self.get_info(move)
                start_pos = enc['start']
                end_pos = enc['end']
                color = enc['piece'][0]
                if type(enc['start']) is not dict:
                    if enc['start'] is None:
                        func = color_class[color].valid_moves(enc['piece'], pieces_surrounding[enc['piece']])
                        for k in range(len(func)):
                            for m in range(len(list(func.values())[k])):
                                if end_pos == list(func.values())[k][m]:
                                    start_pos = list(func.keys())[k]
                        if start_pos is not None:
                            enc['start'] = start_pos
                            self.change_board(start_pos, end_pos, enc['piece'])

                    elif enc['start'][1] is None:
                        func = color_class[color].valid_moves(enc['piece'], pieces_surrounding[enc['piece']])
                        for k in range(len(func)):
                            for m in range(len(list(func.values())[k])):
                                if end_pos == list(func.values())[k][m] and enc['start'][0] == list(func.keys())[k][0]:
                                    start_pos = list(func.keys())[k]
                                    enc['start'] = start_pos
                        if enc['start'][1] is not None:
                            self.change_board(start_pos, end_pos, enc['piece'])

                    elif enc['start'][0] is None:
                        func = color_class[color].valid_moves(enc['piece'], pieces_surrounding[enc['piece']])
                        for k in range(len(func)):
                            for m in range(len(list(func.values())[k])):
                                if end_pos == list(func.values())[k][m] and enc['start'][1] == list(func.keys())[k][1]:
                                    start_pos = list(func.keys())[k]
                                    enc['start'] = start_pos
                        if enc['start'][0] is not None:
                            self.change_board(start_pos, end_pos, enc['piece'])

                elif type(enc['start']) is dict:
                    king_start = enc['start'][color + 'K']
                    king_end = enc['end'][color + 'K']
                    rook_start = enc['start'][color + 'R']
                    rook_end = enc['end'][color + 'R']
                    self.change_board(king_start, king_end, color + 'K')
                    self.change_board(rook_start, rook_end, color + 'R')

    def get_board(self):
        return self.standard_board

    def get_pregame(self):
        return self.pregame
    
    def get_board_list(self):
        for i in range(len(self.board_list)):
            self.board_list[i] = Methods.translator(self.board_list[i])
        return self.board_list

    def change_board(self, start, end, piece):
        start_row, start_col = start
        end_row, end_col = end
        self.standard_board = copy.deepcopy(self.standard_board)
        self.standard_board[start_row][start_col] = 0
        self.standard_board[end_row][end_col] = self.pieces_color_swap[piece]
        self.board_list.append(self.standard_board)

    def get_info(self, move):
        color = ''
        cords = []
        pieces = []
        operation = []
        if self.white_turn is True:
            color = 'w'
            self.white_turn = False
        elif self.white_turn is False:
            color = 'b'
            self.white_turn = True

        piece = color + 'P'

        for i in range(len(move)):
            if move[i] in self.ranks_to_rows:
                cords.append(move[i])
            if move[i] in self.files_to_cols:
                cords.append(move[i])
            if move[i] in self.pieces_swap:
                pieces.append(move[i])
            if move[i] in self.operations:
                operation.append(move[i])
            if move in self.operations:
                operation.append(move)

        if len(pieces) == 1:
            piece = color + str(pieces[0])
        if len(cords) == 2:
            r, c = cords
            return {'start': None, 'end': (self.ranks_to_rows[c], self.files_to_cols[r]), 'piece': piece}
        elif len(cords) == 3:
            s, r, c = cords
            if s.isdigit() is True:
                return {'start': (self.ranks_to_rows[s], None), 'end': (self.ranks_to_rows[c], self.files_to_cols[r]),
                        'piece': piece}
            elif s.isalpha() is True:
                return {'start': (None, self.files_to_cols[s]), 'end': (self.ranks_to_rows[c], self.files_to_cols[r]),
                        'piece': piece}

        elif len(cords) == 0 and len(operation) > 2:
            var = ''
            for n in range(len(operation.copy())):
                var += str(list(operation.copy())[n])
            operation.clear()
            operation.append(var)

            rook_cords = None
            king_num = self.pieces_color_swap[color + 'K']
            rook_num = self.pieces_color_swap[color + 'R']
            king_pos = self.main_board.get_pos(king_num)
            rook_pos = self.main_board.get_pos(rook_num)
            if len(rook_pos) > 1 and rook_cords is None:
                if operation[0] == 'O-O':
                    for i in range(len(rook_pos)):
                        if rook_pos[i][0] == king_pos[0][0] and rook_pos[i][-1] == len(self.board) - 1:
                            rook_cords = rook_pos[i]
                    return {'start': {color + 'K': tuple(*king_pos), color + 'R': rook_cords},
                            'end': {color + 'K': (king_pos[0][0], king_pos[0][1] + 2),
                                    color + 'R': (rook_cords[0], rook_cords[1] - 2)},
                            'piece': piece}

                elif operation[0] == 'O-O-O':
                    for i in range(len(rook_pos)):
                        if rook_pos[i][0] == king_pos[0][0] and rook_pos[i][-1] == 0:
                            rook_cords = rook_pos[i]
                    return {'start': {color + 'K': tuple(*king_pos), color + 'R': rook_cords},
                            'end': {color + 'K': (king_pos[0][0], king_pos[0][1] - 2),
                                    color + 'R': (rook_cords[0], rook_cords[1] + 3)},
                            'piece': piece}
            elif len(rook_pos) == 1 and rook_cords is None:
                rook_cords = rook_pos[0]
                if operation[0] == 'O-O':
                    return {'start': {color + 'K': tuple(*king_pos), color + 'R': rook_cords},
                            'end': {color + 'K': (king_pos[0][0], king_pos[0][1] + 2),
                                    color + 'R': (rook_cords[0], rook_cords[1] - 2)},
                            'piece': piece}
                elif operation[0] == 'O-O-O':
                    return {'start': {color + 'K': tuple(*king_pos), color + 'R': rook_cords},
                            'end': {color + 'K': (king_pos[0][0], king_pos[0][1] - 2),
                                    color + 'R': (rook_cords[0], rook_cords[1] + 3)},
                            'piece': piece}
            else:
                raise Exception