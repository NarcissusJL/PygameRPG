import pygame
from setting import*
from convertFunc import*
from timer import Timer

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,group,collision_sprites):
        super().__init__(group)

        self.import_assets()
        self.status='down_idle'
        self.frame_index=0
        #general setup
        self.image=self.animations[self.status][self.frame_index]
        # self.image.fill('green')
        self.rect=self.image.get_rect(center=pos)
        self.z=LAYERS['main']

        #Collision Use
        # self.hitbox = self.rect.copy()
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.75, -self.rect.height * 0.55)
        # self.hitbox =
        self.collision_sprites = collision_sprites

        # movement attributes
        self.direction=pygame.math.Vector2()
        self.pos=pygame.math.Vector2(self.rect.center)
        self.speed=250

        #timers
        self.timers={
            'weapon use':Timer(350,self.use_weapon),
            'weapon switch': Timer(200),
        }


        # weapons
        self.weapons = ['spear', 'axe', 'flail']
        self.weapon_index = 0
        self.selected_weapon = self.weapons[self.weapon_index]



    def use_weapon(self):
        print("using weapon")



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

    def input(self):
        keys=pygame.key.get_pressed()
        if not self.timers['weapon use'].active:
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.direction.y=-1
                self.status='up'
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.direction.y=1
                self.status='down'
            else:
                self.direction.y=0

            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.direction.x = 1
                self.status='right'
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.direction.x=-1
                self.status='left'
            else:
                self.direction.x=0


            #weapon use
            if keys[pygame.K_SPACE] or keys[pygame.K_e]:
                self.timers['weapon use'].activate()
                self.direction=pygame.math.Vector2()
                self.frame_index=0

            # change weapon
            if keys[pygame.K_q] and not self.timers['weapon switch'].active:
                self.timers['weapon switch'].activate()
                self.weapon_index += 1
                self.weapon_index = self.weapon_index if self.weapon_index < len(self.weapons) else 0
                self.selected_weapon = self.weapons[self.weapon_index]




# check if the player is moving or not
    def get_status(self):
        if self.direction.magnitude() ==0:
            self.status = self.status.split("_" )[0]+'_idle'

        #weapon use
        if self.timers['weapon use'].active:
            self.status=self.status.split("_")[0]+'_'+self.selected_weapon

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()


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





    def move(self,dt):

        #normalizing vector
        if self.direction.magnitude() >0:
            self.direction=self.direction.normalize()

        #horizontal movement
        self.pos.x+=self.direction.x*self.speed*dt
        self.hitbox.centerx = round(self.pos.x)# round is necessary cause python will round the number to the lowest integer
        # self.rect.centerx = self.hitbox.centerx
        self.collision('horizontal')
        self.rect.centerx = self.hitbox.centerx


        #vertical movement
        self.pos.y+=self.direction.y*self.speed*dt
        self.hitbox.centery = round(self.pos.y)
        # self.rect.centery = self.hitbox.centery
        self.collision('vertical')
        self.rect.centery = self.hitbox.centery


    def update(self,dt):
        self.input()
        self.get_status()
        self.update_timers()
        self.move(dt)
        self.animate(dt)
