import pygame as p
from pygame.gfxdraw import *
from pygame.locals import *
from general import *
import os
import math
p.font.init()

class GameOne:
    def __init__(self):
        self.WIDTH, self.HEIGHT = 900, 500
        self.RADIUS = 7
        self.GRAVITY = -6
        self.FPS = 60
        self.GROUND_HEIGHT = 20
        self.TEXT_SIZE = 40
        self.MAX_POWER = 200
        self.OBSTACLE_SPEED = .5
        self.SCREEN = p.display.set_mode((self.WIDTH, self.HEIGHT), 0, 64)
        self.FONT = p.font.SysFont('comicsans', self.TEXT_SIZE)
        self.BACKGROUND = p.transform.scale(p.image.load(os.path.join('images', 'bg.jpg')), (self.WIDTH, self.HEIGHT))
        self.GRASS = p.image.load(os.path.join('images', 'grass.jpg'))
        self.STONE = p.transform.rotate(p.image.load(os.path.join('images', 'stone.jpg')), 90)
    p.display.set_caption('Golf Game')

    def level_setting(self):
        floor, standard_width = 5, 50
        setting = {
            'start': {'rect': p.Rect(self.GROUND_HEIGHT,self.HEIGHT - self.GROUND_HEIGHT - floor,standard_width,floor),'color': p.Color('red')},
            'end': {'rect': p.Rect(self.WIDTH- 1.5*standard_width,self.HEIGHT - self.GROUND_HEIGHT - floor,standard_width,floor), 'color': p.Color('blue')},
            'ground': {'rect': p.Rect(-5, self.HEIGHT - self.GROUND_HEIGHT, self.WIDTH + 10, self.GROUND_HEIGHT + 5), 'color': p.Color('brown')}, 
            'obstacle1': {'rect': p.Rect(self.WIDTH/4, self.HEIGHT/2, self.WIDTH/2, 5*floor), 'color': p.Color('brown')},
            'obstacle2': {'rect': p.Rect(self.WIDTH/2, self.HEIGHT/2 + 5*floor, 5*floor, self.HEIGHT/2 - self.GROUND_HEIGHT- 5*floor), 'color': p.Color('brown')},
            'obstacle3': {'rect': p.Rect(0, 3, 4, self.HEIGHT - self.GROUND_HEIGHT - 2), 'color': (100,100,100)},
            'obstacle4': {'rect': p.Rect(self.WIDTH - 4, 3, 4, self.HEIGHT - self.GROUND_HEIGHT - 2), 'color': (100,100,100)},
            'obstacle5': {'rect': p.Rect(0, 0, self.WIDTH, 4), 'color': (100,100,100)}
            }
        return setting
    
    def textures(self):
        textures = {
            'ground': {'texture': p.transform.scale(self.GRASS, (self.WIDTH + 100, self.GROUND_HEIGHT)), 'pos': (0, self.HEIGHT - self.GROUND_HEIGHT)},
            'horizontal': {'texture': p.transform.scale(self.GRASS, (self.WIDTH//2, 25)), 'pos': (self.WIDTH/4, self.HEIGHT/2)},
            'vertical1': {'texture': p.transform.scale(self.STONE, (25, (self.HEIGHT//2 - self.GROUND_HEIGHT - 25)//2)), 'pos': (self.WIDTH/2, self.HEIGHT/2 + 25)},
            'vertical2': {'texture': p.transform.scale(self.STONE, (25, (self.HEIGHT//2 - self.GROUND_HEIGHT - 25)//2)), 'pos': (self.WIDTH/2, self.HEIGHT/2 + 25 + (self.HEIGHT//2 - self.GROUND_HEIGHT - 25)//2)}
        }
        return textures
    
    def draw_win(self, finish_time: float):
        win_text = f'Hole out! Time: {finish_time}s'
        draw_text = self.FONT.render(win_text, True, p.Color('black'))
        self.SCREEN.blit(draw_text, (self.WIDTH/2 - draw_text.get_width()/2, self.HEIGHT/2 - draw_text.get_height()/2))
        p.display.update()
        p.time.delay(5000)

    def draw_window(self, power, mouse, button, respawn_text, ball, t, line):
        self.SCREEN.blit(self.BACKGROUND, (0, 0))

        power_text = self.FONT.render(str(int(power)),True,p.Color('white'))
        clock_text = self.FONT.render(f'Time: {str(round(t/1000))}',True,p.Color('white'))
        self.SCREEN.blit(power_text,(120, 13))
        self.SCREEN.blit(clock_text,(self.WIDTH - clock_text.get_width() - 10, 13))

        setting = self.level_setting()
        for i in range(len(setting)):
            p.draw.rect(self.SCREEN, list(setting.values())[i]['color'], list(setting.values())[i]['rect'])
            draw_rect_outline(self.SCREEN, list(setting.values())[i]['rect'], (0,0,0))
        textures = self.textures()
        for j in range(len(textures)):
            self.SCREEN.blit(list(textures.values())[j]['texture'], list(textures.values())[j]['pos'])
        
        for k in range(len(setting)):
            draw_rect_outline(self.SCREEN, list(setting.values())[k]['rect'], (0,0,0))

        if button.collidepoint(mouse[0], mouse[1]):
            p.draw.rect(self.SCREEN, (170,170,170), button)
        else:
            p.draw.rect(self.SCREEN, (100,100,100), button)
        draw_rect_outline(self.SCREEN, p.Rect(self.WIDTH/2 - respawn_text.get_width()/2 - 10, 8, respawn_text.get_width() + 10, respawn_text.get_height() + 5), p.Color('black'))
        self.SCREEN.blit(respawn_text, (self.WIDTH/2 - respawn_text.get_width()/2 - 5,10))

        gradient_rect(self.SCREEN, (0,255,0), (255,0,0), p.Rect(10,10,102,30))
        p.draw.line(self.SCREEN, p.Color('black'), (10 + power*100/self.MAX_POWER,25), (10 + power*100/self.MAX_POWER,55), 4)
        draw_rect_outline(self.SCREEN, p.Rect(10,10,102,30), (0,0,0))

        if math.sqrt((line[1][0] - line[0][0])**2 + (line[1][1] - line[0][1])**2) <= self.MAX_POWER:
            p.draw.line(self.SCREEN, p.Color('black'), line[0], line[1], 2)
        ball.draw()
        p.display.update() 
    
    def main(self):
        end = self.level_setting()['start']['rect']
        start_pos = (end[0] + end[2]/2,end[1] - self.RADIUS)
        ball = Ball(start_pos[0],start_pos[1],self.RADIUS,p.Color('white'), self.SCREEN, self.MAX_POWER)
        respawn_text = self.FONT.render('Respawn',True,p.Color('white'))
        button = p.Rect(self.WIDTH/2 - respawn_text.get_width()/2 - 10, 8, respawn_text.get_width() + 10, respawn_text.get_height() + 5)

        shoot, run = False, True
        clock = p.time.Clock()

        x,y = 0,0
        power, time, angle = 0, 0, 0
        collision = [-1]
        hitbox = p.Rect(ball.x - self.RADIUS, ball.y - self.RADIUS, self.RADIUS*2, self.RADIUS*2)

        while run:
            clock.tick(self.FPS)
            mouse =  p.mouse.get_pos()
            line = [(ball.x,ball.y), mouse]

            if shoot:
                hitbox = p.Rect(ball.x - self.RADIUS, ball.y - self.RADIUS, self.RADIUS*2, self.RADIUS*2)
                setting = [list(self.level_setting().values())[i]['rect'] for i in range(len(self.level_setting())) if list(self.level_setting().keys())[i] not in ['start', 'end']]
                if (collide_object := hitbox.collidelist(setting)) != -1 and collide_object != collision[-1]:
                    collision.append(collide_object)
                    x, y = ball.x, ball.y
                    side = ball.find_side((x, y), setting[collide_object], find_angle((x, y), ball.curve[-1]))
                    power, time, angle = int(power/2.25), 0, angle_reflection(find_angle((x, y), ball.curve[-1]), side)
                    side = None
                elif power < self.MAX_POWER/20 and hitbox.colliderect(setting[collision[-1]]) and collide_object in [0,1]:
                    shoot = False
                elif hitbox.bottom > self.HEIGHT - self.GROUND_HEIGHT:
                    ball.y = self.HEIGHT - self.GROUND_HEIGHT - self.RADIUS
                elif hitbox.left < 4:
                    ball.x = 4 + self.RADIUS
                elif hitbox.right > self.WIDTH - 4:
                    ball.x = self.WIDTH - 4 - self.RADIUS
                elif ball.y < 4:
                    ball.y = 4 + self.RADIUS
                else:
                    time += .125
                    pos = ball.path(x,y,power,angle,time, self.GRAVITY)
                    ball.curve.append((ball.x, ball.y))
                    ball.x, ball.y = pos
                    hitbox = p.Rect(ball.x - self.RADIUS, ball.y - self.RADIUS, self.RADIUS*2, self.RADIUS*2)
                    if collision[-1] != -1:
                        if hitbox.collidelist(setting) != collision[-1]:
                            collision.append(-1)           
            if p.Rect(ball.x - self.RADIUS, ball.y - self.RADIUS, self.RADIUS*2, self.RADIUS*2).clipline(find_outlines(self.level_setting()['end']['rect'])['top']) != ():
                self.draw_win(p.time.get_ticks()/1000)
                run = False
                p.quit()  
            if shoot is False and find_lenght(line) <= self.MAX_POWER:
                power = math.sqrt((line[1][1] - line[0][1])**2 + (line[1][0] - line[0][0])**2)
            self.draw_window(power, mouse, button, respawn_text, ball, p.time.get_ticks(), line)
            p.display.flip()

            for event in p.event.get():
                if event.type == QUIT:
                    run = False
                    p.quit()
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        if shoot is False and find_lenght(line) <= self.MAX_POWER:
                            shoot = True
                            x, y = ball.x, ball.y
                            power, time, angle = math.sqrt((line[1][1] - line[0][1])**2 + (line[1][0] - line[0][0])**2)/2, 0, find_angle((ball.x, ball.y), mouse)
                if event.type == MOUSEBUTTONDOWN:
                    if button.collidepoint(mouse[0], mouse[1]):
                        shoot = False
                        ball.x, ball.y = start_pos
                        power = 0
                        collision = [-1]
if __name__ == '__main__':
    game = GameOne()
    game.main()
