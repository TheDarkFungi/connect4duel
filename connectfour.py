# connectfour.py
# The C4Board and C4Piece classes that form the heart of a
# game of Connect Four
# Copyright 2018 David Kopec
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations
from typing import List, Optional
from enum import Enum
from board import Piece, Board, Move


# Do Not Modify
class C4Piece(Piece, Enum):
    B = "B"
    R = "r"
    E = " "  # stand-in for empty

    @property
    def opposite(self) -> C4Piece:
        if self == C4Piece.B:
            return C4Piece.R
        elif self == C4Piece.R:
            return C4Piece.B
        else:
            return C4Piece.E

    def __str__(self) -> str:
        return self.value


# The main class that should extend the Board abstract base class
# It maintains the position of a game
# You should not need to add any additional properties to this class, but
# you may add additional methods
class C4Board(Board):
    # -------------------------------------------
    # Class variables
    NUM_ROWS:       int = 6
    NUM_COLUMNS:    int = 7
    SEGMENT_LENGTH: int = 4
    # -------------------------------------------    

    # This inner helper class is used by C4Board
    # It represents a single column of pieces
    # Do Not Modify this class
    class Column:
        def __init__(self) -> None:
            self._container: List[C4Piece] = []

        @property
        def full(self) -> bool:
            return len(self._container) == C4Board.NUM_ROWS

        def push(self, item: C4Piece) -> None:
            if self.full:
                raise OverflowError("Trying to push piece to full column")
            self._container.append(item)

        def __getitem__(self, index: int) -> C4Piece:
            if index > len(self._container) - 1:
                return C4Piece.E
            return self._container[index]

        def __repr__(self) -> str:
            return repr(self._container)

        def copy(self) -> C4Board.Column:
            temp: C4Board.Column = C4Board.Column()
            temp._container = self._container.copy()
            return temp
        
    # ------ end inner-class Column ----------------------------

    # ---------------------------------------------------------------------------
    # CTOR
    def __init__(self, position: Optional[List[C4Board.Column]] = None, turn: C4Piece = C4Piece.B) -> None:
        if (position is None):
            self.position: List[C4Board.Column] = [C4Board.Column() for _ in range(C4Board.NUM_COLUMNS)]
        else:
            self.position = position
            
        self._turn: C4Piece = turn

    # ---------------------------------------------------------------------------
    # who's turn is it?
    @property
    def turn(self) -> Piece:
        return self._turn

    # ---------------------------------------------------------------------------
    # put a piece in a column
    # Note: returns a *copy* of the board with the move (already) made
    # Note: this does not check if the column is full (assumes a legal move)
    def move(self, location: Move) -> Board:
        new_position = [column.copy() for column in self.position]
        new_position[location].push(self._turn)
        
        return C4Board(position=new_position, turn=self._turn.opposite)

    # ---------------------------------------------------------------------------
    # return a list of all of the current legal moves
    # note: a move is just the column you can play
    @property
    def legal_moves(self) -> List[Move]:
        # if the column if not full, then it is a legal move
        return [
            # save Move(indices) where the column is not full
            Move(index) for index in range(self.NUM_COLUMNS) if not self.position[index].full
        ]

    # ---------------------------------------------------------------------------
    # Is it a win? (checks for wins for user and AI)
    @property
    def is_win(self) -> bool:
        # save the two possible winning conditions (runs of four), e.g. "BBBB"
        win_one = self.SEGMENT_LENGTH * f"{self.turn}"
        win_two = self.SEGMENT_LENGTH * f"{self.turn.opposite}"

        # check columns
        for column in self.position:
            # mash the current column pieces into a string
            check = "".join([column[i].value for i in range(self.NUM_ROWS)])
            if (win_one in check or win_two in check):
                return True

        # check rows
        for i in range(self.NUM_ROWS):
            # mash the ith rows' pieces across all columns
            check = "".join([column[i].value for column in self.position])
            if (win_one in check or win_two in check):
                return True

        # check positive slope (lower-left to upper-right)
        for i in range(self.NUM_COLUMNS - self.SEGMENT_LENGTH + 1):
            for j in range(self.NUM_ROWS - 3):
                check = "".join([self.position[i + k][j + k].value for k in range(4)])
                if (win_one == check or win_two == check):
                    return True

        # check negative slope (upper-left to lower-right)
        for i in range(self.NUM_COLUMNS - self.SEGMENT_LENGTH + 1):
            for j in range(3, self.NUM_ROWS):
                check = "".join([self.position[i + k][j - k].value for k in range(4)])
                if (win_one == check or win_two == check):
                    return True

        # if none of the above conditions are met (no runs of four for either), no win yet
        return False
    
    # ---------------------------------------------------------------------------
    # (not currently in use; would be needed for alternate versions of evaluate() )
    def nextOpenSpotInColumn(self, column: int) -> Move:
        # assume not full
        oneColumn = self.position[column]
        for i in range(self.NUM_ROWS):
            if (oneColumn[i].value == " "):
                return i
 
    # ---------------------------------------------------------------------------        
    # Who is winning in this position?
    # This function scores the position for player
    # and returns a numerical score
    # When player is doing well, the score should be higher
    # When player is doing worse, player's returned score should be lower
    # Scores mean nothing except in relation to one another; so you can
    # use any scale that makes sense to you
    # The more accurately evaluate() scores a position, the better that minimax will work
    # There may be more than one way to evaluate a position but an obvious route
    # is to count how many 1 filled, 2 filled, and 3 filled segments of the board
    # that the player has (that don't include any of the opponents pieces) and give
    # a higher score for 3 filled than 2 filled, 1 filled, etc.
    # You may also need to score wins (4 filled) as very high scores and losses (4 filled
    # for the opponent) as very low scores
    def evaluate(self, player: Piece) -> float:
        # initialize the score and the window length
        score = 0
        window_length = 4

        # check columns
        for column in self.position:
            # make a list of the values appearing in this column
            column = [column[i].value for i in range(self.NUM_ROWS)]
            
            # snag the 3 slices of size 4 and score each "run" (evaluate that "window")
            for index in range(self.NUM_ROWS - self.SEGMENT_LENGTH + 1):
                window = column[index: index + window_length]
                score += self.evaluate_window(window=window, player=player, SEGMENT_LENGTH=self.SEGMENT_LENGTH)

        # check rows
        for i in range(self.NUM_ROWS):
            # make a list of values appearing in each row
            row = [column[i].value for column in self.position]
            
            # snag the 4 slices of size 4 and score each "run"
            for index in range(self.NUM_COLUMNS - self.SEGMENT_LENGTH + 1):
                window = row[index: index + window_length]
                score += self.evaluate_window(window=window, player=player, SEGMENT_LENGTH=self.SEGMENT_LENGTH)

        # check positive slope
        for i in range(self.NUM_COLUMNS - self.SEGMENT_LENGTH + 1):
            for j in range(self.NUM_ROWS - self.SEGMENT_LENGTH + 1):
                window = [self.position[i + k][j + k].value for k in range(window_length)]
                score += self.evaluate_window(window=window, player=player, SEGMENT_LENGTH=self.SEGMENT_LENGTH)

        # check negative slope
        for i in range(self.NUM_COLUMNS - self.SEGMENT_LENGTH + 1):
            for j in range(3, self.NUM_ROWS):
                window = [self.position[i + k][j - k].value for k in range(window_length)]
                score += self.evaluate_window(window=window, player=player, SEGMENT_LENGTH=self.SEGMENT_LENGTH)

        return score

    # ---------------------------------------------------------------------------
    @staticmethod
    def evaluate_window(window: List[str], player: Piece, SEGMENT_LENGTH: int) -> int:
        score = 0
        
        # Note: scores are *very* arbitrary ... and need some love ...

        # checks for optimistic potentials for "one" (current) player
        one = str(player)
        # a row of 5 gives a score of +150, a row of 6 gives +200, etc...
        # a row of 4 still gives +100
        if window.count(one) == 4:
            score += 500 #If you see the winning move, TAKE IT
        # potential win (3 of 4 taken with other one being open ('E')
        elif window.count(one) == 3 and window.count(str(C4Piece.E)) == 1:
            score += 50
        # potential win (2 of 4 taken with other two being open ('E')
        elif window.count(one) == 2 and window.count(str(C4Piece.E)) == 2:
            score += 3
            # CHANGE: A value of 10 was causing the AI to massively overvalue two-long strings
            
        # checks for pessimistic outcomes for one (good for other)
        other = str(player.opposite)
        if window.count(other) == 4:
            score -= 95
        elif window.count(other) == 3 and window.count(str(C4Piece.E)) == 1:
            score -= 80
        elif window.count(other) == 2 and window.count(str(C4Piece.E)) == 2:
            score -= 5
        
        # checks for blocking other's potential progress if "both ends" open

        filledMiddle = True
        if SEGMENT_LENGTH > 2: #Checks every middle slot in the window
            for n in range(1,SEGMENT_LENGTH - 2):
                if window[n] != other:
                    filledMiddle = False

        if (window[0] == str(C4Piece.E) and
            filledMiddle and
            window[SEGMENT_LENGTH - 1] == str(C4Piece.E) ):
            
            score -= 80
      
        
        #print(f"Player {Piece}: score = {score}")
        #if (score < 0):
        #    return 0
        #else:
        return score

    # ---------------------------------------------------------------------------
    # print the board
    def __repr__(self) -> str:
        line = "-" * 29 + "\n"
        board = line
        for i in reversed(range(self.NUM_ROWS)):
            # Format the board elts
            row = " | ".join([column[i].value for column in self.position])
            board += f"| {row} |\n"
            
        board += line
        index = "   ".join([str(i + 1) for i in range(self.NUM_COLUMNS)])
        board += f"  {index}"
        
        return board
    
    # ---------------------------------------------------------------------------
