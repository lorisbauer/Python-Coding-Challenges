from itertools import product, permutations


class Board:
    def __init__(self, board, piece, direction):
        self.board = board
        self.piece = piece
        self.direction = direction
        self.color = piece.color
        self.pos = piece.pos
        self.dimension = 8
        self.color_swap = {'w': 'b', 'b': 'w'}
        self.moves = []
    
    def validation(self, moves):
        for move in moves:
            self.moves.append(move)
    
    def valid_moves(self, directions, control=False):
        x, y = self.pos
        moves = []
        for direction in directions:
            a, b = direction
            for i in range(1, self.dimension):
                x1, y1 = (x + a*i, y + b*i)
                if self.onboard([(x1, y1)]):
                    if (dest:= self.board[y1][x1]) == '--':
                        moves.append((x1, y1))
                    elif dest.color == self.color_swap.get(self.color):
                        moves.append((x1, y1))
                        if control is not False:
                            if (x1, y1) != control:
                                break
                        else:
                            break
                    else:
                        break
                else:
                    break
        return moves
    
    def onboard(self, moves):
        return [(x, y) for x, y in moves if x >= 0 and y >= 0 and x < self.dimension and y < self.dimension]
  
    def knight_moves(self):
        x, y = self.pos
        moves = list(product([x-1, x+1], [y-2, y+2])) + list(product([x-2,x+2],[y-1,y+1]))
        moves = self.onboard(list(set(moves)))
        valid_moves = []
        for (x1, y1) in moves:
            if (dest := self.board[y1][x1]) == '--' or dest.piece.color == self.color_swap.get(self.color):
                valid_moves.append((x1, y1))
        self.validation(valid_moves)
    
    def bishop_moves(self, control=False):
        directions = list(product([1, -1], [-1, 1]))
        moves = self.valid_moves(directions, control)
        self.validation(moves)
    
    def rook_moves(self, control=False):
        directions = list(permutations((0, 1))) + list(permutations((0, -1)))
        moves = self.valid_moves(directions, control)
        self.validation(moves)
    
    def queen_moves(self, control=False):
        directions = list(permutations((0, 1))) + list(permutations((0, -1))) + list(product([1, -1], [-1, 1]))
        moves = self.valid_moves(directions, control)
        self.validation(moves)
    
    def king_moves(self):
        directions = list(permutations((0, 1))) + list(permutations((0, -1))) + list(product([1, -1], [-1, 1]))
        x, y = self.pos
        moves = []
        for direction in directions:
            a, b = direction
            x1, y1 = (x + a, y + b)
            if self.onboard([(x1, y1)]):
                if (dest:= self.board[y1][x1]) == '--' or dest.color == self.color_swap.get(self.color):
                    moves.append((x1, y1))
        if self.piece.moved is False:
            moves += self.castling()
        self.validation(moves)
    
    def pawn_moves(self):
        backrank = 6 if self.color == 'w' else 1
        swap = {1: 6, 6: 1}
        x, y = self.pos
        moves = []
        if y != backrank:
            moves.append((x, y + self.direction))
        else:
            moves += list(product([x, x], [y + self.direction, y + 2*self.direction]))

        if y + 2*self.direction == swap.get(backrank):
            moves += self.enpassant()
        moves += self.pawn_captures()
        self.validation(moves)
    
    def enpassant(self):
        x, y = self.pos
        moves = []
        for (x1, y1) in [(x + 1, y), (x - 1, y)]:
            if (pawn:= self.board[y1][x1]) != '--' and pawn.color + pawn.piece == self.color_swap.get(self.color) + 'P' and len(pawn.move_log) <= 1:
                moves.append((x1, y1 + self.direction))
        return moves
    
    def pawn_captures(self):
        moves = []
        x, y = self.pos
        for (x1, y1) in list(product([x - 1, x + 1], [y + self.direction, y + self.direction])):
            if self.onboard([(y1, x1)]) and (target:= self.board[y1][x1]) != '--' and target.color != self.color:
                moves.append((x1, y1))
        return moves

    def check_empty(self, pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        end = abs(x1 - x2)
        if x1 > x2:
            for i in range(1, end - 1):
                x, y = x2 + i, y1
                if self.board[y][x] != '--':
                    return False
        else:
            for i in range(1, end - 1):
                x, y = x1 + i, y1
                if self.board[y][x] != '--':
                    return False
        return True
    
    def castling(self):
        moves = []
        if self.piece.moved is False:
            x, y = self.pos
            positions = [(x - 4, y), (x + 3, y)]
            for (x1, y1) in positions:
                if (rook:= self.board[y1][x1]) != '--' and rook.color + rook.piece == self.color + 'R' and rook.moved is False and self.check_empty(self.pos, (x1, y1)):
                    distance = (x1 - x)//abs((x1 - x))
                    moves.append((x + 2*distance, y))
            return moves
        else:
            return moves

    @staticmethod
    def get_valid_moves(board, control=False):
        directions = {'w': -1, 'b': 1}
        white = []
        black = []
        for i in range(len(board)):
            for _, element in enumerate(board[i]):
                if element != '--':
                    move_class = Board(board, element, directions.get(element.color))
                    if element.color == 'w':
                        white.append({'piece': element, 'moves': move_class.main(control)})
                    else:
                        black.append({'piece': element, 'moves': move_class.main(control)})
        valid_moves = {'w': white, 'b': black}
        return valid_moves
    
    def main(self, control=False):
        piece = self.piece.piece
        if piece == 'N':
            self.knight_moves()
        if piece == 'Q':
            self.queen_moves(control)
        if piece == 'B':
            self.bishop_moves(control)
        if piece == 'K':
            self.king_moves()
        if piece == 'R':
            self.rook_moves(control)
        if piece == 'P':
            self.pawn_moves()          
        return self.moves
