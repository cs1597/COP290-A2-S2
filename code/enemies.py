from settings import *
from sprites import Sprite, MovingSprite, AnimatedSprite, Item, ParticleEffectSprite, DamageSprite
from timer import Timer

class Gunner(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, create_bullet, direction, speed, player):
        super().__init__(groups)
        self.z = Z_LAYERS['main']
        
        self.frames, self.frame_index = frames, 0
        self.state = 'idle'
        self.image = self.frames[self.state][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        
        self.create_bullet = create_bullet
        self.direction = direction
        self.player = player
        self.damaged = False
        self.health = 3
        self.speed = speed
        
        self.timers = {
            'shoot':Timer(5000),
            'damage_lock':Timer(1000)
        }
        
    def hit(self):
        if not self.timers['damage_lock'].active:
            self.damaged = True
            self.frame_index = 0
            self.timers['damage_lock'].activate()
            self.health -= 1
        
    def shoot(self):
        if not self.timers['shoot'].active:
            self.timers['shoot'].activate()
            self.create_bullet(self.rect.center+vector(20,8), self.direction, self.speed)
    
    def animate(self, dt):
        self.frame_index += ANIMATION_SPEED * dt
        if self.state == 'gunner_damage' and (self.frame_index >= len(self.frames[self.state])):
            self.state = 'idle'
            self.damaged = False
        if self.state == 'gunner_death' and (self.frame_index >= len(self.frames[self.state])):
            self.kill()
        self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]
        self.image = self.image if self.direction=='right' else pygame.transform.flip(self.image, True, False)
    
    def get_state(self):
        if self.damaged :
            self.state = 'gunner_damage'
        if self.health == 0:
            self.state = 'gunner_death'
         
    def update(self, dt):
        self.timers['shoot'].update()
        self.shoot()
        self.timers['damage_lock'].update()
        
        self.get_state()
        self.animate(dt)
    
class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, groups, surf, direction, speed, collision_sprites, player):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(center = pos)
        self.damagebox = self.rect.copy()
        self.direction = (1,0) if direction == 'right' else (-1,0)
        self.speed = speed
        self.collision_sprites = collision_sprites
        self.player = player
        self.z = Z_LAYERS['main']
        
    def check_hit(self):
        if self.rect.colliderect(self.player.hitbox_rect):
            self.player.hit()
            self.kill()
        
    def check_collision(self):
        collide_rects = [sprite.rect for sprite in self.collision_sprites]
        if self.rect.collidelist(collide_rects) >= 0:
            self.kill()
        else:
            self.check_hit()
        
    def move(self, dt):
        self.rect.x += self.direction[0] * self.speed * dt
        self.check_collision()
        
    def update(self, dt):
        self.move(dt)
