from settings import *
# from mob import Zombie
import pygame

matrix_map=[
    'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW',
    'W........W..W.............W....W',
    'W..WWWW..W.....WWWW..WWWWWWWW..W',
    'W..W..W..W..WWWW..W..W......W..W',
    'W..W..WWWW..W..W..W..W......W..W',
    'W..W..0.....W..W..W..W..WW..W..W',
    'W..W........W........W...W.....W',
    'W..WWWW..W..W........W...W.....W',
    'W.....W..W..W..W..W..W...W..W..W',
    'W.....W..W..W..W..W..WWWWW..W..W',
    'W..WWWW..WWWW..W..W.........W..W',
    'W...........................W..W',
    'W........................W..W..W',
    'W..WWWWWWWWW..WWWWWWWWWWWW..WWWW',
    'W.....W...........W..WW........W',
    'W.....W...........W..WW........W',
    'W..W..WWW..WWWWWWWW..WW..WWWW..W',
    'W..W.......W......W......W..W..W',
    'W..W.......W......W......W..W..WWWWW',
    'W..WWWWW..WWWW..WWW..WWWWW..W.......',
    'W.....W..................W.....WWWWW',
    'W.....W..................W.....W',
    'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW',

]

MAP_SCALE = (len(matrix_map) * TILE, len(matrix_map[0]) * TILE)
print(MAP_SCALE)
WORLD_WIDHT = len(matrix_map[0]) * TILE
WORLD_HEIGHT = len(matrix_map) * TILE
world_map = set()
mini_map = set()
collision_walls = []
# mobs = []
for j, row in enumerate(matrix_map):
    for i, char in enumerate(row):
        if char == 'W':
            collision_walls.append(pygame.Rect(i * TILE, j * TILE, TILE, TILE))
            world_map.add((i * TILE, j * TILE))
            mini_map.add((i * MAP_TILE, j * MAP_TILE))
        if char == '0':
            player_pos = (i * TILE + TILE // 2, j * TILE + TILE // 2)
        # if char == '1':
        #     mobs.append(Zombie((i * TILE + TILE // 2, j * TILE + TILE // 2)))