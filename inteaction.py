from settings import *
from map import world_map, matrix_map
from ray_casting import mapping
import math
import pygame
from sprite_objects import *
from numba import njit
from BFS import *

@njit(fastmath=True, cache=True)
def ray_casting_npc_player(npc_x, npc_y, world_map, player_pos):
    ox, oy = player_pos
    xm, ym = mapping(ox, oy)
    delta_x, delta_y = ox - npc_x, oy - npc_y
    cur_angle = math.atan2(delta_y, delta_x)
    cur_angle += math.pi

    sin_a = math.sin(cur_angle)
    sin_a = sin_a if sin_a else 0.000001
    cos_a = math.cos(cur_angle)
    cos_a = cos_a if cos_a else 0.000001

    # verticals
    x, dx = (xm + TILE, 1) if cos_a >= 0 else (xm, -1)
    for i in range(0, int(abs(delta_x)) // TILE):
        depth_v = (x - ox) / cos_a
        yv = oy + depth_v * sin_a
        tile_v = mapping(x + dx, yv)
        if tile_v in world_map:
            return False
        x += dx * TILE

    # horizontals
    y, dy = (ym + TILE, 1) if sin_a >= 0 else (ym, -1)
    for i in range(0, int(abs(delta_y)) // TILE):
        depth_h = (y - oy) / sin_a
        xh = ox + depth_h * cos_a
        tile_h = mapping(xh, y + dy)
        if tile_h in world_map:
            return False
        y += dy * TILE
    return True


class Interaction:
    def __init__(self, player, sprites, drawing):
        self.player = player
        self.sprites = sprites
        # print(self.sprites)
        self.drawing = drawing
        self.go_to_player = False
        self.minotaur = self.sprites.list_of_objects[[_.flag for _ in self.sprites.list_of_objects].index('npc')]

    def minotaur_objects(self):
        for obj in sorted(self.sprites.list_of_objects, key=lambda obj: obj.distance_to_sprite):
            if ray_casting_npc_player(obj.x, obj.y,
                                      world_map, self.player.pos):
                if obj.flag == 'npc':
                    self.go_to_player = True
                    self.last_player_pos = [int(_ // 50) for _ in mapping(*self.player.pos)]
                    # self.minotaur = obj
        try:
            self.minotaur_move()
        except AttributeError:
            pass
        # self.go_to_player = False

    def minotaur_move(self):
        way = []
        if not self.go_to_player:
            # pass
            start = [int(_ // 50) for _ in
                     mapping(*list(*[obj.pos for obj in self.sprites.list_of_objects if obj.flag == 'npc']))]
            way = return_way(matrix_map, start=start)
            # print(way)
        else:
            start = [int(_ // 50) for _ in
                     mapping(*list(*[obj.pos for obj in self.sprites.list_of_objects if obj.flag == 'npc']))]
            # print(self.last_player_pos)
            near_TILE = [tuple[self.last_player_pos[0] + _[0], self.last_player_pos[1] + _[1]]
                         for _ in [[-1, 0], [0, -1], [1, 0], [0, 1]]]
            if start not in [self.last_player_pos] + near_TILE:
                way = return_way(matrix_map, start=start, finish=self.last_player_pos)
            else:
                self.last_player_pos = (-1, -1)
                self.go_to_player = False
        if way:
            try:
                # print(way[0], way[1])
                if way[0][0] > way[1][0]:
                    self.minotaur.x -= 1.5
                elif way[0][0] < way[1][0]:
                    self.minotaur.x += 1.5
                elif way[0][1] > way[1][1]:
                    self.minotaur.y -= 1.5
                elif way[0][1] < way[1][1]:
                    self.minotaur.y += 1.5
            except IndexError:
                if self.go_to_player:
                    dx = self.minotaur.x - self.player.pos[0]
                    dy = self.minotaur.y - self.player.pos[1]
                    self.minotaur.x = self.minotaur.x + 1 if dx < 0 else self.minotaur.x - 1
                    self.minotaur.y = self.minotaur.y + 1 if dy < 0 else self.minotaur.y - 1
                else:
                    pass