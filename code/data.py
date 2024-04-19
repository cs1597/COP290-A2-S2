class Data:
    def __init__(self, ui):
        self._coins = 0
        self._health = 5
        self._level_health = 3
        self._diamonds = 0
        self.ui = ui
        self.unlocked_level = 1
        self.current_level = 1
        
    @property
    def health(self):
        return self._health
    
    @property
    def level_health(self):
        return self._level_health
    
    @property
    def coins(self):
        return self._coins
    
    @property
    def diamonds(self):
        return self._diamonds
    
    @health.setter
    def health(self,value):
        self._health = value
        self.ui.create_hearts(self._health)
    
    @level_health.setter
    def level_health(self,value):
        self._level_health = value
        self.ui.create_hearts(self._level_health)
        
    @coins.setter
    def coins(self,value):
        self._coins = value
        
    @diamonds.setter
    def diamonds(self,value):
        self._diamonds = value