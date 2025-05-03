# connectfour_tests.py
# Tests to ensure Connect Four is working correctly.
# This file should not be modified
# Copyright 2019 David Kopec
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
import unittest
from typing import List
from minimax import find_best_move
from connectfour import C4Piece, C4Board
from board import Move


# Utility function for creating
# boards from columns of integers
def list_to_board(input_list: List[List[int]], turn: C4Piece) -> C4Board:
    columns: List[C4Board.Column] = []
    for col in input_list:
        column: C4Board.Column = C4Board.Column()
        for piece in col:
            if piece == 1:
                column.push(C4Piece.B)
            elif piece == 2:
                column.push(C4Piece.R)
        columns.append(column)
    return C4Board(columns, turn)


class C4LegalMovesTestCase(unittest.TestCase):
    def test_legal_moves1(self):
        board: C4Board = C4Board()
        expected: List[Move] = [Move(0), Move(1), Move(2), Move(3), Move(4), Move(5), Move(6)]
        actual: List[Move] = board.legal_moves
        actual.sort()
        self.assertEqual(expected, actual)

    def test_legal_moves2(self):
        position: List[List[int]] = [
            [2, 2, 0, 0, 0, 0],
            [1, 1, 1, 2, 1, 2],
            [1, 0, 0, 0, 0, 0],
            [2, 1, 2, 1, 2, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0]]
        board: C4Board = list_to_board(position, C4Piece.B)
        expected: List[Move] = [Move(0), Move(2), Move(3), Move(4), Move(5), Move(6)]
        actual: List[Move] = board.legal_moves
        actual.sort()
        self.assertEqual(expected, actual)


class C4DrawTestCase(unittest.TestCase):

    def test_draw1(self):
        position: List[List[int]] = [
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [1, 2, 1, 2, 1, 2],
            [1, 2, 0, 0, 0, 0],
            [1, 2, 1, 2, 1, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0]]
        board: C4Board = list_to_board(position, C4Piece.B)
        self.assertFalse(board.is_draw)

    def test_draw2(self):
        position: List[List[int]] = [
            [2, 1, 1, 1, 2, 2],
            [2, 1, 2, 1, 2, 1],
            [1, 2, 1, 2, 1, 2],
            [1, 2, 1, 2, 1, 2],
            [2, 2, 1, 2, 1, 2],
            [1, 1, 2, 1, 2, 1],
            [2, 1, 2, 1, 2, 1]]
        board: C4Board = list_to_board(position, C4Piece.B)
        self.assertTrue(board.is_draw)


class C4WinTestCase(unittest.TestCase):
    def test_win1(self):
        position: List[List[int]] = [
            [2, 1, 1, 1, 2, 2],
            [2, 1, 2, 1, 2, 1],
            [1, 2, 1, 2, 1, 2],
            [1, 2, 1, 2, 1, 2],
            [2, 2, 1, 2, 1, 2],
            [1, 1, 2, 1, 2, 1],
            [2, 1, 2, 1, 2, 1]]
        board: C4Board = list_to_board(position, C4Piece.B)
        self.assertFalse(board.is_win)

    def test_win2(self):
        position: List[List[int]] = [
            [2, 1, 2, 1, 2, 1],
            [2, 1, 2, 1, 2, 2],
            [1, 2, 1, 2, 1, 2],
            [1, 2, 1, 2, 1, 2],
            [2, 2, 1, 2, 1, 2],
            [1, 1, 2, 1, 2, 1],
            [2, 1, 2, 1, 1, 1]]
        board: C4Board = list_to_board(position, C4Piece.B)
        self.assertTrue(board.is_win)

    def test_win3(self):
        position: List[List[int]] = [
            [2, 1, 1, 1, 2, 2],
            [2, 1, 2, 1, 2, 2],
            [1, 2, 1, 2, 1, 2],
            [1, 2, 1, 2, 1, 1],
            [2, 2, 1, 2, 1, 2],
            [1, 1, 2, 1, 2, 1],
            [2, 1, 2, 1, 1, 2]]
        board: C4Board = list_to_board(position, C4Piece.B)
        self.assertTrue(board.is_win)

    def test_win4(self):
        position: List[List[int]] = [
            [2, 2, 2, 1, 2, 1],
            [2, 1, 2, 1, 2, 2],
            [1, 2, 1, 2, 1, 2],
            [1, 2, 1, 2, 1, 1],
            [2, 2, 1, 2, 1, 2],
            [1, 1, 2, 1, 2, 1],
            [2, 2, 1, 1, 1, 2]]
        board: C4Board = list_to_board(position, C4Piece.B)
        self.assertTrue(board.is_win)

    def test_win5(self):
        position: List[List[int]] = [
            [2, 2, 2, 2, 0, 0],
            [1, 1, 1, 0, 0, 0],
            [1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0]]
        board: C4Board = list_to_board(position, C4Piece.B)
        self.assertTrue(board.is_win)


class C4MinimaxTestCase(unittest.TestCase):
    def test_easy_position(self):
        # win in 1 move
        position: List[List[int]] = [
            [2, 2, 0, 0, 0, 0],
            [1, 1, 1, 0, 0, 0],
            [1, 0, 0, 0, 0, 0],
            [2, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0]]
        test_board1: C4Board = list_to_board(position, C4Piece.B)
        answer1: Move = find_best_move(test_board1, 3)
        self.assertEqual(answer1, 1)

    def test_easy_position2(self):
        # must block opponent from winning
        position: List[List[int]] = [
            [2, 2, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 0],
            [2, 2, 1, 0, 0, 0],
            [2, 1, 2, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0]]
        test_board2: C4Board = list_to_board(position, C4Piece.B)
        answer2: Move = find_best_move(test_board2, 3)
        self.assertEqual(answer2, 4)
    
    def test_block_position(self):
        # ai should block to prevent win
        position: List[List[int]] = [
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0],
            [1, 2, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0]]
        test_board3: C4Board = list_to_board(position, C4Piece.R)
        answer3: Move = find_best_move(test_board3, 3)
        self.assertIn(answer3, [1, 4])


if __name__ == '__main__':
    unittest.main()
