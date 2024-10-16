import pygame
import sys
from .utils import load_image

class Menu:
    def __init__(self, game, m_type):
        pygame.init()
        self.type = m_type
        self.game = game
        self.screen = pygame.display.set_mode((900, 600))
        self.display = pygame.Surface((300, 200)) # 25/ 16 screen
        self.clock = pygame.time.Clock()
        
        self.assets = {
            'title': load_image('title.png')
        }
        
    def run(self):
        while True:
            
            self.display.fill('#1e1320')
            
            self.display.blit(self.assets['title'], (100, 30))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)