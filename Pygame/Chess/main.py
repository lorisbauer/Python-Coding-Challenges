def converter(board):
    converted_board = [['--' for _ in range(len(board))] for _ in range(len(board))]
    for i in range(len(board)):
        for j, element in enumerate(board[i]):
            if element != '--':
                color, piece = list(element)
                converted_board[i][j] = Piece(color, piece, p.transform.scale(p.image.load(os.path.join('imagesChess', element + '.png')), (SQUARE, SQUARE)), (j, i))
    return converted_board

def controlled_squares(board, color, pos):
    directions = {'w': -1, 'b': 1}
    valid_moves = Board.get_valid_moves(board, pos).get(color)
    moves = []
    if pos is not False:
        for element in valid_moves:
            if (piece:= element.get('piece')).piece == 'P':
                x, y = piece.pos
                control_squares = [(x, y) for x, y in list(product([x + 1, x - 1], [y + directions.get(color)])) if x >= 0 and y >= 0 and x < len(board) and y < len(board)]
                element['moves'] = control_squares
    for elem in valid_moves:
        moves += elem.get('moves')
    return moves

class Piece:
    def __init__(self, color, piece, image, pos):
        self.color = color
        self.piece = piece
        self.image = image
        self.pos = pos
        self.x, self.y = self.pos
        self.moved = False
        self.move_log = []

class Game:
    def __init__(self, board, game_length):
        self.board = board
        self.squares = {(i,j): p.Rect(OUTLINE + i*SQUARE, OUTLINE + j*SQUARE, SQUARE, SQUARE) for i in range(len(self.board)) for j in range(len(self.board))}
        self.selected = None
        self.selected_object = None
        self.square_color = {0: p.Color('white'), 1: p.Color('gray')}
        self.current_moves = []
        self.directions = {'w': -1, 'b': 1}
        self.color_swap = {'w': 'b', 'b': 'w'}
        self.backrank = {'w': 7, 'b': 0}
        self.end = False
        self.check = {'w': False, 'b': False}
        self.state = 'game'
        self.current_color = {1: 'b', 0: 'w'}.get(game_length%2)

    @staticmethod
    def draw_rect_outline(surface, rect, color, width=1):
        x, y, w, h = rect
        width = min(min(max(width, 1), w//2), h//2)
        for i in range(width):
            p.gfxdraw.rectangle(surface, (x+i, y+i, w-i*2, h-i*2), color)

    def draw_board(self):
        p.draw.rect(SCREEN, p.Color('white'), p.Rect(OUTLINE, OUTLINE, SIZE - 2*OUTLINE, SIZE - 2*OUTLINE))
        for (x, y) in list(self.squares.keys()):
            p.draw.rect(SCREEN, self.square_color.get((x + y)%2), self.squares.get((x, y)))
        Game.draw_rect_outline(SCREEN, p.Rect(OUTLINE - BOARD_THICKNESS, OUTLINE - BOARD_THICKNESS, SIZE - 2*OUTLINE + 2*BOARD_THICKNESS, SIZE - 2*OUTLINE + 2*BOARD_THICKNESS), p.Color('black'), BOARD_THICKNESS)
    
    def draw_pieces(self):
        for i in range(len(self.board)):
            for j, element in enumerate(self.board[i]):
                if element != EMPTY:
                    x, y = OUTLINE + j*SQUARE, OUTLINE + i*SQUARE
                    SCREEN.blit(element.image, (x, y))

        if self.selected is not None:
            Game.draw_rect_outline(SCREEN, self.selected, p.Color('dark red'), 2)
    
    def draw_possiblities(self):
        x1, y1 = self.selected_object.pos         
        p.draw.rect(SCREEN, (255, 102, 102), p.Rect(OUTLINE + x1*SQUARE, OUTLINE + y1*SQUARE, SQUARE, SQUARE))
        mapped = Board(self.board, self.selected_object, self.directions.get(self.selected_object.color))
        self.current_moves = mapped.main()

        for (x, y) in self.current_moves:
            rect = p.Rect(OUTLINE + x*SQUARE, OUTLINE + y*SQUARE, SQUARE, SQUARE)
            state = self.exception_handling((x, y))

            if state:
                if rect.collidepoint(p.mouse.get_pos()):
                    p.draw.rect(SCREEN, (51, 153, 255), rect)
                else:
                    surface = p.Surface((SQUARE, SQUARE), p.SRCALPHA)
                    surface.fill((153, 255, 153, 128))
                    SCREEN.blit(surface, (OUTLINE + x*SQUARE, OUTLINE + y*SQUARE))
    
    def exception_handling(self, move):
        x, y = move
        state = True
        if self.selected_object.piece == 'K':
            if (x, y) in controlled_squares(self.board, self.color_swap.get(self.selected_object.color), self.selected_object.pos):
                state = False
        elif self.test_move(self.selected_object, (x, y)):
            state = False
        return state
    
    def identify_check(self, king):
        x, y = king.pos
        valid_moves = controlled_squares(self.board, self.color_swap.get(king.color), False)
        return (x, y) in valid_moves

    def search_piece(self, color, piece):
        positions = []
        for i in range(len(self.board)):
            for _, element in enumerate(self.board[i]):
                if element != EMPTY:
                    if color + piece == element.color + element.piece:
                        positions.append(element)
        return positions
    
    def test_move(self, piece, dest):
        x, y = piece.pos
        x1, y1 = dest

        
        dest_piece = self.board[y1][x1]
        self.board[y][x] = '--'
        self.board[y1][x1] = piece

        king_pos = self.search_piece(piece.color, 'K')[0].pos
        state = False

        if king_pos in controlled_squares(self.board, self.color_swap.get(piece.color), king_pos):
            state = True

        self.board[y][x] = piece
        self.board[y1][x1] = dest_piece
        return state
    
    def no_moves(self, obj):
        moves = Board(self.board, obj, self.directions.get(obj.color))
        return moves.main()
    
    def handle_checks(self):
        pass

    def draw(self):
        SCREEN.fill((0, 70, 140))
        if self.end is False:   
            self.draw_board()
            if self.selected_object is not None:
                if self.check.get(self.current_color):
                    self.handle_checks()
                else:
                    self.draw_possiblities()
            self.draw_pieces()

        p.display.update()

    def main(self):
        run = True
        clock = p.time.Clock()
        while run:
            clock.tick(FPS) 
            for event in p.event.get():
                if event.type == QUIT:
                    run = False
                    p.quit()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 3:
                        if self.end is False:
                            if self.check.get(self.current_color) is False:
                                for square in list(self.squares.values()):
                                    if square.collidepoint(p.mouse.get_pos()):
                                        if self.selected != square:
                                            self.selected = square
                                            x, y = list(self.squares.keys())[list(self.squares.values()).index(self.selected)]
                                            if self.board[y][x] != EMPTY:
                                                self.selected_object = self.board[y][x]
                                            else:
                                                self.selected_object = None
                                        else:
                                            self.selected = None
                                            self.selected_object = None
                                        break

                    elif event.button == 1:
                        if self.end is False and self.selected_object is not None and self.current_color == self.selected_object.color:
                            for (x, y) in self.current_moves:
                                if p.Rect(OUTLINE + x*SQUARE, OUTLINE + y*SQUARE, SQUARE, SQUARE).collidepoint(p.mouse.get_pos()):
                                    x1, y1 = self.selected_object.pos
                                    self.board[y1][x1] = EMPTY
                                    self.board[y][x] = self.selected_object
                                    if self.selected_object.piece == 'K' and abs(x - x1) > 1:
                                        if (x - x1) < 0:
                                            x2, y2 = (0, self.backrank.get(self.selected_object.color))
                                            x3, y3 = (3, self.backrank.get(self.selected_object.color))
                                        else:
                                            x2, y2 = (7, self.backrank.get(self.selected_object.color))
                                            x3, y3 = (5, self.backrank.get(self.selected_object.color))

                                        obj = self.board[y2][x2]
                                        self.board[y2][x2] = EMPTY
                                        self.board[y3][x3] = obj
                                        obj.pos = (x3, y3)
                                        obj.moved = True

                                    self.selected_object.pos = (x, y)
                                    if self.selected_object.moved is False:
                                        self.selected_object.moved = True

                                    if self.selected_object.piece == 'P':
                                        self.selected_object.move_log.append((x1, y1))

                                    if self.check.get(self.current_color):
                                        self.check[self.current_color] = False
                                        
                                    self.current_color = self.color_swap.get(self.selected_object.color)
                                    self.selected = None
                                    self.selected_object = None

                                    break

            if self.identify_check((king:= self.search_piece(self.current_color, 'K')[0])):
                self.check[self.current_color] = True
                valid_moves = Board.get_valid_moves(self.board).get(self.current_color)
                escapes = []
                for element in valid_moves:
                    possibilities = []
                    piece = element.get('piece')
                    moves = element.get('moves')
                    for move in moves:
                        if self.test_move(piece, move) is False:
                            possibilities.append(move)
                    if possibilities:
                        escapes.append({'piece': element, 'moves': possibilities})

                if self.no_moves(king):
                    #escapes.append([king, p.Rect(OUTLINE + king.x*SQUARE, OUTLINE + king.y*SQUARE, SQUARE, SQUARE)])
                    pass
                if escapes:
                    self.selected_object = escapes

            self.draw()
            p.display.flip()

if __name__ == '__main__':
    import pygame as p
    from pygame.gfxdraw import *
    from pygame.locals import *
    from itertools import product
    import os
    from possibilities import Board
    from setup import Setup
    p.init()

    SIZE = 660
    OUTLINE = 50
    DIMENSION = 8
    FPS = 30
    BOARD_THICKNESS = 4
    SQUARE = (SIZE - 2*OUTLINE)//DIMENSION
    EMPTY = '--'

    standard_board = [
        ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
        ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
        ['--', '--', '--', '--', '--', '--', '--', '--'],
        ['--', '--', '--', '--', '--', '--', '--', '--'],
        ['--', '--', '--', '--', '--', '--', '--', '--'],
        ['--', '--', '--', '--', '--', '--', '--', '--'],
        ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
        ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
    ]

    pgn = '1. e4 e5 2. Ke2 a6 3. Kf3 b5 4. Kg4 d6+'
    SCREEN = p.display.set_mode((SIZE, SIZE))
    setup = Setup(pgn, converter(standard_board))
    game = Game(setup.main(), len(setup.split_pgn(pgn)))
    game.main()