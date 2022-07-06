import pygame as pg
from pygame.sprite import Sprite

class Alien(Sprite):
    """class that represents single alien in the fleet"""
    def __init__(self, ai_game_):
        """initializing alien and defining its initial position"""
        super().__init__()
        self.screen = ai_game_.screen
        self.settings = ai_game_.settings
        
        #loading image and defining its rectangle
        self.image = pg.image.load('images/green_oct.png')
        self.rect = self.image.get_rect()
        
        #placing new alien in the upper left corner
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        #storing alien's exact horizontal position
        self.x = float(self.rect.x)
    
    def check_edges(self):
        """returns 'true' if alien touches the edge of the screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
    
    def update(self):
        """moving alien to the right or left"""
        self.x += (self.settings.alien_speed*self.settings.fleet_direction)
        self.rect.x = self.x