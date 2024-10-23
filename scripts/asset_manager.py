from .utils import load_image, load_images
from .animation import Animation
from .font import Font

class AssetManager:
    def __init__(self):
        self.assets = {}
        
        self.load_sprites()
        self.load_tiles()
        self.load_font()
        self.load_misc()
        
    @property
    def load_assets(self):
        return self.assets
        
    def load_sprites(self):
        self.assets['player/'] =  Animation(images=[load_image('entities/player/0.png')])
        self.assets['player/jump'] =  Animation(load_images('entities/player/jump'))
        self.assets['player/walk'] = Animation(load_images('entities/player/walk'), img_dur=5)
        self.assets['slime/'] = Animation(images=[load_image('entities/enemy/slime/0.png')])
        
    def load_tiles(self):
        self.assets['bricks'] =  load_images('tiles/bricks')
        self.assets['decor'] = load_images('tiles/decor')
        self.assets['spawners'] = load_images('tiles/spawners')
        
    def load_font(self):
        self.assets['small_font'] = Font('data/fonts/small_font.png', (255, 255, 255))
        self.assets['large_font'] = Font('data/fonts/large_font.png')
        
    def load_misc(self):
        self.assets['gun'] = load_image('gun.png')
        self.assets['gun_ui'] = load_image('gun_ui.png')
        self.assets['projectile'] = load_image('projectile.png')
        self.assets['heart'] = load_image('heart.png')
        self.assets['particles/star'] = load_images('particles/stars')
            
    def __repr__(self):
        return repr(self.assets)
    
   # self.assets = {
        #     'player/': Animation(images=[load_image('entities/player/0.png')]),
        #     'player/jump': Animation(load_images('entities/player/jump')),
        #     'player/walk': Animation(load_images('entities/player/walk'), img_dur=5),
        #     'slime/': Animation(images=[load_image('entities/enemy/slime/0.png')]),
        #     'bricks': load_images('tiles/bricks'),
        #     'decor': load_images('tiles/decor'),
        #     'spawners': load_images('tiles/spawners'),
        #     'gun': load_image('gun.png'),
        #     'gun_ui': load_image('gun_ui.png'),
        #     'projectile': load_image('projectile.png'),
        #     'small_font': Font('data/fonts/small_font.png', (255, 255, 255)),
        #     'large_font': Font('data/fonts/large_font.png'),
        # }