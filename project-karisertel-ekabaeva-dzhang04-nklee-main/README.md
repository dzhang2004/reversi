# CMSC 14200 Course Project

Team members:
- Karis Ertel (Bot)
- Elizaveta Kabaeva (QA)
- Darian Zhang (TUI)
- Allison Lee (GUI)


Enhancements:
- GUI background music
- GUI title screen
- Using termcolor module for TUI player colors


Improvements:
1. Game logic: This component received two S's in Milestone 2.

2. Bot: This component received two S's in Milestone 2

3. GUI: This component received two S's in Milestone 2

        Some code quality improvements that were made:

        Code Quality Feedback 1: 20x20 board grid is too slow

        Previously 1: the draw_window method was drawing the entire board and highlighting
        the available moves while drawing the initial black and white board background, and then once
        the full board (including highlighting) was drawn, the player pieces would be drawn on top of this.

        Improvement 1: Altered so the draw_window method first draws the black and white board background,
        then in a different loop separately go through each of the available moves and highlight each avaiable move on the grid. After this, draw the player pieces on the board. Therefore, drawing the board background, highlighting the available moves, and drawing the pieces are all now done in separate for loops, meaning that the gui runs more quickly as everything isn't nested within each other.

        Code Quality Feedback 2: Clicking somewhere other than where a move is possible should have no effect.
        If the left corner is randomly clicked after the winner is announced in 20x20 reversi, the text that
        displays the winner changes to another player.

        Previously 2: Each conditional in the event loop was "if", so it checked for if the game was quit,
        if the game was done, and if the mouse button was pushed every loop.

        Improvement 2: changed it to "elif" instaead of "if" so that if the reversi is done, clicking somewhere on the screen won't do anything. If the game is quit, the for loop won't check if the game is done
        or if the mouse button is pushed; if the game is not quitted but done, the for loop won't check if the mouse button is pushed.

4. TUI: This component received two S's in Milestone 2

5. QA: This component received two S's in Milestone 2. Some tests function were divided into smaller test cases for legal_moves and available_moves: test_non_othello_8_1, test_non_othello_8_2, test_non_othello_8_3, test_non_othello_9_1, test_non_othello_9_2, test_non_othello_9_3.

Additional notes:
- We have only successfully tested our GUI background music enhancement using Mac computers, since by default WSL does not support audio.
