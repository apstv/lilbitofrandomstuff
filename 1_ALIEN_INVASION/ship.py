import pygame as pg
from pygame.sprite import Sprite

class Ship:
    """class intended to mangaging our spaceturtle"""
    def __init__(self,ai_game):
        """initializing a ship and its initial position"""
        super().__init__()
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        
        #loading the image of spaceturtle and getting its rectangle
        self.image = pg.image.load('images/turtle.png')
        self.rect = self.image.get_rect()
        
        #every new turtle appears in the bottom of the screen 
        self.rect.midbottom = self.screen_rect.midbottom
        
        #horizontal position is stored as a floating point
        self.x = float(self.rect.x) 
        
        #options indicating that our ship moves
        self.moving_right = False
        self.moving_left = False
        
    def update(self):
        """updating ship's location, basing on the option indicating movement"""
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
                   
        #updating 'rect' basing on 'self.x' value
        self.rect.x = self.x
            
    def blitme(self):
        """displaying spaceship in its current location"""
        self.screen.blit(self.image,self.rect)
    
    def center_ship(self):
        """placing a ship in the middle bottom screen"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)