import pygame
import sys

class InputManager:
    def __init__(self, game):
        self.game = game
        
    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_UP:
                    self.game.player.jump()
                if event.key == pygame.K_RIGHT:
                    self.game.movement[0] = True
                if event.key == pygame.K_LEFT:
                    self.game.movement[1] = True
                if event.key == pygame.K_z:
                    self.game.player.shoot()
                if event.key == pygame.K_x:
                    self.game.player.dash()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.game.movement[0] = False
                if event.key == pygame.K_LEFT:
                    self.game.movement[1] = False
                    
 # for event in pygame.event.get():
            #     if event.type == pygame.QUIT:
            #         pygame.quit()
            #         sys.exit()
            #     if event.type == pygame.KEYDOWN:
            #         if event.key == pygame.K_ESCAPE:
            #             pygame.quit()
            #             sys.exit()
            #         if event.key == pygame.K_UP:
            #             self.player.jump()
            #         if event.key == pygame.K_RIGHT:
            #             self.movement[0] = True
            #         if event.key == pygame.K_LEFT:
            #             self.movement[1] = True
            #         if event.key == pygame.K_z:
            #             self.player.shoot()
            #         if event.key == pygame.K_x:
            #             self.player.dash()
            #     if event.type == pygame.KEYUP:
            #         if event.key == pygame.K_RIGHT:
            #             self.movement[0] = False
            #         if event.key == pygame.K_LEFT:
            #             self.movement[1] = False        
        
        