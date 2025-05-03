# tictactoe_ai.py
# A main game loop to play the computer
# in Connect Four
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
from minimax import find_best_move
from connectfour import C4Board, C4Piece
from board import Move, Board
from connectfour_tests import list_to_board


# ---------------------------------------------------------------------------
# Find the user's next move
def get_player_move(board: Board) -> Move:
    legalMoves = board.legal_moves
    
    validMove = False # assume the worst
    while (not validMove):
        print("Your turn! You can put a chip in the following columns:")
        print(f"{', '.join([str(move + 1) for move in legalMoves])}")
        
        yourMove = Move(int(input("Type in your move: ")) - 1)
        if yourMove in legalMoves:
            validMove = True
        else:
            print("Error: bad column entered; please enter a valid column.\n")
    # end while not a valid move entered ... (yet)
    
    return yourMove

# ---------------------------------------------------------------------------
def main():
    # fresh board
    board: Board = C4Board()
    print(f"\n{board}\n")
    
    """
    # good place to set up debugging test games ...
    position: List[List[int]] = [
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0],
        [1, 2, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0]]
    board: C4Board = list_to_board(position, C4Piece.R)
    """
  
    print("\nWelcome to Connect4.")
    print("More info on the game here:  https://en.wikipedia.org/wiki/Connect_Four")
    print("-"*60)

    
    print("You will play with Black(B) pieces; the AI will play Red(R)")

    savedMoves = []
    
    while not board.is_win and not board.is_draw:
        print("-"*60)
        
        # USER
        if board.turn == C4Piece.B:
            #move  = get_player_move(board=board)
            move = find_best_move(board, 3)
            print(f"BLACK AI's move is {move+1}.")
            savedMoves.append(move)
            board = board.move(location=move)
            
        # AI
        else:
            move = find_best_move(board, 3)
            print(f"RED AI's move is {move+1}.")
            savedMoves.append(move)
            board = board.move(location=move)
            
        print(f"\n{board}\n")
        
    # end while game continues ...
    
    if (board.is_win):
        print(f"{board.turn.opposite} WINS!")
    else:
        print("The Game is a DRAW.")

    print("-"*60, "\n")

    print("Moves: ")
    print("Black       Red")
    for i in range(len(savedMoves)):
        print(savedMoves[i], end = "")
        if i%2==0:
            print("           ", end = "")
        else:
            print("\n", end = "")

# ---------------------------------------------------------------------------
if __name__ == "__main__":
    main()
