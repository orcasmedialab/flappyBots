# flappyBots
A stepwise-progression version of the classic game **Flappy Bird**, sourced from a python/pygame version of the program in my flappyBird repo. The primary objective is make the game controllable by a set of bots, which can be generated and improved by a genetic ML algorithm.

## (Eventual) Features
- **Multiplayer**: Game can be initiated with multiple simultaneous AI players.
- **Control**: Commands can be sent to the gameController to instruct birds to jump or do nothing.
- **State Feedback**: gameController will return position of all players in relation to obstacles.
- **Obstacles**: Bird(s) must navigate through randomly generated pipes.
- **Scoring**: Earn points by passing through pipes.
- **Game Over**: A player dies upon collision with ground, sky, or pipe.


## Program structure

<pre>
|------------------------------|
|       Flappy Bird Game       |                   |--------------|                     |---------------|
|                              |  --Game State-->  |     Bot      |  --Game Results-->  |    Genetic    |
|    Game           Game       |                   |  Controller  |                     |  Algorirthm   |
|  Resources     Controller    |  <---Controls---  |              |   <---New Bots---   |               |
|------------------------------|                   |--------------|                     |---------------|
</pre>


## Run Requirements
- python 3.12 or newer
- pygame 2.6 or newer


## Instructions
from flappyBots/ directory:
```console
python3 flappyBots.py
```


## ToDo
**Primary**
- Improve all class reset functions
- Create bot controller
- Update README Features section
- Update runtime options (flags)
- Implement genetic algorithm 
- Enable parallel compute capabilities

**Non-Critical**
- Move global definitions to yaml file
- Address console warnings at start
- Bug (maybe?) where sometimes pipe isn't scored
- Pass gameover status to individual birds. Would stop sliding

