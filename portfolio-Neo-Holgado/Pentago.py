# Author: Neo Holgado
# GitHub Username: Neo-Holgado
# Date: 08/08/2024
# Description: Pentago game simulator

class Pentago:
    """
    Represents the game of Pentago.
    Manages game setup, game state, and game logic
    """
    def __init__(self):
        self._board = GameBoard()
        self._current_player = None
        self._opponent = None
        self._game_state = 'UNFINISHED'
        self._game_log = GameLog()

    def get_current_player(self) -> str:
        """
        Retrieves the current player
        :return: The current player
        """
        return self._current_player

    def set_current_player(self, marble_color: str) -> None:
        """
        Sets the current player's marble color as the current player
        :param marble_color: Marble color
        """
        self._current_player = marble_color

    def get_opponent(self) -> str:
        """
        Retrieves the opponent on current turn
        :return: Opponent of current turn
        """
        return self._opponent

    def set_opponent(self, opponent: str) -> None:
        """
        Sets the opponent's marble color
        :param opponent: Current turn's opponent
        """
        self._opponent = opponent

    def get_game_state(self) -> str:
        """
        Retrieves the current game state.
        :return: String 'UNFINISHED', 'WHITE_WON', 'BLACK_WON', or 'DRAW'
        """
        return self._game_state

    def set_game_state(self, game_state: str) -> None:
        """
        Sets the current game state
        :param game_state: String 'UNFINISHED', 'WHITE_WON', 'BLACK_WON', or 'DRAW'
        """
        self._game_state = game_state

    def is_board_full(self) -> bool:
        """
        Checks if the game board is full.
        :return: True if the board is full
        """
        return self._board.is_full()

    @staticmethod
    def convert_position(position: str) -> tuple:
        """
        Converts the string position into a tuple of indices (row, column)
        :param position: String position
        :return: Tuple of indices (row, column)
        """
        letter_conversion = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5}
        row_index = letter_conversion[position[0].lower()]      # Convert 'a' to 0 etc.
        column_index = int(position[1])                         # Convert '1' to 0 etc.

        indices = (row_index, column_index)
        return indices

    def make_move(self, marble_color: str, position: str, sub_board: str, rotation: str) -> bool:
        """
        Makes a move in the Pentago game.
        :param marble_color: String 'white' or 'black' representing the player's color
        :param position: Tuple (row, column) representing the position on the board
        :param sub_board: Integer representing the sub-board to be rotated (1, 2, 3, 4)
        :param rotation: String 'C' for clockwise or 'A' for counterclockwise rotation
        :return: String message if game is finished or move is invalid, otherwise return True
        """
        # Convert the position to correct indices
        position = self.convert_position(position)

        # Convert marble color to marble and update current player
        marble_color = "W" if marble_color.upper() == "WHITE" else "B"
        self._current_player = marble_color

        # If the move is valid
        player = self.get_current_player()
        validation_result = self.is_valid_move(position, player)
        if validation_result is not True:
            return validation_result

        # Place a marble on the board
        self._board.update_game_board(marble_color, position)

        # Check for a win before rotating
        game_state = self._board.check_end_conditions(marble_color)
        if game_state != "UNFINISHED":
            self.set_game_state(game_state)
            return True

        # Rotate the sub-board
        self._board.rotate_sub_board(sub_board, rotation)

        # Update the main board from sub-boards
        self._board.update_board_from_sub_boards()

        # Define player win
        current_player_win = self._board.check_end_conditions(marble_color)

        # Define the opponents color
        opponent_color = "W" if marble_color == "B" else "B"
        self.set_opponent(opponent_color)

        # Define opponent win
        opponent_win = self._board.check_end_conditions(opponent_color)

        # Check for wins after rotating and convert colors
        convert_color = {'W': 'WHITE', 'B': 'BLACK'}
        current_player_color = convert_color[self.get_current_player()]
        current_opponent_color = convert_color[self.get_opponent()]

        # Check for both players winning after rotation
        if current_player_win:
            if opponent_win:
                self.set_game_state("DRAW")
                return True
            else:
                self.set_game_state(f"{current_player_color}_WON")
                return True

        # Check if opponent won
        if opponent_win:
            self.set_game_state(f"{current_opponent_color}_WON")
            return True

        # Check if the board is full after the move
        if self.is_board_full():
            self.set_game_state("DRAW")
            return True

        # If there is no win or draw, switch the player and log the move
        self._game_log.log_move(marble_color, position, sub_board, rotation)
        self.switch_player()

        return True

    def is_valid_move(self, position: str, player: str) -> None:
        """
        Checks if the move is valid.
        :param position: Tuple (row, column) representing the position on the board
        :param player: Current player
        :return: True if the move is valid, else False
        """
        # Check if the game is already finished
        if self.get_game_state() != 'UNFINISHED':
            return "game is finished"

        # Check if it's the correct players turn
        if player == self.get_opponent():
            return "not this player's turn"

        # Check if a marble is already in the current position
        # Find the row and column from position
        row, column = position

        # Checks if the cell at position is empty
        if self._board.get_board()[row][column] != '.':
            return "position is not empty"

        # If checks pass, then valid move
        return True

    def switch_player(self) -> None:
        """
        Switches the current player and the opponent
        """
        # Switches current player and opponent
        if self.get_current_player() == 'B':
            self.set_current_player('W')
            self.set_opponent('B')
        elif self.get_current_player() == 'W':
            self.set_current_player('B')
            self.set_opponent('W')

    def print_board(self) -> None:
        """
        Prints the current state of the game board.
        """
        for row in self._board.get_board():
            row_display = ' '.join(row)
            print(row_display)


class GameBoard:
    """
    Represents the 6x6 Pentago game board.
    Defines the positions for each space on the game board (by row and column).
    Displays the board to the user and updates the board state.
    Communicates marble positions and board changes to Pentago class.
    """
    def __init__(self):
        # Initialize the 6x6 game board as a 2D list
        self._game_board = [
            ['.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.']
        ]

        # Initialize 4 3x3 sub-boards
        self._sub_boards = {
            1: SubBoard(self._game_board, 0, 0),
            2: SubBoard(self._game_board, 0, 3),
            3: SubBoard(self._game_board, 3, 0),
            4: SubBoard(self._game_board, 3, 3)
        }

    def get_board(self):
        """
        Retrieves the current game board
        :return: Current game board
        """
        return self._game_board

    def get_sub_board(self, sub_board_num):
        """
        Retrieves the requested sub_board
        :return: The requested sub_board
        """
        return self._sub_boards[sub_board_num].get_sub_board()

    def update_game_board(self, marble_color, position):
        """
        Adds a marble to the current game board
        :param marble_color: String 'white' or 'black' representing the player's color
        :param position: Tuple (row, column) representing the position on the board
        """
        row, col = position
        self._game_board[row][col] = marble_color

    def rotate_sub_board(self, sub_board, rotation):
        """
        Communicates with SubBoard class to rotate a specific sub-board either CW or CCW.
        :param sub_board: Integer representing the sub-board to be rotated (1, 2, 3, 4)
        :param rotation: String 'C' for clockwise or 'A' for counterclockwise rotation
        """
        # Rotate the sub-board
        self._sub_boards[sub_board].rotate(rotation)

        # Update the main board to incorporate rotated sub-board
        self.update_board_from_sub_boards()

    def update_board_from_sub_boards(self):
        """
        Updates the main board with the current state of sub-boards.
        """
        # Map the sub-board indices to the main board's corner positions
        sub_board_map = {
            1: (0, 0),
            2: (0, 3),
            3: (3, 0),
            4: (3, 3)
        }

        # Iterate through each sub-board and update the corresponding section of the main board
        for sub_board_num, (starting_row, starting_column) in sub_board_map.items():
            sub_board = self._sub_boards[sub_board_num].get_sub_board()
            for row in range(3):        # For each row in the sub-board
                for column in range(3):     # For each column in the sub-board
                    self._game_board[starting_row + row][starting_column + column] = sub_board[row][column]

    def is_full(self):
        """
        Checks if a marble is placed on every position
        :return: True if full, else False
        """
        for row in self._game_board:
            if '.' in row:
                return False

        return True

    def check_end_conditions(self, current_player_color):
        """
        Checks for win/loss/draw conditions and updates game state
        :param current_player_color: Color of the player who just made a move
        :return: 'UNFINISHED', 'WHITE_WON', 'BLACK_WON', or 'DRAW' depending on end condition
        """
        def check_five_in_a_row(board, color):
            """
            Checks for five marbles in a row horizontally and vertically
            :param board: The current state of the game board
            :param color: color of the player's marble
            :return: True if there are 5 marbles in a row, else False
            """
            # Check rows
            for row in range(6):
                for column in range(2):
                    if (
                            board[row][column] == color and
                            board[row][column + 1] == color and
                            board[row][column + 2] == color and
                            board[row][column + 3] == color and
                            board[row][column + 4] == color
                    ):
                        return True

            # Check columns
            for column in range(6):
                for row in range(2):
                    if (
                            board[row][column] == color and
                            board[row + 1][column] == color and
                            board[row + 2][column] == color and
                            board[row + 3][column] == color and
                            board[row + 4][column] == color
                    ):
                        return True

            # Check diagonals from top-left to bottom-right
            for row in range(2):
                for column in range(2):
                    if (
                            board[row][column] == color and
                            board[row + 1][column + 1] == color and
                            board[row + 2][column + 2] == color and
                            board[row + 3][column + 3] == color and
                            board[row + 4][column + 4] == color
                    ):
                        return True

            # Check diagonals from top-right to bottom-left
            for row in range(2):
                for column in range(2, 6):
                    if (
                            board[row][column] == color and
                            board[row + 1][column - 1] == color and
                            board[row + 2][column - 2] == color and
                            board[row + 3][column - 3] == color and
                            board[row + 4][column - 4] == color
                    ):
                        return True

            return False

        # Check if the current player has won
        if check_five_in_a_row(self._game_board, current_player_color):
            return True

        # Game is not finished
        return False


class SubBoard:
    """
    Represents a 3x3 sub-board.
    Handles the rotation of the sub-board by 90 degrees.
    Communicates the transformed positions to GameBoard class.
    """
    def __init__(self, main_board, start_row, start_col):
        # Reference the main board
        self._main_board = main_board
        self._start_row = start_row
        self._start_col = start_col

    def get_sub_board(self):
        """
        Retrieves the current sub-board
        :return: The current sub-board
        """
        sub_board = []
        for row in range(3):
            rows = []
            for col in range(3):
                rows.append(self._main_board[self._start_row + row][self._start_col + col])
            sub_board.append(rows)
        return sub_board

    def rotate(self, rotation):
        """
        Rotates the sub-board by 90 degrees clockwise 'C' or counterclockwise 'A'.
        :param rotation: String 'C' for clockwise or 'A' for counterclockwise
        """
        # Retrieve the current sub-board
        sub_board = self.get_sub_board()

        if rotation == 'C':
            # Rotate 90 degrees clockwise
            rotated_board = [
                [sub_board[2][0], sub_board[1][0], sub_board[0][0]],
                [sub_board[2][1], sub_board[1][1], sub_board[0][1]],
                [sub_board[2][2], sub_board[1][2], sub_board[0][2]]
            ]
        elif rotation == 'A':
            # Rotate 90 degrees counterclockwise
            rotated_board = [
                [sub_board[0][2], sub_board[1][2], sub_board[2][2]],
                [sub_board[0][1], sub_board[1][1], sub_board[2][1]],
                [sub_board[0][0], sub_board[1][0], sub_board[2][0]]
            ]

        # Update main board with rotated sub-board
        for row in range(3):
            for col in range(3):
                self._main_board[self._start_row + row][self._start_col + col] = rotated_board[row][col]


class GameLog:
    """
    Logs the game's events, moves, and state changes for debugging.
    Records all moves and board transformations.
    Allows review of previous game moves.
    """
    def __init__(self):
        self._game_log = []  # Stores moves made and game states

    def get_game_log(self):
        """
        Retrieves the game log of previous moves and game states
        :return: Game log of previous moves and game states
        """
        return self._game_log

    def log_move(self, marble_color, position, sub_board, rotation):
        """
        Logs a move in the Pentago game.
        :param marble_color: String 'white' or 'black' representing the player's color
        :param position: Tuple (row, column) representing the position on the board
        :param sub_board: Integer representing the sub-board to be rotated (1, 2, 3, 4)
        :param rotation: String 'C' for clockwise or 'A' for counterclockwise rotation
        """
        # Converts rotation abbreviation to full word
        rotation_converted = "Clockwise" if rotation == "C" else "A"

        # Logs the move
        self._game_log.append(f"{marble_color} was placed on {position}, sub-board {sub_board} was rotated {rotation_converted}")

    def log_game_state(self, game_state):
        """
        Logs current game states
        :param game_state: Current game state
        :return:
        """
        self._game_log.append(f"Game State: {game_state}")

    def review_log(self):
        """
        Reviews the log of all moves made in the game.
        """
        for entry in self._game_log:
            print(entry)


def main():
    game = Pentago()
    game_log = GameLog()
    print(game.make_move('black', 'a2', 1, 'C'))
    print(game.make_move('white', 'a2', 1, 'C'))
    print(game.make_move('black', 'a2', 1, 'C'))
    print(game.make_move('white', 'a2', 1, 'C'))
    print(game.make_move('white', 'a3', 1, 'C'))
    print(game.make_move('white', 'd2', 3, 'C'))
    print(game.is_board_full())
    game.print_board()
    print(game.get_game_state())


if __name__ == '__main__':
    main()