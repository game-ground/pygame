import pygame
import sys
import os
import random
from time import sleep

res_path = './resource'

file_list = os.listdir(res_path)

rockImage = []
explosionSound = []

#Resource file lists
for item in file_list:
    if item.find('rock') ==  0 :
        rockImage.append(item)
    if item.find('explosion') != -1 and item.find('.wav') != -1:
        explosionSound.append(item)

reset= True
Life =0
BLACK = (0, 0, 0)
padWidth = 480
padHeight = 640

def drawObject(obj, x, y):
    global gamePad
    gamePad.blit(obj, (x,y))

def writeScore(count):
    global gamePad
    font = pygame.font.Font('resource/NanumGothic.ttf', 20)
    text = font.render('파괴한 운석수 : ' + str(count), True, (255, 255, 255))
    gamePad.blit(text, (10, 0))

def writePassed(count):
    global gamePad
    font = pygame.font.Font('resource/NanumGothic.ttf', 20)
    text = font.render('놓친 운석수 : ' + str(count), True, (255, 0, 0))
    gamePad.blit(text, (260, 0))

def writeMessage(text):
    global gamePad, gameoverSound
    textfont = pygame.font.Font('resource/NanumGothic.ttf', 80)
    text = textfont.render(text, True, (255,0,0))
    textpos = text.get_rect()
    textpos.center = (padWidth/2, padHeight/2)
    gamePad.blit(text, textpos)
    pygame.display.update()
    pygame.mixer.music.stop()
    gameoverSound.play()
    sleep(2)
    pygame.mixer.music.play(-1)
    runGame()

def crash():
    global gamePad
    writeMessage('전투기 파괴!')

def gameOver():
    global gamePad
    writeMessage('게임 오버!')


def initGame():
    global gamePad, clock, background, fighter, missile,explosion,missileSound,gameoverSound, Life,reset

    Life=3
    reset= True
    pygame.init()
    gamePad = pygame.display.set_mode((padWidth, padHeight))
    pygame.display.set_caption('PyShooting')
    background = pygame.image.load('resource/background.png')
    fighter = pygame.image.load('resource/fighter.png')
    missile = pygame.image.load('resource/missile.png')
    explosion = pygame.image.load('resource/explosion.png')
    pygame.mixer.music.load('resource/music.wav')
    pygame.mixer.music.play(-1)
    missileSound = pygame.mixer.Sound('resource/missile.wav')
    gameoverSound = pygame.mixer.Sound('resource/gameover.wav')
    clock = pygame.time.Clock()

    missileSound.set_volume(0.3)


def runGame():
    global gamepad, clock, background, fighter, missile,explosion,missileSound,destroySound, quit_flag, reset, Life

    print(Life)
    fighterSize = fighter.get_rect().size
    missileSize = missile.get_rect().size
    
    missileHeight = missileSize[1]
    fighterWidth = fighterSize[0]
    fighterHeight = fighterSize[1]

    x = padWidth * 0.5
    y = padHeight - fighterHeight
    y_sel=padWidth/3
    quit_flag = 1
    
    fighterX = 0
    missileXY= []

    rock = pygame.image.load('resource/'+random.choice(rockImage))
    rockSize = rock.get_rect().size
    rockWidth = rockSize[0]
    rockHeight = rockSize[1]
    destroySound = pygame.mixer.Sound('resource/'+random.choice(explosionSound))
    destroySound.set_volume(0.3)

    rockX = random.randrange(0, padWidth - rockWidth)
    rockY = 0
    rockSpeed = 5

    isShot = False
    shotCount = 0
    rockPassed = 0
    onGame = False
    pygame.mixer.music.set_volume(1)
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
                    missileSound.play()
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

        if y < rockY + rockHeight:
            if(x+fighterWidth > rockX and rockX + rockWidth > x):
                Life=Life-1
                crash()

        drawObject(fighter,x,y)

        if len(missileXY) != 0:
            for i, bxy in enumerate(missileXY):
                bxy[1] -= 10
                missileXY[i][1] = bxy[1]

                if bxy[1] < rockY:
                    if bxy[0] > rockX and bxy[0] < rockX + rockWidth :
                        missileXY.remove(bxy)
                        isShot = True
                        shotCount += 1

                if bxy[1] <= 0:
                    try:
                        missileXY.remove(bxy)
                    except:
                        pass
                if len(missileXY) != 0:
                    for bx, by in missileXY:
                        drawObject(missile, bx, by)
        rockY += rockSpeed
        writeScore(shotCount)

        if rockY > padHeight:
            rock = pygame.image.load('resource/'+random.choice(rockImage))

            rockSize = rock.get_rect().size
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]
            rockX = random.randrange(0, padWidth - rockWidth)
            rockY = 0
            rockPassed += 1

        if rockPassed == 3:
            Life=Life-1
            gameOver()


        writePassed(rockPassed)

        if isShot :
            drawObject(explosion, rockX, rockY)
            destroySound.play()
            destroySound = pygame.mixer.Sound('resource/'+random.choice(explosionSound))
            destroySound.set_volume(0.3)
            rock = pygame.image.load('resource/'+random.choice(rockImage))

            rockSize = rock.get_rect().size
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]
            rockX = random.randrange(0, padWidth - rockWidth)
            rockY = 0
            isShot = False

        if Life ==0 :
            game_over=pygame.image.load('resource/GAME_OVER.png')
            YorN = pygame.image.load('resource/YorN.png')
            select =pygame.image.load('resource/Select.png')
            pygame.mixer.music.set_volume(0.3)
            while reset:
                drawObject(background, 0, 0)
                drawObject(fighter,x,y)
                drawObject(game_over,padWidth/3, padHeight/3 )
                drawObject(YorN,padWidth/3, padHeight/2 )
                drawObject(select,y_sel, padHeight/2)
                pygame.display.update() 
                for event in pygame.event.get():
                    if event.type in [pygame.KEYDOWN]:
                        if event.key == pygame.K_LEFT:
                            quit_flag=1
                            y_sel = padWidth/3
                            print("RIGHT 1")
                        elif event.key == pygame.K_RIGHT:
                            quit_flag=0
                            y_sel = padWidth/3+120
                            print("RIGHT 0")
                        elif event.key == pygame.K_DOWN:
                            if quit_flag==1:
                                print("reset?")
                                reset= False
                                initGame()
                                runGame()
                                
                            elif quit_flag==0:
                                print("quit?")
                                pygame.quit()
                                sys.exit()
                                
            
        drawObject(rock, rockX, rockY)
        pygame.display.update()
        clock.tick(60)

    pygame.quit()

initGame()
runGame()
