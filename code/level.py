from settings import *
from sprites import Sprite, MovingSprite, AnimatedSprite, Item, ParticleEffectSprite, DamageSprite
from enemies import Gunner, Bullet
from player import Player, MazePlayer
from groups import AllSprites

class Level:
    def __init__(self, tmx_map, level_frames, data):
        self.display_surface = pygame.display.get_surface()
        self.data = data
        
        self.level_width = tmx_map.width * TILE_SIZE
        self.level_bottom = tmx_map.height * TILE_SIZE
        self.all_sprites = AllSprites(tmx_map.width, tmx_map.height)
        self.collision_sprites = pygame.sprite.Group()
        self.semicollision_sprites = pygame.sprite.Group()
        self.item_sprites = pygame.sprite.Group()
        self.damage_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        
        self.setup(tmx_map, level_frames)
        
        self.particle_frames = level_frames['effects']
        self.bullet_frames = level_frames['bullet'][0]
       
    def setup(self, tmx_map, level_frames):   
        # tiles
        for layer in ['BG', 'Terrain', 'FG', 'Platforms', 'Backdrop', 'FG_2']:
            for x,y,surf in tmx_map.get_layer_by_name(layer).tiles():
                groups = [self.all_sprites]
                if layer == 'Terrain' :
                    groups.append(self.collision_sprites)
                if layer == 'Platforms':
                    groups.append(self.semicollision_sprites)
                match layer:
                    case 'FG_2': z = Z_LAYERS['fg_2']
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
                    frames = level_frames['player'],
                    data = self.data)
            # traps and other objects
            elif obj.name =='elephant':
                frames = level_frames[obj.name]
                AnimatedSprite((obj.x, obj.y), frames, (self.all_sprites))
                self.level_finish_rect = pygame.Rect((obj.x, obj.y), (obj.width, obj.height))
            elif obj.name =='penguin':
                frames = level_frames[obj.name]
                AnimatedSprite((obj.x, obj.y), frames, (self.all_sprites))
                self.level_finish_rect = pygame.Rect((obj.x, obj.y), (obj.width, obj.height))
            else:
                frames = level_frames[obj.name]
                if obj.properties['flip']:
                    frames = [pygame.transform.flip(frame, False, True) for frame in frames]
                DamageSprite((obj.x, obj.y), (obj.properties['damage_width'], obj.properties['damage_height']), frames, (self.all_sprites, self.damage_sprites), obj.properties['flip'])
                
        # items
        for obj in tmx_map.get_layer_by_name('Items'):
            Item(obj.name, (obj.x + TILE_SIZE/2, obj.y + TILE_SIZE/2), level_frames['items'][obj.name], (self.all_sprites, self.item_sprites), self.data)
        
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
                # if obj.properties['direction'] == 'left':
                    # frames = [pygame.transform.flip(frame, True, False) for frame in frames]
                Gunner((obj.x, obj.y), frames, (self.all_sprites, self.enemy_sprites), self.create_bullet, obj.properties['direction'], obj.properties['speed'], self.player)
        
    def create_bullet(self, pos, direction, speed):
       Bullet(pos, (self.all_sprites, self.bullet_sprites), self.bullet_frames, direction, speed, self.collision_sprites, self.player) 
    
    def hit_collision(self):
        damage_rects = [sprite.damagebox for sprite in self.damage_sprites]
        if self.player.hitbox_rect.collidelist(damage_rects) >=0 :
            self.player.hit()
    
    def item_collision(self):
        if self.item_sprites:
            item_sprites = pygame.sprite.spritecollide(self.player, self.item_sprites, True)
            if item_sprites:
                item_sprites[0].activate()
                ParticleEffectSprite((item_sprites[0].rect.center), self.particle_frames['particle'], self.all_sprites)
        
    def attack_collision(self):
        # if not self.player.timers['attack_lock'].active:
            for target in self.enemy_sprites.sprites():
                facing_target = self.player.rect.centerx<target.rect.centerx and self.player.facing_right or (self.player.rect.centerx>target.rect.centerx and not self.player.facing_right)
                if target.rect.colliderect(self.player.rect) and self.player.attacking and facing_target:
                    target.hit()
                
        
    def check_constraint(self):
        if self.player.hitbox_rect.left<=0:
            self.player.hitbox_rect.left = 0
        if self.player.hitbox_rect.right>=self.level_width:
            self.player.hitbox_rect.right = self.level_width
            
        if self.player.hitbox_rect.bottom > self.level_bottom:
            print('deafs')
            
        if self.player.hitbox_rect.colliderect(self.level_finish_rect):
            print("lessgo")
            
        
    def run(self, dt):
        self.display_surface.fill('black')
        
        self.all_sprites.update(dt)
        self.item_collision()
        self.attack_collision()
        self.hit_collision()
        self.check_constraint()
        
        self.all_sprites.draw(self.player.hitbox_rect.center)
        
        
class MazeLevel:
    def __init__(self, tmx_map, level_frames):
        self.display_surface = pygame.display.get_surface()
        
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.item_sprites = pygame.sprite.Group()
        
        self.setup(tmx_map, level_frames)

    def setup(self, tmx_map, level_frames):
        for layer in ['BG', 'Terrain', 'FG']:
            for x,y,surf in tmx_map.get_layer_by_name(layer).tiles():
                groups = [self.all_sprites]
                if layer == 'Terrain' :
                    groups.append(self.collision_sprites)
                match layer:
                    case 'BG': z = Z_LAYERS['bg tiles']
                    case 'FG': z = Z_LAYERS['fg']
                    case _ : z = Z_LAYERS['main']   
                Sprite((x* TILE_SIZE, y * TILE_SIZE), surf, groups, z)
            
        # objects    
        # for obj in tmx_map.get_layer_by_name('Objects').objects:
        #     print(obj)
        for obj in tmx_map.get_layer_by_name('Objects'):
            if obj.name == 'player':
                self.player = MazePlayer(
                    pos = (obj.x, obj.y), 
                    groups = self.all_sprites, 
                    collision_sprites = self.collision_sprites, 
                    frames = level_frames['maze_player'])
            elif obj.name == 'bush':
                pass
                
        # items
        for obj in tmx_map.get_layer_by_name('Items'):
            Item(obj.name, (obj.x + TILE_SIZE/2, obj.y + TILE_SIZE/2), level_frames['items'][obj.name], (self.all_sprites, self.item_sprites))
        
    def item_collision(self):
        if self.item_sprites:
            item_sprites = pygame.sprite.spritecollide(self.player, self.item_sprites, True)
            # True means sprite will be destroyed after collision
            if item_sprites:
                ParticleEffectSprite((item_sprites[0].rect.center), self.particle_frames['particle'], self.all_sprites)
                
    def check_constraint(self):
        if self.player.hitbox_rect.left<=0:
            self.player.hitbox_rect.left = 0 
        if self.player.hitbox_rect.right>=self.level_width:
            self.player.hitbox_rect.right = self.level_width
            
        # if self.player.hitbox_rect.bottom > self.level_bottom:
            
                
    def run(self, dt):
        self.display_surface.fill((70,100,99))
        
        self.all_sprites.update(dt)
        self.item_collision()
        self.check_constraint()
        self.all_sprites.draw(self.player.hitbox_rect.center)