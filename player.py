# from pprint import pprint

from settings import *
import pygame
import math
from map import collision_walls, player_pos, door


class Player:
    @property
    def key(self):
        return self._key

    def __init__(self, sprites):
        self.x, self.y = player_pos
        self.sprites = sprites
        self.angle = player_angle
        self.sensitivity = 0.004
        # collision parameters
        self.side = 20
        self.rect = pygame.Rect(*player_pos, self.side, self.side)
        self.key = 0
        self.iswining = 0


    @property
    def pos(self):
        return (self.x, self.y)

    @property
    def collision_list(self):
        return collision_walls + [pygame.Rect(*obj.pos, obj.side, obj.side) for obj in
                                  self.sprites if obj.blocked]

    def find_colision_object(self, list_objects: list, size: int):
        list_objects.reverse()
        for _ in list_objects:
            if _[-1] == size:
                return len(list_objects) - 1 - list_objects.index(_)

    def get_key(self):
        self.collision_list.remove(self.collision_list[self.find_colision_object(self.collision_list, 30)])
        del self.sprites[0]
        self.key = 1

    @property
    def iskey(self):
        return self.key

    @property
    def iswin(self):
        return self.iswining

    def detect_collision(self, dx, dy):
        next_rect = self.rect.copy()
        next_rect.move_ip(dx, dy)
        hit_indexes = next_rect.collidelistall(self.collision_list)

        if len(hit_indexes):
            delta_x, delta_y = 0, 0
            for hit_index in hit_indexes:
                # print(self.collision_list[hit_index][:])
                if self.collision_list[hit_index][:] == door:
                    if self.key:
                        self.iswining = 1
                if self.collision_list[hit_index][2] == 30:
                    self.get_key()
                try:
                    hit_rect = self.collision_list[hit_index]
                    if dx > 0:
                        delta_x += next_rect.right - hit_rect.left
                    else:
                        delta_x += hit_rect.right - next_rect.left
                    if dy > 0:
                        delta_y += next_rect.bottom - hit_rect.top
                    else:
                        delta_y += hit_rect.bottom - next_rect.top
                except IndexError:
                    pass

            if abs(delta_x - delta_y) < 10:
                dx, dy = 0, 0
            elif delta_x > delta_y:
                dy = 0
            elif delta_y > delta_x:
                dx = 0
        self.x += dx
        self.y += dy

    def movement(self):
        self.keys_control()
        self.mouse_control()
        self.rect.center = self.x, self.y
        self.angle %= DOUBLE_PI

    def keys_control(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            exit()

        if keys[pygame.K_w]:
            dx = player_speed * cos_a
            dy = player_speed * sin_a
            self.detect_collision(dx, dy)
        if keys[pygame.K_s]:
            dx = -player_speed * cos_a
            dy = -player_speed * sin_a
            self.detect_collision(dx, dy)
        if keys[pygame.K_a]:
            dx = player_speed * sin_a
            dy = -player_speed * cos_a
            self.detect_collision(dx, dy)
        if keys[pygame.K_d]:
            dx = -player_speed * sin_a
            dy = player_speed * cos_a
            self.detect_collision(dx, dy)

        if keys[pygame.K_LEFT]:
            self.angle -= 0.02
        if keys[pygame.K_RIGHT]:
            self.angle += 0.02

    def mouse_control(self):
        if pygame.mouse.get_focused():
            difference = pygame.mouse.get_pos()[0] - HALF_WIDTH
            pygame.mouse.set_pos((HALF_WIDTH, HALF_HEIGHT))
            self.angle += difference * self.sensitivity

    @key.setter
    def key(self, value):
        self._key = value
