from .utils import load_img, load_imgs
from .animation import Animation
from .font import Font

IMG_PATH = 'data/images/'

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
        self.assets['player/'] =  Animation(images=[load_img(IMG_PATH + 'entities/player/0.png', (0, 0, 0))])
        self.assets['player/jump'] =  Animation(images=load_imgs(IMG_PATH + 'entities/player/jump',(0, 0, 0)))
        self.assets['player/walk'] = Animation(images=load_imgs(IMG_PATH + 'entities/player/walk', (0, 0, 0)))
        self.assets['slime/'] = Animation(images=[load_img(IMG_PATH + 'entities/enemy/slime/0.png', (0, 0, 0))])
        
    def load_tiles(self): 
        self.assets['bricks'] =  load_imgs(IMG_PATH +'tiles/bricks', (0, 0, 0))
        self.assets['decor'] = load_imgs(IMG_PATH +'tiles/decor', (0, 0, 0))
        self.assets['spawners'] = load_imgs(IMG_PATH +'tiles/spawners', (0, 0, 0))
        
    def load_font(self):
        self.assets['small_font'] = Font('data/fonts/main_font.png', (255, 255, 255))
        # self.assets['large_font'] = Font('data/fonts/large_font.png')
        
    def load_misc(self):
        self.assets['gun'] = load_img(IMG_PATH +'gun.png', (0, 0, 0))
        self.assets['gun_ui'] = load_img(IMG_PATH +'gun_ui.png', (0, 0, 0))
        self.assets['projectile'] = load_img(IMG_PATH +'projectile.png', (0, 0, 0))
        self.assets['heart'] = load_img(IMG_PATH +'heart.png', (0, 0, 0))
        self.assets['minimap'] = load_img(IMG_PATH +'minimap.png', (0, 0, 0))
        self.assets['particles/star'] = load_imgs(IMG_PATH +'particles/stars', (0, 0, 0))
            
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