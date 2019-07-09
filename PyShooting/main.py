import pygame
import sys
from time import sleep

BLACK = (0, 0, 0)
padwidth = 480
padHeight = 640

def drawObject(obj, x, y):
    global gamePad
    gamePad.blit(obj, (x,y))

def initGame():
    global gamePad, clock

    pygame.init()
    gamePad = pygame.display.set_mode((padwidth, padHeight))
    #pygame.display.set_caption('PyShooting')
    clock = pygame.time.Clock()


def runGame():
    global gamepad, clock

    onGame = False

    while not onGame:
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]:
                pygame.quit()
                sys.exit()

        gamePad.fill(BLACK)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

initGame()
runGame()