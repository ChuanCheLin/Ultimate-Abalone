## Ultimate Abalone with Minimax
### Introduction

---
### The Typical Game of Abalone 
Abalone is a strategic board game designed for two players. It was invented in 1987 by Michel Lalet and Laurent Lévi, and has since captivated players around the world. The game’s objective is to push six of the opponent's marbles off the edge of the hexagon-shaped board.

#### Board and Setup
The board consists of 61 circular spaces where marbles can reside. Each player starts with 14 marbles positioned on opposite sides of the board.

#### Moves
Players alternate turns, moving their marbles in one of six directions. Moves can be made in-line (pushing) or broadside (side-stepping).
* In-line Move: Marbles are moved as a column into a free space
  * 3 marbles push 1 marble
  * 3 marbles push 2 marbles
  * 2 marbles push 1 marble
* Side Step: Marbles are moved sideways into adjacent free spaces
  
#### Reference
[Wikipedia](https://en.wikipedia.org/wiki/Abalone_(board_game))

---

### Ultimate Abalone - Enhanced Strategy
* Enhanced Move Mechanics: In the Ultimate Abalone, the classic move limitations are expanded. Players can now push any number of marbles (N) with a greater number of their own (M), given N>M and M>=5, making the game more dynamic and strategic.
* Offensive Plays: Ultimate Abalone proposes offensive strategy by permitting players to push the opponent's marbles directly off the board in a single action. This rule applies even if the opponent's marbles are not positioned adjacent to the board's edge at the start of the turn. To achieve such a bold push, there must be a direct, unobstructed line between the opponent's marbles and the board's edge. These newly introduced high-stakes plays amplify the intensity of each move, compelling players to engage with foresight and boldness as they orchestrate their path to victory.

---

### Data Structure of Game Board

```
            self.board = np.array([
            [-2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2],
            [-2, -2, -2, -2, -2,  1,  1,  1,  1,  1, -2],
            [-2, -2, -2, -2,  1,  1,  1,  1,  1,  1, -2],
            [-2, -2, -2, -1, -1,  1,  1,  1, -1, -1, -2],
            [-2, -2, -1, -1, -1, -1, -1, -1, -1, -1, -2],
            [-2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -2],
            [-2, -1, -1, -1, -1, -1, -1, -1, -1, -2, -2],
            [-2, -1, -1,  0,  0,  0, -1, -1, -2, -2, -2],
            [-2,  0,  0,  0,  0,  0,  0, -2, -2, -2, -2],
            [-2,  0,  0,  0,  0,  0, -2, -2, -2, -2, -2],
            [-2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2]
         ])
```
The code above refers to the hexagonal board. In this code, 1 represents white marbles, while 0 represents black marbles. -1 represents a blank space on the board, while -2 represents a position outside of the board.

```
            DIRECTIONS = {
                    'LEFT': (0, -1),
                    'RIGHT': (0, 1),
                    'UP_LEFT': (-1, 0),
                    'UP_RIGHT': (-1, 1),
                    'DOWN_LEFT': (1, -1),
                    'DOWN_RIGHT': (1, 0)
                }
```
The provided code illustrates the correspondence between directions on a hexagonal board and their equivalents in a 2D array. The keys of the dictionary represent the directions on the hexagonal board, while the values indicate the corresponding directions in the 2D array.

---

### Code Analysis

#### Move 
The code for moving marbles checks the next few marble positions to determine if they are empty or occupied by opponents' marbles. If there are fewer opponent marbles, it then evaluates the likelihood of offensive play success by examining subsequent positions. The computation is completed in constant time, denoted as O(1), Θ(1), and Ω(1).

---

### Slides
[Slide link]()
### Work Allocation
* Spencer: Brainstorm the concept for Ultimate Abalones and focus on programming the move.py, the key functionality for executing the game.
