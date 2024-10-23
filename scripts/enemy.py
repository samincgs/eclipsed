import pygame
import random
from .entities import PhysicsEntity

class Enemy(PhysicsEntity):
    def __init__(self, game, e_type, pos, size):
        super().__init__(game, e_type, pos, size)
        self.aggro_radius = (120, 40)
        self.acceleration = 0.6
        self.max_health = 3
        self.health = self.max_health
        self.killed = False
        self.damage_cooldown = 0
        self.death_timer = 0
        self.jumped = 0
        
    def update(self, tilemap, movement=(0, 0)):
         
        super().update(tilemap, movement=movement)
        dis = (self.game.player.pos[0] - self.pos[0], self.game.player.pos[1] - self.pos[1])
        if dis[0] < 0:
            self.flip = True
        elif dis[0] > 0:
            self.flip = False
        
        if self.game.player.rect().colliderect(self.rect()):
            if not self.damage_cooldown:
                self.game.player.health -= 1
                self.damage_cooldown = 60
        
        if abs(dis[1]) < self.aggro_radius[1] and abs(dis[0]) < self.aggro_radius[0]:
            if random.random() < 0.05 and not self.jumped:
                self.jumped = 160
                self.velocity[1] = -2.5            
            if dis[0] > 0:
                self.velocity[0] = self.acceleration 
            elif dis[0] < 0:
                self.velocity[0] = -self.acceleration 
        else:
            self.velocity[0] = 0  
            
        if self.health <= 0:
            self.killed = True
            self.death_timer = 1        
        if self.jumped:
            self.jumped -= 1
        if self.damage_cooldown:
            self.damage_cooldown -=1
                 
    def health_bar(self, surf, offset=(0, 0)):
        health_ratio = self.health / self.max_health
        bar_width = 8
        bar_height = 2
        background_rect = pygame.Rect(self.rect().centerx - bar_width // 2 - offset[0], self.rect().centery - bar_height // 2 - 10 - offset[1], bar_width, bar_height)
        health_bar_rect = pygame.Rect(self.rect().centerx - bar_width // 2 - offset[0], self.rect().centery - bar_height // 2 - 10 - offset[1], bar_width * health_ratio, bar_height)
        pygame.draw.rect(surf, (255, 0, 0), background_rect)
        pygame.draw.rect(surf, (0, 255, 0), health_bar_rect)
        
     
    def render(self,surf, offset=(0, 0)):
        if not self.killed:
            super().render(surf, offset=offset)
            self.health_bar(surf, offset=offset)
        else:
            self.mask_blink(surf, offset=offset)
            
            
                
            

                
                
        
        