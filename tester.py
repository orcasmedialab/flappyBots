
import pygame
from pygame.locals import *
import random
import gameResources as gr
import numpy as np

pygame.init()

clock = pygame.time.Clock()
fps = 60
guiEnabled = True
collisionsEnabled = True

screenWidth = gr.screenWidth
groundHeight = gr.groundHeight

#environment stuff
birdWorld = gr.environment(guiEnabled)

#bird stuff
numBirds = 100
birdGroup = gr.birdGroup(numBirds)
counter = 0
flapCooldown = 30

#gameplay stuff
gameplay = gr.gameplay(birdGroup, birdWorld, collisionsEnabled)


run = True

while run:

    clock.tick(fps)


    birdWorld.update(birdGroup)

    if counter == flapCooldown:
        jump = True
        counter = 0
    else:
        jump = False
        counter += 1

    jumpIS = np.random.choice([False, True], size = (numBirds,), 
            p = [(flapCooldown-1) / flapCooldown, 1./flapCooldown])

    birdGroup.update(jumpIS)
    gameplay.update()



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()


