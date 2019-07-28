import pygame
import sys
import os
import random
from time import sleep


BLACK = (255, 255, 255)
padWidth = 800
padHeight = 800


def drawObject(obj, x, y):
    global gamePad
    gamePad.blit(obj, (x, y))

def initGame():
    global gamePad, clock, background, man
    pygame.init()
    gamePad = pygame.display.set_mode((padWidth, padHeight))
    pygame.display.set_caption('Gangster')
    background = pygame.image.load('res_work/menu_bar.png')
    man = pygame.image.load('res_work/man.png')
    clock = pygame.time.Clock()


def runGame():
    global gamePad, clock, background, man

    man_x = padWidth / 2
    man_y = padHeight / 2

    man_dx = 0
    man_dy = 0


    on_Game = True;

    while on_Game :
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]:
                pygame.quit()
                sys.exit()

            if event.type in [pygame.KEYDOWN]:
                if event.key == pygame.K_LEFT:
                    man_dx += -5
                    print('left')
                if event.key == pygame.K_RIGHT:
                    man_dx += 5
                    print('right')

            if event.type in [pygame.KEYUP]:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    man_dx = 0

        man_x += man_dx
        man_y += man_dy

        print ((man_x,man_y))

        gamePad.fill(BLACK)
        drawObject(background, 0, 0)
        drawObject(man, man_x, man_y)
        pygame.display.update()
        clock.tick(60)

    pygame.quit()


initGame()
runGame()
