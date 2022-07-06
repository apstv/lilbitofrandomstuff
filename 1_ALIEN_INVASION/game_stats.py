class GameStats:
    """monitoring statistics in Alien Invasion"""
    def __init__(self,ai_game):
        """initializing statistics"""
        self.settings = ai_game.settings
        self.reset_stats()
        self.game_active = False
        #best result, that will never be resetted
        self.high_score = 0
    
    def reset_stats(self):
        """initializing statistics that can be changed during the game"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 0