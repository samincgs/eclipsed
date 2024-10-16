import pygame
import os

IMG_BASE_PATH = 'data/images/'

def load_image(path, colorkey=(0,0,0), alpha=False):
    img = pygame.image.load(IMG_BASE_PATH + path).convert_alpha() if alpha else pygame.image.load(IMG_BASE_PATH + path).convert()
    img.set_colorkey((colorkey))
    return img

def load_images(path, colorkey=(0, 0, 0)):
    img_list = []
    
    for img_name in os.listdir(IMG_BASE_PATH + path):
        img = load_image(path=f'{path}/{img_name}', colorkey=colorkey)
        img_list.append(img)
    return img_list

def clip(surf, x, y, x_size, y_size):
    handle_surf = surf.copy()
    clipped_rect = pygame.Rect(x, y, x_size, y_size)
    handle_surf.set_clip(clipped_rect)
    image = surf.subsurface(handle_surf.get_clip())
    return image.copy()

def palette_swap(surf, old_color, new_color):
    img_copy = surf.copy()
    img_copy.fill(new_color)
    surf.set_colorkey(old_color)
    img_copy.blit(surf, (0, 0))
    return img_copy
    