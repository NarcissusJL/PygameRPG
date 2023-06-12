import pygame
from setting import *

class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z=LAYERS['main']):
        super().__init__(groups)
        self.image=surf
        self.rect=self.image.get_rect(topleft=pos)
        self.z=z
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.5, -self.rect.height * 0.8)

class Treasure(Generic):
    def __init__(self, pos, frames, groups):

        #animations
        self.frame = frames
        self.frame_index = 0

        super().__init__(pos = pos, surf = self.frame[self.frame_index], groups = groups, z=LAYERS['treasure'])

        #collision

        self.hitbox = self.rect.copy().inflate(-13,-13)


    def update(self,dt):
        self.frame_index+=5 * dt
        if self.frame_index >= len(self.frame):
            self.frame_index = 0
        self.image = self.frame[int(self.frame_index)]

class Keys(Generic):
    def __init__(self, pos, frames, groups):

        #animations
        self.frame = frames
        self.frame_index = 0

        super().__init__(pos = pos, surf = self.frame[self.frame_index], groups = groups, z=LAYERS['keys'])

    def update(self,dt):
        self.frame_index+=4 * dt
        if self.frame_index >= len(self.frame):
            self.frame_index = 0
        self.image = self.frame[int(self.frame_index)]

class Torch(Generic):
        def __init__(self, pos, frames, groups):

            #animations
            self.frame = frames
            self.frame_index = 0

            super().__init__(pos = pos, surf = self.frame[self.frame_index], groups = groups, z=LAYERS['torch'])

        def update(self,dt):
            self.frame_index+=4 * dt
            if self.frame_index >= len(self.frame):
                self.frame_index = 0
            self.image = self.frame[int(self.frame_index)]

# class Gate(Generic):
#     super().__init__(groups)
