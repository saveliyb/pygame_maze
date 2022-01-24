from settings import *
from map import world_map, world_map_for_minotaur
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
        self.lose = False
        self.see = False
        # self.see_drawning = False
        self.see_sound_flag = False
        self.see_sound = pygame.mixer.Sound('sound/see.wav')
        self.way_flag = True
        self.LEFT, self.RIGHT, self.TOP, self.BOTTOM = False, False, False, False

    def minotaur_objects(self):
        for obj in sorted(self.sprites.list_of_objects, key=lambda obj: obj.distance_to_sprite):
            if ray_casting_npc_player(obj.x, obj.y,
                                      world_map, self.player.pos):
                if obj.flag == 'npc':
                    self.go_to_player = True
                    self.last_player_pos = [int(_ // 50) for _ in mapping(*self.player.pos)]
                    if not self.see:
                        self.see_sound_flag = True
                    self.see = True
            else:
                if obj.flag == 'npc':
                    self.see = False



        try:
            self.minotaur_move()
        except AttributeError:
            pass

        # self.go_to_player = False

    def minotaur_move(self):
        way = []
        start = [int(_ // 50) for _ in mapping(*[self.minotaur.x, self.minotaur.y])]
        if not self.go_to_player:
            # pass
            # start = [int(_ // 50) for _ in
            #          mapping(*list(*[obj.pos for obj in self.sprites.list_of_objects if obj.flag == 'npc']))]
            way = return_way(matrix_map, start=start)

        else:
            # start = [int(_ // 50) for _ in
            #          mapping(*list(*[obj.pos for obj in self.sprites.list_of_objects if obj.flag == 'npc']))]
            # print(self.last_player_pos)
            near_TILE = [tuple[self.last_player_pos[0] + _[0], self.last_player_pos[1] + _[1]]
                         for _ in [[-1, 0], [0, -1], [1, 0], [0, 1]]]
            if start not in [self.last_player_pos] + near_TILE:
                way = return_way(matrix_map, start=start, finish=self.last_player_pos)
            else:
                self.last_player_pos = (-1, -1)
                self.go_to_player = False
        # print(way)
        # way = [(_[0] * TILE + TILE // 2, _[1] * TILE + TILE // 2) for _ in way]
        # print(way)
        if way:

            # way_start = 0

            try:
                # if not way_start:
                #     way_start = way[0]
                # else:
                #     if self.LEFT
                # print(way[0], way[1])
                # print(way[0][0] * TILE + TILE //2)
                print(self.LEFT, self.RIGHT, self.TOP, self.BOTTOM, self.way_flag, way)
                if self.way_flag:
                    # print(way[0][1] > way[1][1])
                    if way[0][0] > way[1][0]:
                        self.minotaur.x -= self.minotaur.speed
                        # self.LEFT = True
                        # self.way_flag = False
                    elif way[0][0] < way[1][0]:
                        self.minotaur.x += self.minotaur.speed
                        # self.RIGHT = True
                        # self.way_flag = False
                    elif way[0][1] > way[1][1]:
                        # self.TOP = True
                        # self.way_flag = False
                        self.minotaur.y -= self.minotaur.speed
                    elif way[0][1] < way[1][1]:
                        self.minotaur.y += self.minotaur.speed
                        # self.BOTTOM = True
                        # self.way_flag = False
                # else:
                #     # print(way[0][1] * TILE + TILE // 2,  way[1][1] * TILE)
                #     if self.LEFT:
                #         print(way[0][0] * TILE - TILE // 2, way[1][0] * TILE)
                #         if way[0][0] * TILE - TILE // 2 > way[1][0] * TILE:
                #             self.minotaur.x -= 2
                #         else:
                #             self.LEFT = False
                #             self.way_flag = True
                #     elif self.RIGHT:
                #         if way[0][0] * TILE + TILE // 2 < way[1][0] * TILE:
                #             self.minotaur.x += 2
                #         else:
                #             self.RIGHT = False
                #             self.way_flag = True
                #     elif self.TOP:
                #         print('self.TOP')
                #         if way[0][1] * TILE - TILE // 2 > way[1][1] * TILE:
                #             self.minotaur.y -= 2
                #         else:
                #             self.TOP = False
                #             self.way_flag = True
                #     elif self.BOTTOM:
                #         if way[0][1] * TILE + TILE // 2 < way[1][1] * TILE:
                #             self.minotaur.x += 2
                #         else:
                #             self.BOTTOM = False
                #             self.way_flag = True


            except IndexError:
                print('ERROR')
                if self.go_to_player:
                    dx = self.minotaur.x - self.player.pos[0]
                    dy = self.minotaur.y - self.player.pos[1]
                    self.minotaur.x = self.minotaur.x + 1 if dx < 0 else self.minotaur.x - 1
                    self.minotaur.y = self.minotaur.y + 1 if dy < 0 else self.minotaur.y - 1
                else:
                    pass

        if [int(_ // 50) for _ in mapping(self.minotaur.x, self.minotaur.y)] == \
                [int(_ // 50) for _ in mapping(*self.player.pos)]:
            self.lose = True
        self.k = 0
        self.minotaur_pos = [int(_) for _ in mapping(self.minotaur.x, self.minotaur.y)]
        self.check()

    def check(self):
        # print(self.minotaur_pos)
        for _ in [-0.2, -0.1, 0, 0.1, 0.2]:
            try:
                if world_map_for_minotaur[tuple([k + _ for k in self.minotaur_pos])] == 1:
                    if world_map_for_minotaur[tuple([int(_) for _ in mapping(self.minotaur.x + self.k, self.minotaur.y)])] == 0:
                        self.minotaur.x += self.k
                        self.k = 0
                    elif world_map_for_minotaur[tuple([int(_) for _ in mapping(self.minotaur.x - self.k, self.minotaur.y)])] == 0:
                        self.minotaur.x -= self.k
                        self.k = 0
                    elif world_map_for_minotaur[tuple([int(_) for _ in mapping(self.minotaur.x, self.minotaur.y + self.k)])] == 0:
                        self.minotaur.y += self.k
                        self.k = 0
                    elif world_map_for_minotaur[tuple([int(_) for _ in mapping(self.minotaur.x, self.minotaur.y - self.k)])]  == 0:
                        self.minotaur.y -= self.k
                        self.k = 0
                    else:
                        self.k += 0.2

            except KeyError:
                pass

    def see_music(self):
        # pygame.mixer.music.load('sound/see.wav')
        if self.see_sound_flag:
            self.see_sound.play()
            self.see_sound_flag = False

    def play_music(self):
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        pygame.mixer.music.load('sound/theme.wav')
        pygame.mixer.music.play(10)