# flappyBots
A stepwise-progression version of the classic game **Flappy Bird**, sourced from a pygame version of the program in my flappyBird repo. The primary objective is to make the game controllable by a set of bots that get generated and improved by a genetic ML algorithm.

## Features
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
- [python](https://www.python.org/) 3.12 or newer
- [Pygame](https://github.com/pygame) (based on v2.6)
- [PyGad](https://github.com/ahmedfgad/GeneticAlgorithmPython) (based on v3.3)
- 950px vertical resolution (minimum)


## Instructions
from `flappyBots/` directory:
```console
python3 flappyBots.py [-h] [--iters] [--gui] [--fast] [--birds]
```
<pre>
-h --help    Help Menu
-i --iters   Number of iterations [Default=1]
-g --gui     Disable(0) or Enable(1) GUI [Default=1]
-f --fast    Run at regular game speed (0) or max speed (1) [Default=1]
-b --birds   Number of birds [Default=100]
</pre>


## ToDo
**Primary**
- Optimize numpy initializations
- Implement genetic training algorithm 
- Update README Features section
- Optimize GANN structure and parameters
- Auto-set number of iterations
- Enable parallel compute capabilities

**Non-Critical**
- Add verbose runtime argument
- Make program exit better
- Move randJumpGenerator() to Bot Controller
- Move global definitions to yaml file
- Address console warnings at start
- Bug (maybe?) where sometimes pipe isn't scored
- Pass gameover status to individual birds. Would stop sliding
- Bug where game freezes at the end of last iteration on fast mode
- Edit nn.py to resolve bug with single-dimension inputs

