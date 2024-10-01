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
- Implement option to record logging only at program completion
- Issue: Program crash can delete or partially delete log file (look into safedump)
- Add high level Program Info to logging
- Add ANN network info to logging (structure, etc.)
- Add generation-specific info to logging
- Ability to import solution(s) from logs
- Add runtime arguments related to training algorithm
- Add ability to gracefully exit headless 
- Extend mutex lock beyond just the jump calculation
- Update README Features section
- Optimize GANN structure and parameters
- Address redundant repeat calls of fitnessFunction()
- Import only specific (or best) solution from generation
- Auto-set number of iterations
- Display game score on screen
- Add reset button on screen
- Enable parallel compute capabilities
- Optimize game processes 
- Edit nn.py to resolve bug with single-dimension inputs

**Bot Improvements/Thoughts**
- Make sure not to eliminate good bots after 1 bad/anomalous generation
- Figure out plan for time limits on positions (next project)
- Retain more parents, especially in stalemate cases
- Retain best ancestors from past few generations, despite success levels on most recent run(s)
- If solutions get pigeonholed into a hopeless strategy, start entire process over. Need to think about how this gets determined for next project.
- Last point is often associated with "bad starts" that get locked in. May or may not be relevent for next project.
- Decendents should have a large range of genetic similarity from almost-same to completely different.
- Isolated subspecies with reintroduction.

**Non-Critical**
- Add verbose runtime argument
- Ensure game score(s) are printed at end
- Consider reimplementing game score for algorithmic grading
- Move randJumpGenerator() to Bot Controller
- Move global definitions to yaml file
- Address console warnings at start
- Bug (maybe?) where sometimes pipe isn't scored
- Pass gameover status to individual birds. Would stop sliding
- Bug where game freezes at the end of last iteration on fast mode

