from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from abc import ABC, abstractmethod
import sys
from G_CustomWidgets.TextAnim import AnimateCharacterWindow
from Sprites.Player import PlayerAnimate

class Color(QWidget):
    def __init__(self, color_name):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color_name))
        self.setPalette(palette)

"""The prologue class"""
class Prologue(QMainWindow):
    def __init__(self, plr_data=None, parent=None, **kwargs):
        super(Prologue, self).__init__(**kwargs)

        self.setWindowTitle("Fisherman Chronicles")
        self.showFullScreen()
        
        self.plr_data = plr_data
        print(f"\n\nPLR DATA IN PROLOGUE: {self.plr_data}")
        
        # Load custom fonts and set the custom fonts
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
        self.setStyleSheet("background-color: black;")

        self.stack_widget = QStackedWidget(self.central_widget)
        self.stack_widget.setFixedSize(QSize(self.width(), self.height()))

        self.bg_load = QPixmap(fr"H_images\story_img\scene1.png")
        self.bg_image = QLabel(self.central_widget)
        self.bg_image.setGeometry(0, 0, self.width(), self.height())
        self.bg_image.setPixmap(self.bg_load)
        self.bg_image.setScaledContents(True)

        # call the methods
        self.__widgets_comp()
        self.first_text()

    def __widgets_comp(self):
        self.vbox = QVBoxLayout(self.central_widget)
        self.vbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.central_widget.setLayout(self.vbox)
        self.vbox.setStretch(0, 5)

        self.hbox = QHBoxLayout()
        self.vbox.addLayout(self.hbox)

        self.bottom_layout = QHBoxLayout()
        self.vbox.addLayout(self.bottom_layout)

##### TEXT METHODS (TEXT ANIMATION METHODS)
    def first_text(self):
        self.bg_image.hide()
        self.t1 = AnimateCharacterWindow(background_color=(0, 0, 0))
        self.t1.animation_finished.connect(self.second_text)  # Connect to text2() directly
        self.t1.set_next_animation(""" 
                                    Long time ago, there was a fisherman...\n
                                    who lives on the island
        """)
        self.t1.start_next_animation()
        self.vbox.addWidget(self.t1)
    
    def second_text(self):
        self.bg_image.hide()
        self.t1.hide()
        self.t2 = AnimateCharacterWindow(background_color=(0, 0, 0))
        self.t2.animation_finished.connect(self.third_text)  # Connect to text2() directly
        self.t2.set_next_animation(""" 
                                    But one day
                                    .
                                    .
                                    .
                                    He fell down into the water while fishing
                                    
        """)
        self.t2.start_next_animation()
        self.vbox.addWidget(self.t2)
    
    def third_text(self):
        self.bg_image.hide()
        self.t2.hide()
        self.t3 = AnimateCharacterWindow(background_color=(0, 0, 0))
        self.t3.animation_finished.connect(self.text1)  # Connect to text2() directly
        self.t3.set_next_animation(""" 
                                    "What's happening?!!"
                                    .
                                    .
                                    .
                                    
                                    "Am I actually becoming a legendary monster fisher??"

        """)
        self.t3.start_next_animation()
        self.vbox.addWidget(self.t3)

    def text1(self):
        self.bg_image.show() # show the bg image
        self.t3.hide()
        self.txt1 = AnimateCharacterWindow(opacity=100, background_color=(0, 0, 0))
        self.txt1.animation_finished.connect(self.text2)  # Connect to text2() directly
        self.txt1.set_next_animation(""" 
        As I opened my eyes, everything was totally fine. I realized that 
        Im standing in the middle of the forest holding the lantern 
        while the cold wind is blowing through me. It was so peaceful, 
        like living in the countryside
        """)
        self.txt1.start_next_animation()
        self.vbox.addWidget(self.txt1)

    def text2(self):
        self.txt1.hide()
        self.txt2 = AnimateCharacterWindow(opacity=100, background_color=(0, 0, 0))
        self.txt2.animation_finished.connect(self.escape_the_forest)
        self.txt2.set_next_animation(""" 
        By looking from my perspective, I could see the endless sea 
        far away on the right side of the horizon. Let's walk there to 
        to look for some observation
        """) 
        self.vbox.addWidget(self.txt2)

    def escape_the_forest(self):
        self.txt2.hide()
        self.obj_lab = QLabel("Objective: Escape the forest \n\nPress A and D to move\nPress Space to jump")
        self.obj_lab.setStyleSheet(f"""
            QLabel {{
                background-color: rgba(0, 0, 0, 100);
                font-family: {self.font_family}; 
                color: white;
                font-size: 30px;          
                padding: 20px;
                border-radius: 10px;
                margin: 30px;
            }}
        """)
        # configure the vbox (make it to the right side)
        self.vbox.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
        self.vbox.addWidget(self.obj_lab)
        self.player_moving() # call the player method

    def player_moving(self):
        if not hasattr(self, "player"):
            self.player = PlayerAnimate(self)
            self.player.setStyleSheet("background-color: transparent; margin-bottom: 0px;")
            self.player.move(0, 600)
            self.player.setParent(self.central_widget)
            self.player.show()
            self.player.setFocus()

            self.timer = QTimer(self)
            self.timer.timeout.connect(self.track_player_pos)
            self.timer.start(50)

    def track_player_pos(self):
        if hasattr(self, "player") and self.player is not None:
            self.player_x = self.player.x()
            self.player_width = self.player.width()
            self.screen_width = self.width()

            if self.player_x + self.player_width >= self.screen_width:
                self.change_scene()
                self.stop_tracking()

    def change_scene(self):
        from AA_StoryMode.Scene1 import FirstScene
        print("Changing the scene")

        if not hasattr(self, "scene1"):
            self.scene1 = FirstScene(plr_data=self.plr_data)

        self.stack_widget.addWidget(self.scene1)
        self.stack_widget.setCurrentWidget(self.scene1)
        self.scene1.show()
        self.setCentralWidget(self.stack_widget)

    def stop_tracking(self):
        if hasattr(self, "timer") and self.timer is not None:
            self.timer.stop()
    
def main():
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    window = Prologue()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()