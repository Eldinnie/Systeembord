import pygame
import os
from objects import Objects

pygame.init()
pygame.mixer.init()
HIGH = True
LOW = False
font_small = pygame.font.Font(os.path.join("Items", "freesansbold.ttf"), 11)
font_big = pygame.font.Font(os.path.join("Items", "freesansbold.ttf"), 32)

fps_clock = pygame.time.Clock()
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
BACKGROUND = (240, 240, 240)
DARK_BLUE = (0, 0, 102)
FPS = 60
beep = pygame.mixer.Sound(os.path.join("Items", "Beep.wav"))


def draw_text(text, font, color):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    return text_surface, text_rect