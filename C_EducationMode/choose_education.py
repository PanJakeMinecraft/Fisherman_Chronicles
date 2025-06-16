from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
import sys
import time

class Color(QWidget):
    def __init__(self, color_name):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color_name))
        self.setPalette(palette)

class EducationChoose(QMainWindow):
    def __init__(self, plr_data=None, parent=None, **kwargs):
        super(EducationChoose, self).__init__(**kwargs)
        
        # print the Plr data
        self.plr_data = plr_data
        print(f"\n\nPLAYER DATA IN EDUCATION SELECT: \n{self.plr_data}")

        # The window
        self.setWindowTitle("Fisherman Chronicles")
        self.showFullScreen()

        # Load custom fonts
        self.font_id = QFontDatabase.addApplicationFont("Z_custom_fonts/Jersey15-Regular.ttf")
        self.font_id2 = QFontDatabase.addApplicationFont("Z_custom_fonts/PixelifySans-VariableFont_wght.ttf")

        self.font_family = QFontDatabase.applicationFontFamilies(self.font_id)[0]
        self.custom_font = QFont(self.font_family)
        self.custom_font.setBold(True)

        self.font_family2 = QFontDatabase.applicationFontFamilies(self.font_id2)[0]
        self.custom_font2 = QFont(self.font_family2)
        self.custom_font2.setBold(False)

        # central widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # The stacking widget
        self.stacking = QStackedWidget(self.central_widget)
        self.stacking.setFixedSize(QSize(self.width(), self.height()))

        # load bg images
        self.bg_load = QPixmap(f"H_images\choose_modes\choose_education.png")
        self.bg_image = QLabel(self.central_widget)
        self.bg_image.setGeometry(0, 0, self.width(), self.height())
        self.bg_image.setPixmap(self.bg_load)
        self.bg_image.setScaledContents(True)

        # Call the methods
        self.__widget_components()

    
    def __widget_components(self):
        # prevent circular import
        """This method will use for widget creating and placing on the window"""
        from G_CustomWidgets.ChooseButtonLabel import ChooseButton

        self.vbox = QVBoxLayout(self.central_widget)  
        self.central_widget.setLayout(self.vbox)

        # Choose education mode layout
        self.h1 = QHBoxLayout()
        self.h1.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)
        self.vbox.addLayout(self.h1)

        # The choosemode Label
        self.edu = QLabel("EDUCATION MODE")
        self.edu.setObjectName("chose")
        self.edu.setStyleSheet(f"""
                               QLabel#chose{{
                               background-color: #0b0075;
                               color: white;
                               font-family: {self.font_family};
                               font-size: 140px;
                               margin-top: 40px;
                               border-radius: 5px;
                               padding-right: 40px;
                               padding-left: 40px;
                               }}
                               """)
        self.h1.addWidget(self.edu)

        # Mode buttons and layout
        self.h2 = QHBoxLayout()
        self.h2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.vbox.addLayout(self.h2)

        # Button custom widgets
        self.fish_book = ChooseButton("FISH INFO", r"H_images\choose_modes\fishbook.png")
        self.math_fish = ChooseButton("FISH MATH", r"H_images\choose_modes\onlineFish.png")
        self.fish_quiz = ChooseButton("FISH QUIZ", r"H_images\choose_modes\fishmath.png")

        self.fish_quiz.btn.clicked.connect(self.go_to_quiz)
        self.fish_book.btn.clicked.connect(self.information_book)

        # Add the buttons to the layout
        self.h2.addWidget(self.fish_book)
        self.h2.addWidget(self.math_fish)
        self.h2.addWidget(self.fish_quiz)

        # The sub layout (add hbox to vbox) (bottom left)
        self.hbox = QHBoxLayout() 
        self.vbox.addLayout(self.hbox)  
        self.hbox.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignLeft)

        self.back_btn = QPushButton("BACK")
        self.back_btn.setObjectName("back")
        self.back_btn.setStyleSheet(f"""
                                    QPushButton#back{{
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

                                    QPushButton#back:hover{{
                                        background-color: #ec0000;
                                    }}
                                    """)
        self.back_btn.clicked.connect(lambda: self.back_to_mode())
        self.hbox.addWidget(self.back_btn)

    def back_to_mode(self):
        from A_Title.choosemode import ChooseMode
        
        if not hasattr(self, "choosing"):
            self.choosing = ChooseMode(plr_data= self.plr_data)
        
        self.stacking.addWidget(self.choosing)
        self.stacking.setCurrentWidget(self.choosing)
        self.choosing.show()
        self.central_widget.hide()
        self.setCentralWidget(self.stacking)
    
    def go_to_quiz(self):
        from C_EducationMode.FishQuiz import MainWindow
        
        if not hasattr(self, "choose"):
            self.choose = MainWindow(plr_data= self.plr_data)

        self.close()

    
    def information_book(self):
        from C_EducationMode.FishBook import FishInformation
        
        if not hasattr(self, "book"):
            self.book = FishInformation(plr_data= self.plr_data)
        
        self.stacking.addWidget(self.book)
        self.stacking.setCurrentWidget(self.book)
        self.book.show()
        self.central_widget.hide()
        self.setCentralWidget(self.stacking)
        
def main():
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    window = EducationChoose()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()