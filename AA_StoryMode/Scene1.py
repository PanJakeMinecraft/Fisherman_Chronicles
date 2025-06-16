from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from abc import ABC, abstractmethod
import sys
from G_CustomWidgets.TextAnim import AnimateCharacterWindow
from Sprites.Player import PlayerAnimate
from time import sleep as delay

class Color(QWidget):
    def __init__(self, color_name):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color_name))
        self.setPalette(palette)

class FirstScene(QMainWindow):
    def __init__(self, parent = None, plr_data= None, **kwargs):
        super(FirstScene, self).__init__(parent, **kwargs)
        self.setWindowTitle("Fisherman Chronicles")
        self.showFullScreen()

        self.plr_data = plr_data
        print(f"\n\nPLR DATA IN SCENE1: {self.plr_data}")

        # central widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.setStyleSheet("background-color: black;")

        # stack widget
        self.stack_widget = QStackedWidget(self.central_widget)
        self.stack_widget.setFixedSize(QSize(self.width(), self.height()))

        self.bg_load = QPixmap(fr"H_images\choose_modes\forest2.png")
        self.bg_image = QLabel(self.central_widget)
        self.bg_image.setGeometry(0, 0, self.width(), self.height())
        self.bg_image.setPixmap(self.bg_load)
        self.bg_image.setScaledContents(True)

        # Call the methods
        self.load_fonts()
        self.__widgets_comp()
        self.first_text()

    def load_fonts(self):
        self.font_id = QFontDatabase.addApplicationFont("Z_custom_fonts/Jersey15-Regular.ttf")
        self.font_id2 = QFontDatabase.addApplicationFont("Z_custom_fonts/PixelifySans-VariableFont_wght.ttf")

        self.font_family = QFontDatabase.applicationFontFamilies(self.font_id)[0]
        self.custom_font = QFont(self.font_family)
        self.custom_font.setBold(True)

        self.font_family2 = QFontDatabase.applicationFontFamilies(self.font_id2)[0]
        self.custom_font2 = QFont(self.font_family2)
        self.custom_font2.setBold(False)

    def __widgets_comp(self):
        self.vbox = QVBoxLayout(self.central_widget)
        self.vbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.central_widget.setLayout(self.vbox)
        self.vbox.setStretch(0, 5)

        self.hbox = QHBoxLayout()
        self.vbox.addLayout(self.hbox)

        self.bottom_layout = QHBoxLayout()
        self.vbox.addLayout(self.bottom_layout)

################### Text methods
    def first_text(self):
        self.t1 = AnimateCharacterWindow(opacity=100, background_color=(0, 0, 0))
        self.t1.animation_finished.connect(self.second_text)  # Connect to text2() directly
        self.t1.set_next_animation(""" 
        As Im walking, I realized that I should give up being a fisherman 
        a long time ago since I entered this world. Every day, every night,
        I always pray to myself to survive from this endless nightmare. 
        I know I want to escape from this nightmare
        .
        .
        .
        Everything changes

        """)
        self.t1.start_next_animation()
        self.vbox.addWidget(self.t1)

    def second_text(self):
        self.t1.hide()
        self.t2 = AnimateCharacterWindow(opacity=100, background_color=(0, 0, 0))
        self.t2.animation_finished.connect(self.third_text)  # Connect to text2() directly
        self.t2.set_next_animation(""" 
        As I got closer to the endless sea, the storm was getting 
        harder and harder, unlike anything I had seen before. 
        The sky slowly turned darker and darker into jagged veins 
        of lightning. The waves from the ocean are very high, 
        looking like tsunami waves.                       
        """)
        self.t2.start_next_animation()
        self.vbox.addWidget(self.t2)

    def third_text(self):
        self.t2.hide()
        self.t3 = AnimateCharacterWindow(opacity=100, background_color=(0, 0, 0))
        self.t3.animation_finished.connect(self.fourth_text)  # Connect to text2() directly
        self.t3.set_next_animation(""" 
        I think I should stop getting there, but with my determination, 
        I should have turned away. I should have run. But something inside 
        my head tells me to go forward.
        """)
        self.t3.start_next_animation()
        self.vbox.addWidget(self.t3)

    def fourth_text(self):
        self.t3.hide()
        self.t4 = AnimateCharacterWindow(opacity=100, background_color=(0, 0, 0))
        self.t4.animation_finished.connect(self.quest1)  # Connect to text2() directly
        self.t4.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.t4.set_next_animation("""
                Quest 1: Entering the Endless Sea
        
        Objective: Rearrange the number from low to high within the time

        """)
        self.t4.start_next_animation()
        self.vbox.addWidget(self.t4)

    ##################### First quest
    def quest1(self):
        from G_CustomWidgets.drag_num import ArrangeNum
        self.t4.hide()

        self.arrange_number = ArrangeNum(self)
        self.vbox.addWidget(self.arrange_number)

        self.arrange_number.correct_signal.connect(lambda: self.change_scene())

    def change_scene(self):
        self.correct_label = QLabel("CORRECT!")
        self.correct_label.setStyleSheet(f"""QLabel{{
                                            font-family: {self.font_family};
                                            font-size: 300px;
                                            background-color: black;
                                            color: #ffc606;
                                            padding: 80px;
                                            border-radius: 10px;
        }}""")
        self.correct_label.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignCenter)
        self.vbox.addWidget(self.correct_label)

        self.arrange_number.hide()
        print("Displaying Correct Label")

        QTimer.singleShot(1800, self.changing_scene)  

    def changing_scene(self):
        from AA_StoryMode.Scene2 import SecondScene
        
        if not hasattr(self, "second_scene"):
            self.second_scene = SecondScene(plr_data=self.plr_data)
        
        self.setStyleSheet("background-color: none;")
        self.stack_widget.addWidget(self.second_scene)
        self.stack_widget.setCurrentWidget(self.second_scene)
        self.second_scene.show()
        self.setCentralWidget(self.stack_widget)

def main():
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    window = FirstScene()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()