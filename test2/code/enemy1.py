import pygame
from setting import *
from convertFunc import *
from player import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self,monster_name,pos,groups,collision_sprites):
        super().__init__(groups)
        self.frame_index = 0
        self.sprite_type='enemy'
        self.direction=pygame.math.Vector2()
        self.import_assets()
        self.status='down_idle'
        self.image=self.animations[self.status][self.frame_index]
        self.rect=self.image.get_rect(center=pos)
        self.z=LAYERS['main']
        self.pos=pygame.math.Vector2(self.rect.center)
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.75, -self.rect.height * 0.55)
        self.collision_sprites = collision_sprites

        self.monster_name=monster_name
        monster_info=monster_data[self.monster_name]
        self.health=monster_info['health']
        self.speed=monster_info['speed']
        self.attack_damage=monster_info['damage']
        self.attackRange=monster_info['attackRange']
        self.AlertRange=monster_info['AlertRange']

    def import_assets(self):
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
                           'right_spear': [], 'left_spear': [], 'up_spear': [], 'down_spear': [],
                           'right_axe': [], 'left_axe': [], 'up_axe': [], 'down_axe': [],
                           'right_flail': [], 'left_flail': [], 'up_flail': [], 'down_flail': []}

        for animation in self.animations.keys():
            full_path = '../graphics/character/' + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self,dt):
        self.frame_index+=3*dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index =0
        self.image=self.animations[self.status][int(self.frame_index)]


    def collision(self, direction):
        for sprite in self.collision_sprites.sprites():
            if hasattr(sprite, 'hitbox'):
                if sprite.hitbox.colliderect(self.hitbox):
                    if direction == 'horizontal':
                        if self.direction.x > 0:
                            self.hitbox.right = sprite.hitbox.left
                        if self.direction.x < 0:
                            self.hitbox.left = sprite.hitbox.right
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx

                    if direction == 'vertical':
                        if self.direction.y > 0:
                            self.hitbox.bottom = sprite.hitbox.top
                        if self.direction.y < 0:
                            self.hitbox.top = sprite.hitbox.bottom
                        self.rect.centery= self.hitbox.centery
                        self.pos.y = self.hitbox.centery

    def move(self):

        #normalizing vector
        if self.direction.magnitude() >0:
            self.direction=self.direction.normalize()

        #horizontal movement
        self.pos.x+=self.direction.x*self.speed
        self.hitbox.centerx = round(self.pos.x)# round is necessary cause python will round the number to to lowerest integer
        self.rect.centerx = self.hitbox.centerx
        self.collision('horizontal')


        #vertical movement
        self.pos.y+=self.direction.y*self.speed
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self.collision('vertical')

    def update(self,dt):
        self.move()
        self.animate(dt)




    def get_playerdirection(self,player):
        enemy_vec=pygame.math.Vector2(self.rect.center)
        player_vec=pygame.math.Vector2(player.rect.center)
        distance=(player_vec-enemy_vec).magnitude()
        if distance>0:
            direction=(player_vec-enemy_vec).normalize()
            # self.direction=(player_vec-enemy_vec).normalize()
        else:
            direction=pygame.math.Vector2()
            # self.direction=pygame.math.Vector2()
        return(distance,direction)

    def get_status(self,player):
        distance= self.get_playerdirection(player)[0]
        if distance <= 200:
            # print('attack radius')
            print(self.pos.x)
            self.status = self.status.split("_" )[0]+'_spear'
            print(self.direction)
        elif distance<=400:
            # print('notice radius')
            self.status = self.status.split("_" )[0]+'_idle'
        else:
            self.status = self.status.split("_" )[0]+'_idle'


    def actions(self,player):
        if self.status=='attack':
            print('attack')
        elif self.status=='down_idle':
            print('move')
            self.direction=self.get_playerdirection(player)[1]
            self.move()
        else:
            self.direction=pygame.math.Vector2()

    def OverlapWithEnemy(self,player):
        outlineEnemy = self.rect.inflate(-100, -100)
        outlinePlayer = player.rect.inflate(-100, -100)
        if outlineEnemy.colliderect(outlinePlayer):
            player.kill()




    def enemy_update(self,player):
        print(self.status)
        self.get_status(player)
        self.actions(player)
        self.OverlapWithEnemy(player)

    # def get_status(self,player):
    #     distance= self.get_playerdirection(player)[0]
    #     if distance <= 20:
    #         # print('attack radius')
    #         print(self.pos.x)
    #         self.status = self.status.split("_" )[0]+'_spear'
    #         print(self.direction)
    #     elif distance<=40:
    #         # print('notice radius')
    #         self.status = self.status.split("_" )[0]+'_idle'
    #     else:
    #         self.status = self.status.split("_" )[0]+'_idle'
