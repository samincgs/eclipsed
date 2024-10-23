import pygame


class Minimap:
    def __init__(self, game, tilemap):
        self.game = game
        self.tilemap = tilemap
        self.tile_size = self.tilemap.tile_size
        self.tiles = {'bricks'}
        self.minimap_width = 64
        self.minimap_height = 48
        self.minimap_surf = pygame.Surface((self.minimap_width, self.minimap_height))
        # self.minimap_surf.set_colorkey((0, 0, 0))
           
    def render(self, surf, offset=(0, 0)):
        
        self.minimap_surf.fill((0, 0, 0))  # Fill the minimap with black
        
        tile_width_scale = int(self.minimap_width / (surf.get_width() / self.tile_size) )
        tile_height_scale = int(self.minimap_height / (surf.get_height() / self.tile_size) )
        
        for loc in self.tilemap.tilemap:
            tile = self.tilemap.tilemap[loc]
            if tile['type'] in self.tiles:
                small_rect = pygame.Rect(tile['pos'][0]  * tile_width_scale, tile['pos'][1] * tile_height_scale, 2,2)
                pygame.draw.rect(self.minimap_surf, (58, 68, 102), small_rect)
        
        surf.blit(self.minimap_surf, (surf.get_width() - self.minimap_width, 0))
    
    