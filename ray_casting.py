from settings import *
import pygame
from map import world_map, WORLD_WIDHT, WORLD_HEIGHT
# from mob import Zombie


def mapping(a, b):
    return (a // TILE) * TILE, (b // TILE) * TILE


def ray_casting_player(display, player_pos, player_angel):
    xo, yo = player_pos
    xm, ym = mapping(xo, yo)
    cur_angle = player_angel - HALF_FOV
    for ray in range(NUM_RAYS):
        sin_a = math.sin(cur_angle)
        cos_a = math.cos(cur_angle)

        x, dx = (xm + TILE, 1) if cos_a >= 0 else (xm, -1)
        for i in range(0, WORLD_WIDHT, TILE):
            depth_v = (x - xo) / cos_a
            y = yo + depth_v * sin_a
            if mapping(x + dx, y) in world_map:
                break
            x += dx * TILE

        y, dy = (ym + TILE, 1) if sin_a >= 0 else (ym, -1)
        for i in range(0, WORLD_HEIGHT, TILE):
            depth_h = (y - yo) / sin_a
            x = xo + depth_h * cos_a
            if mapping(x, y + dy) in world_map:
                break

            y += dy * TILE

        depth = depth_v if (depth_v < depth_h) else depth_h

        depth *= math.cos(player_angel - cur_angle)
        depth = max(depth, 0.0000001)
        proj_height = min(int(PROJ_COEFF / depth), PENTA_HIGHT)

        pygame.draw.rect(display, RED, (ray * SCALE, HALF_HEIGHT - proj_height // 2, SCALE, proj_height))

        c = 255 / (1 + depth * depth * 0.000002)
        color = (c // 2, c // 2, c // 2)
        pygame.draw.rect(display, color, (ray * SCALE, HALF_HEIGHT - proj_height // 2, SCALE, proj_height))
        cur_angle += DELTA_ANGEL


# def ray_casting_mob(mob: Zombie):
#     xo, yo = mob.get_pos
#     xm, ym = mapping(xo, yo)
#     cur_angle = mob.angle
#     for ray in range(NUM_RAYS):
#         sin_a = math.sin(cur_angle)
#         cos_a = math.cos(cur_angle)
#         x, dx = (xm + TILE, 1) if cos_a >= 0 else (xm, -1)
#         for i in range(0, WORLD_WIDHT, TILE):
#             depth_v = (x - xo) / cos_a
#             y = yo + depth_v * sin_a
#             if mapping(x + dx, y) == mapping(player.get_pos):
#                 print(1)
#                 break
#             if mapping(x + dx, y) in world_map:
#                 break
#             x += dx * TILE
#
#         y, dy = (ym + TILE, 1) if sin_a >= 0 else (ym, -1)
#         for i in range(0, WORLD_HEIGHT, TILE):
#             depth_h = (y - yo) / sin_a
#             x = xo + depth_h * cos_a
#             if mapping(x, y + dy) == mapping(player.get_pos):
#                 print(1)
#                 break
#             if mapping(x, y + dy) in world_map:
#                 break
#
#
#         depth = depth_v if (depth_v < depth_h) else depth_h
#
#         depth *= math.cos(mob.angle - cur_angle)
#         depth = max(depth, 0.0000001)



