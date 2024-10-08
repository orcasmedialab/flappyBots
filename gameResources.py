
import pygame
from pygame.locals import *
import numpy as np
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
downwardAngle = -90

#define Game variables
scrollSpeed = 4
pipeGapSize = 150 #space between top/bottom pipe
pipeOffsetRange = 150 #+/-, range of random vertical shift
pipeCadence = 400 #distance from one set of pipes to next
maxScore = 500 #Set to None to have no maximum score


class bird(pygame.sprite.Sprite):
    def __init__(self, birdID):
        pygame.sprite.Sprite.__init__(self)
        self.id = birdID
        self.loadImages()
        self.rect = self.image.get_rect()
        self.faceDown = downwardAngle
        self.reset()

    def loadImages(self):
        self.images = []
        for num in range (1, 4):
            img = pygame.image.load(f'img/bird{num}.png')
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]

    def reset(self):
        self.index = 0
        self.counter = 0
        self.rect.center = [startDist, startHeight]
        self.vel = 0
        self.score = 0
        self.finalProgress = 0
        self.birdAlive = True

    def getBottom(self):
        return self.rect.bottom
    
    def getTop(self):
        return self.rect.top
    
    def getLeft(self):
        return self.rect.left
    
    def getFinalProgress(self):
        return self.finalProgress

    def updatePhysics(self):
        #gravity
        if self.getBottom() < groundHeight:
            if self.vel < terminalVel:
                self.vel += birdAccel
            self.rect.y += int(self.vel)

    def incrementScore(self):
        self.score += 1

    def jump(self, jumpAction):
        if jumpAction[self.id] and self.isAlive():
            self.vel = jumpSpeed

    def animateBird(self):
        if self.isAlive():
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

    def update(self, jumpInstructionSet):
        self.updatePhysics()
        self.jump(jumpInstructionSet)
        self.animateBird()

    def isAlive(self):
        return self.birdAlive

    def killBird(self, totalMovement):
        self.birdAlive = False
        self.finalProgress = totalMovement


class birdGroup(pygame.sprite.Group):
    def __init__(self, numBirds):
        pygame.sprite.Group.__init__(self)
        for birdID in range(numBirds):
            self.add(bird(birdID))

    def reset(self):
        for bird in self.sprites():
            bird.reset()

    def getBirdVelocities(self):
        birdVels = [bird.vel if bird.birdAlive else None for bird in self.sprites()]
        return birdVels
    
    def getBirdHeights(self):
        birdHeights = [bird.rect.bottom if bird.birdAlive else None for bird in self.sprites()]
        return birdHeights
    
    def getBirdProgress(self):
        birdProgress = np.array([bird.getFinalProgress() for bird in self.sprites()])
        return birdProgress


class pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/pipe.png')
        self.rect = self.image.get_rect()
        self.selfGenerate(x, y, position)

    def selfGenerate(self, x, y, position):
        #position = 1 is a top pipe, = -1 is a bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, (y - int(pipeGapSize / 2))]
        if position == -1:
            self.rect.topleft = [x, (y + int(pipeGapSize / 2))]

    def getRight(self):
        return self.rect.right
    
    def getTopRight(self):
        return self.rect.topright
    
    def scrollPipe(self):
        self.rect.x -= scrollSpeed

    def removePipe(self, pipeGroup):
        pipeGroup.decrementIndex()
        self.kill()

    def update(self, pipeGroup):
        self.scrollPipe()
        if self.getRight() < 0:
            self.removePipe(pipeGroup)


class pipeGroup(pygame.sprite.Group):
    def __init__(self):
        pygame.sprite.Group.__init__(self)
        self.currentIndex = 0

    def reset(self):
        for pipe in self.sprites():
            pipe.removePipe(self)
        self.currentIndex = 0

    def generateNewPipes(self):
        pipeHeight = random.randint((-1 * pipeOffsetRange), pipeOffsetRange)
        bottomPipe = pipe(screenWidth, int(groundHeight / 2) + pipeHeight, -1)
        topPipe = pipe(screenWidth, int(groundHeight / 2) + pipeHeight, 1)
        self.add(bottomPipe)
        self.add(topPipe)

    def incrementIndex(self):
        self.currentIndex += 2  #two to account for top and bottom pipe

    def decrementIndex(self):
        self.currentIndex -= 1  #one because called twice, by each top/bottom

    def getSide(self):
        return self.sprites()[self.currentIndex].getRight()
    
    def getCorner(self):
        return self.sprites()[self.currentIndex].getTopRight()


#Responsible for rendering and animating all game elements
#Also manages pipes but not birds (only animate)
class environment():
    def __init__(self, guiEnabled):
        self.guiEnabled = guiEnabled
        self.backgroundImg = pygame.image.load('img/bg.png')
        self.groundImg = pygame.image.load('img/ground.png')
        self.pipeGroup = pipeGroup()
        self.setWindow()
        self.reset(None)

    def setWindow(self):
        if self.guiEnabled:
            self.screen = pygame.display.set_mode((screenWidth, screenHeight))
            pygame.display.set_caption(windowTitle)

    def reset(self, birdGroup):
        self.totalMovement = 0
        self.groundScroll = 0
        self.gameOver = False
        if len(self.pipeGroup) > 0:
            self.pipeGroup.reset()
        if birdGroup is not None:
            birdGroup.reset()
        if self.guiEnabled:
            self.renderScene(birdGroup)


    def getPipeLocation(self):
        if len(self.pipeGroup) > 0:
            return self.pipeGroup.getCorner()
        else:
            return (-1, -1)
        
    def getTotalMovement(self):
        return self.totalMovement

    def renderScene(self, birdGroup):
        self.renderBackground()
        if birdGroup is not None:
            self.renderElements(birdGroup)
        self.renderGround()
        pygame.display.update()

    def renderBackground(self):
        self.screen.blit(self.backgroundImg, (0, 0))

    def renderGround(self):
        self.screen.blit(self.groundImg, (self.groundScroll, groundHeight))

    def renderBirds(self, birdGroup):
        birdGroup.draw(self.screen)

    def renderPipes(self):
        self.pipeGroup.draw(self.screen)

    def renderElements(self, birdGroup):
        self.renderPipes()
        self.renderBirds(birdGroup)

    def updateGround(self):
        #Scroll the ground
        self.groundScroll -= scrollSpeed
        if abs(self.groundScroll) > groundLength:
            self.groundScroll = 0

    def updatePipes(self):
        self.totalMovement += scrollSpeed
        if (self.totalMovement % pipeCadence) < scrollSpeed:
            self.pipeGroup.generateNewPipes()
        self.pipeGroup.update(self.pipeGroup)

    def endGame(self):
        self.gameOver = True

    def update(self, birdGroup):
        if self.gameOver == False:
                self.updatePipes()
        if self.guiEnabled:
            if self.gameOver == False:
                self.updateGround()
            self.renderScene(birdGroup)


class gameplay():
    def __init__(self, birdGroup, environment, collisionsEnabled):
        #init gameplay class
        self.birdGroup = birdGroup
        self.environment = environment
        self.collisionsEnabled = collisionsEnabled
        self.pipeGroup = self.environment.pipeGroup
        self.numBirds = len(self.birdGroup)
        self.reset()

    def reset(self):
        self.remBirds = self.numBirds
        self.score = np.zeros(self.numBirds)
        self.gameOver = False
        
    def isGameOver(self):
        return self.gameOver
    
    def getScore(self, useBirdProgress):
        if useBirdProgress == True:
            return self.birdGroup.getBirdProgress()
        return self.score

    def birdHealth(self):
        #check to see if each alive bird has hit anything or reached max score.
        #if so, kill it
        if self.collisionsEnabled:
            for bird in self.birdGroup:
                if bird.isAlive():
                    if (pygame.sprite.spritecollideany(bird, self.pipeGroup) or
                            (bird.getBottom() >= groundHeight) or
                            (bird.getTop() < 0) or
                            ((maxScore != None) and (self.score[bird.id] >= maxScore))):
                        bird.killBird(self.environment.getTotalMovement())
                        self.remBirds -= 1

    def updateScore(self):
        #track score for each alive bird
        if len(self.pipeGroup) > 0:
            scoreUpdate = False
            for bird in self.birdGroup:
                if bird.isAlive():
                    if bird.getLeft() > self.pipeGroup.getSide():
                        self.score[bird.id] += 1
                        bird.incrementScore()
                        scoreUpdate = True
                        #print('bird #', bird.id, ': ', bird.score)
            if scoreUpdate:
                self.pipeGroup.incrementIndex()

    def endGame(self):
        self.gameOver = True
        print('GameOver')
        #print(self.score)
        self.environment.endGame()

    def checkGameStatus(self):
        #determine if the game has ended
        if self.remBirds == 0 and self.gameOver == False:
            self.endGame()
            #ToDo: inform birds
    
    def update(self):
        self.birdHealth()
        self.checkGameStatus()
        self.updateScore()



