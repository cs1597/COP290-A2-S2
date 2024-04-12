from settings import *
from sprites import Sprite, MovingSprite, AnimatedSprite, Item, ParticleEffectSprite, DamageSprite
from enemies import Gunner, Bullet
from player import Player
from groups import AllSprites

class Level:
    def __init__(self, tmx_map, level_frames):
        self.display_surface = pygame.display.get_surface()
        
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.semicollision_sprites = pygame.sprite.Group()
        self.item_sprites = pygame.sprite.Group()
        self.damage_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        
        self.setup(tmx_map, level_frames)
        
        self.particle_frames = level_frames['effects']
        self.bullet_frames = level_frames['bullet'][0]
       
    def setup(self, tmx_map, level_frames):   
        # tiles
        for layer in ['BG', 'Terrain', 'FG', 'Platforms', 'Backdrop']:
            for x,y,surf in tmx_map.get_layer_by_name(layer).tiles():
                groups = [self.all_sprites]
                if layer == 'Terrain' :
                    groups.append(self.collision_sprites)
                if layer == 'Platforms':
                    groups.append(self.semicollision_sprites)
                match layer:
                    case 'BG': z = Z_LAYERS['bg tiles']
                    case 'FG': z = Z_LAYERS['fg']
                    case 'Backdrop': z = Z_LAYERS['bg']
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
            # traps and other objects
            else:
                frames = level_frames[obj.name]
                if obj.properties['flip']:
                    frames = [pygame.transform.flip(frame, False, True) for frame in frames]
                DamageSprite((obj.x, obj.y), (obj.properties['damage_width'], obj.properties['damage_height']), frames, (self.all_sprites, self.damage_sprites))
                
        # items
        for obj in tmx_map.get_layer_by_name('Items'):
            Item(obj.name, (obj.x + TILE_SIZE/2, obj.y + TILE_SIZE/2), level_frames['items'][obj.name], (self.all_sprites, self.item_sprites))
        
        # moving objects
        for obj in tmx_map.get_layer_by_name('Moving Objects'):
            frames = level_frames[obj.name]
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
                MovingSprite(frames, (self.all_sprites, self.semicollision_sprites), start_pos, end_pos, move_dir, speed, obj.properties['flip'])
    
            if obj.name == 'boat':
                speed = obj.properties['speed']
                start_pos = (obj.x, obj.y + obj.height // 2)
                end_pos = (obj.x + obj.width, obj.y + obj.height // 2)
                MovingSprite(frames, (self.all_sprites, self.collision_sprites), start_pos, end_pos, 'x', speed, obj.properties['flip'])
    
        for obj in tmx_map.get_layer_by_name('Enemies'):
            frames = level_frames[obj.name]
            if obj.name == 'gunner':
                if obj.properties['direction'] == 'left':
                    frames = [pygame.transform.flip(frame, True, False) for frame in frames]
                Gunner((obj.x, obj.y), frames, (self.all_sprites), self.create_bullet, obj.properties['direction'], obj.properties['speed'])
    
    def create_bullet(self, pos, direction, speed):
       Bullet(pos, (self.all_sprites, self.damage_sprites, self.bullet_sprites), self.bullet_frames, direction, speed, self.collision_sprites, self.player) 
    
    def hit_collision(self):
        damage_rects = [sprite.damagebox for sprite in self.damage_sprites]
        if self.player.hitbox_rect.collidelist(damage_rects) >=0 :
            self.player.hit()
    
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
        self.hit_collision()
        self.all_sprites.draw(self.player.hitbox_rect.center)