import pygame
from pygame.locals import *
import random

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range (1,4):
            img = pygame.image.load(f'img/bird{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False

    def update(self):

        #gravity
        if flying == True:
            if self.vel < 8:
                self.vel += 0.5
            if self.rect.bottom < 768:
                self.rect.y += int(self.vel)

        if gameover == False:
            #jump
            if (((pygame.mouse.get_pressed()[0] == 1) or (pygame.key.get_pressed()[pygame.K_SPACE] == 1)) 
                    and self.clicked == False):
                self.clicked = True
                self.vel = -8
            if ((pygame.mouse.get_pressed()[0] == 0) and (pygame.key.get_pressed()[pygame.K_SPACE] == 0)):
                self.clicked = False

            #handle animation
            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            #rotate the bird
            self.image = pygame.transform.rotate(self.images[self.index], 
                    (-3 * self.vel))
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/pipe.png')
        self.rect = self.image.get_rect()
        #position = 1 is a top pipe, = -1 is a bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, (y - int(pipe_gap / 2))]
        if position == -1:
            self.rect.topleft = [x, (y + int(pipe_gap / 2))]

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        action = False

        #get mouse position
        pos = pygame.mouse.get_pos()
        #check if mouse is over button
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True      
        # Fix this to allow spacebar reset
        #while (pygame.key.get_pressed()[pygame.K_SPACE] == 1):
        #    action = True

        #draw button
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action

