from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from abc import ABC, abstractmethod
import sys
from G_CustomWidgets.TextAnim import AnimateCharacterWindow
from Sprites.Player import PlayerAnimate
from time import sleep as delay

class ThirdScene(QMainWindow):
    def __init__(self, parent=None, plr_data=None, **kwargs):
        super(ThirdScene, self).__init__(parent, **kwargs)
        self.setWindowTitle("Fisherman Chronicles")
        self.showFullScreen()

        self.plr_data = plr_data
        print(f"\n\nPLR DATA IN SCENE3: {self.plr_data}")

        # central widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.setStyleSheet("background-color: black;")

        # stack widget
        self.stack_widget = QStackedWidget(self.central_widget)
        self.stack_widget.setFixedSize(QSize(self.width(), self.height()))

        self.bg_load = QPixmap(fr"H_images\story_img\scene5.png")
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

    ############### Aniamted text
    def first_text(self):
        self.bg_image.hide()

        self.t1 = AnimateCharacterWindow(opacity=100, background_color=(0, 0, 0))
        self.t1.animation_finished.connect(self.second_text)  # Connect to text2() directly
        self.t1.set_next_animation(""" 
        As the last fish fell to the ground. I stood there and trying to 
        make sense of what had just happened. The storm had intensified,
        and the rain still ranining
        """)
        self.t1.start_next_animation()
        self.vbox.addWidget(self.t1)

    def second_text(self):
        self.bg_image.hide()
        self.t1.hide()
        self.t2 = AnimateCharacterWindow(opacity=100, background_color=(0, 0, 0))
        self.t2.animation_finished.connect(self.third_text)  # Connect to text2() directly
        self.t2.set_next_animation(""" 
        From my common sense, I need to escape the rain and find shelter. 
        However, luckily, I saw something. At the eastern side of the endless sea, 
                                                      
        It's looks like a structure. 
        It's very dark...
        It was a dark cave from a distance. 
        The cave opened wide letting the waves crashing inside
        """)
        self.t2.start_next_animation()
        self.vbox.addWidget(self.t2)

    def third_text(self):
        self.t2.hide()
        self.bg_image.show()
        self.t3 = AnimateCharacterWindow(opacity=100, background_color=(0, 0, 0))
        self.t3.animation_finished.connect(self.cave_quest)  # Connect to text2() directly
        self.t3.set_next_animation(""" 
        As I reached the cave, the area was locked, I was figuring 
        out the puzzle in order to enter the cave. It was a drawing 
        puzzle. How should I draw it?
        """)
        self.t3.start_next_animation()
        self.vbox.addWidget(self.t3)

    def quest_objective(self):
        self.t3.hide()
        self.obj_lab = QLabel("Objective: Draw the following shape (RECTANGLE) \nThe program will detect what you draw")
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
        self.vbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.vbox.addWidget(self.obj_lab)

    def cave_quest(self):
        self.t3.hide()
        self.quest_objective()

        from G_CustomWidgets.drawingGUI import Main # Custom
        self.drawGui = Main(parent=self)
        self.vbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.vbox.addWidget(self.drawGui)

        # emit the signal (when draw complete, the signal will works)
        self.drawGui.success_signal.connect(lambda: self.complete_quest())

    def complete_quest(self):
        print("The quest is complete")

        self.obj_lab.hide()
        self.drawGui.setEnabled(False)
        self.drawGui.hide()
        self.drawGui.deleteLater()
        
        self.t4 = AnimateCharacterWindow(opacity=100, background_color=(0, 0, 0))
        self.t4.animation_finished.connect(self.old_man_quest)  # Connect to text2() directly
        self.t4.set_next_animation(""" 
        The cave was strangely quiet, but atleast it safe. The cave was so quiet 
        whereas I could hear footsteps while walking. Suddendly, there was 
        something
                                   
        What is it?
        """)
        self.t4.start_next_animation()
        self.vbox.addWidget(self.t4)

    def old_man_quest(self):
        self.t4.hide()
        print("Old man quest")
        self.setStyleSheet("background-color: transparent")

        # Call the method
        self.player_show()
        self.old_man()

    def player_show(self):
        if not hasattr(self, "player"):
            self.player = PlayerAnimate(self)
            self.player.setStyleSheet("background-color: transparent; margin-bottom: 0px;")
            self.player.move(0, 600)
            self.player.setParent(self.central_widget)
            self.player.show()
            self.player.setFocus()


    def old_man(self):
        self.old_man_lab = QLabel()
        self.old_man_movie = QMovie(r"Z_Enemies\oldman.gif")
        self.old_man_movie.setScaledSize(QSize(220,220))
        self.old_man_lab.setMovie(self.old_man_movie)
        self.old_man_lab.setParent(self.central_widget)
        self.old_man_movie.start()
        self.old_man_lab.show()

        x = 1300
        y = 545
        self.old_man_lab.move(x, y)

        player_x = self.player.x()
        stop = player_x + 50

        # move the old man
        self.old_anim = QPropertyAnimation(self.old_man_lab, b"pos")
        self.old_anim.setDuration(3500)
        self.old_anim.setStartValue(QPoint(x, y))
        self.old_anim.setEndValue(QPoint(stop, y))
        
        self.track_player_timer = QTimer(self)
        self.track_player_timer.timeout.connect(self.checkPOS)
        self.track_player_timer.start(10)

    def checkPOS(self):
        if hasattr(self, "player"):
            player_x = self.player.x()
            player_y = self.player.y()
            
            stop_x = player_x + 200
            stop_y = player_y - 30

        self.old_anim.setEndValue(QPoint(stop_x, stop_y))
        self.old_anim.start()

        if abs(self.old_man_lab.x() - stop_x) <= 5: # check whether the old man and player pos is within 30px
            self.stop_old_man()  
            self.track_player_timer.stop()

    def stop_old_man(self):
        self.old_man_movie.stop()
        self.show_text()

    def show_text(self):
        print("Showing the text")
        self.t5 = AnimateCharacterWindow(opacity=100, background_color=(0, 0, 0), width=1200, height=120)
        self.t5.animation_finished.connect(self.show_text2)  # Connect to text2() directly
        self.t5.set_next_animation(""" 
        Old man: Ah, a brave traveler. I never seen someone here for so long ago.
        """)
        self.t5.start_next_animation()
        self.spacer = QSpacerItem(10,10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.vbox.addItem(self.spacer)
        self.vbox.addWidget(self.t5)

    def show_text2(self):
        self.t5.hide()
        self.t6 = AnimateCharacterWindow(opacity=100, background_color=(0, 0, 0), width=1200, height=120)
        self.t6.animation_finished.connect(self.show_text3)  # Connect to text2() directly
        self.t6.set_next_animation(""" 
        Old man: The forest is very dangerous
        """)
        self.t6.start_next_animation()
        self.spacer = QSpacerItem(10,10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.vbox.addItem(self.spacer)
        self.vbox.addWidget(self.t6)

    def show_text3(self):
        self.t6.hide()
        self.t7 = AnimateCharacterWindow(opacity=100, background_color=(0, 0, 0), width=1200, height=120)
        self.t7.animation_finished.connect(self.show_text4)  # Connect to text2() directly
        self.t7.set_next_animation(""" 
        Old man: If you help me, I will help you to find the way out
        """)
        self.t7.start_next_animation()
        self.spacer = QSpacerItem(10,10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.vbox.addItem(self.spacer)
        self.vbox.addWidget(self.t7)

    def show_text4(self):
        self.t7.hide()
        self.t8 = AnimateCharacterWindow(opacity=100, background_color=(0, 0, 0), width=1200, height=200)
        self.t8.animation_finished.connect(self.change_scene)  # Connect to text2() directly
        self.t8.set_next_animation(""" 
        Old man: There's a grass mountain over there, just go fishing and\n\tgive 3 fish to me at the shop
        """)
        self.t8.start_next_animation()
        self.spacer = QSpacerItem(10,10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.vbox.addItem(self.spacer)
        self.vbox.addWidget(self.t8)

    def change_scene(self):
        self.t8.hide()
        from AA_StoryMode.Scene4 import FourthScene
        print("Changing the scene to scene4")

        if not hasattr(self, "scene4"):
            self.scene4 = FourthScene(plr_data=self.plr_data)

        self.stack_widget.addWidget(self.scene4)
        self.stack_widget.setCurrentWidget(self.scene4)
        self.scene4.show()
        self.setCentralWidget(self.stack_widget)

def main():
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    window = ThirdScene()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()