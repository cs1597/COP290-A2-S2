from settings import *
from sprites import Sprite, MovingSprite, AnimatedSprite, Item, ParticleEffectSprite
from player import Player
from groups import AllSprites

class Level:
    def __init__(self, tmx_map, level_frames):
        self.display_surface = pygame.display.get_surface()
        
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.semicollision_sprites = pygame.sprite.Group()
        self.item_sprites = pygame.sprite.Group()
        
        self.setup(tmx_map, level_frames)
        
        self.particle_frames = level_frames['effects']
        
    def setup(self, tmx_map, level_frames):   
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
                self.player = Player(
                    pos = (obj.x, obj.y), 
                    groups = self.all_sprites, 
                    collision_sprites = self.collision_sprites, 
                    semicollision_sprites = self.semicollision_sprites,
                    frames = level_frames['player'])
            else:
                print(obj.name, obj.width, obj.height)
                Sprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))
                
        # items
        for obj in tmx_map.get_layer_by_name('Items'):
            Item(obj.name, (obj.x + TILE_SIZE/2, obj.y + TILE_SIZE/2), level_frames['items'][obj.name], (self.all_sprites, self.item_sprites))
        
        # moving objects
        for obj in tmx_map.get_layer_by_name('Moving Objects'):
            if obj.name == 'helicopter':
                if obj.width > obj.height:
                    move_dir='x'
                    start_pos = (obj.x, obj.y + obj.height // 2)
                    end_pos = (obj.x + obj.width, obj.y + obj.height // 2)
                else:
                    move_dir = 'y'
                    start_pos = (obj.x + obj.width // 2, obj.y)
                    end_pos = (obj.x + obj.width // 2, obj.y + obj.height) 
                speed = obj.properties['speed']
                MovingSprite((self.all_sprites, self.semicollision_sprites), start_pos, end_pos, move_dir, speed)
    
    def item_collision(self):
        if self.item_sprites:
            item_sprites = pygame.sprite.spritecollide(self.player, self.item_sprites, True)
            # True means sprite will be destroyed after collision
            if item_sprites:
                ParticleEffectSprite((item_sprites[0].rect.center), self.particle_frames['particle'], self.all_sprites)
        
    def run(self, dt):
        self.display_surface.fill('black')
        
        self.all_sprites.update(dt)
        self.item_collision()
        self.all_sprites.draw(self.player.hitbox_rect.center)