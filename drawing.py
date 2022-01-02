import pygame
from settings import *
from ray_casting import ray_casting_player
from map import mini_map


class Drawing:
    def __init__(self, display, mini_map):
        self.display = display
        self.display_mini_map = mini_map
        self.font = pygame.font.SysFont('Ariral', 36, bold=True)

    def backround(self):
        pygame.draw.rect(self.display, SKY_BLUE, (0, 0, WIDTH, HALF_HEIGHT))
        pygame.draw.rect(self.display, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HALF_HEIGHT))

    def world(self, player_pos, player_angel):
        ray_casting_player(self.display, player_pos, player_angel)

    def fps(self, clock: pygame.time.Clock):
        display_fps = str(int(clock.get_fps()))
        render = self.font.render(display_fps, 0, RED)
        self.display.blit(render, FPS_POS)

    def draw_mini_map(self, player):
        self.display_mini_map.fill(BLACK)
        map_x, map_y = player.x // MAP_SCALE, player.y // MAP_SCALE
        pygame.draw.line(self.display_mini_map, YELLOW, (map_x, map_y), (map_x + 12 * math.cos(player.angle),
                                                        map_y + 12 * math.sin(player.angle)))
        pygame.draw.circle(self.display_mini_map, RED, (int(map_x), int(map_y)), 5)

        [pygame.draw.rect(self.display_mini_map, GREEN, (x, y, MAP_TILE, MAP_TILE)) for x, y in mini_map]
        self.display.blit(self.display_mini_map, MINI_MAP_POS)