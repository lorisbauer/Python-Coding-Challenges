from main import *
from Evaluation import Evaluation


class MoveSelection:
    def __init__(self, color, board):
        self.color = color
        self.board = board
        self.chess_board = Board(self.board)
        self.pieces = {'white': {11: 'wP', 12: 'wR', 13: 'wN', 14: 'wB', 15: 'wQ', 16: 'wK'},
                       'black': {21: 'bP', 22: 'bR', 23: 'bN', 24: 'bB', 25: 'bQ', 26: 'bK'}}
        self.swap_color = {'white': 'black', 'black': 'white'}
        self.color_short = {'white': 'w', 'black': 'b'}
        self.funcs = {'white': {'valid': Methods.prep_moves(self.board)['valid'][0],
                                'board control': Methods.prep_moves(self.board)['board control'][0],
                                'eval': Evaluation(self.color, self.board)},
                      'black': {'valid': Methods.prep_moves(self.board)['valid'][1],
                                'board control': Methods.prep_moves(self.board)['board control'][1],
                                'eval': Evaluation(self.color, self.board)}}
        self.values = Board.get_values()

    def valid_moves(self):
        valid = self.funcs[self.color]['valid']
        collection_possible_moves = {}
        for i in range(len(valid)):
            elements = []
            for j in range(len(list(valid.values())[i])):
                row, col = list(valid.values())[i][j]
                if (row, col) not in Methods.unpack_V2(self.funcs[self.swap_color[self.color]]['valid']) and \
                        self.board[row][col] not in self.pieces[self.color]:
                    elements.append((row, col))
                collection_possible_moves[list(valid.keys())[i]] = elements
        return collection_possible_moves

    def all_captures(self):
        valid = self.funcs[self.color]['valid']
        collection_capture = {}
        for i in range(len(valid)):
            for j in range(len(list(valid.values())[i])):
                row, col = list(valid.values())[i][j]
                if self.board[row][col] in self.pieces[self.swap_color[self.color]] \
                        and (row, col) not in list(collection_capture.keys()):

                    board_control_color = self.funcs[self.color]['eval']. \
                        board_control(self.funcs[self.color]['board control'])
                    board_control_other_color = self.funcs[self.swap_color[self.color]]['eval']. \
                        board_control(self.funcs[self.swap_color[self.color]]['board control'])

                    control = board_control_color[(row, col)]
                    defence = board_control_other_color[(row, col)]
                    collection_capture[(row, col)] = {'control': self.chess_board.build_sequence(self.color, *control['positions']),
                                                      'defence': self.chess_board.build_sequence(self.swap_color[self.color], *defence['positions'])}
        return collection_capture

    def valid_captures(self):
        all_captures = self.all_captures()
        collection_valid_capture = {}
        for i in range(len(all_captures)):
            if self.funcs[self.color]['eval'].valid_capture_sequence(list(all_captures.values())[i]['control'],
                                                                     list(all_captures.values())[i]['defence']):
                collection_valid_capture[list(all_captures.keys())[i]] = list(all_captures.values())[i]
        return collection_valid_capture



