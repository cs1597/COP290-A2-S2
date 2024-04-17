from pygame import Surface
from settings import ANIMATION_SPEED, Z_LAYERS
from settings import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf = pygame.Surface((TILE_SIZE, TILE_SIZE)), groups = None, z = Z_LAYERS['main']):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.old_rect = self.rect.copy()
        self.z = z
        
class AnimatedSprite(Sprite):
    def __init__(self, pos, frames, groups, z=Z_LAYERS['main'], animation_speed =  ANIMATION_SPEED):
        self.frames, self.frame_index = frames, 0
        super().__init__(pos, self.frames[self.frame_index], groups, z)
        self.animation_speed = animation_speed
        
    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        self.image = self.frames[int(self.frame_index) % len(self.frames)]
    
    def update(self, dt):
        self.animate(dt)
        
class Item(AnimatedSprite):
    def __init__(self, item_type, pos, frames, groups):
        super().__init__(pos, frames, groups)
        self.rect.center = pos
        self.item_type = item_type
        
class ParticleEffectSprite(AnimatedSprite):
    def __init__(self, pos, frames, groups):
        super().__init__(pos, frames, groups)
        self.rect.center =  pos
        self.z = Z_LAYERS['fg']
        
    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.kill()
            
class DamageSprite(AnimatedSprite):
    def __init__(self, pos, damagebox, frames, groups, flipped):
        super().__init__(pos, frames, groups)
        if flipped:
            self.damagebox = pygame.Rect(self.rect.topleft, damagebox)
        else:
            self.damagebox = pygame.Rect(self.rect.bottomleft, damagebox)    
            
                    
class MovingSprite(AnimatedSprite):
    def __init__(self, frames, groups, start_pos, end_pos, move_dir, speed, flip = False): 
        super().__init__(start_pos, frames, groups)
        if move_dir == 'x':
            self.rect.midleft = start_pos
        else:
            self.rect.midtop = start_pos
        self.start_pos = start_pos 
        self.end_pos = end_pos
        
        self.moving = True
        self.speed = speed
        self.flip = flip
        self.direction = vector(1,0) if move_dir == 'x' else vector(0,1)
        self.move_dir = move_dir
        self.rev = {'x': False, 'y': False}
    
    def check_border(self):
        if self.move_dir=='x':
            if self.rect.right >= self.end_pos[0] and self.direction.x==1:
                self.direction.x = -1
                self.rect.right = self.end_pos[0]
            if self.rect.left <= self.start_pos[0] and self.direction.x==-1:
                self.direction.x = 1
                self.rect.left = self.start_pos[0]
            self.rev['x'] = self.direction.x < 0
        else:
            if self.rect.bottom >= self.end_pos[1] and self.direction.y==1:
                self.direction.y = -1
                self.rect.bottom = self.end_pos[1]
            if self.rect.top <= self.start_pos[1] and self.direction.y==-1:
                self.direction.y = 1
                self.rect.top = self.start_pos[1]
            self.rev['y'] = self.direction.y < 0
                
    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.rect.topleft += self.direction * self.speed * dt
        self.check_border()
        
        self.animate(dt)
        if self.flip:
            self.image = pygame.transform.flip(self.image, self.rev['x'], self.rev['y'])

class Node(pygame.sprite.Sprite):
    def __init__(self,pos,surf_black,surf,groups,level,data):
        super().__init__(groups)
        self.image = surf
        self.image_black = surf_black
        self.rect = self.image.get_rect(center=(pos[0]+TILE_SIZE/2,pos[1]+TILE_SIZE/2))
        self.z=Z_LAYERS['path']
        self.level=level
        self.data=data
        # self.paths=paths
    
    # def can_move(self,direction):
    #     if direction in list(self.paths.keys()):
    #         return True

class Icon(pygame.sprite.Sprite):
    def __init__(self,pos,groups,frames):
        super().__init__(groups)
        self.icon = True
        self.path=None
        self.direction = vector(0,0)
        self.speed = 400
        #images
        self.frames,self.frame_index=frames,1
        self.state ='idle'
        self.image=self.frames[self.state][self.frame_index]
        self.rect=self.image.get_rect(center=pos)
        self.z=Z_LAYERS['main']
    
    def start_move(self,path):
        self.rect.center = path[0]
        self.path = path[1:]
        self.find_path()
    
    def find_path(self):
        if self.path:
            print(self.path)
            if self.rect.centerx == self.path[0][0]: # vertical
                self.direction = vector(0,1 if self.path[0][1]>self.rect.centery else -1)
            else: # horizontal
                self.direction = vector(1 if self.path[0][0]>self.rect.centerx else -1,0)
        else:
            self.direction = vector(0,0)
        
    def point_collision(self):
        if self.direction.y ==1 and self.rect.centery>=self.path[0][1] or \
            self.direction.y ==-1 and self.rect.centery<=self.path[0][1]:
            self.rect.centery=self.path[0][1]
            del self.path[0]
            self.find_path()
        
        if self.direction.x ==1 and self.rect.centerx>=self.path[0][0] or \
            self.direction.x ==-1 and self.rect.centerx<=self.path[0][0]: # left and below the point
            self.rect.centerx=self.path[0][0]
            del self.path[0]
            self.find_path()


    def update(self,dt):
        if self.path:
            self.point_collision
            self.rect.center+= self.direction * self.speed * dt
