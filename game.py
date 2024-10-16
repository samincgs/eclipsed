import pygame
import sys

from scripts.utils import load_image, load_images
from scripts.entities import Player
from scripts.enemy import Enemy
from scripts.tilemap import Tilemap
from scripts.menu import Menu
from scripts.animation import Animation
from scripts.font import Font

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Eclipsed') # TODO: change name later
        self.screen = pygame.display.set_mode((900, 600))
        self.display = pygame.Surface((300, 200)) # 25/ 16 screen
        self.clock = pygame.time.Clock()
        
        self.main_menu = Menu(self, 'main')
        
        self.assets = {
            'player/': Animation(images=[load_image('entities/player/0.png')]),
            'player/jump': Animation(load_images('entities/player/jump')),
            'player/walk': Animation(load_images('entities/player/walk'), img_dur=5),
            'slime/': Animation(images=[load_image('entities/enemy/slime/0.png')]),
            'bricks': load_images('tiles/bricks'),
            'decor': load_images('tiles/decor'),
            'gun': load_image('gun.png'),
            'projectile': load_image('projectile.png'),
            'small_font': Font('data/fonts/small_font.png', (255, 255, 255)),
            'large_font': Font('data/fonts/large_font.png'),
        }
        
        self.player = Player(self, (50, 50), self.assets['player/'].img.get_size())
        
        self.tilemap = Tilemap(self, tile_size=12)
                
        self.movement = [False, False]
        
        self.scroll = [0, 0]
        
        self.projectiles = []
        self.enemies = [Enemy(self, 'slime', (220, 50), (9, 8))]
        
        
        try:
            self.tilemap.load(0)
        except FileNotFoundError:
            pass

    def run(self):
        while True:
            self.display.fill('#1e1320') # dark purple background
            
            self.assets['small_font'].render(self.display, f'Health: {self.player.health}', (3, 5))
            
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
            
            self.tilemap.render(self.display, offset=render_scroll)
                        
            self.player.update(self.tilemap, movement=(self.movement[0] - self.movement[1], 0))
            self.player.render(self.display, offset=render_scroll)
            
            for enemy in self.enemies.copy():
                if enemy.death_timer > 15:
                    self.enemies.remove(enemy)
                enemy.update(self.tilemap)
                enemy.render(self.display, offset=render_scroll)
            
            # [[x, y], direction, timer]
            for projectile in self.projectiles.copy():
                projectile[0][0] += projectile[1] * 3
                projectile[2] += 1 # increase the timer
                img = self.assets['projectile']
                self.display.blit(img, (projectile[0][0] - render_scroll[0], projectile[0][1] - render_scroll[1]))
                for enemy in self.enemies:
                    if enemy.rect().collidepoint(projectile[0]):
                        enemy.health -= 1
                        self.projectiles.remove(projectile)
                if projectile[2] > 180: # remove the projectile after it reaches 3 secs
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
                    # if event.key == pygame.K_z:
                    #     self.player.dash()
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