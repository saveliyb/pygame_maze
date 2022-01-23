import pygame
from settings import *
import sys
from random import randrange
from sprite_objects import SpritesParams
from ray_casting import ray_casting
from map import mini_map


class Drawing:
    def __init__(self, display, clock):
        self.font_win = pygame.font.Font('font/font.ttf', 144)
        self.display = display
        self.font = pygame.font.SysFont('Arial', 36, bold=True)
        self.clock = clock
        self.textures = {1: pygame.image.load('img/wall3.png').convert(),
                         # 2: pygame.image.load('img/wall4.png').convert(),
                         # 3: pygame.image.load('img/wall5.png').convert(),
                         # 4: pygame.image.load('img/wall6.png').convert(),
                         5: pygame.image.load('img/door.png').convert(),
                         'S': pygame.image.load('img/sky2.png').convert()
                         }
        self.menu_trigger = True
        self.menu_picture = pygame.image.load('img/sky2.png').convert_alpha()

    def background(self, angle):
        sky_offset = -10 * math.degrees(angle) % WIDTH
        self.display.blit(self.textures['S'], (sky_offset, 0))
        self.display.blit(self.textures['S'], (sky_offset - WIDTH, 0))
        self.display.blit(self.textures['S'], (sky_offset + WIDTH, 0))
        pygame.draw.rect(self.display, DARKGRAY, (0, HALF_HEIGHT, WIDTH, HALF_HEIGHT))

    def world(self, world_objects):
        for obj in sorted(world_objects, key=lambda n: n[0], reverse=True):
            if obj[0]:
                _, object, object_pos = obj
                self.display.blit(object, object_pos)

    def fps(self, clock):
        display_fps = str(int(clock.get_fps()))
        render = self.font.render(display_fps, 0, DARKORANGE)
        self.display.blit(render, FPS_POS)

    def win(self):
        render = self.font_win.render('YOU WIN!!!', 1, (randrange(40, 120), 0, 0))
        rect = pygame.Rect(0, 0, 1000, 300)
        rect.center = HALF_WIDTH, HALF_HEIGHT
        pygame.draw.rect(self.display, BLACK, rect, border_radius=50)
        self.display.blit(render, (rect.centerx - 430, rect.centery - 140))
        pygame.display.flip()

    def lose(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.load('sound/died.wav')
        pygame.mixer.music.play()
        while True:
            render = self.font_win.render(' YOU DIED', 1, (randrange(40, 120), 0, 0))
            rect = pygame.Rect(0, 0, 1000, 300)
            rect.center = HALF_WIDTH, HALF_HEIGHT
            pygame.draw.rect(self.display, BLACK, rect, border_radius=50)
            self.display.blit(render, (rect.centerx - 430, rect.centery - 140))
            pygame.display.flip()

    def key(self, key):
        if key:
            key = SpritesParams().sprite_parameters['sprite_key']['sprite']
            key_rect = (15, 15, 15, 15)
            self.display.blit(key, key_rect)

    def see(self):
        see = pygame.image.load('img/see.png').convert_alpha()
        see_rect = (WIDTH // 2 - 45 // 2, 30, 45, 45)
        self.display.blit(see, see_rect)


    def menu(self):
        x = 0
        button_font = pygame.font.Font('font/font.ttf', 72)
        label_font = pygame.font.Font('font/font1.otf', 267)
        start = button_font.render('START', 1, pygame.Color('lightgray'))
        button_start = pygame.Rect(0, 0, 400, 150)
        button_start.center = HALF_WIDTH, HALF_HEIGHT
        exit = button_font.render('EXIT', 1, pygame.Color('lightgray'))
        button_exit = pygame.Rect(0, 0, 400, 150)
        button_exit.center = HALF_WIDTH, HALF_HEIGHT + 200

        while self.menu_trigger:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.display.blit(self.menu_picture, (0, 0), (x % WIDTH, HALF_HEIGHT, WIDTH, HEIGHT))
            x += 1

            pygame.draw.rect(self.display, BLACK, button_start, border_radius=25, width=10)
            self.display.blit(start, (button_start.centerx - 130, button_start.centery - 70))

            pygame.draw.rect(self.display, BLACK, button_exit, border_radius=25, width=10)
            self.display.blit(exit, (button_exit.centerx - 85, button_exit.centery - 70))

            color = randrange(40)
            label = label_font.render('MINOTAURS', 1, (color, color, color))
            self.display.blit(label, (15, -30))

            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()
            if button_start.collidepoint(mouse_pos):
                pygame.draw.rect(self.display, BLACK, button_start, border_radius=25)
                self.display.blit(start, (button_start.centerx - 130, button_start.centery - 70))
                if mouse_click[0]:
                    pygame.mouse.set_visible(False)
                    self.menu_trigger = False
            elif button_exit.collidepoint(mouse_pos):
                pygame.draw.rect(self.display, BLACK, button_exit, border_radius=25)
                self.display.blit(exit, (button_exit.centerx - 85, button_exit.centery - 70))
                if mouse_click[0]:
                    pygame.quit()
                    sys.exit()

            pygame.display.flip()
            self.clock.tick(20)
