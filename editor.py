import pygame
import sys

from scripts.utils import load_image, load_images
from scripts.entities import PhysicsEntity
from scripts.tilemap import Tilemap
from scripts.camera import Camera

RENDER_SCALE = 3.0

class Editor:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Level Editor') # TODO: change name later
        self.screen = pygame.display.set_mode((900, 600))
        self.display = pygame.Surface((300, 200)) # 25/ 16 screen
        self.clock = pygame.time.Clock()
        
        self.assets = {
            'bricks': load_images('tiles/bricks'),
            'decor': load_images('tiles/decor'),
            'spawners': load_images('tiles/spawners'),
        }
        
        self.tilemap = Tilemap(self, tile_size=12)
        
        self.camera = Camera(width=self.display.get_width(), height=self.display.get_height(), entity=None)
        
        self.movement = [False, False, False, False]
        
        self.blocks = list(self.assets)
        self.tile_group = 0
        self.tile_variant = 0
        
        self.ongrid = True
        self.shift = False
        self.click = False
        self.right_click = False
        
        try:
            self.tilemap.load(0)
        except FileNotFoundError:
            pass

    def run(self):
        while True:
            
            self.display.fill('#1e1320') # dark purple background
            
            self.camera.update(self.movement) # to update camera
            
            # show current tile selected on the top left of the screen
            current_img = self.assets[self.blocks[self.tile_group]][self.tile_variant].copy()
            current_img.set_alpha(180)
            
            # get the mouse position
            mpos = pygame.mouse.get_pos()
            mpos = (mpos[0] / RENDER_SCALE, mpos[1] / RENDER_SCALE)
            tile_pos = (int((mpos[0] + self.camera.scroll[0]) // self.tilemap.tile_size), int((mpos[1] + self.camera.scroll[1]) // self.tilemap.tile_size)) # convert world mpos into the tile position
            
            # if the current selected mode is ongrid we can attach the block to the grid
            if self.ongrid:
                if self.click: # if left click place the tile
                    self.tilemap.tilemap[str(tile_pos[0]) + ';' + str(tile_pos[1])] = {'type': self.blocks[self.tile_group], 'variant': self.tile_variant, 'pos': tile_pos}
                elif self.right_click: # if right click get rid of the tile
                    check_loc = str(tile_pos[0]) + ';' + str(tile_pos[1])
                    if check_loc in self.tilemap.tilemap.copy():
                        del self.tilemap.tilemap[check_loc]
            else:
                # if not on grid, get rid of the offgrid tiles using right click
                if self.right_click:
                    for tile in self.tilemap.offgrid_tiles.copy():
                        tile_rect = pygame.Rect(tile['pos'][0], tile['pos'][1], self.tilemap.tile_size, self.tilemap.tile_size)
                        mpos_scaled = (mpos[0] + self.camera.scroll[0], mpos[1] + self.camera.scroll[1])
                        if tile_rect.collidepoint(mpos_scaled):
                            self.tilemap.offgrid_tiles.remove(tile)

            self.tilemap.render(self.display, offset=self.camera.render_scroll)
            
            if self.ongrid:
            # display the block ur about to place
                self.display.blit(self.assets[self.blocks[self.tile_group]][self.tile_variant], (tile_pos[0] * self.tilemap.tile_size - self.camera.scroll[0], tile_pos[1] * self.tilemap.tile_size - self.camera.scroll[1]))
            else:
                self.display.blit(self.assets[self.blocks[self.tile_group]][self.tile_variant], mpos)
                
            self.display.blit(current_img, (5, 5))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_d:
                        self.movement[0] = True
                    if event.key == pygame.K_a:
                        self.movement[1] = True
                    if event.key == pygame.K_w:
                        self.movement[2] = True
                    if event.key == pygame.K_s:
                        self.movement[3] = True
                    if event.key == pygame.K_LSHIFT:
                        self.shift = True
                    if event.key == pygame.K_g:
                        self.ongrid = not self.ongrid
                    if event.key == pygame.K_o:
                        self.tilemap.save(0)
                    if event.key == pygame.K_t:
                        self.tilemap.autotile()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_d:
                        self.movement[0] = False
                    if event.key == pygame.K_a:
                        self.movement[1] = False
                    if event.key == pygame.K_w:
                        self.movement[2] = False
                    if event.key == pygame.K_s:
                        self.movement[3] = False
                    if event.key == pygame.K_LSHIFT:
                        self.shift = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.click = True
                        if not self.ongrid:
                            self.tilemap.offgrid_tiles.append({'type': self.blocks[self.tile_group], 'variant': self.tile_variant, 'pos': (mpos[0] + self.camera.scroll[0], mpos[1] + self.camera.scroll[1])})
                    if event.button == 3:
                        self.right_click = True
                    if event.button == 4: # scroll up
                        self.tile_variant = (self.tile_variant + 1) % len(self.assets[self.blocks[self.tile_group]])  
                        if self.shift:
                            self.tile_variant = 0
                            self.tile_group = (self.tile_group - 1) % len(self.blocks)
                    if event.button == 5: # scroll down
                        self.tile_variant = (self.tile_variant + 1) % len(self.assets[self.blocks[self.tile_group]])
                        if self.shift:
                            self.tile_variant = 0
                            self.tile_group = (self.tile_group + 1) % len(self.blocks)
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.click = False
                    if event.button == 3:
                        self.right_click = False
            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)
            
            
if __name__ == '__main__':
    editor = Editor()
    editor.run()