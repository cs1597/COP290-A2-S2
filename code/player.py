from pygame.sprite import Group
from settings import *
from timer import Timer
from os.path import join

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites, semicollision_sprites, frames):
        super().__init__(groups)
        self.z = Z_LAYERS['main']
        
        self.frames, self.frame_index = frames, 0
        self.state, self.facing_right = 'idle', True
        self.image = self.frames[self.state][self.frame_index]
        
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox_rect = self.rect.inflate(-50, -28)
        self.old_rect = self.hitbox_rect.copy()
        
        self.direction = vector()
        self.speed = 250
        self.gravity = 1500
        self.jump = False
        self.jump_height = 700
        self.attacking = False
        self.damaged = False
        
        self.collision_sprites = collision_sprites
        self.semicollision_sprites = semicollision_sprites
        self.on_surface = {'floor' : False, 'left' : False, 'right' : False}
        self.platform = None
        
        self.timers = {
            'wall jump' : Timer(250),
            'allow wall jump' : Timer(250),
            'platform skip' : Timer(250),
            'attack_lock' : Timer(800),
            'damage_lock' : Timer(600)
        }
        
    def input(self):
        keys = pygame.key.get_pressed()
        input_vector = vector(0,0)
        if not self.timers['wall jump'].active:
            if keys[pygame.K_d]:
                input_vector.x += 1
                self.facing_right = True
            if keys[pygame.K_a]:
                input_vector.x -= 1
                self.facing_right = False
            if keys[pygame.K_s]:
                self.timers['platform skip'].activate()
            if keys[pygame.K_x]:
                self.attack()
            
            (self.direction).x = (input_vector.normalize()).x if input_vector else 0
        
        if keys[pygame.K_SPACE]:
            self.jump = True
            
    def attack(self):
        if not self.timers['attack_lock'].active:
            self.attacking = True
            self.frame_index = 0
            self.timers['attack_lock'].activate()
            
    def hit(self):
        if not self.timers['damage_lock'].active:
            self.damaged = True
            self.frame_index = 0
            self.timers['damage_lock'].activate()
            
    def move(self, dt):
        # horizontal
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')
        
        # vertical
        if not self.on_surface['floor'] and any((self.on_surface['left'], self.on_surface['right'])) and not self.timers['allow wall jump'].active:
            self.direction.y=0
            self.hitbox_rect.y += self.gravity / 10 * dt
        else: 
            self.direction.y += (self.gravity / 2) * dt
            self.hitbox_rect.y += self.direction.y * dt
            self.direction.y += (self.gravity / 2) * dt
        
        if self.jump:
            if self.on_surface['floor']:
                self.timers['allow wall jump'].activate()
                self.direction.y = -self.jump_height
                self.hitbox_rect.bottom -= 1
            elif any((self.on_surface['left'], self.on_surface['right'])) and not self.timers['allow wall jump'].active:
                self.timers['wall jump'].activate()
                self.direction.y = -self.jump_height
                self.direction.x = 1 if self.on_surface['left'] else -1
            self.jump = False
            
        self.collision('vertical')
        self.semicollision()
        self.rect.center = self.hitbox_rect.center
             
    def platform_move(self, dt):
        if self.platform:
            self.hitbox_rect.topleft += self.platform.direction * self.platform.speed * dt
    
    def check_contact(self):
        floor_rect = pygame.Rect(self.hitbox_rect.bottomleft, (self.hitbox_rect.width, 2))
        left_rect = pygame.Rect(self.hitbox_rect.topleft + vector(-2,self.hitbox_rect.height/4), (2,self.hitbox_rect.height/2))
        right_rect = pygame.Rect(self.hitbox_rect.topright + vector(2,self.hitbox_rect.height/4), (2,self.hitbox_rect.height/2))
        collide_rects = [sprite.rect for sprite in self.collision_sprites]
        semicollide_rects = [sprite.rect for sprite in self.semicollision_sprites]
        
        self.on_surface['floor'] = True if floor_rect.collidelist(collide_rects)>=0 or (floor_rect.collidelist(semicollide_rects) >= 0 and self.direction.y>=0) else False
        self.on_surface['right'] = True if right_rect.collidelist(collide_rects)>=0 else False
        self.on_surface['left'] = True if left_rect.collidelist(collide_rects)>=0 else False
        
        self.platform = None
        sprites = self.collision_sprites.sprites() + self.semicollision_sprites.sprites()
        for sprite in [sprite for sprite in sprites if hasattr(sprite, 'moving')]:
            if sprite.rect.colliderect(floor_rect):
                self.platform = sprite
                
    def collision(self,axis):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if axis=='horizontal':
                    if self.hitbox_rect.left <= sprite.rect.right and int(self.old_rect.left) >= int(sprite.old_rect.right):
                        self.hitbox_rect.left = sprite.rect.right
                    if self.hitbox_rect.right >= sprite.rect.left and int(self.old_rect.right) <= int(sprite.old_rect.left):
                        self.hitbox_rect.right = sprite.rect.left
                else:
                    if self.hitbox_rect.bottom >= sprite.rect.top and int(self.old_rect.bottom) <= int(sprite.old_rect.top):
                        self.hitbox_rect.bottom = sprite.rect.top
                    if self.hitbox_rect.top <= sprite.rect.bottom and int(self.old_rect.top) >= int(sprite.old_rect.bottom):
                        self.hitbox_rect.top = sprite.rect.bottom
                        if hasattr(sprite, 'moving'):
                            self.hitbox_rect.top+=6
                    self.direction.y = 0
    
    def semicollision(self):
        if not self.timers['platform skip'].active:
            for sprite in self.semicollision_sprites:
                if sprite.rect.colliderect(self.hitbox_rect):
                    if self.hitbox_rect.bottom >= sprite.rect.top and int(self.old_rect.bottom)-2 <= sprite.old_rect.top:
                        self.hitbox_rect.bottom = sprite.rect.top
                        if self.direction.y > 0:
                            self.direction.y = 0
        
    def update_timers(self):
        for timer in self.timers:
            self.timers[timer].update()
            
    def animate(self, dt):
        self.frame_index += ANIMATION_SPEED * dt
        if self.state == 'attack' and (self.frame_index >= len(self.frames[self.state])):
            self.state = 'idle'
            self.attacking = False
        if self.state == 'damage' and (self.frame_index >= len(self.frames[self.state])):
            self.state = 'idle'
            self.damaged = False
        self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]
        self.image = self.image if self.facing_right else pygame.transform.flip(self.image, True, False)
        
    def get_state(self):
        if self.on_surface['floor']:
            if self.attacking:
                self.state = 'attack'
            elif self.damaged:
                self.state = 'damage'
            else:
                self.state = 'idle' if self.direction.x == 0 else 'run'
        else:
            if self.attacking:
                self.state = 'attack'
            elif self.damaged:
                self.state = 'damage'
            else:
                if any((self.on_surface['left'], self.on_surface['right'])):
                    self.state = 'wall'
                else:
                    self.state = 'jump'if self.direction.y > 0 else 'fall'
    
    def update(self, dt):
        self.old_rect = self.hitbox_rect.copy()
        self.update_timers()
        
        self.input()
        self.move(dt)
        self.platform_move(dt)
        self.check_contact()
        
        self.get_state()
        self.animate(dt)
        
class MazePlayer(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites, frames):
        super().__init__(groups)
        self.z = Z_LAYERS['main']
        
        self.frames, self.frame_index = frames, 0
        self.state = 'idle_up'
        self.image = self.frames[self.state][self.frame_index]
        
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox_rect = self.rect.inflate(-30, -24)
        self.old_rect = self.hitbox_rect.copy()
        
        self.direction = vector()
        self.speed = 150
        
        self.collision_sprites = collision_sprites
        self.on_surface = {'top' : False, 'bottom' : False, 'left' : False, 'right' : False}
        
        self.timers = {
        }
    
    def input(self):
        keys = pygame.key.get_pressed()
        input_vector = vector(0,0)
        if keys[pygame.K_d]:
            input_vector.x += 1
        if keys[pygame.K_a]:
            input_vector.x -= 1
        if keys[pygame.K_s]:
            input_vector.y += 1
        if keys[pygame.K_w]:
            input_vector.y -= 1
            
        (self.direction).x = (input_vector.normalize()).x if input_vector else 0
        (self.direction).y = (input_vector.normalize()).y if input_vector else 0

    def move(self, dt):
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')
        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.collision('vertical')
        
        self.rect.center = self.hitbox_rect.center
        
    def collision(self,axis):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if axis=='horizontal':
                    if self.hitbox_rect.left <= sprite.rect.right and int(self.old_rect.left) >= int(sprite.old_rect.right):
                        self.hitbox_rect.left = sprite.rect.right
                    if self.hitbox_rect.right >= sprite.rect.left and int(self.old_rect.right) <= int(sprite.old_rect.left):
                        self.hitbox_rect.right = sprite.rect.left
                else:
                    if self.hitbox_rect.bottom >= sprite.rect.top and int(self.old_rect.bottom) <= int(sprite.old_rect.top):
                        self.hitbox_rect.bottom = sprite.rect.top
                    if self.hitbox_rect.top <= sprite.rect.bottom and int(self.old_rect.top) >= int(sprite.old_rect.bottom):
                        self.hitbox_rect.top = sprite.rect.bottom
                        
    def animate(self, dt):
        self.frame_index += ANIMATION_SPEED * dt
        self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]
        
    def get_state(self):
        if self.direction.y != 0:
            self.state = 'run_down' if self.direction.y > 0 else 'run_up'
        elif self.direction.y == 0 and self.direction.x != 0:
            self.state = 'run_right' if self.direction.x > 0 else 'run_left'
        else:
            self.state = 'idle_up' 
    
    def update(self, dt):
        self.old_rect = self.hitbox_rect.copy()
        
        self.input()
        self.move(dt)
        
        self.get_state()
        self.animate(dt)