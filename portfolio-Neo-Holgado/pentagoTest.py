# Author: Neo Holgado
# GitHub Username: Neo-Holgado
# Date: 08/08/2024
# Description: Tests for Pentago.py

import unittest
from Pentago import *


class TestPentago(unittest.TestCase):
    """
    Contains unit tests for the Pentago class
    """

    def setUp(self):
        """
        Initializes a new Pentago game before each test.
        """
        self.pentago = Pentago()

    def test_initial_game_state(self):
        """
        Tests that the initial game state is 'UNFINISHED' and the starting player is None.
        """
        self.assertEqual(self.pentago.get_game_state(), 'UNFINISHED')
        self.assertIsNone(self.pentago.get_current_player())

    def test_set_current_player(self):
        """
        Tests setting the current player.
        """
        self.pentago.set_current_player('WHITE')
        self.assertEqual(self.pentago.get_current_player(), 'WHITE')

        self.pentago.set_current_player('BLACK')
        self.assertEqual(self.pentago.get_current_player(), 'BLACK')

    def test_make_move_valid(self):
        """
        Tests making a valid move and checking game state transitions.
        """
        self.pentago.set_current_player('WHITE')
        result = self.pentago.make_move('WHITE', 'a2', 1, 'C')
        self.assertTrue(result)  # Move should be valid
        self.assertEqual(self.pentago.get_game_state(), 'UNFINISHED')

    def test_make_move_invalid(self):
        """
        Tests making an invalid move and checking the response.
        """
        self.pentago.set_current_player('WHITE')
        self.pentago.make_move('WHITE', 'a2', 1, 'C')
        result = self.pentago.make_move('BLACK', 'a2', 1, 'C')  # Invalid move, cell already occupied
        self.assertEqual(result, "Invalid Move")

    def test_make_move_win_condition(self):
        """
        Tests making a move that results in a win.
        """
        self.pentago.set_current_player('WHITE')
        # Simulate a sequence of moves that results in a win
        for pos in ['a1', 'a2', 'a3', 'a4', 'a5']:
            self.pentago.make_move('WHITE', pos, 1, 'C')
        self.assertEqual(self.pentago.get_game_state(), 'WHITE_WON')

    def test_make_move_draw_condition(self):
        """
        Tests making moves that result in a draw.
        """
        self.pentago.set_current_player('WHITE')
        # Simulate moves to fill the board and check for draw
        moves = [
            ('WHITE', 'a1'), ('BLACK', 'a2'), ('WHITE', 'a3'),
            ('BLACK', 'a4'), ('WHITE', 'a5'), ('BLACK', 'a6'),
            # Add more moves to fill the board
        ]
        for color, pos in moves:
            self.pentago.make_move(color, pos, 1, 'C')
        self.assertEqual(self.pentago.get_game_state(), 'DRAW')


class TestGameBoard(unittest.TestCase):
    """
    Contains unit tests for the GameBoard class
    """

    def test_game_board_init(self):
        """
        Tests if a 6x6 game board and 4 3x3 sub-boards are created
        """
        test_game_board = GameBoard()
        board = test_game_board.get_board()

        self.assertEqual(len(board), 6)
        self.assertEqual(len(board[0]), 6)

        for row in board:
            for cell in row:
                self.assertEqual(cell, '.')

        for num in range(1, 5):
            sub_board = test_game_board.get_sub_board(num)
            self.assertEqual(len(sub_board), 3)
            self.assertEqual(len(sub_board[0]), 3)

            for row in sub_board:
                for cell in row:
                    self.assertEqual(cell, '.')


class TestSubBoard(unittest.TestCase):
    """
    Contains unit tests for the SubBoard class
    """

    def test_sub_board_rotation(self):
        """
        Tests if the sub-board was rotated correctly
        """
        sub_board = SubBoard()
        sub_board._sub_board = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]

        clockwise_rotation = [
            [7, 4, 1],
            [8, 5, 2],
            [9, 6, 3]
        ]

        sub_board.rotate('C')
        self.assertEqual(sub_board._sub_board, clockwise_rotation)

        sub_board._sub_board = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]

        counterclockwise_rotation = [
            [3, 6, 9],
            [2, 5, 8],
            [1, 4, 7]
        ]

        sub_board.rotate('A')
        self.assertEqual(sub_board._sub_board, counterclockwise_rotation)


class TestGameLog(unittest.TestCase):
    """
    Contains unit tests for the GameLog class
    """

    def setUp(self):
        """
        Initializes a new GameLog before each test.
        """
        self.game_log = GameLog()

    def test_initial_log_empty(self):
        """
        Tests that the initial game log is empty.
        """
        self.assertEqual(self.game_log.get_game_log(), [])

    def test_log_move(self):
        """
        Tests logging a move.
        """
        self.game_log.log_move("WHITE placed on a2")
        log_entries = self.game_log.get_game_log()
        self.assertEqual(len(log_entries), 1)
        self.assertEqual(log_entries[0], "Move: WHITE placed on a2")

    def test_log_game_state(self):
        """
        Tests logging a game state.
        """
        self.game_log.log_game_state("WHITE_WON")
        log_entries = self.game_log.get_game_log()
        self.assertEqual(len(log_entries), 1)
        self.assertEqual(log_entries[0], "Game State: WHITE_WON")

    def test_review_log(self):
        """
        Tests reviewing the game log.
        """
        # Add some entries to the log
        self.game_log.log_move("WHITE placed on a2")
        self.game_log.log_game_state("UNFINISHED")
        self.game_log.log_move("BLACK placed on b3")
        self.game_log.log_game_state("WHITE_WON")

        # Capture the log entries
        log_entries = self.game_log.get_game_log()

        # Manually check each entry in the log
        self.assertEqual(len(log_entries), 4)
        self.assertEqual(log_entries[0], "Move: WHITE placed on a2")
        self.assertEqual(log_entries[1], "Game State: UNFINISHED")
        self.assertEqual(log_entries[2], "Move: BLACK placed on b3")
        self.assertEqual(log_entries[3], "Game State: WHITE_WON")


if __name__ == '__main__':
    unittest.main()