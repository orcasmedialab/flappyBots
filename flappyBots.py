
#flappyBots.py

import pygame
from pygame.locals import *
import argparse
import gameController as gc




if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog = 'flappyBots',
        formatter_class=lambda 
        prog: argparse.HelpFormatter(prog,max_help_position=27)
    )
    parser.add_argument('-i', '--iters', type=int, help='Number of iterations [Default=1]')
    parser.add_argument('-g', '--gui', type=int, help='Disable(0) or Enable(1) GUI [Default=1]')
    parser.add_argument('-f', '--fast', type=int, help='Run at regular game speed (0) or max speed (1) [Default=1]')
    parser.add_argument('-b', '--birds', type=int, help='Number of birds [Default=100]')
    args = parser.parse_args()
    
    #keys must match global names in gameController.py !!
    argDict = {
        'numberIterations': args.iters,
        'guiEnabled': (bool(args.gui) if (args.gui is not None) else None),
        'realTime': (not bool(args.fast) if (args.fast is not None) else None),
        'numBirds': args.birds
    }


run = True

flappyBots = gc.gameController(argDict)




while run:
 
    flappyBots.step(flappyBots.randJumpGenerator())


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False




pygame.quit()



