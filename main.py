import pygame
from settings import *
from player import Player
import math
from map import world_map
from ray_casting import ray_casting_player
from drawing import Drawing

pygame.init()
display = pygame.display.set_mode((WIDTH, HEIGHT), vsync=1)
# display = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN, vsync=1)
mini_map_display = pygame.Surface(MINIMAP_RES)
pygame.mouse.set_visible(False)


clock = pygame.time.Clock()

player = Player()
drawing = Drawing(display, mini_map_display)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    player.movement()

    display.fill(BLACK)

    drawing.backround()

    drawing.world(player.get_pos, player.angle)

    # drawing.draw_mini_map(player)

    drawing.fps(clock)




    # #
    # pygame.draw.circle(display, GREEN, player.get_pos, 12)
    # pygame.draw.line(display, RED, player.get_pos, (player.x + WIDTH * math.cos(player.angle),
    #                                                 player.y + WIDTH * math.sin(player.angle)))
    #
    # [pygame.draw.rect(display, BLUE, (x, y, TILE, TILE), 2) for x, y in world_map]
    pygame.display.flip()
    clock.tick(FPS)