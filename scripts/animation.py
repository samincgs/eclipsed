class Animation:
    def __init__(self, images, img_dur=5, loop=True):
        self.images = images
        self.img_dur = img_dur
        self.loop = loop
        
        self.frame = 0
    
    @property
    def img(self):
        return self.images[int(self.frame / self.img_dur)]
    
    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (len(self.images) * self.img_dur)
        else:
            self.frame = min(self.frame + 1, (len(self.images) * self.img_dur - 1))
        