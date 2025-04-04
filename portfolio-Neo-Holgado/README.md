# portfolio-project

**Remember that this project cannot be submitted late.**

Pentago is a two-player abstract strategy game played on a 6×6 board, which is divided into four 3×3 sub-boards (or quadrants). Players take turns placing a marble of their color (either black or white) onto an unoccupied space on the board and then rotating one of the sub-boards by 90 degrees, either clockwise or anti-clockwise. The rotation step is mandatory, and the player can choose to rotate any of the four sub-boards, not necessarily the one where they placed the marble.

To learn how to play the game, check out this video: How to Play Pentago.[(https://boardgamegeek.com/video/482262/pentago/how-to-play-pentago)](https://boardgamegeek.com/video/482262/pentago/how-to-play-pentago) and you could play it by yourself in this website: [(https://pentago.vercel.app/)](https://pentago.vercel.app/)

A player wins by getting five of their marbles in a vertical, horizontal, or diagonal row, either before or after the sub-board rotation. If a player achieves five-in-a-row before the rotation step, the game ends immediately, and the player doesn't need to rotate a sub-board. If both players achieve five-in-a-row after the rotation, the game is a draw. If only the opponent gets a five-in-a-row after the rotation, the opponent wins. If all 36 spaces on the entire board are occupied without forming a row of five after the rotation, the game ends in a draw.

For example, after the white player places a marble on the board, several scenarios could occur:

If the white player achieves five-in-a-row, they win immediately.

If the white player does not achieve five-in-a-row, after the rotation:

* If neither white nor black has a five-in-a-row, the game continues.
* If black achieves five-in-a-row, black wins.
* If white achieves five-in-a-row, white wins.
* If both players achieve five-in-a-row, the game is a draw.
 
If neither white nor black has a five-in-a-row after the rotation and the board is full with 36 pieces, the game ends in a draw.

Here, we assume that **black will play first**. The figure "game_board" illustrates how the board will be labeled using our notation. ![board](game_board.png "game board")The four sub-boards are labeled with the integers 1, 2, 3, and 4, as shown in the figure. The six rows are labeled from 'a' to 'f' from top to bottom, and the six columns are labeled from '0' to '5' from left to right. Each space on the board can then be referred to as 'a0', 'a1', and so on.

Write a class named **Pentago** for playing this abstract board game. You will need to keep track of which player's turn it is.

Your Pentago class must include the following:

1.	An **init** method that initializes any data members
2.	A method called **get_game_state** that just returns **'UNFINISHED', 'WHITE_WON', 'BLACK_WON' or 'DRAW'**.
3.	A method called **is_board_full** that takes no parameter and return True or False that indicate whether the board is already full (True if full).
4.	A method called **make_move** that takes four parameters: 
* **Color**: a string that represent the color of the marble. It will be either ‘white’ or ‘black’ 
* **Position**: a string that represent the position the marble will be put onto the board. It will be like ‘a0’, ’b1’, etc.
* **Sub-board**: an integer of either 1, 2, 3 or 4 that represents the sub-board the player choose to rotate
* **Rotation**: a string that represent the direction the sub-board will rotate, either ‘C’ (clockwise) or ‘A’ (anti-clockwise).
  
For example, make_move('white', 'a2', 1, 'C'). You can assume all user inputs will be valid when the make_move method is called. The method should verify the following special cases:
* If the game is finished at this stage, the method should do nothing else and return **"game is finished"**
* If the color of the piece to be placed doesn't match the current player's color, the method should do nothing but return **"not this player's turn"**
* If the position where the piece is to be placed is already taken, the method should return **"position is not empty"**
  
Otherwise, it should **place** the marble onto the board, **rotate** the sub-board (if the player hasn't won after placing the marble), **update** the board and game state (from unfinished to indicate who wins, if necessary), **update** whose turn it is, and **return True**. 

Since this method handles most of the gameplay tasks, you can call other methods within it. For example, you could have a separate method to check if a player has achieved a 5-in-a-row, and call this method in make_move both before and after the rotation to determine the win state. You could also have a separate method to handle rotating the sub-board, given the sub-board number and the rotation direction.

5. You need to implement a method called **print_board** that outputs the current state of the board. This will be extremely helpful for testing. You can choose any format for displaying the board, provided it is legible to others. If you're uncertain about the acceptability of your format, ask it on the discussion board.
   
Feel free to add whatever other classes, methods, or data members you want. All data members of a class must be **private**. Every class should have an init method that initializes all of the data members for that class.
The file must be named: **Pentago.py**

Here's a very simple example of how the class could be used:

```
game = Pentago()
print(game.make_move('black', 'a2', 1, 'C'))
print(game.make_move('white', 'a2', 1, 'C'))
print(game.is_board_full())
game.print_board()
print(game.get_game_state())

```
And the output could look like this:

True

True

False

□   □   □   □   □   □

□   □   □   □   □   □

●   □   ○   □   □   □

□   □   □   □   □   □

□   □   □   □   □   □

□   □   □   □   □   □

UNFINISHED

