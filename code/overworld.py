from settings import *
from sprites import Sprite, MovingSprite, AnimatedSprite, Item, ParticleEffectSprite, DamageSprite, Node
from enemies import Gunner, Bullet
from player import Player, OverworldPlayer
from groups import WorldSprites

class Overworld:
    def __init__(self, tmx_map, overworld_frames, data, switch_stage):
        self.display_surface = pygame.display.get_surface()
        self.data=data
        self.switch_stage = switch_stage
        
        self.level_width = tmx_map.width * TILE_SIZE
        self.level_bottom = tmx_map.height * TILE_SIZE
        self.all_sprites = WorldSprites(data, tmx_map.width, tmx_map.height)
        self.collision_sprites = pygame.sprite.Group()
        self.item_sprites = pygame.sprite.Group()
        self.node_sprites = pygame.sprite.Group()
        self.setup(tmx_map, overworld_frames)
        self.current_node = [node for node in self.node_sprites if node.level == 0][0]

    def setup(self, tmx_map, overworld_frames):
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
            
        for obj in tmx_map.get_layer_by_name('Objects'):
            if obj.name == 'player':
                self.player = OverworldPlayer(
                    pos = (obj.x, obj.y), 
                    groups = self.all_sprites, 
                    collision_sprites = self.collision_sprites, 
                    frames = overworld_frames['icon'])
            elif obj.name == 'Node':
                Node(
                    pos=(obj.x,obj.y),
                    surf_black = overworld_frames['point_loc'][0], # forlocked level
                    surf = overworld_frames['point_loc'][1], # for unlocked level
                    groups = (self.all_sprites,self.node_sprites), 
                    level=obj.properties['stage'], # stage number
                    data= self.data, 
                )
                
    def input(self, level):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            self.data.current_level = level
            self.switch_stage('level')            
                
    def level_collision(self):
        for target in self.node_sprites.sprites():
            if target.rect.colliderect(self.player.rect) and self.data.unlocked_level >= target.level and target.level!=0:
                self.input(target.level)
                        
    def item_collision(self):
        if self.item_sprites:
            item_sprites = pygame.sprite.spritecollide(self.player, self.item_sprites, True)
            # True means sprite will be destroyed after collision
            if item_sprites:
                ParticleEffectSprite((item_sprites[0].rect.center), self.particle_frames['particle'], self.all_sprites)
                
    def run(self, dt):
        # self.display_surface.fill((70,100,99))
        self.all_sprites.update(dt)
        self.item_collision()
        self.level_collision()
        self.all_sprites.draw(self.player.hitbox_rect.center)