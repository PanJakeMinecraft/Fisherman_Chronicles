import unittest
from PyQt6.QtWidgets import QApplication
from tictac import TicTacToe 
from PyQt6.QtCore import QCoreApplication
from PyQt6.QtTest import QTest
import sys

class TestTicTac(unittest.TestCase):
    def __init__(self):
        super(TestTicTac, self).__init__()

    def setUp(self):
        self.game = TicTacToe()

    def initial_test(self):
        # Create a test game logic
         # check whether the board is empty at statr and player turn move
        pass

    def test_player_move(self):
       # check whether player move is correct
        pass

    def test_win(self):
        # This is the example I make (you can change based on your logic)
        self.game.game_logic(0, 0) 
        self.game.game_logic(1, 0)  
        self.game.game_logic(0, 1)  
        self.game.game_logic(1, 1)  
        self.game.game_logic(0, 2)  
    
    def test_draw(self):
        # create a move list
        # self.assertTrue(functions)
        pass

    def test_reset(self):
        # Reseet the game condition to initial state
        # test whether thsere is no error on test
        pass

class GUITicTacTest(unittest.TestCase):
    
    def setUp(self):
        self.app = QApplication(sys.argv)
        self.tictac_game = TicTacToe()

    def initial_tictac_gui(self):
        pass

    def test_playerGUI(self):
        pass

    def test_winGUI(self):
        pass

    def test_drawGUI(self):
        pass

    def test_gameRestartGUI(self):
        pass

    def test_resetGUI(self):
        pass

if __name__ == "__main__":
    unittest.main()