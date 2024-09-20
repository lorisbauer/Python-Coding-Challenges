from possibilities import Board
import string

class Move:
    def __init__(self, piece, color, end, start=None):
        self.piece = piece
        self.color = color
        self.start = start
        self.end = end
        self.complete_start = self.check_start()
    
    def check_start(self):
        if self.start is not None:
            x, y = self.start
            if x is None or y is None:
                return False
            return True
        else:
            return False
    
    def __repr__(self):
        return f'{self.color + self.piece}: {self.start} -> {self.end}'


class Setup:
    def __init__(self, pgn, board):
        self.pgn = pgn
        self.dimension = 8
        self.board = board
        self.pieces = ['R', 'B', 'N', 'Q', 'K']
        self.directions = {'w': -1, 'b': 1}
        self.castling = ['O-O', 'O-O-O']
        self.operators = ['+', '#', 'x']
        self.colors = {1: 'b', 0: 'w'}
        self.backrank = {'w': 7, 'b': 0}
        self.moves = self.get_detailed()

    def split_pgn(self, pgn):
        moves = [element for _, element in enumerate(pgn.split()) if element[0].isnumeric() is False]
        for i, pos in enumerate(moves):
            filtered = ''
            for l in pos:
                if l not in self.operators:
                    filtered += l
            moves[i] = filtered
        return moves
    
    def indicator(self, element):
        pos: tuple
        if element.isnumeric():
            pos = (None, self.dimension - int(element))
        elif element.isalpha():
            pos = (string.ascii_lowercase.index(element), None)
        return pos
    
    def get_detailed(self):
        simplified = self.split_pgn(self.pgn)
        moves = []
        for i, move in enumerate(simplified):
            color = self.colors.get(i % 2)
            if len(move) == 2:
                moves.append(Move('P', color, end=self.notation_converter(move)))
            elif len(move) == 3:
                if move not in self.castling:
                    if move[0] in self.pieces:
                        moves.append(Move(move[0], color, end=self.notation_converter(move[1:])))
                    else:
                        moves.append(Move('P', color, start=self.indicator(move[0]), end=self.notation_converter(move[1:])))
                else:
                    moves.append(Move('K', color, start=(4, self.backrank.get(color)), end=(6, self.backrank.get(color))))
                    moves.append(Move('R', color, start=(7, self.backrank.get(color)), end=(5, self.backrank.get(color))))
            elif len(move) == 4:
                if move not in self.castling:
                    moves.append(Move(move[0], color, start=self.indicator(move[1]), end=self.notation_converter(move[2:])))
                else:
                    moves.append(Move('K', color, start=(4, self.backrank.get(color)), end=(2, self.backrank.get(color))))
                    moves.append(Move('R', color, start=(0, self.backrank.get(color)), end=(3, self.backrank.get(color))))
        return moves

    def notation_converter(self, pos):
        x, y = pos
        return (string.ascii_lowercase.index(x), self.dimension - int(y))
    
    @staticmethod
    def get_piece_moves(color, piece, board):
        all_moves = Board.get_valid_moves(board).get(color)
        moves = {}
        for dict in all_moves:
            if (element:= dict.get('piece')).piece == piece:
                moves[element.pos] = dict.get('moves')
        return moves
    
    def get_start(self, board, move):
        start = None
        if move.start is None:
            valid_moves = Setup.get_piece_moves(move.color, move.piece, board)
            completed = False
            for key in list(valid_moves.keys()):
                if completed is False:
                    for (x, y) in valid_moves.get(key):
                        if (x, y) == move.end:
                            start = key
                            completed = True
                            break
                else:
                    break
        else:
            x, y = move.start
            valid_moves = Setup.get_piece_moves(move.color, move.piece, board)
            if x is not None:
                for key in list(valid_moves.keys()):
                    if key[0] == x and move.end in valid_moves.get(key):
                        start = key
                        break
            if y is not None:
                for key in list(valid_moves.keys()):
                    if key[1] == y and move.end in valid_moves.get(key):
                        start = key
                        break
        if start is not None:
            return Move(move.piece, move.color, start=start, end=move.end)
  
    def main(self):
        for move in self.moves:
            if move.complete_start:
                start_x, start_y = move.start
                end_x, end_y = move.end
            else:
                result = self.get_start(self.board, move)
                start_x, start_y = result.start
                end_x, end_y = result.end
                
            piece = self.board[start_y][start_x]
            self.board[start_y][start_x] = '--'
            self.board[end_y][end_x] = piece
            piece.pos = (end_x, end_y)
            piece.moved = True
        return self.board