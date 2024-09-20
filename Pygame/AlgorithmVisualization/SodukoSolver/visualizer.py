class Visualizer:
    def __init__(self, board):
        self.board = board
        self.progress = self.get_solution()
        self.running = True
        self.progress_positions = [(self.progress[i][0][1], self.progress[i][0][0]) for i in range(len(self.progress))]

    @staticmethod
    def draw_rect_outline(surface, rect, color, width=1):
        x, y, w, h = rect
        width = max(width, 1)
        width = min(min(width, w // 2), h // 2)
        for i in range(width):
            p.gfxdraw.rectangle(surface, (x + i, y + i, w - i * 2, h - i * 2), color)

    def get_solution(self):
        solver = Solver(deepcopy(self.board))
        solver.solve()
        return solver.progress

    def solve(self):
        delay = 10000 // len(self.progress)
        delay = 100 if delay > 100 else delay
        for element in self.progress:
            (x, y), value = element
            self.board[x][y] = value
            self.draw()
            if delay > 1:
                p.time.delay(delay)

    def draw_values(self, element, pos):
        x, y = pos
        color = p.Color('black')
        if (x, y) in self.progress_positions:
            color = p.Color('red')
        value = FONT.render(str(element), True, color)
        rect = value.get_rect(center=((x * SQUARE_SIZE + OUTLINE) + SQUARE_SIZE // 2,
                                      (y * SQUARE_SIZE + OUTLINE) + SQUARE_SIZE // 2))
        SCREEN.blit(value, rect)

    def draw(self):
        SCREEN.fill((0, 70, 140))
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                p.draw.rect(SCREEN, p.Color('white'), rect := p.Rect(
                    i * SQUARE_SIZE + OUTLINE, j * SQUARE_SIZE + OUTLINE, SQUARE_SIZE, SQUARE_SIZE))
                self.draw_rect_outline(SCREEN, rect, p.Color('black'))
                element = self.board[j][i]
                if element != 0:
                    self.draw_values(element, (i, j))

        for i in range(1, 3):
            p.draw.line(SCREEN, p.Color('black'),
                        (i * 3 * SQUARE_SIZE + OUTLINE, OUTLINE),
                        (i * 3 * SQUARE_SIZE + OUTLINE, SIZE - OUTLINE), 5)
            p.draw.line(SCREEN, p.Color('black'),
                        (OUTLINE, i * 3 * SQUARE_SIZE + OUTLINE),
                        (SIZE - OUTLINE, i * 3 * SQUARE_SIZE + OUTLINE), 5)

        p.display.update()

    def main(self):
        clock = p.time.Clock()
        while self.running:
            clock.tick(FPS)
            for event in p.event.get():
                if event.type == QUIT:
                    self.running = False
                    p.quit()
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        self.solve()

                        p.time.delay(3000)
                        self.running = False
            self.draw()


if __name__ == '__main__':
    import pygame as p
    from pygame.locals import *
    import pygame.gfxdraw
    from copy import deepcopy
    from solver import Solver
    p.init()

    main_board = [
        [0, 0, 0, 4, 8, 0, 0, 6, 7],
        [8, 3, 0, 0, 6, 9, 5, 0, 0],
        [7, 0, 6, 5, 0, 0, 4, 0, 8],
        [0, 7, 0, 9, 0, 6, 0, 5, 2],
        [6, 0, 3, 0, 7, 2, 1, 9, 0],
        [0, 2, 9, 1, 0, 0, 8, 0, 0],
        [3, 8, 0, 0, 5, 7, 0, 0, 9],
        [0, 0, 7, 3, 0, 4, 2, 8, 0],
        [5, 0, 2, 6, 0, 0, 7, 0, 3]
    ]

    SIZE, OUTLINE = 720, 90
    SQUARE_SIZE = (SIZE - 2 * OUTLINE) // len(main_board)
    FONT = p.font.SysFont('Times', SQUARE_SIZE)
    FPS = 100
    SCREEN = p.display.set_mode((SIZE, SIZE))

    visualizer = Visualizer(main_board)
    visualizer.main()
