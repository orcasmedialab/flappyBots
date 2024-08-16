
import pygame
from pygame.locals import *
import random


###############################
####### Definitions ###########
###############################
#Global Environment Definitions
screenWidth = 864
screenHeight = 936
groundHeight = 768
groundLength = 35
windowTitle = 'Flappy Bots'

#Global Player Definitions
startHeight = int(groundHeight / 2)
startDist = 100
terminalVel = 8
birdAccel = 0.5
jumpSpeed = -8
flapCooldown = 5
rotateFactor = -3

#define Game variables
scrollSpeed = 4
pipeGap = 150
pipeFrequency = 1500 #ms
gameover = False #move to game controller init
lastPipe = pygame.time.get_ticks() - pipeFrequency
passPipe = False


class bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range (1,4):
            img = pygame.image.load(f'img/bird{num}.png')
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.faceDown = -90
        self.reset()

    def reset(self):
        self.index = 0
        self.counter = 0
        self.rect.center = [startDist, startHeight]
        self.vel = 0
        self.score = 0
        self.birdAlive = True

    def updatePhysics(self):
        #gravity
        if self.rect.bottom < groundHeight:
            if self.vel < terminalVel:
                self.vel += birdAccel
            self.rect.y += int(self.vel)

    def jump(self, jumpAction):
        if jumpAction:
            self.vel = jumpSpeed

    def animateBird(self):
        if self.birdAlive:
            #flapping animation
            if self.counter > flapCooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]
            self.counter += 1

            #rotate the bird
            self.image = pygame.transform.rotate(self.images[self.index], 
                    (rotateFactor * self.vel))
        else:
            #make dead bird face down
            self.image = pygame.transform.rotate(self.images[self.index], self.faceDown)
            #bird moves backwards with ground
            self.rect.x -= int(scrollSpeed)

    def updateBird(self, jumpAction):
        self.updatePhysics()
        self.jump(jumpAction)
        self.animateBird()

    def killBird(self):
        self.birdAlive = False


class pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/pipe.png')
        self.rect = self.image.get_rect()
        #position = 1 is a top pipe, = -1 is a bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, (y - int(pipeGap / 2))]
        if position == -1:
            self.rect.topleft = [x, (y + int(pipeGap / 2))]

    def update(self):
        self.rect.x -= scrollSpeed
        if self.rect.right < 0:
            self.kill()


class environment():
    def __init__(self, guiEnabled):
        self.backgroundImg = pygame.image.load('img/bg.png')
        self.groundImg = pygame.image.load('img/ground.png')
        self.guiEnabled = guiEnabled
        self.groundScroll = 0

        if self.guiEnabled:
            self.screen = pygame.display.set_mode((screenWidth, screenHeight))
            pygame.display.set_caption(windowTitle)
            self.renderScene()

    def renderScene(self):
        self.screen.blit(self.backgroundImg, (0, 0))
        self.screen.blit(self.groundImg, (self.groundScroll, groundHeight))

    def renderBird(self, birdGroup):
        birdGroup.draw(self.screen)

    def renderElements(self, pipeGroup, birdGroup):
        pipeGroup.draw(self.screen)
        self.renderBird(birdGroup)

    def updateGround(self):
        #Scroll the ground
        self.groundScroll -= scrollSpeed
        if abs(self.groundScroll) > groundLength:
            self.groundScroll = 0

    def update(self, pipeGroup, birdGroup):
        if self.guiEnabled:
            self.updateGround()
            self.renderElements(pipeGroup, birdGroup)
            self.renderGround()


