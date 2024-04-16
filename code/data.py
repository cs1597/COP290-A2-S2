class Data:
    def __init__(self, ui):
        self.coins = 0
        self._health = 5
        self.ui = ui
        
    @property
    def health(self):
        return self._health
    
    @health.setter
    def health(self,value):
        self._health = value
        self.ui.create_hearts(self._health)