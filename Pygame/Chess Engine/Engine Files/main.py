
class Board:
    def __init__(self, board):
        self.board = board
        self.notations = {}
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


    def build_sequence(self, color, *positions):
        elements = {}
        for pos in positions:
            if len(pos) == 0:
                return []
            row, col = pos
            elements[pos] = {'value': Board.get_values()[color][self.board[row][col]]}
        sequence = sorted(elements, key=lambda x: elements[x]['value'])
        return sequence

    def board_informations(self):
        elements = []
        blanksquares = []
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if self.board[i][j] in self.pieces and self.board[i][j] != 0:
                    elements.append(self.pieces[self.board[i][j]])
                elif self.board[i][j] == 0:
                    blanksquares.append((i, j))
        return {'piece types': Counter(elements), 'blank squares': blanksquares}
    


    def center_control(self):
        white_evaluation_center = Evaluation('white', self.board)
        black_evaluation_center = Evaluation('black', self.board)
        center = self.get_center()
        center_control = {}
        board_controls = {'white': white_evaluation_center.board_control(Methods.prep_moves(self.board)['board control'][0]),
                          'black': black_evaluation_center.board_control(Methods.prep_moves(self.board)['board control'][1])}
        for i in range(len(center)):
            dominance = None
            if white_evaluation_center.valid_capture_sequence(board_controls['white'][center[i]]['positions'],
                                                              board_controls['black'][center[i]]['positions']):
                dominance = 'white'
            elif black_evaluation_center.valid_capture_sequence(board_controls['black'][center[i]]['positions'],
                                                                board_controls['white'][center[i]]['positions']):
                dominance = 'black'
            center_control[center[i]] = {'white': board_controls['white'][center[i]]['positions'],
                                         'black': board_controls['black'][center[i]]['positions'],
                                         'dominance': dominance}
        return center_control

    def get_start_pos(self, piece: int):
        positions = []
        for r in range(len(self.start_board)):
            for c in range(len(self.start_board[0])):
                if self.start_board[r][c] == piece:
                    positions.append((r, c))
        return positions

    def get_game_notations(self):
        return self.notations

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
            Board.draw_game_state(screen, self.board, self.pieces)

    @staticmethod
    def draw_game_state(screen, board, pieces):
        Board.draw_board(screen)
        Board.draw_pieces(screen, board, pieces)

    @staticmethod
    def draw_board(screen):
        colors = [p.Color('white'), p.Color('gray')]
        for r in range(DIMENSION):
            for c in range(DIMENSION):
                color = colors[(r + c) % 2]
                p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

    @staticmethod
    def draw_pieces(screen, board, pieces):
        for r in range(DIMENSION):
            for c in range(DIMENSION):
                piece = pieces[board[r][c]]
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

    def simulate_board(self, start, end):
        r1, c1 = start
        r2, c2 = end
        simulation_board = copy.deepcopy(self.board)
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
    def save_boards(boards):
        import indentation
        import json
        data_structure = {
            i + 1: [indentation.NoIndent(elem) for elem in boards[i]] for i in range(len(boards))
        }
        with open('boards.json', 'w') as fp:
            json.dump(data_structure, fp, cls=indentation.MyEncoder, sort_keys=True, indent=4)
            fp.write('\n')
    
    @staticmethod
    def save_notation(notation):
        import json
        with open('notations.json', 'w') as fp:
            json.dump({'game notation': notation}, fp)

    @staticmethod
    def translator(board):
        pieces = {11: 'wP', 12: 'wR', 13: 'wN', 14: 'wB', 15: 'wQ', 16: 'wK',
                  21: 'bP', 22: 'bR', 23: 'bN', 24: 'bB', 25: 'bQ', 26: 'bK', 0: '--'}
        for i in range(len(board)):
            for j in range(len(board)):
                board[i][j] = pieces[board[i][j]]
        return board


class EvaluationResults:
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
    

if __name__ == '__main__':
    import time
    start_time = time.time()
    from collections import Counter
    import copy
    import pygame as p
    from Setup import *
    from MLB import MoveLogBlack
    from MLW import MoveLogWhite
    from Evaluation import Evaluation
    from MoveSelection import MoveSelection

    """pygame"""
    WIDTH = HEIGHT = 512
    DIMENSION = 8
    SQ_SIZE = HEIGHT // DIMENSION
    MAX_FPS = 15
    IMAGES = {}

    """pregame build"""
    moves = '1. e4 c5 2. Nf3 d6 3. d4 cxd4 4. Nxd4 Nf6 5. Nc3 a6 6. Be3 e5 7. Nb3 d5'
    setup = SetupGame(moves.strip())
    setup.search_start()
    base_board = setup.get_board()

    """basic initialization"""
    board = Board(base_board)
    main_board = board.get_board()

    show_time = time.time()
    # board.main()
    total_show_time = time.time() - show_time

    Methods.save_boards(setup.get_board_list())
    Methods.save_notation(setup.get_pregame())

    white_evaluation = Evaluation('white', main_board)
    black_evaluation = Evaluation('black', main_board)
    evaluation_results = EvaluationResults()
    white_move_selection = MoveSelection('white', main_board)
    black_move_selection = MoveSelection('black', main_board)
    
    print(f'Runtime: {time.time() - start_time - total_show_time}')

