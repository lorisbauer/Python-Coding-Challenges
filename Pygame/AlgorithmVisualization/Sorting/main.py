
class ListGenerator:
    def __init__(self, length):
        self.length = length
    
    def get_list(self):
        generated_list = []
        for i in range(self.length):
            # generated_list.append(random.randint(10, HEIGHT - 2*OUTLINE - 2*EDGE))
            generated_list.append(round((HEIGHT - 2*OUTLINE + 1)*((i + 1)/self.length), 1))
        random.shuffle(generated_list)
        return generated_list

class Main:
    def __init__(self):
        self.exception = None
        self.run, self.finished = True, False
        self.length = (WIDTH - 2*OUTLINE)//3
        self.width = (WIDTH - 2*OUTLINE)/self.length
        self.name = None
        self.delay = 1
        self.input_window()
        self.obj = ListGenerator(self.length).get_list()
        self.check_call()
        self.progression: list
        self.screen = p.display.set_mode((WIDTH, HEIGHT), p.RESIZABLE, 32, vsync=1)      
        self.main()
    
    @staticmethod
    def draw_rect_outline(surface, rect, color, width=1):
        x, y, w, h = rect
        width = min(min(max(width, 1), w//2), h//2)
        for i in range(width):
            p.gfxdraw.rectangle(surface, (x+i, y+i, w-i*2, h-i*2), color)
    
    @staticmethod
    def convert_name(str):
        return str.split(' ')[0].lower() + '_sort'
    
    def check_call(self):
        if self.name is None:
            self.run = False
        else:
            if self.name == 'Radix Sort':
                self.obj = [int(element) for _, element in enumerate(self.obj)]

            algorithm = Algorithms(self.obj, (CD*1000)//self.delay)
            method = getattr(Algorithms, self.convert_name(self.name))
            method(algorithm)
            self.progression = algorithm.progression

    def draw_colums(self, state, color='white'):
        for i, element in enumerate(state):
            y = OUTLINE + ((HEIGHT - 2*OUTLINE + 1) - element)
            p.draw.rect(self.screen, p.Color(color), p.Rect(OUTLINE + self.width*i, y, self.width, element))

    def columns(self, time):
        state = self.progression[time]
        self.draw_colums(state)
    
    def draw(self, time):
        self.screen.fill((0, 70, 140))
        p.draw.rect(self.screen, p.Color('black'), p.Rect(OUTLINE, OUTLINE, WIDTH - 2*OUTLINE, HEIGHT - 2*OUTLINE))
        if time < len(self.progression):
            self.columns(time)

        elif time >= len(self.progression) and self.finished is False:
            state = self.obj
            self.draw_colums(state, 'light green')
            self.finished = True
       
        elif self.finished:
            p.time.delay(5000)
            self.run = False

        self.draw_rect_outline(self.screen, p.Rect(OUTLINE - EDGE, OUTLINE - EDGE, WIDTH - 2*OUTLINE + 2*EDGE, HEIGHT - 2*OUTLINE + 2*EDGE), p.Color('gray'), EDGE)
        p.display.flip()
    
    def main(self):
        clock = p.time.Clock()
        while self.run:
            clock.tick(FPS)
            time = p.time.get_ticks()//self.delay
            self.draw(time)
            for event in p.event.get():
                if event.type == QUIT:
                    self.run = False
                    p.quit()

    @staticmethod
    def rgb_to_hex(rgb):
        return '#%02x%02x%02x' % rgb
    
    def input_window(self):
        root = tk.Tk()
        root.title('Input Window')
        root.resizable(False, False)
        root.config(bg=self.rgb_to_hex((0, 70, 140)))

        screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()
        center_x, center_y = int(screen_width/2 - WIDTH/2), int(screen_height/2 - HEIGHT/2)
        root.geometry(f'{WIDTH}x{HEIGHT}+{center_x}+{center_y}')
        bg_color = self.rgb_to_hex((0, 70, 140))

        options = [' /Quick Sort', ' /Bubble Sort', ' /Insertion Sort', ' /Merge Sort', ' /Selection Sort', ' /Heap Sort', ' /Shell Sort', ' /Radix Sort']
        delays = [20, 2, 4, 15, 35, 10, 10, 10]
        list_box = tk.Listbox(root, width=40, height=len(options), selectmode='single', font=font.Font(size=15), bg='light gray', borderwidth=5)
        label = tk.Label(root, text='Select Sorting Algorithm', font=font.Font(size=20, underline=True), bg=bg_color, fg='white')
        label1 = tk.Label(root, text='\n\n', bg=bg_color)
        label2 = tk.Label(root, text='\n\n', bg=bg_color)
        label3 = tk.Label(root, text='\n', bg=bg_color)

        for i, option in enumerate(options):
            list_box.insert(i, option)

        def selected_item():
            try:
                self.name = options[list_box.curselection()[0]][2:]
                self.delay = delays[list_box.curselection()[0]]
                root.destroy()
            except:
                root.destroy()
                self.exception = 'NoInputError'
                self.input_window()
        
        button = tk.Button(root, text='Submit', font=font.Font(size=10), command=selected_item, height=3, width=20, borderwidth=2, activebackground='light green')

        label3.pack()
        label.pack()
        label1.pack()
        list_box.pack()
        label2.pack()
        button.pack()

        if self.exception == 'NoInputError':
            tk.Label(fg='red', text=self.exception, font=font.Font(size=20), bg=bg_color).pack()
        root.mainloop()


if __name__ == '__main__':
    import pygame as p
    from pygame.gfxdraw import *
    from pygame.locals import *
    from SortingAlgorithms import Algorithms
    import tkinter as tk
    import tkinter.font as font
    import random
    p.init()

    WIDTH, HEIGHT = 720, 560
    CD = 5
    OUTLINE = 60
    EDGE = 6
    FPS = 100
    
    Main()