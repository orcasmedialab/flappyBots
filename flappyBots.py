
#flappyBots.py

import pygame
from pygame.locals import *
import argparse
import gameController as gc
import botController as bc




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


    flappy = gc.gameController(argDict)
    bots = bc.botController(flappy.getNumBirds(), argDict['numberIterations'])


    run = True

    while run:
    
        # Send game state to bot algorithm to produce jump instructions
        gameState = flappy.gameStateCompiler()
        jumpInstructions = bots.getInstructions(gameState)

        # Step-wise progress through game, each bird sent corresponding command
        flappy.step(jumpInstructions)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False




    bots.joinGaThread()
    pygame.quit()



