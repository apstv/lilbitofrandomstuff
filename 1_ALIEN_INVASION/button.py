import pygame.font

class Button():
    def __init__(self, ai_game, msg):
        """initialization button's attributes"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        
        #defining size and attributes of a button
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        
        #creating button's rectangle and centering it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        
        self._prep_msg(msg)
    
    def _prep_msg(self,msg):
        """placing a message and centering it on a button"""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
    
    def draw_button(self):
        """displaying an empty button and a message on it"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)