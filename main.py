import pygame
from settings import *

pygame.init()
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.mixer.init()

from sprite_objects import *

from player import *
from ray_casting import ray_casting_walls
from drawing import Drawing
from inteaction import Interaction

clock = pygame.time.Clock()
player = Player(Sprites.list_of_objects)
drawing = Drawing(display, clock)

# print(SpritesParams)
interaction = Interaction(player, Sprites, drawing)

drawing.menu()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    player.movement()

    display.fill(BLACK)

    drawing.background(player.angle)

    walls = ray_casting_walls(player, drawing.textures)

    drawing.world(walls + [obj.object_locate(player) for obj in Sprites.list_of_objects])

    drawing.key(player.iskey)

    # print(player.iswining)
    if player.iswin:
        drawing.win()

    drawing.fps(clock)
    interaction.minotaur_objects()
    if interaction.lose:
        drawing.lose()
    if interaction.see:
        interaction.see_music()
        drawing.see()
        # interaction.see = False
        # interaction.see_sound_flag = False

    pygame.display.flip()
    clock.tick(FPS)
