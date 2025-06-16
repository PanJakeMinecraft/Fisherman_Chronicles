from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
import sys
import time

class ModeButton(QWidget):
    def __init__(self, txt, icon_path=None, parent=None):
        super(ModeButton, self).__init__(parent) 
        self.setObjectName(txt.lower().replace(" ", "_"))
        self.txt = txt
        self.icon_path = icon_path
        
        # Load custom fonts
        self.font_id = QFontDatabase.addApplicationFont("Z_custom_fonts/Jersey15-Regular.ttf")
        self.font_id2 = QFontDatabase.addApplicationFont("Z_custom_fonts/PixelifySans-VariableFont_wght.ttf")

        self.font_family = QFontDatabase.applicationFontFamilies(self.font_id)[0]
        self.custom_font = QFont(self.font_family)
        self.custom_font.setBold(True)

        self.font_family2 = QFontDatabase.applicationFontFamilies(self.font_id2)[0]
        self.custom_font2 = QFont(self.font_family2)
        self.custom_font2.setBold(False)

        self.btn = QPushButton(self)
        self.btn.setObjectName("btn") 

        if self.icon_path:
            self.btn.setIcon(QIcon(self.icon_path))
            self.btn.setIconSize(QSize(300,400)) 

        self.label = QLabel(self.txt, self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        self.label.setFixedSize(QSize(380,70))

        self.layouts_ = QVBoxLayout(self)
        self.layouts_.addWidget(self.btn)
        self.setLayout(self.layouts_)

        self.subLayout = QHBoxLayout()
        self.subLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subLayout.addWidget(self.label)
        self.layouts_.addLayout(self.subLayout)

        self.setStyleSheet(f"""
            QPushButton#btn {{
                background-color: #150063;
                font-family: {self.font_family2};
                font-size: 30px;
                color: white;
                margin: 30px;
                width: 250px;
                height: 270px;
                padding: 20px;
                text-align: center;
                border-radius: 10px;
                border: 5px outset #a01fc3;
                font-weight: bold;
                position: relative;
            }}

            QPushButton#btn:hover {{
                background-color: #070d35;
            }}

            QPushButton#btn:pressed {{
                background-color: #2c0330;
            }}

            QLabel {{
                color: white;
                font-size: 70px;
                font-family: {self.font_family};
                font-weight: bold;
                background-color: rgba(255, 18, 230, 0.7);
                border-radius: 10px;
            }}
        """)

class Color(QWidget):
    def __init__(self, color_name):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color_name))
        self.setPalette(palette)

class ChooseMode(QMainWindow): # inherit from QMainWindow
    def __init__(self, plr_data=None, title=None, **kwargs):
        super(ChooseMode, self).__init__(**kwargs)
        self.setWindowTitle(title)
        self.showFullScreen()  

        # The custom fonts
        """These fonts will be use within the game"""
        self.font_id = QFontDatabase.addApplicationFont("Z_custom_fonts\Jersey15-Regular.ttf")
        self.font_id2 = QFontDatabase.addApplicationFont("Z_custom_fonts\PixelifySans-VariableFont_wght.ttf")

        self.font_family = QFontDatabase.applicationFontFamilies(self.font_id)[0] 
        self.custom_font = QFont(self.font_family) 
        self.custom_font.setBold(True)

        self.font_family2 = QFontDatabase.applicationFontFamilies(self.font_id2)[0] 
        self.custom_font2 = QFont(self.font_family2) 
        self.custom_font2.setBold(False)

        # call player data from previous class passing
        self.plr_data = plr_data
        print(f"\n\n\nCHOOSE MODE PLR\n{self.plr_data}")

        # central widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # The stacking widget
        self.stacking = QStackedWidget(self.central_widget)
        self.stacking.setFixedSize(QSize(self.width(), self.height()))

        # load bg images
        self.bg_load = QPixmap(f"H_images\choose_modes\choosemode.png")
        self.bg_image = QLabel(self.central_widget)
        self.bg_image.setGeometry(0, 0, self.width(), self.height())
        self.bg_image.setPixmap(self.bg_load)
        self.bg_image.setScaledContents(True)

        # The stylesheet
        self.setStyleSheet(f"""
            QPushButton#back {{
                background-color: #b6032a;
                font-family: {self.font_family};
                font-size: 40px;
                color: white;
                margin-bottom: 40px;
                margin-left: 30px;
                width: 190px;
                height: 60px;
                border: 0px;
                border-radius: 5px;
            }}

            QLabel#chose{{
                color: white;
                font-family: {self.font_family};
                font-weight: bold;
                font-size: 150px;
                margin-top: 60px;b
                background-color: transparent;
            }}

            QPushButton#back:hover {{
                background-color: #ec0000;
            }}

        """)

        # call the methods
        self.__mode_choosing()

    def __mode_choosing(self): # private method

        # main layout
        self.vbox = QVBoxLayout(self.central_widget)  
        self.central_widget.setLayout(self.vbox)

        # Choose mode layout
        self.h1 = QHBoxLayout()
        self.h1.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)
        self.vbox.addLayout(self.h1)

        # The choosemode Label
        self.choose_lab = QLabel("CHOOSE MODE")
        self.choose_lab.setObjectName("chose")
        self.h1.addWidget(self.choose_lab)

        # Mode buttons and layout
        self.h2 = QHBoxLayout()
        self.h2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.vbox.addLayout(self.h2)

        # Button custom widgets
        self.story_mode = ModeButton("STORY",r"H_images\choose_modes\storymode.png")
        self.tictac = ModeButton("TIC-TAC-TOE", r"H_images\choose_modes\tictac.png")
        self.fish_attack = ModeButton("FISH ATTACK", r"H_images\choose_modes\FishAttack.png")
        self.education = ModeButton("EDUCATION", r"H_images\choose_modes\EducationFish.png")

        # Set it to checkable
        self.story_mode.btn.setCheckable(True) 
        self.tictac.btn.setCheckable(True) 
        self.fish_attack.btn.setCheckable(True)
        self.education.btn.setCheckable(True)

        self.story_mode.btn.clicked.connect(lambda checked: self.go_to_story_mode(checked)) # call click of the button, the button name (btn)
        self.education.btn.clicked.connect(lambda: self.go_to_education())
        self.fish_attack.btn.clicked.connect(lambda: self.go_to_fishAttack())
        self.tictac.btn.clicked.connect(lambda: self.go_to_tic_tac())

        # Add the buttons to the layout
        self.h2.addWidget(self.story_mode)
        self.h2.addWidget(self.tictac)
        self.h2.addWidget(self.fish_attack)
        self.h2.addWidget(self.education)

        # The sub layout (add hbox to vbox) (bottom left)
        self.hbox = QHBoxLayout() 
        self.vbox.addLayout(self.hbox)  
        self.hbox.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignLeft)

        self.back_btn = QPushButton("BACK")
        self.back_btn.setObjectName("back")
        self.back_btn.clicked.connect(self.go_back_title)
        self.hbox.addWidget(self.back_btn)

    def go_back_title(self):
        from A_Title.title_page import TitlePage
        
        if not hasattr(self, "title_back"):
            self.title_back = TitlePage(plr_data= self.plr_data)
        
        self.stacking.addWidget(self.title_back)
        self.stacking.setCurrentWidget(self.title_back)
        self.title_back.show()
        self.central_widget.hide()
        self.setCentralWidget(self.stacking)

    def go_to_story_mode(self, event):
        from AA_StoryMode.MainControl import MainWindow
        print(f"Going to story mode: {event}")

        if not hasattr(self, "story_mode_click"):
            self.story_mode_click = MainWindow(plr_data= self.plr_data)
        
        self.stacking.addWidget(self.story_mode_click)
        self.stacking.setCurrentWidget(self.story_mode_click)
        self.story_mode_click.show()
        self.central_widget.hide()
        self.setCentralWidget(self.stacking)

    def go_to_tic_tac(self):
        from Fish_Tic_Tac.tictac import MainWindow
        
        if not hasattr(self, "tic_tac"):
            self.tic_tac = MainWindow(plr_data=self.plr_data)
        
        self.stacking.addWidget(self.tic_tac)
        self.setStyleSheet("background-color: transparent;")
        self.stacking.setCurrentWidget(self.tic_tac)
        self.tic_tac.show()
        self.central_widget.hide()
        self.setCentralWidget(self.stacking)

    def go_to_fishAttack(self):
        from B_FishAttack.FishAttack import FishAttack
        
        if not hasattr(self, "fishing_att"):
            self.fishing_att = FishAttack(plr_data=self.plr_data)
        
        self.stacking.addWidget(self.fishing_att)
        self.stacking.setCurrentWidget(self.fishing_att)
        self.fishing_att.show()
        self.central_widget.hide()
        self.setCentralWidget(self.stacking)

    def go_to_education(self):
        from C_EducationMode.choose_education import EducationChoose
        
        if not hasattr(self, "title_back"):
            self.educationChoose = EducationChoose(plr_data= self.plr_data)
        
        self.stacking.addWidget(self.educationChoose)
        self.stacking.setCurrentWidget(self.educationChoose)
        self.educationChoose.show()
        self.central_widget.hide()
        self.setCentralWidget(self.stacking)

def main():
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
        
    window = ChooseMode(title="Choose Mode")
    window.show()
    app.exec()

if __name__ == "__main__":
    main()