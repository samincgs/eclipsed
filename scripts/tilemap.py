import pygame
import json

NEIGHBOR_OFFSETS = [(-2, -2), (-2, -1), (-2, 0), (-2, 1), (-2, 2),
                    (-1, -2), (-1, -1), (-1, 0), (-1, 1), (-1, 2),
                    (0, -2), (0, -1), (0, 0), (0, 1), (0, 2),
                    (1, -2), (1, -1), (1, 0), (1, 1), (1, 2),
                    (2, -2), (2, -1), (2, 0), (2, 1), (2, 2)]

PHYSICS_TILES = {'bricks'}

class Tilemap:
    def __init__(self, game, tile_size=12):
        self.game = game
        self.tile_size = tile_size
        
        self.tilemap = {}
        self.offgrid_tiles = []
        
        # for i in range(25):
        #     self.tilemap[str(i) + ';6'] = {'type': 'bricks', 'variant': 1, 'pos': [i, 6]}
        #     self.tilemap['5;'+ str(i)] = {'type': 'bricks', 'variant': 1, 'pos': [5, i]}
        #     self.tilemap['2;'+ str(i)] = {'type': 'bricks', 'variant': 1, 'pos': [2, i]}
            
    
    def tiles_around(self, pos):
        tiles = []
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in NEIGHBOR_OFFSETS:
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])   
        return tiles
    
    def physics_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))    
        return rects
    
    def save(self, map_id):
        f = open(f'data/maps/{map_id}.json', 'w')
        json.dump({'tilemap': self.tilemap, 'offgrid': self.offgrid_tiles, 'tile_size': self.tile_size}, fp=f)
        f.close()
    
    def load(self, map_id):
        f = open(f'data/maps/{map_id}.json', 'r')
        tile_data = json.load(fp=f)
        self.tilemap = tile_data['tilemap']
        self.offgrid_tiles = tile_data['offgrid']
        self.tile_size = tile_data['tile_size']
        f.close()
           
    def render(self, surf, offset=(0, 0)):
        
        # off grid tiles
        for tile in self.offgrid_tiles:
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))
        
        # on grid tiles
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))