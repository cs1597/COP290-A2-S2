# from settings import *
# from sprites import Sprite, Node, Icon
# from groups import WorldSprites

# class Overworld:
#     def __init__(self,tmx_map,data,overworld_frames):
#         self.display_surface = pygame.display.get_surface()
#         self.data = data

#         # groups
#         self.all_sprites = WorldSprites(data) 
#         # self.all_sprites=AllSprites()
#         self.collision_sprites = pygame.sprite.Group()  # make a collision sprite for level interaction
#         # self.item_sprites = pygame.sprite.Group()
#         self.node_sprites = pygame.sprite.Group() # node to display the unlocked levels

#         self.setup(tmx_map,overworld_frames)
#         self.current_node = [node for node in self.node_sprites if node.level == 0][0]
    
#     def setup(self,tmx_map,overworld_frames):
#         for layer in ['BG','Terrain']:
#             for x,y,surf in tmx_map.get_layer_by_name(layer).tiles():
#                 if layer == 'Terrain':
#                     groups = [self.all_sprites,self.collision_sprites]
#                 Sprite((x*TILE_SIZE,y*TILE_SIZE),surf,self.all_sprites,Z_LAYERS['bg tiles'])

#         # for obj in tmx_map.get_layer_by_name('Objects'):
#         #     Sprite((obj.x, obj.y), overworld_frames['point_loc'][0], self.all_sprites, Z_LAYERS['fg'])
#         #paths
#         # self.paths={}
#         # for obj in tmx_map.get_layer_by_name('Paths'):
#         #     pos=[(p.x,p.y) for p in obj.points]
#         #     start = obj.properties['start']
#         #     end  = obj.properties['end']
#         #     self.paths[end]={'pos':pos,'start':start}


#         #nodes and player
#         for obj in tmx_map.get_layer_by_name('Nodes'):
#             if obj.name == 'Node' and obj.properties['stage'] == self.data.current_level:
#                 self.icon = Icon((obj.x+4*TILE_SIZE, obj.y+6*TILE_SIZE), self.all_sprites, overworld_frames['icon'])

#             #nodes
#             if obj.name=='Node':
#                 # available_paths={k:v for k,v in obj.properties.items() if k in ('left','right','up','down')}
#                 # print(available_paths)
#                 Node(
#                 pos=(obj.x,obj.y),
#                 surf_black = overworld_frames['point_loc'][0],
#                 surf = overworld_frames['point_loc'][1],
#                 groups = (self.all_sprites,self.node_sprites),
#                 level=obj.properties['stage'],
#                 data= self.data,
#                 # paths=available_paths
#                 )
    
#     def input(self):
#         keys = pygame.key.get_pressed()
#         if self.current_node:
#             if keys[pygame.K_RIGHT] and self.current_node.can_move('right'):
#                 self.move('right')
#             if keys[pygame.K_LEFT] and self.current_node.can_move('left'):
#                 self.move('left')
#             if keys[pygame.K_UP] and self.current_node.can_move('up'):
#                 self.move('up')
#             if keys[pygame.K_DOWN] and self.current_node.can_move('down'):
#                 self.move('down')
            
#     def move(self,direction):
#         path_key = int(self.current_node.paths[direction])
#         path_reverse = True if self.current_node.paths[direction][-1] =='r' else False
#         path = self.paths[path_key]['pos'][:] if not path_reverse else self.paths[path_key]['pos'][::-1]  
#         self.icon.start_move(path)
    
#     def get_current_node(self):
#         nodes=pygame.sprite.spritecollide(self.icon,self.node_sprites,False)
#         if nodes:
#             self.current_node=nodes[0]

#     def run(self,dt):
#         self.input()
#         self.get_current_node()
#         self.all_sprites.update(dt)
#         self.all_sprites.draw(self.icon.rect.center)

from settings import *
from sprites import Sprite, MovingSprite, AnimatedSprite, Item, ParticleEffectSprite, DamageSprite, Node
from enemies import Gunner, Bullet
from player import Player, OverworldPlayer
from groups import WorldSprites



class Overworld:
    def __init__(self, tmx_map,data, overworld_frames):
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = WorldSprites(data)
        self.data=data
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
            
        # objects    
        # for obj in tmx_map.get_layer_by_name('Objects').objects:
        #     print(obj)
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
        
    def item_collision(self):
        if self.item_sprites:
            item_sprites = pygame.sprite.spritecollide(self.player, self.item_sprites, True)
            # True means sprite will be destroyed after collision
            if item_sprites:
                ParticleEffectSprite((item_sprites[0].rect.center), self.particle_frames['particle'], self.all_sprites)
                
    def run(self, dt):
        self.display_surface.fill((70,100,99))
        self.all_sprites.update(dt)
        self.item_collision()
        self.all_sprites.draw(self.player.hitbox_rect.center)