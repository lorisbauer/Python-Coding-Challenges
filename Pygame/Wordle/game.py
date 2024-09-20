class Spot:
    def __init__(self, rect):
        self.rect = rect
        self.value = None
        self.color = p.Color('black')

    def draw_spot(self):
        p.draw.rect(SCREEN, self.color, self.rect)
        Game.draw_rect_outline(SCREEN, self.rect, p.Color('white'))
        if self.value is not None:
            x, y = self.rect[:2]
            letter = FONT.render(str(self.value).upper(), True, p.Color('white'))
            rect = letter.get_rect(center=(x + SQUARE_SIZE//2, y + SQUARE_SIZE//2))
            SCREEN.blit(letter, rect)

class Game:
    def __init__(self):
        self.running = True
        self.selected = None
        self.word = self.generate_word()
        self.current_row = 0
        self.fields = [[Spot(p.Rect(SQUARE_SIZE*i + SIDE, SQUARE_SIZE*j + TOP, SQUARE_SIZE, SQUARE_SIZE)) for i in range(COLS)] for j in range(ROWS)]
    
    @staticmethod
    def generate_word():
        with open('Wordle/allWords.txt', 'r') as f:
            return random.choice(f.readlines())[:-1]
         
    def check_current_row(self):
        for spot in self.fields[self.current_row]:
            if spot.value is None:
                return False
        return True

    @staticmethod
    def draw_rect_outline(surface, rect, color, width=1):
        x, y, w, h = rect
        width = min(min(max(width, 1), w//2), h//2)
        for i in range(width):
            p.gfxdraw.rect(surface, (x+i, y+i, w-i*2, h-i*2), color)
    
    def check_word(self):
        correct = True
        for i, spot in enumerate(self.fields[self.current_row]):
            if spot.value == self.word[i]:
                spot.color = (0, 204, 0)
            elif spot.value in self.word:
                spot.color = (48, 104, 201)
                correct = False
            else:
                spot.color = p.Color('gray')
                correct = False
        return correct
    
    def draw(self):
        SCREEN.fill(p.Color('black'))
        for i in range(ROWS):
            for j, spot in enumerate(self.fields[i]):
                spot.draw_spot()
        if self.selected is not None:
            x, y = self.selected.rect[:2]
            self.draw_rect_outline(SCREEN, p.Rect(x + 1, y + 1, SQUARE_SIZE - 2, SQUARE_SIZE - 2), p.Color('red'), 2)
        p.display.update()

    def main(self):
        clock = p.time.Clock()
        while self.running:
            clock.tick(FPS)
            mouse_pos = p.mouse.get_pos()
            for event in p.event.get():
                if event.type == QUIT:
                    self.running = False
                    p.quit()
                if event.type == MOUSEBUTTONDOWN:
                    for j, spot in enumerate(self.fields[self.current_row]):
                        if spot.rect.collidepoint(mouse_pos):
                            self.selected = spot
                            break
                if event.type == KEYDOWN:
                    if event.key == K_SPACE and self.check_current_row():
                        state = self.check_word()
                        if state or self.current_row + 1 == ROWS:
                            p.time.delay(500)
                            self.running = False
                        self.current_row += 1
                        self.selected = None
                    else:
                        if self.selected is not None:
                            if event.unicode.isalpha():
                                self.selected.value = event.unicode 
            self.draw()
        print(self.word)


if __name__ == '__main__':
    import pygame as p
    from pygame.gfxdraw import *
    from pygame.locals import *
    import random
    p.init()

    SIZE = 800
    TOP = 100
    SQUARE_SIZE = 100
    ROWS, COLS = 6, 5
    FONT = p.font.SysFont('Times', SQUARE_SIZE)
    SIDE = (SIZE - COLS*SQUARE_SIZE)//2
    FPS = 60
    SCREEN = p.display.set_mode((SIZE, SIZE))

    game = Game()
    game.main()
