import pygame
from .entities import PhysicsEntity

class Camera:
    def __init__(self, width, height, entity):
        self.width = width
        self.height = height
        self.scroll = [0, 0]
        self.render_scroll = self.scroll.copy()
        self.entity = entity
        self.slowness = 5
        
    def update(self, movement=(0, 0)):
        if isinstance(self.entity, PhysicsEntity):
            self.scroll[0] += (self.entity.rect().centerx - self.width / 2 - self.scroll[0]) / self.slowness # divide by 5 if you want a lagged behind camera following the player
            self.scroll[1] += (self.entity.rect().centery - self.height / 2 - self.scroll[1]) / self.slowness
        else:
            self.scroll[0] += (movement[0] - movement[1]) * 2
            self.scroll[1] += (movement[3] - movement[2]) * 2
        self.render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
    
        
    # def apply(self):
    #     return (self.entity.pos[0] - self.render_scroll[0], self.entity.pos[1] - self.render_scroll[1])