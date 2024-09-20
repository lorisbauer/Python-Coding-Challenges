
class Board:
    def __init__(self, board):
        self.board = board
        self.pieces = {11: 'wP', 12: 'wR', 13: 'wN', 14: 'wB', 15: 'wQ', 16: 'wK',
                       21: 'bP', 22: 'bR', 23: 'bN', 24: 'bB', 25: 'bQ', 26: 'bK', 0: '--'}
        self.start_board = [[22, 23, 24, 25, 26, 24, 23, 22],
                            [21, 21, 21, 21, 21, 21, 21, 21],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [11, 11, 11, 11, 11, 11, 11, 11],
                            [12, 13, 14, 15, 16, 14, 13, 12]]

    def get_board(self):
        return self.board

    def get_start_pos(self, piece: int):
        positions = []
        for r in range(len(self.start_board)):
            for c in range(len(self.start_board[0])):
                if self.start_board[r][c] == piece:
                    positions.append((r, c))
        return positions

    def is_moved(self, piece):
        pass

    def get_game_state(self):
        pass

    def make_move(self, move):
        self.board[move.startRow][move.startCol] = 0
        self.board[move.endRow][move.endCol] = move.pieceMoved

    @staticmethod
    def load_images():
        pieces = ['wR', 'wN', 'wB', 'wQ', 'wK', 'wP', 'bR', 'bN', 'bB', 'bQ', 'bK', 'bP']
        for piece in pieces:
            IMAGES[piece] = p.transform.scale(p.image.load('images/' + piece + '.png'), (SQ_SIZE, SQ_SIZE))

    def main(self):
        p.init()
        p.display.set_caption('Chess Engine')
        screen = p.display.set_mode((WIDTH, HEIGHT), 0, 8)
        screen.fill(p.Color('white'))
        clock = p.time.Clock()
        Board.load_images()
        running = True
        while running:
            for e in p.event.get():
                if e.type == p.QUIT:
                    running = False
            clock.tick(MAX_FPS)
            p.display.flip()
            self.draw_game_state(screen)

    def draw_game_state(self, screen):
        Board.draw_board(screen)
        self.draw_pieces(screen)

    @staticmethod
    def draw_board(screen):
        colors = [p.Color('white'), p.Color('gray')]
        for r in range(DIMENSION):
            for c in range(DIMENSION):
                color = colors[(r + c) % 2]
                p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

    def draw_pieces(self, screen):
        for r in range(DIMENSION):
            for c in range(DIMENSION):
                piece = self.pieces[self.board[r][c]]
                if piece != '--':
                    screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

    @staticmethod
    def get_values():
        values = {'white': {11: 1, 12: 5, 13: 3, 14: 3.125, 15: 9, 16: 0.5},
                  'black': {21: 1, 22: 5, 23: 3, 24: 3.125, 25: 9, 26: 0.5}}
        return values

    @staticmethod
    def get_pieces():
        pieces = ['wR', 'wN', 'wB', 'wQ', 'wK', 'wP', 'bR', 'bN', 'bB', 'bQ', 'bK', 'bP']
        return pieces

    def get_pos(self, piece: int):
        positions = []
        for r in range(len(self.board)):
            for c in range(len(self.board[0])):
                if self.board[r][c] == piece:
                    positions.append((r, c))
        if len(positions) > 0:
            return positions
        else:
            return None

    def get_center(self):
        center = [(i, j) for i in range(len(self.board) // 2 - 1, len(self.board) // 2 + 1)
                  for j in range(len(self.board) // 2 - 1, len(self.board) // 2 + 1)]
        return center

    def display_board(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if j == 7:
                    print(self.pieces[self.board[i][j]])
                else:
                    print(self.pieces[self.board[i][j]] + " ", end="")

    @staticmethod
    def simulate_board(bo, start, end):
        r1, c1 = start
        r2, c2 = end
        simulation_board = copy.deepcopy(bo)
        simulation_board[r2][c2] = simulation_board[r1][c1]
        simulation_board[r1][c1] = 0
        return simulation_board


class Methods:
    @staticmethod
    def surrounding_3x3(position):
        row, col = position
        surrounding_3x3 = []
        for i in range(3):
            for j in range(3):
                if 0 <= (row + 1) - i <= 7 and 0 <= (col - 1) + j <= 7:
                    surrounding_3x3.append(((row + 1) - i, (col - 1) + j))
        return surrounding_3x3

    @staticmethod
    def surrounding_5x5(position):
        row, col = position
        surrounding_5x5 = []
        for i in range(5):
            for j in range(5):
                if 0 <= (row + 2) - i <= 7 and 0 <= (col - 2) + j <= 7:
                    surrounding_5x5.append(((row + 2) - i, (col - 2) + j))
        return surrounding_5x5

    @staticmethod
    def unpack_V1(surrounding):
        list_surrounding = {}
        for i in range(len(surrounding)):
            element = []
            for j in range(len(list(surrounding.values())[i])):
                if type(list(surrounding.values())[i][j]) is list:
                    elements = []
                    for k in range(len(list(surrounding.values())[i])):
                        elements += list(surrounding.values())[i][k]
                    if type(elements[0]) is not list:
                        for e1 in elements:
                            element.append(e1)
                        list_surrounding[list(surrounding.keys())[i]] = element
                    else:
                        special_elements = []
                        for m in range(len(list(elements))):
                            special_elements += elements[m]
                        for e2 in special_elements:
                            element.append(e2)
                        list_surrounding[list(surrounding.keys())[i]] = element
                    break
                else:
                    element.append(list(surrounding.values())[i][j])
            if type(list(surrounding.values())[i][0]) is not list:
                list_surrounding[list(surrounding.keys())[i]] = element
        return list_surrounding

    @staticmethod
    def unpack_V2(all_valid_moves):
        list_valid_moves = []
        for i in range(len(all_valid_moves)):
            element = []
            for j in range(len(list(all_valid_moves.values())[i])):
                if type(list(all_valid_moves.values())[i][j]) is list:
                    elements = []
                    for k in range(len(list(all_valid_moves.values())[i])):
                        elements += list(all_valid_moves.values())[i][k]
                    if type(elements[0]) is not list:
                        for element in elements:
                            list_valid_moves.append(element)
                    else:
                        special_elements = []
                        for l in range(len(list(elements))):
                            special_elements += elements[l]
                        for element in special_elements:
                            list_valid_moves.append(element)
                    break
                else:
                    element.append(list(all_valid_moves.values())[i][j])
            if type(list(all_valid_moves.values())[i][0]) is not list:
                for e in element:
                    list_valid_moves.append(e)
        return list_valid_moves

    @staticmethod
    def merge_dicts(*dict_args):
        result = {}
        for dictionary in dict_args:
            result.update(dictionary)
        return result

    @staticmethod
    def merge_lists(*lists):
        result = []
        for l in lists:
            result += l
        return result

    @staticmethod
    def prep_moves(board):
        types = ['board control', 'x-ray', 'valid']
        prep = {}
        for t in types:
            elements_white = []
            elements_black = []
            for piece in Board.get_pieces():
                if piece[0] == 'w':
                    if Methods.get_moves(piece, board)[t] is not None:
                        elements_white.append(Methods.get_moves(piece, board)[t])
                elif piece[0] == 'b':
                    if Methods.get_moves(piece, board)[t] is not None:
                        elements_black.append(Methods.get_moves(piece, board)[t])
            prep[t] = [Methods.unpack_V1(Methods.merge_dicts(*elements_white)),
                       Methods.unpack_V1(Methods.merge_dicts(*elements_black))]
        return prep

    @staticmethod
    def get_moves(piece: str, board):
        from MLB import MoveLogBlack
        from MLW import MoveLogWhite
        move_log_white = MoveLogWhite(board)
        move_log_black = MoveLogBlack(board)

        x_ray_moves = {'wP': move_log_white.all_moves_pawn(), 'wR': move_log_white.all_moves_rook(),
                       'wN': move_log_white.all_moves_knight(), 'wB': move_log_white.all_moves_bishop(),
                       'wQ': move_log_white.all_moves_queen(), 'wK': move_log_white.all_moves_king(),
                       'bP': move_log_black.all_moves_pawn(), 'bR': move_log_black.all_moves_rook(),
                       'bN': move_log_black.all_moves_knight(), 'bB': move_log_black.all_moves_bishop(),
                       'bQ': move_log_black.all_moves_queen(), 'bK': move_log_black.all_moves_king()}

        if piece[0] == 'w':
            return {'valid': move_log_white.valid_moves(piece, x_ray_moves[piece]),
                    'board control': move_log_white.board_control(piece, x_ray_moves[piece]),
                    'x-ray': x_ray_moves[piece]}
        elif piece[0] == 'b':
            return {'valid': move_log_black.valid_moves(piece, x_ray_moves[piece]),
                    'board control': move_log_black.board_control(piece, x_ray_moves[piece]),
                    'x-ray': x_ray_moves[piece]}

    @staticmethod
    def get_pregame_moves():
        m = '1. e4 c5 2. Nf3 d6 3. d4 cxd4 4. Nxd4 Nf6 5. Nc3 a6 6. Be3 e5 7. Nb3 d5'
        return m

    @staticmethod
    def get_pregame():
        setup = SetupGame(Methods.get_pregame_moves())
        setup.search_start()
        pregame = setup.get_pregame()
        return pregame


class EvaluationResults:
    @staticmethod
    def center_control(board_control_white, board_control_black):
        center = board.get_center()
        center_details = {}
        for i in range(len(center)):
            center_details[center[i]] = [board_control_white[center[i]], board_control_black[center[i]]]

    @staticmethod
    def material_difference():
        material_white = white_evaluation.material()
        material_black = black_evaluation.material()
        return material_white - material_black

    @staticmethod
    def king_safety():
        king_safety = white_evaluation.king_safety()


class Move:
    ranks_to_rows = {'1': 7, '2': 6, '3': 5, '4': 4,
                     '5': 3, '6': 2, '7': 1, '8': 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_cols = {'a': 0, 'b': 1, 'c': 2, 'd': 3,
                     'e': 4, 'f': 5, 'g': 6, 'h': 7}
    cols_to_files = {v: k for k, v in files_to_cols.items()}

    def __init__(self, start, end):
        self.board = board.get_board()
        self.startRow = start[0]
        self.startCol = start[1]
        self.endRow = end[0]
        self.endCol = end[1]
        self.pieceMoved = self.board[self.startRow][self.startCol]
        self.pieces = {11: 'wP', 12: 'wR', 13: 'wN', 14: 'wB', 15: 'wQ', 16: 'wK',
                       21: 'bP', 22: 'bR', 23: 'bN', 24: 'bB', 25: 'bQ', 26: 'bK'}
        self.operations = {'capture': 'x', 'check': '+', 'castle short': 'O-O', 'castle long': 'O-O-O', 'mate': '#'}

    def get_notations(self):
        pass

    def get_rank_file(self, r, c):
        return self.cols_to_files[c] + self.rows_to_ranks[r]


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

    def change_board(self, start, end, piece):
        start_row, start_col = start
        end_row, end_col = end
        self.standard_board[start_row][start_col] = 0
        self.standard_board[end_row][end_col] = self.pieces_color_swap[piece]
        self.board_list.append(self.standard_board)
        # self.display_board()

    def get_pregame(self):
        return {'board': self.standard_board, 'pregame': self.pregame}

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
            piece = color + pieces[0].__str__()
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


if __name__ == '__main__':
    import time
    import copy
    start_time = time.time()
    import pygame as p
    from MLB import MoveLogBlack
    from MLW import MoveLogWhite
    from Evaluation import Evaluation
    from MoveSelection import MoveSelection

    """pygame vars"""
    WIDTH = HEIGHT = 640
    DIMENSION = 8
    SQ_SIZE = HEIGHT // DIMENSION
    MAX_FPS = 15
    IMAGES = {}

    """basic initialization"""
    board = Board(Methods.get_pregame()['board'])
    main_board = board.get_board()

    show_time = time.time()
    # board.main()
    total_show_time = time.time() - show_time

    move_log_white = MoveLogWhite(main_board)
    move_log_black = MoveLogBlack(main_board)
    white_evaluation = Evaluation('white', main_board.copy())
    black_evaluation = Evaluation('black', main_board)
    evaluation_results = EvaluationResults()
    white_move_selection = MoveSelection('white', main_board)
    black_move_selection = MoveSelection('black', main_board)

    """board control data"""
    all_board_control_white, all_board_control_black = Methods.prep_moves(main_board)['board control']
    board_control_w = white_evaluation.board_control(all_board_control_white)
    board_control_b = black_evaluation.board_control(all_board_control_black)

    """evaluation part"""
    EvaluationResults.center_control(board_control_w, board_control_b)
    EvaluationResults.king_safety()

    print(f'Runtime: {time.time() - start_time - total_show_time}')

