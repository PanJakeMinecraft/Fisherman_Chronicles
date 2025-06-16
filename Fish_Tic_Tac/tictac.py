from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import sys
from functools import partial
import random

class Color(QWidget):
    """This class is used for testing layout by applying bg colors"""
    def __init__(self, color_name):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color_name))
        self.setPalette(palette)


class MainWindow(QMainWindow):
    def __init__(self, plr_data = None, parent=None, **kwargs):
        super(MainWindow, self).__init__(parent, **kwargs)
        self.setWindowTitle("Ultimate tic tac toe")
        #self.setFixedSize(QSize(600,600))
        self.showFullScreen()
        self.plr_data = plr_data
        print(f"PLAYER DATA IN TIC TAC: {self.plr_data}")
        self.difficultly = "Easy"
        self.theme = "Dark Theme"
        self.gamemode = "Player VS Player"

        # central widget
        self.tic_tac = TicTacToe(self.gamemode, plr_data=self.plr_data)
        self.setCentralWidget(self.tic_tac)

        # We need to use stack widget (for change player vs player or player vs bot)
        self.stacking = QStackedWidget()
        self.stacking.setFixedSize(QSize(self.width(), self.height()))

        # Call the methods
        self.__create_menubar()
    
        # The stylesheet (main style)
        self.l_theme = """
        QWidget {
            background-color: #E5E5E5;
        }
        QMenuBar {
            background-color: #bEE3CE;
            color: black;
            font-size: 14px;
            font-family: Tahoma;
            padding: 10px;
            font-weight: bold;
        }
        QMenuBar::item {
            background: transparent;
            padding: 5px 15px;
            margin: 2px;
        }
        QMenuBar::item:selected {  /* Hover effect */
            background: #7393B3;
        }
        QMenu {
            background-color: #FFFFFF;
            color: black;
            border: 1px solid #FFFFFF;
        }
        QMenu::item {
            padding: 5px 20px;
            background-color: #FFFFFF;
            font-family: Tahoma;
            font-size: 12px;
            padding: 15px;
        }
        QMenu::item:selected {
            background-color: #7393B3;
        }
    """
        self.d_theme = """
        QWidget {
            background-color: #2D2D30;
        }
        QMenuBar {
            background-color: #007ACC;
            color: white;
            font-size: 14px;
            font-family: Tahoma;
            padding: 10px;
            font-weight: bold;
        }
        QMenuBar::item {
            background: transparent;
            padding: 5px 15px;
            margin: 2px;
        }
        QMenuBar::item:selected {  /* Hover effect */
            background: #00045d;
        }
        QMenu {
            background-color: #222;
            color: white;
            border: 1px solid #555;
        }
        QMenu::item {
            padding: 5px 20px;
            background-color: #555;
            font-family: Tahoma;
            font-size: 12px;
            padding: 15px;
        }
        QMenu::item:selected {
            background-color: #000000;
        }
    """
        self.setStyleSheet(self.d_theme)

        
    def __create_menubar(self):
            self.main_menu = self.menuBar()
            self.main_menu.setNativeMenuBar(False)
            
            # add the sub menu to main menu
            self.diffs = self.main_menu.addMenu("Difficulty")
            self.change_colors = self.main_menu.addMenu("Color Themes")
            self.modes = self.main_menu.addMenu("Tic Tac Toe mode")

            # add the menu actions to menubar
            set_diff = ["Easy", "Medium", "Hard"]
            for i in range(len(set_diff)):
                self.diff_action = QAction(set_diff[i], self)
                self.diffs.addAction(self.diff_action)
                self.diff_action.triggered.connect(lambda event, diff=set_diff[i]: self.menu_difficulty_chosen(diff))

            colors = ["Dark theme", "Light theme"]
            for j in range(len(colors)):
                self.theme_act = QAction(colors[j], self)
                self.change_colors.addAction(self.theme_act)
                self.theme_act.triggered.connect(lambda event, theme=colors[j]: self.color_choose_menu(theme))

            modes = ["Player VS Player", "Bot VS Player"]
            for k in range(len(modes)):
                self.action_mode = QAction(modes[k], self)
                self.modes.addAction(self.action_mode)
                self.action_mode.triggered.connect(lambda event, mode=modes[k]: self.menu_choose_mode(mode))

    def menu_choose_mode(self, mode):
        print(f"Mode choose: {mode}")
        # remove widget
        self.gamemode = mode
        self.setCentralWidget(None)
        self.tic_tac.deleteLater()
        self.tic_tac = None
        # re-create widget
        self.tic_tac = TicTacToe(self.gamemode, plr_data=self.plr_data)
        self.setCentralWidget(self.tic_tac)
        
    
    def color_choose_menu(self, theme):
        print(f"Choose theme: {theme}")
        self.theme = theme

        if self.theme == "Dark theme":
            self.setStyleSheet(self.d_theme)
        elif self.theme == "Light theme":
            self.setStyleSheet(self.l_theme)

    def menu_difficulty_chosen(self, diff):
        print(f"You choose diff: {diff}")
        self.difficultly = diff

        """Apply your difficulty logic here"""

    def go_back(self):
        from A_Title.choosemode import ChooseMode
  
        if not hasattr(self, "choosemode"):
            self.choosemode = ChooseMode(plr_data=self.plr_data, title="Choose mode")
        
        self.setStyleSheet("background-color: transparent")
        self.main_menu.hide()
        self.stacking.addWidget(self.choosemode)
        self.stacking.setCurrentWidget(self.choosemode)
        self.choosemode.show()
        self.tic_tac.hide()
        self.setCentralWidget(self.stacking)

class TicTacToe(QWidget):
    def __init__(self, gamemode, plr_data = None, parent=None, **kwargs):
        super(TicTacToe, self).__init__(parent, **kwargs)
        self.gamemode = gamemode
        self.plr_data = plr_data
        print("PLR DATA IN TIC TAC: {}".format(self.plr_data))
        self.current_player = "X"
        self.winner = ""

        # Main 
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.main_layout)
        
        # The Title (YOU NEED TO CHANGE WHEN CHANGE MODE, use .setText)
        self.title = QLabel("Tic Tac Toe")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        self.title.setStyleSheet("background-color: #e4abff; font-family: Tahoma; font-size: 50px; font-weight: bold; margin-bottom: 5px; margin-top: 5px;")
        self.main_layout.addWidget(self.title)

        # Tic tac toee layout
        self.grid_layout = QGridLayout()
        self.main_layout.addLayout(self.grid_layout)


        # Call the methods

        self.__create_buttons()

        # create the turns label (when player turn, just change status)
        self.status_lab = QLabel(f"Player turns: {self.current_player}")
        self.status_lab.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom)
        self.status_lab.setStyleSheet("font-family: Tahoma; font-size: 40px; font-weight: bold; margin-bottom: 10px;")
        self.main_layout.addWidget(self.status_lab)

        self.back_btn = QPushButton("Back")
        self.back_btn.setStyleSheet("background-color: red; font-weight: bold; font-family: Tahoma; font-size: 20px; color: white; width: 40px;")
        self.main_layout.addWidget(self.back_btn)
        self.back_btn.clicked.connect(lambda: self.click_back())
    
    def click_back(self):
        print(self.plr_data)
        self.main_window = MainWindow(plr_data=self.plr_data)
        self.main_window.go_back()

    def __create_buttons(self):
        self.board = [[QPushButton("") for _ in range(3)] for _ in range(3)]
        for row in range(3):
            for col in range(3):
                self.board[row][col].setFixedSize(QSize(300,250))
                self.board[row][col].setStyleSheet("font-size: 45px; background-color:#9de6ff; font-weight: bold; margin: 5px;")
                self.board[row][col].clicked.connect(partial(self.clickbtn, row, col))
                self.grid_layout.addWidget(self.board[row][col], row, col)

    def clickbtn(self, row, col):
        if self.board[row][col].text() == "" and self.winner == "":
            self.board[row][col].setText(self.current_player)

            if self.check_win():
                self.title.setText(f"{self.winner} wins!")
                return
            elif self.board_full() and not self.check_win():
                self.title.setText(f"No winner.")
                return
                    
            if self.current_player == "X":
                if self.gamemode == "Bot VS Player":
                    self.current_player = "O"
                    r = random.randint(0, 2)
                    c = random.randint(0, 2)
                    while self.board[r][c].text() != "":
                        r = random.randint(0, 2)
                        c = random.randint(0, 2)
                    self.board[r][c].setText(self.current_player)
                    if self.check_win():
                        self.title.setText(f"{self.winner} wins!")
                        return
                    elif self.board_full() and not self.check_win():
                        self.title.setText(f"No winner.")
                        return
                    self.current_player = "X"
                else:
                    self.current_player = "O"
            else:
                self.current_player = "X"

    def check_win(self):
        # rows
        for row in range(3):
            if (self.board[row][0].text() == self.board[row][1].text() == self.board[row][2].text()) and self.board[row][0].text() != "":
                self.board[row][0].setStyleSheet("color: yellow; font-size: 45px; background-color:#9de6ff; font-weight: bold; margin: 5px;")
                self.board[row][1].setStyleSheet("color: yellow; font-size: 45px; background-color:#9de6ff; font-weight: bold; margin: 5px;")
                self.board[row][2].setStyleSheet("color: yellow; font-size: 45px; background-color:#9de6ff; font-weight: bold; margin: 5px;")
                self.winner = self.board[row][0].text()
                return True

        # columns
        for col in range(3):
            if (self.board[0][col].text() == self.board[1][col].text() == self.board[2][col].text()) and self.board[0][col].text() != "":
                self.board[0][col].setStyleSheet("color: yellow; font-size: 45px; background-color:#9de6ff; font-weight: bold; margin: 5px;")
                self.board[1][col].setStyleSheet("color: yellow; font-size: 45px; background-color:#9de6ff; font-weight: bold; margin: 5px;")
                self.board[2][col].setStyleSheet("color: yellow; font-size: 45px; background-color:#9de6ff; font-weight: bold; margin: 5px;")
                self.winner = self.board[0][col].text()
                return True

        # diagonal
        if (self.board[0][0].text() == self.board[1][1].text() == self.board[2][2].text()) and self.board[0][0].text() != "":
            self.board[0][0].setStyleSheet("color: yellow; font-size: 45px; background-color:#9de6ff; font-weight: bold; margin: 5px;")
            self.board[1][1].setStyleSheet("color: yellow; font-size: 45px; background-color:#9de6ff; font-weight: bold; margin: 5px;")
            self.board[2][2].setStyleSheet("color: yellow; font-size: 45px; background-color:#9de6ff; font-weight: bold; margin: 5px;")
            self.winner = self.board[0][0].text()
            return True

        # anti-diagonal
        if (self.board[0][2].text() == self.board[1][1].text() == self.board[2][0].text()) and self.board[0][2].text() != "":
            self.board[0][2].setStyleSheet("color: yellow; font-size: 45px; background-color:#9de6ff; font-weight: bold; margin: 5px;")
            self.board[1][1].setStyleSheet("color: yellow; font-size: 45px; background-color:#9de6ff; font-weight: bold; margin: 5px;")
            self.board[2][0].setStyleSheet("color: yellow; font-size: 45px; background-color:#9de6ff; font-weight: bold; margin: 5px;")
            self.winner = self.board[0][2].text()
            return True

        # no winner
        return False
    
    def board_full(self):
        for row in range(3):
            for col in range(3):
                if self.board[row][col].text() == "":  
                    return False
        return True

class PlayerTicTac(QWidget):
    """This mode is when player vs player"""
    def __init__(self, plr_data = None, parent=None, **kwargs):
        super(PlayerTicTac, self).__init__(parent, **kwargs)
        self.plr_data = plr_data


def main():
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()