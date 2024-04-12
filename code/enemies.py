from settings import *
from sprites import Sprite, MovingSprite, AnimatedSprite, Item, ParticleEffectSprite, DamageSprite
from timer import Timer

class Gunner(AnimatedSprite):
    def __init__(self, pos, frames, groups, create_bullet, direction, speed):
        super().__init__(pos, frames, groups)
        self.shoot_timer = Timer(5000)
        self.create_bullet = create_bullet
        self.direction = direction
        if(self.direction == 'left'):
            self.image = pygame.transform.flip(self.image, True, False)
        self.speed = speed
        self.bullet = None
        
    def shoot(self):
        if not self.shoot_timer.active:
            self.shoot_timer.activate()
            self.create_bullet(self.rect.center+vector(20,8), self.direction, self.speed)
            
    def update(self, dt):
        self.shoot_timer.update()
        self.shoot()
        return super().update(dt)
    
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
        # print(self.direction, type(self.speed), dt)
        self.rect.x += self.direction[0] * self.speed * dt
        self.check_collision()
        
    def update(self, dt):
        self.move(dt)
