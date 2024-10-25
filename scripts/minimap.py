import pygame


class Minimap:
    def __init__(self, game, tilemap):
        self.game = game
        self.tilemap = tilemap
        self.tile_size = self.tilemap.tile_size
        self.tiles = {'bricks'}
        self.minimap_surf = self.game.assets['minimap']
           
    def render(self, surf, offset=(0, 0)):    
        for loc in self.tilemap.tilemap:
            tile = self.tilemap.tilemap[loc]
            if tile['type'] in self.tiles:
               pass
        
        surf.blit(self.minimap_surf, (surf.get_width() - self.minimap_surf.get_width(), 0))
    
    