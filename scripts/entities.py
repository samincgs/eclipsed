import pygame


class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.max_health = 3
        self.health = self.max_health
        
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        self.flip = False
        self.action =''
        self.animation = self.game.assets[self.type + '/' + self.action]
        
    
    def rect(self):
        return pygame.Rect(*self.pos, *self.size)
            
    def set_action(self, action=''):
        if self.action != action:
            self.action = action
            self.animation = self.game.assets[self.type + '/' + self.action]
            self.animation.frame = 0
            
    def update(self, tilemap, movement=(0, 0)):
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        
        
        # physics
        self.pos[0] += frame_movement[0]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x
                      
        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y
        
        # y velocity pulling entity down
        self.velocity[1] = min(self.velocity[1] + 0.1, 3)
        
        if self.collisions['up'] or self.collisions['down']:
            self.velocity[1] = 0
                 
        if movement[0] > 0:
            self.flip = False
        elif movement[0] < 0:
            self.flip = True
        
        self.animation.update()
    
    def mask_blink(self, surf, offset=(0, 0)):
        img = self.game.assets[self.type + '/' + self.action].img
        img_mask = pygame.mask.from_surface(img)
        blink_img = img_mask.to_surface()
        blink_img.set_colorkey((0, 0, 0))
        surf.blit(pygame.transform.flip(blink_img, self.flip, False), (self.pos[0] - offset[0], self.pos[1] - offset[1]))
           
    def render(self, surf, offset=(0, 0)):
        img = self.game.assets[self.type + '/' + self.action].img
        surf.blit(pygame.transform.flip(img, self.flip, False), (self.pos[0] - offset[0], self.pos[1] - offset[1]))

class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'player', pos, size)
        
        self.jumps = 2
        self.air_time = 0
        self.shoot_time = 0
        
        self.dashing = 0
    
    def jump(self):
        if self.jumps:
            self.jumps = max(0, self.jumps - 1)
            self.velocity[1] = -2
    
    def dash(self):
        if not self.dashing:
            if self.flip:
                self.dashing = -40
            else:
                self.dashing = 40
                 
    def shoot(self):
        bullet_dis = 4
        if self.shoot_time >= 25:
            if self.flip:
                self.game.projectiles.append([[self.rect().centerx - bullet_dis, self.rect().centery], -1, 0])
            elif not self.flip:
                self.game.projectiles.append([[self.rect().centerx + bullet_dis, self.rect().centery], 1, 0])
            self.shoot_time = 0
            
    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement=movement)
        # timers
        self.air_time += 1
        self.shoot_time += 1
                
        if self.collisions['down']:
            self.jumps = 2
            self.air_time = 0
            
        if self.air_time > 5:
            self.set_action('jump')
        elif movement[0] != 0:
            self.set_action('walk')
        else:
            self.set_action()
        
        if self.dashing > 0:
            self.dashing = max(self.dashing - 1, 0)
        else:
            self.dashing = min(self.dashing + 1, 0)
        
        if abs(self.dashing) > 35:
            self.velocity[0] = abs(self.dashing) / self.dashing * 5
        else:
            if self.dashing > 0:
                self.velocity[0] = max(self.velocity[0] - 0.5, 0)
            else:
                self.velocity[0] = min(self.velocity[0] + 0.5, 0) 
                
            
            
    def render(self, surf, offset=(0,0)):
        super().render(surf, offset=offset)
        
        gun = self.game.assets['gun'] # TODO: fix gun slightly jittering when falling down from platform
        if self.flip:
            surf.blit(pygame.transform.flip(gun, self.flip, False), (self.rect().centerx - gun.get_width() - offset[0], self.rect().centery - offset[1]))
        else:
            surf.blit(gun, (self.rect().centerx - offset[0], self.rect().centery - offset[1]))
            
        