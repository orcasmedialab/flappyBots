
#flappyBots.py

import pygame
from pygame.locals import *
import gameController as gc


run = True

flappyBots = gc.gameController()




while run:
 
    flappyBots.step(flappyBots.randJumpGenerator())


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False




pygame.quit()



