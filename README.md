# Connect 4 Challenge
- Connect 4 written in Python 3.7
- No external dependencies beyond the Python standard library
- Starter code is included

## Finishing the Implementation
Please do not change any of the methods that are already implemented, any of the method signatures, and please do not change any of the unit tests. Add your code into the incomplete methods and add any additional utility methods/functions. Incomplete methods are explicitly marked "Your Code Here."

## Pitting the AI against itself

Run `python3 play.py` when in the same directory as the source files. Your Python command may be defined as `python` instead of `python3`.

## Extended Description
You will be creating an artificial opponent that plays the game of Connect Four using the [minimax](https://en.wikipedia.org/wiki/Minimax) algorithm. Your Connect Four AI will likely be good enough to beat most human players.

### Connect Four Description

In [Connect Four](https://en.wikipedia.org/wiki/Connect_Four), two players alternate dropping different colored (red or black traditionally) pieces in a seven-column, six-row grid. Pieces fall from the top of the grid to the bottom until they hit the bottom or another piece. In essence, the player’s only decision each turn is which of the seven columns to drop a piece into. The player may not drop it into a full column. The first player that has four pieces of their color next to one another with no breaks in a row, column, or diagonal wins. If no player achieves this, and the grid is completely filled, the game is a draw.

### What has been added

The user no longer gets to play. It is machine versus machine.
Weights have been adjusted, however, AI still makes stupid plays sometimes. It seems like a more complex score system needs to be implemented to prevent obvious mistakes, but I adjusted numbers as best as I could.
FIXED: If the score for all plays is negative, the AI will no longer default to playing in the middle.
FIXED: If the best score for plays is tied, the AI will no longer default to playing in the middle, and now will default to the middlemost TIED value. (It used to be that if 2 and 6 were tied for heighest, the AI would deault to 3)