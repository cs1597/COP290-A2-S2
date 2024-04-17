from settings import *

class WorldSprites(pygame.sprite.Group):
    def __init__(self,data):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.data = data
        self.offset = vector(0, 0)
    def draw(self,target_pos):
        self.offset.x=-(target_pos[0]-WINDOW_WIDTH/2)
        self.offset.y=-(target_pos[1]-WINDOW_HEIGHT/2)
        for sprite in sorted(self,key=lambda sprite:sprite.z):
            if sprite.z ==Z_LAYERS['path']:
                if sprite.level<=self.data.unlocked_level:
                    self.display_surface.blit(sprite.image,sprite.rect.center+self.offset)
                else:
                    self.display_surface.blit(sprite.image_black,sprite.rect.center+self.offset)
            else:
                self.display_surface.blit(sprite.image,sprite.rect.topleft+self.offset)
            

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = vector(0,0)
    
    def draw(self, target_pos):
        self.offset.x = -(target_pos[0] - WINDOW_WIDTH / 2)
        self.offset.y = -(target_pos[1] - WINDOW_HEIGHT / 2)
        for sprite in sorted(self, key=lambda x: x.z):
            offset_position = sprite.rect.topleft + self.offset
            self.display_surface.blit(sprite.image, offset_position)