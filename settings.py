import math


WIDTH = 1024
HEIGHT = 768
PENTA_HIGHT = 5 * HEIGHT
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2


FPS = 30
FPS_POS = (WIDTH-65, 5)

TILE = 50

#raycast settings
FOV = math.pi / 3
HALF_FOV = FOV / 2
NUM_RAYS = 256
MAX_DEPTH = 200
DELTA_ANGEL = FOV / NUM_RAYS
DIST = NUM_RAYS / (2 * math.tan(HALF_FOV))
PROJ_COEFF = 3 * DIST * TILE
SCALE = WIDTH // NUM_RAYS



# map settings
MINIMAP_SCALE = 5
MINIMAP_RES = (WIDTH // MINIMAP_SCALE, HEIGHT // MINIMAP_SCALE)

MAP_SCALE = 2 * MINIMAP_SCALE
MAP_TILE = TILE // (MAP_SCALE)
MINI_MAP_POS = (0, HEIGHT - HEIGHT // MINIMAP_SCALE)


# player_pos = (HALF_WIDTH, HALF_HEIGHT)
player_angle = 0
player_speed = 4

#Zombie params
zombie_speed_running = 5
zombie_speed_walk = 2


BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
SKY_BLUE = (100, 191, 230)
DARK_GRAY = (169, 169, 169)
YELLOW = (220, 220, 0)
PUPLE = (120, 0, 120)
FLOOR_COLOR = (212, 83, 25)