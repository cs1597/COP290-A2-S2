from settings import *
from sprites import Sprite, MovingSprite
from player import Player
from groups import AllSprites

class Level:
    def __init__(self, tmx_map):
        self.display_surface = pygame.display.get_surface()
        
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.semicollision_sprites = pygame.sprite.Group()
        
        self.setup(tmx_map)
        
    def setup(self, tmx_map):   
        # tiles
        for layer in ['BG', 'Terrain', 'FG', 'Platforms']:
            for x,y,surf in tmx_map.get_layer_by_name(layer).tiles():
                groups = [self.all_sprites]
                if layer == 'Terrain' :
                    groups.append(self.collision_sprites)
                if layer == 'Platforms':
                    groups.append(self.semicollision_sprites)
                match layer:
                    case 'BG': z = Z_LAYERS['bg tiles']
                    case 'FG': z = Z_LAYERS['fg']
                    case _ : z = Z_LAYERS['main']   
                Sprite((x* TILE_SIZE, y * TILE_SIZE), surf, groups, z)
            
        # objects    
        for obj in tmx_map.get_layer_by_name('Objects'):
            if obj.name == 'player':
                print(obj.name, obj.width, obj.height)
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites, self.semicollision_sprites)
            else:
                print(obj.name, obj.width, obj.height)
                Sprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))
        
        # moving objects
        # for obj in tmx_map.get_layer_by_name('Moving Objects'):
        #     if obj.name == 'helicopter':
        #         if obj.width > obj.height:
        #             move_dir='x'
        #             start_pos = (obj.x, obj.y + obj.height / 2)
        #             end_pos = (obj.x + obj.width, obj.y + obj.height / 2)
        #         else:
        #             move_dir = 'y'
        #             start_pos = (obj.x + obj.width / 2, obj.y)
        #             end_pos = (obj.x + obj.width / 2, obj.y + obj.height) 
        #         speed = obj.properties['speed']
        #         MovingSprite((self.all_sprites, self.semicollision_sprites), start_pos, end_pos, move_dir, speed)
        
    def run(self, dt):
        self.all_sprites.update(dt)
        self.display_surface.fill('black')
        self.all_sprites.draw(self.player.hitbox_rect.center)