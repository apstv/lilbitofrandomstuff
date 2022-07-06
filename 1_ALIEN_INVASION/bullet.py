import pygame as pg
from pygame.sprite import Sprite

class Bullet(Sprite):
    """class intended to managing turtle's bullets"""
    def __init__(self,ai_game):
        """creating bullet objcet in the current ship's position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color
        
        #creating bullet's rectangle in the position (0,0), then defining its own position
        self.rect = pg.Rect(0,0,self.settings.bullet_width,self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop
        
        #bullet's position is defined with a floating point value
        self.y = float(self.rect.y)
        
    def update(self):
        """moving a bullet on the screen"""
        #udpating bullet's position
        self.y -= self.settings.bullet_speed
        #updating bullet's rectangle's position
        self.rect.y = self.y
    
    def draw_bullet(self):
        """displaying bullet on the screen"""
        pg.draw.rect(self.screen,self.color,self.rect)