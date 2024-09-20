import math
import pygame as p

class Ball:
    def __init__(self, x, y, radius, color, screen, max_power):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.screen = screen
        self.max_power = max_power
        self.curve = []
    
    def draw(self):
        p.draw.circle(self.screen, p.Color('gray'), (self.x,self.y), self.max_power, 1)
        p.draw.circle(self.screen, self.color, (self.x,self.y), self.radius)
        p.draw.circle(self.screen, p.Color('black'), (self.x,self.y), self.radius,1)
    
    def find_side(self, pos, rect, angle):
        x,y,w,h = rect
        side = None
        sections = {
            'top': p.Rect(x, y - self.radius - 2, w, self.radius + 2), 'bottom': p.Rect(x, y + h, w, self.radius + 2),
            'left': p.Rect(x - self.radius - 2, y, self.radius + 2, h), 'right': p.Rect(x + w, y, self.radius + 2, h)
        }
        for i in range(len(sections)):
            if list(sections.values())[i].collidepoint(pos):
                side = list(sections.keys())[i]
                break
        if angle in [0, 2*math.pi]:
            side = 'right'
        return side
    
    @staticmethod
    def path(startx, starty, power, angle, time, gravity):
        velx = math.cos(angle)*power
        vely = math.sin(angle)*power

        dx = velx * time
        dy = (vely*time) + ((gravity*time**2)/2)

        nx = round(dx + startx)
        ny = round(starty - dy)
        return (nx,ny)
    
def find_angle(pos1, pos2):
    x, y = pos1
    try:
        angle = math.atan((y - pos2[1])/(x - pos2[0]))
    except:
        angle = math.pi / 2
    if pos2[1] < y and pos2[0] > x:
        angle = abs(angle)
    elif pos2[1] < y and pos2[0] < x:
        angle = math.pi - angle
    elif pos2[1] > y and pos2[0] < x:
        angle = math.pi + abs(angle)
    elif pos2[1] > y and pos2[0] > x:
        angle = math.pi*2 - angle
    return angle

def angle_reflection(angle, side):
    if side is not None:
        if 0 <= angle <= math.pi/2:
            if side in ['right', 'left']:
                if angle != 0:
                    angle = 2*math.pi - angle
                else:
                    angle = math.pi
            else:
                if angle < math.pi/2:
                    angle = math.pi/2 + (math.pi/2 - angle)
                else:
                    angles = {'top': math.pi/2, 'bottom': -math.pi/2}
                    angle = angles[side]
        elif math.pi/2 < angle <= math.pi:
            if side in ['right', 'left']:
                angle = math.pi + (math.pi - angle)
            else:
                angle = math.pi/2 - (angle - math.pi/2)
        elif math.pi < angle <= 3*math.pi/2:
            if side in ['top', 'bottom']:
                angle = 3*math.pi/2 + (3*math.pi/2 - angle)
            else:
                angle = math.pi - (angle - math.pi)
        elif 3*math.pi/2 < angle <= 2*math.pi:
            if side in ['top', 'bottom']:
                angle = 3*math.pi/2 - (angle - 3*math.pi/2)
            else:
                angle = 0 + (2*math.pi - angle)
    return angle

def find_lenght(line):
    return math.sqrt((line[1][0] - line[0][0])**2 + (line[1][1] - line[0][1])**2)

def moving_obstacle(rect, speed, distance, loop, *directions):
    progress = {}
    rect_list = [*rect]
    for i in range(int(distance/speed)):
        if i <= int(distance/speed)//2:
            for direction in directions:
                rect_list[direction] = rect_list[direction] + loop*speed
            progress[i] = p.Rect(*(rect_list))
        if i > int(distance/speed)//2:
            for direction in directions:
                rect_list[direction] = rect_list[direction] + (-loop)*speed
            progress[i] = p.Rect(*(rect_list))         
    return progress

def gradient_rect(window, left_colour, right_colour, target_rect):
    colour_rect = p.Surface((2, 2))
    p.draw.line(colour_rect, left_colour, (0,0), (0,1))
    p.draw.line(colour_rect, right_colour, (1,0), (1,1))
    colour_rect = p.transform.smoothscale(colour_rect,(target_rect.width,target_rect.height))
    window.blit(colour_rect, target_rect)   

def draw_rect_outline(surface, rect, color, width=1):
    x, y, w, h = rect
    width = max(width, 1)
    width = min(min(width, w//2), h//2)
    for i in range(width):
        p.gfxdraw.rectangle(surface, (x+i, y+i, w-i*2, h-i*2), color)

def find_outlines(rect):
    x,y,w,h = rect
    outlines = {
        'top':[(x,y),(x + w,y)], 'bottom':[(x,y+h),(x + w,y+h)],
        'left':[(x,y),(x,y+h)], 'right':[(x + w,y),(x + w,y+h)]
    }   
    return outlines