import pygame as pg
import random
import tkinter as tk
from tkinter import messagebox
import sys

class Cube(object):
    rows = 20
    
    def __init__(self, start, dirnx = 1, dirny = 0, color=(255,255,255)):
        self.pos = start
        self.dirnx = dirnx
        self.dirny = dirny
        self.color = color
    
    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)
    
    def draw(self, surface, eyes = False):
        dis = size // rows
        row = self.pos[0]
        col = self.pos[1]
        pg.draw.rect(surface, self.color, (row * dis + 1, col * dis + 1, dis - 2, dis - 2))
        
        if eyes:
            center = dis // 2
            radius = 3
            c_center = (row * dis + center - radius - 2 , col * dis + 8)
            c_center2 = (row * dis + dis - radius * 2, col * dis + 8)
            pg.draw.circle(surface, (0,0,0), c_center, radius)
            pg.draw.circle(surface, (0,0,0), c_center2, radius)

class Snake(object):
    body = []
    turns = {}
    
    def __init__(self,color,pos):
        pg.display.set_caption("Snake")
        self.color = color
        self.head = Cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1
    
    def move(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            
        keys = pg.key.get_pressed()
            
        if keys[pg.K_LEFT]:
            self.dirnx = -1
            self.dirny = 0
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                
        elif keys[pg.K_RIGHT]:
            self.dirnx = 1
            self.dirny = 0
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
            
        elif keys[pg.K_UP]:
            self.dirnx = 0
            self.dirny = -1
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
            
        elif keys[pg.K_DOWN]:
            self.dirnx = 0
            self.dirny = 1
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        
        for index, cube in enumerate(self.body):
            p = cube.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                cube.move(turn[0], turn[1])
                if index == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                if cube.dirnx == -1 and cube.pos[0] <= 0:
                    cube.pos = (cube.rows - 1, cube.pos[1])
                elif cube.dirnx == 1 and cube.pos[0] >= cube.rows - 1:
                    cube.pos = (0, cube.pos[1])
                elif cube.dirny == 1 and cube.pos[1] >= cube.rows - 1:
                    cube.pos = (cube.pos[0], 0)
                elif cube.dirny == -1 and cube.pos[1] <= 0:
                    cube.pos = (cube.pos[0], cube.rows - 1)
                else:
                    cube.move(cube.dirnx, cube.dirny)
        
    
    def reset(self, pos):
        self.head = Cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1
    
    def add_cube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny
        
        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] + 1)))
        
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy
    
    def draw(self, surface):
        for index, cube in enumerate(self.body):
            if index == 0:
                cube.draw(surface, True)
            else:
                cube.draw(surface)

def draw_grid(width,rows, surface):
    """drawing game's grid"""
    size_between = width // rows
    x = 0
    y = 0
    for line in range(rows):
        x += size_between
        y += size_between
        pg.draw.line(surface,(102,102,102),(x, 0),(x,width))
        pg.draw.line(surface,(102,102,102),(0, y),(width,y))

def draw_window(surface):
        surface.fill((140,140,140))
        s.draw(surface)
        apple.draw(surface)
        draw_grid(size, rows, surface)
        pg.display.update()

def random_apple(snake):
    positions = snake.body
    
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break
        
    return (x,y)

def msg_box():
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    res = messagebox.askquestion('You lost!', f'Score: {len(s.body)}\nDo you want to play again?')
    if res.lower() == 'no':
        sys.exit()

    try:
        root.destroy()
    except:
        pass

def main():
    """main function that runs the programme"""
    global size, rows, s, apple
    size = 500
    rows = 20
    
    window = pg.display.set_mode((size, size))
    
    s = Snake((255,255,255),(10,10))
    apple = Cube(random_apple(s), color=(255,0,0))
    
    enable = True #if True, game is running
    clock = pg.time.Clock()
    
    while enable:        
        pg.time.delay(50)
        clock.tick(10)
        s.move()
        if s.body[0].pos == apple.pos:
            s.add_cube()
            apple = Cube(random_apple(s), color=(255,0,0))
        
        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos, s.body[x+1:])):
                print('Score: ', len(s.body))  
                msg_box()
                s.reset((10, 10))
                break
            
        draw_window(window)

main()