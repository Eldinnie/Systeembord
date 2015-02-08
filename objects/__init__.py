import pygame, os
pygame.init()
# pygame.mixer.init()
HIGH = True
LOW = False
BASICFONT = pygame.font.Font(os.path.join("Items","freesansbold.ttf"), 11)
FONTBIG = pygame.font.Font(os.path.join("Items","freesansbold.ttf"), 32)
DISPLAYSURF=pygame.display.set_mode((200,200))
FPSCLOCK = pygame.time.Clock()
RED=(255,0,0)
BLUE=(0,0,255)
BLACK=(0,0,0)
ACHTERGROND=(240,240,240)
DARKBLUE=(0,0,102)
FPS = 60
beep = pygame.mixer.Sound(os.path.join("Items","Beep.wav"))
def drawText(text,font,color):
    textSurf = font.render(text, True, color)
    textRect = textSurf.get_rect()
    return textSurf,textRect