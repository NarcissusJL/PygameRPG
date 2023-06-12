import pygame
from setting import *
class Overlay:
	def __init__(self,player):

		# general setup
		self.display_surface = pygame.display.get_surface()
		self.player = player

		# imports
		overlay_path = '../graphics/overlay/'
		self.weapons_surf = {weapon: pygame.image.load(f'{overlay_path}{weapon}.png').convert() for weapon in player.weapons}


	def display(self):

		# weapon
		weapon_surf = self.weapons_surf[self.player.selected_weapon]
		weapon_rect = weapon_surf.get_rect(midbottom = OVERLAY_POSITIONS['weapon'])
		self.display_surface.blit(weapon_surf,weapon_rect)
