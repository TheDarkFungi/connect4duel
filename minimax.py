# minimax.py
# An implementation of Minimax search to
# find the best move in a position
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
from board import Piece, Board, Move


# ---------------------------------------------------------------------------
# Find the best possible outcome for original player
# Do Not Modify
def minimax(board: Board, maximizing: bool, original_player: Piece, max_depth: int = 8) -> float:
    # Base case – terminal position or maximum depth reached
    if board.is_win or board.is_draw or max_depth == 0:
        return board.evaluate(original_player)

    # Recursive case - maximize your gains or minimize the opponent's gains
    if maximizing:
        best_eval: float = float("-inf")  # arbitrarily low starting point
        for move in board.legal_moves:
            result: float = minimax(board.move(move), False, original_player, max_depth - 1)
            best_eval = max(result, best_eval)  # we want the move with the highest evaluation
        return best_eval
    else:  # minimizing
        worst_eval: float = float("inf")
        for move in board.legal_moves:
            result = minimax(board.move(move), True, original_player, max_depth - 1)
            worst_eval = min(result, worst_eval)  # we want the move with the lowest evaluation
        return worst_eval

# ---------------------------------------------------------------------------
# Minimax with alphabeta enhancement to eliminate
# unnecessary search branches
# Do Not Modify
def alphabeta(board: Board, maximizing: bool, original_player: Piece, max_depth: int = 8, alpha: float = float("-inf"),
              beta: float = float("inf")) -> float:
    # Base case – terminal position or maximum depth reached
    if board.is_win or board.is_draw or max_depth == 0:
        x = board.evaluate(original_player)
        #print(board)
        #print(x)
        #junk = input("Pause")
        return x

    # Recursive case - maximize your gains or minimize the opponent's gains
    if maximizing:
        for move in board.legal_moves:
            result: float = alphabeta(board.move(move), False, original_player, max_depth - 1, alpha, beta)
            alpha = max(result, alpha)
            if beta <= alpha:
                break
        return alpha
    else:  # minimizing
        for move in board.legal_moves:
            result = alphabeta(board.move(move), True, original_player, max_depth - 1, alpha, beta)
            beta = min(result, beta)
            if beta <= alpha:
                break
        return beta

# ---------------------------------------------------------------------------
# Find the best possible move in the current position
# looking up to max_depth ahead
def find_best_move(board: Board, max_depth: int = 3) -> Move:
    # initialize result and move, respectively
    # We want best_score to be set to the value of row 1 to start.
    # Set it to a score that is impossible to accomplish naturally
    best_score = -4.04
    best_move = None
    
    for move in board.legal_moves:
        score = alphabeta(
            board=board.move(location=move), maximizing=True, original_player=board.turn, max_depth=max_depth
        )
        if best_score == -4.04:
            best_score = score
        print(score, end='   ')
        if score > best_score:
            best_score = score
            best_move = move
    print("| Best score: ", best_score)


    if best_move is None:
        # hmmmm? if get here then punt:  try to play in the middle of the board if possible
        for index in [3, 2, 4, 1, 5, 0, 6]:
            if index in board.legal_moves:
                return Move(index)

    return best_move
