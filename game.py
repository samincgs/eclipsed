import pygame
import sys
import random
import time

from scripts.entities import Player
from scripts.enemy import Enemy
from scripts.tilemap import Tilemap
from scripts.asset_manager import AssetManager
from scripts.minimap import Minimap

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Eclipsed') 
        self.screen = pygame.display.set_mode((900, 600)) # 75/50
        self.display = pygame.Surface((300, 200)) # 25/ 16 screen
        self.clock = pygame.time.Clock()
                
        self.assets = AssetManager().load_assets
           
        self.player = Player(self, (50, 50), self.assets['player/'].img.get_size())
        
        self.tilemap = Tilemap(self, tile_size=12)
        
        self.minimap = Minimap(self, self.tilemap)
        
        self.last_time = time.time()
          
        self.movement = [False, False]
        self.scroll = [0, 0]
        self.projectiles = []
        self.enemies = []
        self.stars = []
                
        self.tilemap.load(0)
        
        for entity in self.tilemap.extract([('spawners', 0), ('spawners', 1)], keep=False):
            if entity['variant'] == 0:
                self.player.pos = entity['pos']
            else:
                self.enemies.append(Enemy(self, 'slime', entity['pos'], self.assets['slime/'].img.get_size()))
                        
        # TODO: fix star position and allows it to move parallax to the scroll        
        for _ in range(40):
            star_x = (random.random() * self.display.get_width())
            star_y = (random.random() * self.display.get_height()) 
            self.stars.append([(star_x, star_y), random.choice(self.assets['particles/star'])])
    
    
    def draw_ui(self, surf):
        for heart in range(self.player.health):
            surf.blit(self.assets['heart'], (5 + heart * (self.assets['heart'].get_width() + 3), 5))
        # self.assets['small_font'].render(surf, 'FPS: ' + str(int(self.clock.get_fps())), (surf.get_width() - 30 , 5))
        rect_width, rect_height = 21, 21
        draw_rect = pygame.Rect(11 - rect_width // 2, surf.get_height() - 11 - rect_height // 2, rect_width, rect_height)
        pygame.draw.rect(surf, (255, 255, 255), draw_rect, 3, 5)
        surf.blit(self.assets['gun_ui'], (draw_rect.centerx - self.assets['gun_ui'].get_width() // 2, draw_rect.centery - self.assets['gun_ui'].get_height() // 2))
    
    def run(self):
        while True:
            
            dt = time.time() - self.last_time
            dt *= 60
            self.last_time = time.time()
                            
            self.display.fill('#1e1320') # dark purple background
            
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
            
            # parallax_effect = 0.5
            for star in self.stars:
                self.display.blit(star[1], star[0])
              
            self.tilemap.render(self.display, offset=render_scroll)
 
            self.player.update(self.tilemap, movement=(self.movement[0] - self.movement[1], 0))
            self.player.render(self.display, offset=render_scroll)
            
            self.minimap.render(self.display, offset=render_scroll)
            
            self.draw_ui(self.display)
            
            for enemy in self.enemies.copy():
                if not enemy.killed:
                    enemy.update(self.tilemap)
                else:
                    enemy.death_timer +=1
                    if enemy.death_timer > 15:
                        self.enemies.remove(enemy)
                enemy.render(self.display, offset=render_scroll)
            
            # [[x, y], direction]
            for projectile in self.projectiles.copy():
                projectile[0][0] += projectile[1] * 3
                projectile[2] += 1 # increase the timer
                img = self.assets['projectile']
                self.display.blit(img, (projectile[0][0] - render_scroll[0], projectile[0][1] - render_scroll[1]))
                for enemy in self.enemies:
                    if enemy.rect().collidepoint(projectile[0]):
                        enemy.health -= 1
                        self.projectiles.remove(projectile)
                if projectile[2] > 120:  #TODO: fix so bullet is removed after it leaves the screen
                    self.projectiles.remove(projectile)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_UP:
                        self.player.jump()
                    if event.key == pygame.K_RIGHT:
                        self.movement[0] = True
                    if event.key == pygame.K_LEFT:
                        self.movement[1] = True
                    if event.key == pygame.K_z:
                        self.player.shoot()
                    if event.key == pygame.K_x:
                        self.player.dash()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        self.movement[0] = False
                    if event.key == pygame.K_LEFT:
                        self.movement[1] = False       
               
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)
                      
if __name__ == '__main__':
    game = Game()
    game.run()