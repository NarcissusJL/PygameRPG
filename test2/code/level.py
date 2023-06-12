import pygame
from setting import *
from player import Player
from sprites import Generic, Treasure, Keys, Torch
from overlay import Overlay
from enemy1 import Enemy
from convertFunc import *
from pytmx.util_pygame import load_pygame

class Level:
    def __init__(self):
        self.display_surface=pygame.display.get_surface()

        self.all_Sprites=CameraGroup()
        self.collision_Sprites = pygame.sprite.Group()

        self.initiate()

        self.overlay = Overlay(self.player)

    def initiate(self):
        tmx_map = load_pygame('../graphics/dungeon.tmx')

        # Walls
        for x,y,surface in tmx_map.get_layer_by_name('Walls').tiles():
            Generic((x * TILE_SIZE , y* TILE_SIZE), surface, [self.all_Sprites, self.collision_Sprites], LAYERS['Walls'])

        #Ground
        for x,y,surface in tmx_map.get_layer_by_name('Ground').tiles():
            Generic((x * TILE_SIZE , y* TILE_SIZE), surface, self.all_Sprites, LAYERS['ground'])

        #Treasure
        treasure_Frame = import_folder('../graphics/chest_idle')
        for x,y,surface in tmx_map.get_layer_by_name('treasure').tiles():
            Treasure((x * TILE_SIZE , y* TILE_SIZE), treasure_Frame, [self.all_Sprites, self.collision_Sprites])

        #Keys
        key_Frame = import_folder('../graphics/key_idle')
        for x,y,surface in tmx_map.get_layer_by_name('keys').tiles():
            Keys((x * TILE_SIZE , y* TILE_SIZE), key_Frame, [self.all_Sprites, self.collision_Sprites])


        #Torch
        torch_Frame = import_folder('../graphics/torch_idle')
        for x,y,surface in tmx_map.get_layer_by_name('collision objects').tiles():
            Torch((x * TILE_SIZE , y* TILE_SIZE), torch_Frame, [self.all_Sprites, self.collision_Sprites])


        #Gates
        for x,y,surface in tmx_map.get_layer_by_name('Gates').tiles():
            Generic((x * TILE_SIZE , y* TILE_SIZE), surface, [self.all_Sprites, self.collision_Sprites], LAYERS['Gates'])




        #Player
        self.player = Player((1000,800),self.all_Sprites, self.collision_Sprites)
        # self.enemy = Enemy('Demon',(800,1000),self.all_Sprites)

        #Enemy Groups
        self.enemy1 = Enemy('Demon',(800,1000),self.all_Sprites, self.collision_Sprites)
        self.enemy2 = Enemy('Demon',(700,1000),self.all_Sprites, self.collision_Sprites)
        self.enemy3 = Enemy('Demon',(800,1100),self.all_Sprites, self.collision_Sprites)
        self.enemy4 = Enemy('Demon',(600,600),self.all_Sprites, self.collision_Sprites)
        self.enemy5 = Enemy('Demon',(500,1000),self.all_Sprites, self.collision_Sprites)
        self.enemy6 = Enemy('Demon',(1100,600),self.all_Sprites, self.collision_Sprites)
        # for i in range(10):
        #     Enemy('Demon',(800,i*50),self.all_Sprites, self.collision_Sprites)

        # Generic(
        #     pos=(0,0),
        #         surf=pygame.image.load('../graphics/world/ground.png').convert(),
        #             groups=self.all_Sprites,
        #             z=LAYERS['ground'])


    def run(self,dt):
        self.display_surface.fill('black')
        self.all_Sprites.draw(self.display_surface)
        self.all_Sprites.custom_draw(self.player)
        self.all_Sprites.update(dt)
        self.all_Sprites.enemy_update(self.player)
        self.overlay.display()

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface=pygame.display.get_surface()
        self.offset=pygame.math.Vector2()

    def custom_draw(self,player):
        self.offset.x=player.rect.centerx-SCREEN_WIDTH/2
        self.offset.y=player.rect.centery-SCREEN_HEIGHT/2
        for layer in LAYERS.values():
            for sprite in self.sprites():
                if sprite.z==layer:
                    offset_rect=sprite.rect.copy()
                    offset_rect.center-=self.offset
                    self.display_surface.blit(sprite.image,offset_rect)


    def enemy_update(self,player):
        enemy_sprites=[sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type=='enemy']
        for sprite in enemy_sprites:
            sprite.enemy_update(player)
