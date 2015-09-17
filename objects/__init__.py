import pygame
import os

pygame.init()
pygame.mixer.init()
HIGH = True
LOW = False
font_small = pygame.font.Font(os.path.join("Items", "freesansbold.ttf"), 11)
font_medium = pygame.font.Font(os.path.join("Items", "freesansbold.ttf"), 20)
font_big = pygame.font.Font(os.path.join("Items", "freesansbold.ttf"), 32)

fps_clock = pygame.time.Clock()
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
BACKGROUND = (240, 240, 240)
DARK_BLUE = (0, 0, 102)
FPS = 60
RESET = 9
BOARD = 8
SAVE = 10
LOAD = 11
beep = pygame.mixer.Sound(os.path.join("Items", "Beep.wav"))


def draw_text(text, font, color,back=BACKGROUND):
    text_surface = font.render(text, True, color,back)
    text_rect = text_surface.get_rect()
    return text_surface, text_rect

def gen(n):
    num = n
    while True:
        yield num
        num += 1
