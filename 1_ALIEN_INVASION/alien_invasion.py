"""In game 'Aliens' Invasion' you control a spaceship"""

import sys
from time import sleep

import pygame as pg

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    """general class, intended to managing resources and the way of running our game"""
    def __init__(self):
        """initializing a game and creating its resources"""
        pg.init()
        self.settings = Settings()
        
        #this part is for fullscreen mode
        # self.screen = pg.display.set_mode((0,0),pg.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height
        
        self.screen = pg.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pg.display.set_caption("Alien Invasion")
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pg.sprite.Group()
        self.aliens = pg.sprite.Group()
        self._create_fleet()
        self.play_button = Button(self, "Play")

    def run_game(self):
        """starting main game loop"""
        while True:
            #waiting for player to press any key or click a mouse
            self._check_events()
            
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            
            self._update_screen()
            
    def _check_events(self):
        """reaction to events generated with keyboard and mouse"""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            elif event.type == pg.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pg.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                self._check_play_button(mouse_pos)
    
    def _check_play_button(self, mouse_pos):
        """starting new game after clicking play button by user"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.settings.initialize_dynamic_settings()
            #resetting game statistics
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            
            #deleting content of alien's and bullets' lists
            self.aliens.empty()
            self.bullets.empty()
            
            #creating new fleet and centering the ship
            self._create_fleet()
            self.ship.center_ship()
            
            #hiding a cursor
            pg.mouse.set_visible(False)
                                
    def _check_keydown_events(self,event):
        """reaction to pressing a key"""
        if event.key == pg.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pg.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pg.K_q:
            sys.exit()
        elif event.key == pg.K_SPACE:
            self._fire_bullet()
    
    def _check_keyup_events(self,event):
        """reaction to releasing a key"""
        if event.key == pg.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pg.K_LEFT:
            self.ship.moving_left = False 
    
    def _fire_bullet(self):
        """creating new bullet and adding it to bullet group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)      
    
    def _update_bullets(self):
        """updating bullets' position and removing invisible ones"""
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()
        
    def _check_bullet_alien_collisions(self):
        """reaction to collision between bullet and alien"""
        collisions = pg.sprite.groupcollide(self.bullets,self.aliens,True,True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()
    
    def _create_fleet(self):
        """creating full fleet of aliens"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2*alien_width)
        number_aliens_x = available_space_x // (2*alien_width)
        
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3*alien_height) - ship_height)
        number_rows = available_space_y // (2*alien_height)
        
        # creating aliens' fleet
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                #creating alien and placing it in a row
                self._create_alien(alien_number, row_number)
    
    def _create_alien(self,alien_number,row_number):
        """creating alien and placing it in a row"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2*alien_width*alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2*alien.rect.height*row_number 
        self.aliens.add(alien)
    
    def _check_fleet_edges(self):
        """proper reaction, when alien touches the edge of the screen"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        """moving all fleet down and changing its direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
    
    def _update_aliens(self):
        """checking if fleet touches the edge of the screen and tehn updating all aliens' position"""
        self._check_fleet_edges()
        self.aliens.update()
        if pg.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()
        
        if pg.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()
            
        self._check_aliens_bottom
    
    def _update_screen(self):
        """updating screen and going to the next one"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        
        self.sb.show_score()
        
        #displaying button only when game is disabled
        if not self.stats.game_active:
            self.play_button.draw_button()
            
        pg.display.flip()
        
    def _ship_hit(self):
        """reaction to ship being hit by an alien"""
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()
            sleep(0.5)
        else:
            self.stats.game_active = False
            pg.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """checking if any alien reached the bottom of the screen"""    #to fix, game doesn't react when alien touches the bottom
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

            
if __name__ == '__main__':
    #creating game element and launching it
    ai = AlienInvasion()
    ai.run_game()