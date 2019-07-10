import pygame
import sys
import os
import random
from time import sleep

res_path = './resource'

file_list = os.listdir(res_path)

rockImage = []
for item in file_list:
    if item.find('r') ==  0 :
        rockImage.append(item)


BLACK = (0, 0, 0)
padWidth = 480
padHeight = 640

def drawObject(obj, x, y):
    global gamePad
    gamePad.blit(obj, (x,y))

def initGame():
    global gamePad, clock, background, fighter, missile

    pygame.init()
    gamePad = pygame.display.set_mode((padWidth, padHeight))
    pygame.display.set_caption('PyShooting')
    background = pygame.image.load('resource/background.png')
    fighter = pygame.image.load('resource/fighter.png')
    missile = pygame.image.load('resource/missile.png')
    clock = pygame.time.Clock()


def runGame():
    global gamepad, clock, background, fighter, missile

    fighterSize = fighter.get_rect().size
    missileSize = missile.get_rect().size

    missileHeight = missileSize[1]
    fighterWidth = fighterSize[0]
    fighterHeight = fighterSize[1]

    x = padWidth * 0.5
    y = padHeight - fighterHeight
    fighterX = 0
    missileXY= []

    rock = pygame.image.load('resource/'+random.choice(rockImage))
    rockSize = rock.get_rect().size
    rockWidth = rockSize[0]
    rockHeight = rockSize[1]

    rockX = random.randrange(0, padWidth - rockWidth)
    rockY = 0
    rockSpeed = 2

    onGame = False

    while not onGame:
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]:
                pygame.quit()
                sys.exit()

            if event.type in [pygame.KEYDOWN]:
                if event.key == pygame.K_LEFT:
                    fighterX -= 5
                    print("LEFT DOWN")
                elif event.key == pygame.K_RIGHT:
                    fighterX += 5
                    print("RIGHT DOWN")
                elif event.key == pygame.K_SPACE:
                    missileX=x + fighterWidth/2 - 1
                    missileY=y - missileHeight

                    missileXY.append([missileX, missileY])

            if event.type in [pygame.KEYUP]:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    fighterX = 0
                    print("KEY UP")

        drawObject(background, 0, 0)

        x += fighterX
        if x < 0 :
            x = 0
        elif x > padWidth - fighterWidth:
            x = padWidth - fighterWidth

        drawObject(fighter,x,y)

        if len(missileXY) != 0:
            for i, bxy in enumerate(missileXY):
                bxy[1] -= 10
                missileXY[i][1] = bxy[1]

                if bxy[1] <= 0:
                    try:
                        missileXY.remove(bxy)
                    except:
                        pass
                if len(missileXY) != 0:
                    for bx, by in missileXY:
                        drawObject(missile, bx, by)
        rockY += rockSpeed

        if rockY > padHeight:
            rock = pygame.image.load('resource/'+random.choice(rockImage))

            rockSize = rock.get_rect().size
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]
            rockX = random.randrange(0, padWidth - rockWidth)
            rockY = 0

        drawObject(rock, rockX, rockY)
        pygame.display.update()
        clock.tick(60)

    pygame.quit()

initGame()
runGame()
