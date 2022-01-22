from settings import *
import pygame
from numba.core import types
from numba.typed import Dict
from numba import int32
from sprite_objects import *

_ = False
matrix_map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, _, _, _, _, _, 1, _, _, _, _, _, _, _, _, _, _, 1, _, _, _, _, _, 1],
    [1, _, 1, 1, _, _, _, _, _, 1, 1, 1, _, _, _, 1, _, _, _, _, 1, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, 1, 1, _, _, _, 1, _, _, _, _, _, _, 1],
    [1, _, 1, 1, _, _, _, _, _, _, _, _, 1, _, 1, _, _, 1, _, _, _, 1, _, 1],
    [1, _, _, _, _, _, 1, _, _, 1, 1, _, 1, _, _, _, _, _, _, 1, _, _, _, 1],
    [1, _, 1, _, _, _, 1, _, _, 1, _, _, 1, _, _, _, 1, _, _, _, _, 1, _, 1],
    [1, _, _, 1, _, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, 1, _, _, _, _, _, _, _, 1, _, _, 1, 1, _, _, _, _, 1, 1, _, _, 1],
    [1, _, 1, _, _, _, 1, 1, _, 1, _, _, _, 1, 1, _, _, _, _, 'P', 1, _, _, 1],
    [1, _, _, _, _, 1, _, 1, _, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, 1, _, 1, _, _, _, _, 1, _, _, 1, _, _, _, _, _,  _, _, _, 1, _, 1],
    [1, _, _, _, _, _, 1, _, _, _, _, _, 1, 1, _, _, _, _, _, _, 1, 1, _, 1],
    [1, _, _, 1, _, _, _, _, 1, _, _, _, _, 1, 1, 1, 1, 1, 1, 1, 1, _, _, _],
    [1, _, _, _, _, _, _, _, _, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]



WORLD_WIDTH = len(matrix_map[0]) * TILE
WORLD_HEIGHT = len(matrix_map) * TILE
world_map = Dict.empty(key_type=types.UniTuple(int32, 2), value_type=int32)
mini_map = set()
collision_walls = []
for j, row in enumerate(matrix_map):
    for i, char in enumerate(row):
        if char:
            collision_walls.append(pygame.Rect(i * TILE, j * TILE, TILE, TILE))
            if char == 1:
                world_map[(i * TILE, j * TILE)] = 1
            elif char == 'P':
                world_map[(i * TILE, j * TILE)] = 1
                player_pos = ((i - 1) * TILE, (j * TILE))
            elif char == 'K':
                print(i * TILE, (j * TILE))
                Sprites.list_of_objects.append(SpriteObject(Sprites.sprite_parameters['sprite_key'], (i * TILE + 0.1, j * TILE + 0.1)))
                print(Sprites.list_of_objects)