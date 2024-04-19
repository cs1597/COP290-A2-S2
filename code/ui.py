from settings import *
from sprites import Sprite, AnimatedSprite
from timer import Timer

class UI:
    def __init__(self, font, frames):
        self.display_surface = pygame.display.get_surface()
        self.sprites = pygame.sprite.Group()
        self.font = font
        
        self.heart_frames = frames['heart']
        self.heart_width = self.heart_frames[0].get_width()
        self.heart_padding = 10
        self.create_hearts(5)
        
    def create_hearts(self, num):
        for sprite in self.sprites:
            sprite.kill()
        for heart in range(num):
            x = 10 + heart * (self.heart_width + self.heart_padding)
            y = 10
            Heart((x,y), self.heart_frames, self.sprites)
    
    def update(self, dt):
        self.sprites.update(dt)
        self.sprites.draw(self.display_surface)
            
class Heart(AnimatedSprite):
    def __init__(self,pos,frames,groups):
        super().__init__(pos,frames,groups)