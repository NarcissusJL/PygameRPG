from pygame.math import Vector2
# screen
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
TILE_SIZE = 64

# overlay positions
OVERLAY_POSITIONS = {
	'weapon' : (40, SCREEN_HEIGHT - 15),
	}

PLAYER_weapon_OFFSET = {
	'left': Vector2(-50,40),
	'right': Vector2(50,40),
	'up': Vector2(0,-10),
	'down': Vector2(0,50)
}


LAYERS = {
	'ground': 0,
	'enemy': 1,
	'treasure': 2,
	'keys': 3,
	'Walls': 4,
	'Gates': 5,
	'Collision_Obj': 6,
	'main' : 7,
	'torch' : 8
}

monster_data={
	'Demon':{'health':100,'damage':20,'speed':0.4,'attackRange':10,'AlertRange':20,'feedback':2}
}
