from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from abc import ABC, abstractmethod
import sys
from G_CustomWidgets.TextAnim import AnimateCharacterWindow
from Sprites.Player import PlayerAnimate
from time import sleep as delay
import random

class Color(QWidget):
    def __init__(self, color_name):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color_name))
        self.setPalette(palette)

class SecondScene(QMainWindow):
    def __init__(self, parent=None, plr_data=None, **kwargs):
        super(SecondScene, self).__init__(parent, **kwargs)
        self.setWindowTitle("Fisherman Chronicles")
        self.showFullScreen()

        self.plr_data = plr_data
        print(f"\n\nPLR DATA IN SCENE2: {self.plr_data}")

        # central widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.setStyleSheet("background-color: black;")

        # stack widget
        self.stack_widget = QStackedWidget(self.central_widget)
        self.stack_widget.setFixedSize(QSize(self.width(), self.height()))

        self.bg_load = QPixmap(fr"H_images\img_login\night_time.png")
        self.bg_image = QLabel(self.central_widget)
        self.bg_image.setGeometry(0, 0, self.width(), self.height())
        self.bg_image.setPixmap(self.bg_load)
        self.bg_image.setScaledContents(True)

        # Call the methods
        self.load_fonts()
        self.__widgets_comp()
        self.first_text()

        # Set the style for window
        self.setStyleSheet(f"""
            QRadioButton {{
                color: white;
                font-size: 45px;
                font-family: {self.font_family};
                border: 2px solid #3498db;
                border-radius: 12px;
                padding: 8px;
                margin: 10px;
                background-color: #2c3e50;
            }}

            QRadioButton:hover {{
                background-color: #34495e;
                border-color: #2980b9;
            }}

            QRadioButton:checked {{
                background-color: #2980b9;
                border-color: #1abc9c;
            }}

            QRadioButton:checked:hover {{
                background-color: #1abc9c;
                border-color: #16a085;
            }}

            QRadioButton::indicator {{
                width: 20px;
                height: 20px;
                border: 2px solid #3498db;
                border-radius: 10px;
                background-color: #34495e;
            }}

            QRadioButton::indicator:checked {{
                background-color: #cb3c00;
                border-color: #1abc9c;
            }}

            QRadioButton::indicator:unchecked {{
                background-color: #34495e;
                border-color: #3498db;
            }}
        """)

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
        I was holding the fishing rod and the sword in my hands 
        while hearing some echo sound coming from the end of the sea
        .
        .
        .

        """)
        self.t1.start_next_animation()
        self.vbox.addWidget(self.t1)

    def second_text(self):
        self.t1.hide()
        self.t2 = AnimateCharacterWindow(opacity=100, background_color=(0, 0, 0))
        self.t2.animation_finished.connect(self.choose_choice)  # Connect to text2() directly
        self.t2.set_next_animation(""" 
        Is this actually the endless sea?!?
        .
        .
        .
                                   
        WHAT IS THAT SOUND!>!>!
        Should I go to head foward to that sound?                     
        """)
        self.t2.start_next_animation()
        self.vbox.addWidget(self.t2)

    def choose_choice(self):
        self.t2.hide()
        self.choose_label = QLabel("Should I head foward?? or go back?")
        self.choose_label.setStyleSheet(f"""QLabel{{
                                        font-family: {self.font_family};
                                        font-size: 80px;
                                        color: white;
                                        padding: 20px;
        }}""")
        self.choose_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.vbox.addWidget(self.choose_label)

        self.choice1 = QRadioButton("Walk immediately to check")
        self.choice2 = QRadioButton("Hesitate for a moment and fall back")
        self.vbox.addWidget(self.choice1)
        self.vbox.addWidget(self.choice2)

        self.choice1.toggled.connect(lambda event: self.radio_choice(event))
        self.choice2.toggled.connect(lambda event: self.radio_choice(event))
    
    def radio_choice(self, event):
        if self.choice1.isChecked():
            print(self.choice1.text())
            self.continue_game()
            
        elif self.choice2.isChecked():
            print(self.choice2.text())
            self.show_dead_page()

    def show_dead_page(self):
        if not hasattr(self, "ded_page"):
            self.ded_page = DeadPage(plr_data=self.plr_data)
        
        self.stack_widget.addWidget(self.ded_page)
        self.stack_widget.setCurrentWidget(self.ded_page)
        self.ded_page.show()
        self.setCentralWidget(self.stack_widget)

    ######### CONTINUE THE GAME
    def continue_game(self):
        # Disable radiobuttons and hide, also hide the labeled text
        self.choose_label.hide()
        self.choice1.setDisabled(True)
        self.choice2.setDisabled(True)
        self.choice1.hide()
        self.choice2.hide()

        # Show the labeled text
        self.fish_lab = QLabel()
        self.fish_movie = QMovie(r"Z_Enemies\FishSwim2.gif")
        self.fish_lab.setMovie(self.fish_movie)
        self.fish_movie.start()

        self.fish_lab2 = QLabel()
        self.fish_movie2= QMovie(r"Z_Enemies\fish3.gif")
        self.fish_lab2.setMovie(self.fish_movie2)
        self.fish_movie2.start()

        self.fish_lab.setStyleSheet("padding-bottom: 400px;")
        self.fish_lab2.setStyleSheet("padding-bottom: 400px;")

        self.fish_lab.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.fish_lab2.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)

        # make the fish align top on hbox layout (assign indiv alignment to the hbox), does not affect other widget
        # alignment (assign on the addWidget method)
        self.hbox.addWidget(self.fish_lab, alignment=Qt.AlignmentFlag.AlignHCenter)  
        self.hbox.addWidget(self.fish_lab2, alignment=Qt.AlignmentFlag.AlignHCenter)  

        # Show this function for 3 seconds
        QTimer.singleShot(3000, self.fish_talk)

    def fish_talk(self):
        self.fish_lab.hide()
        self.fish_lab2.hide()
        self.fish_lab.deleteLater()
        self.fish_lab2.deleteLater()

        self.vbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.txt1 = AnimateCharacterWindow(opacity=100, background_color=(0, 0, 0))
        self.txt1.animation_finished.connect(self.fish_talk2)  # Connect to text2() directly
        self.txt1.set_next_animation(""" 
        Fish: “#$)#)$(()$()@(($)dsg)(40h#U*OWIO$#WHRPORJ{#J)R
        (P_R(Y#P(*Y#RY*@#y*(88Y8@)*)@I#)@#)#)U)#%U*#%U(#*H$O#*$)
        (_@($@_($)@(_($_@$))@#@)#@*@$$^^$^^*@$*@#)#$#O$)#$O##RH)
        PR@P)(Y@HP”#$U(U#$(##$(#*#($*(#*$(*$^&#^!@!))#(@)(#(#)@(
        """)
        self.txt1.start_next_animation()
        self.vbox.addWidget(self.txt1)

    def fish_talk2(self):
        self.txt1.hide()
        self.player_name = self.plr_data["name"] if self.plr_data and "name" in self.plr_data else ""

        self.txt2 = AnimateCharacterWindow(opacity=100, background_color=(0, 0, 0))
        self.txt2.animation_finished.connect(self.attack_with_fish)
        self.txt2.set_next_animation(f""" 
        Fish: wHo aRe yOU? yOu inVader!? inVAder?!!?!
        
        Fisherman ({self.player_name}): I'm just a legendary fisherman, 
        I woke up again, but I couldn't figure out where is this place? 
        So I came here ( ˘︹˘ )

        Fish: (￣︿￣) ... 😡😠

        """)
        self.txt2.start_next_animation()
        self.vbox.addWidget(self.txt2)

    def attack_with_fish(self):
        self.txt2.hide()
        self.obj_lab = QLabel("Objective: Attack the fish\n\n(Press left mouse to attack)")
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
        self.fish_attacking()

    def fish_attacking(self):
        """
        This method will call the fish from another class
        The fish class will have handle dead method
        """
        from Z_Enemies.fishEnemy import FishEnemy
        
        self.fish_enemy = FishEnemy(self, plr_data=self.plr_data)
        self.fish_enemy.setStyleSheet("background: transparent; margin-bottom: 0px;")
        self.fish_enemy.setFixedSize(QSize(400,320))
        self.fish_enemy.move(1150,750)
        self.fish_enemy.setParent(self.central_widget)
        self.fish_enemy.show()

        # When the fish is dead (Call the another function)
        # use the signal
        self.fish_enemy.fish_died.connect(self.fish_is_dead)

    def fish_is_dead(self):
        print(f"Calling Fish Is Dead function")
        self.obj_lab.hide()

        self.rain_effect = RainEffect(parent=self)
        self.rain_effect.setFixedSize(QSize(self.width(), self.height()))
        self.rain_effect.move(0,0)
        self.rain_effect.setParent(self.central_widget)
        self.rain_effect.show()

        self.txx1 = AnimateCharacterWindow(opacity=100, background_color=(0, 0, 0))
        self.txx1.animation_finished.connect(self.player_walk2)  # Connect to text2() directly
        self.txx1.set_next_animation(f""" 
        Fish: ... ... ...

        Fisherman ({self.player_name}): Seems like it's raining, I should find somewhere
        to hide
        """)
        self.txx1.start_next_animation()
        self.vbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.vbox.addWidget(self.txx1)
    
    def player_walk2(self):
        self.txx1.hide()

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
                print("Player reach the end of the screen")
                self.change_scene()
                self.stop_tracking()    

    def stop_tracking(self):
        if hasattr(self, "timer") and self.timer is not None:
            self.timer.stop()
    
    def change_scene(self):
        from AA_StoryMode.Scene3 import ThirdScene
        print("Changing the scene to scene3")

        if not hasattr(self, "scene3"):
            self.scene3 = ThirdScene(plr_data=self.plr_data)

        self.stack_widget.addWidget(self.scene3)
        self.stack_widget.setCurrentWidget(self.scene3)
        self.scene3.show()
        self.setCentralWidget(self.stack_widget)

#### RAin drop class
class RainEffect(QWidget):
    def __init__(self, parent=None):
        super(RainEffect, self).__init__(parent)
        self.setGeometry(0, 0, parent.width(), parent.height())
        self.setStyleSheet("background-color: transparent;")

        self.num_drops = 300  
        self.raindrops = [
            [random.randint(0, self.width()), random.randint(0, self.height()), random.randint(7, 15)] 
            for _ in range(self.num_drops)
        ]
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_rain)
        self.timer.start(30) 

    ##### For this logic, I ask chat gpt for the solution
    def update_rain(self):
        for drop in self.raindrops:
            drop[1] += drop[2]  
            drop[0] += random.uniform(-1, 1)  

            if drop[1] > self.height():  
                drop[1] = random.randint(-20, 0)
                drop[0] = random.randint(0, self.width())  
                drop[2] = random.randint(7, 15) 

        self.update() # update function use for updating randrops and resetting

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rain_color = QColor("#56e2ff")
        painter.setPen(QPen()) 
        painter.setBrush(rain_color)

        for x, y, speed in self.raindrops:
            alpha = min(255, 100 + speed * 10)
            pen = QPen(QColor(86, 226, 255, alpha), 2, Qt.PenStyle.SolidLine)  # Adjusted color to #56e2ff with alpha
            painter.setPen(pen)
            painter.drawLine(int(x), int(y), int(x), int(y + speed))


class DeadPage(QMainWindow):
    def __init__(self, parent=None, plr_data=None):
        super(DeadPage, self).__init__(parent)
        self.showFullScreen()
        self.plr_data = plr_data

        self.load_fonts()
        self.setStyleSheet("background-color: black")

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout1 = QVBoxLayout()
        self.central_widget.setLayout(self.layout1)

        # stack widget
        self.stack_widget = QStackedWidget(self.central_widget)
        self.stack_widget.setFixedSize(QSize(self.width(), self.height()))

        self.dead_lab = QLabel("You Died (got attack by the fish)")
        self.dead_lab.setStyleSheet(f"""QLabel{{
                                    font-family: {self.font_family};
                                    font-weight: bold;
                                    font-size: 80px;
                                    color: white;
        }}""")
        self.dead_lab.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        self.layout1.addWidget(self.dead_lab)

        self.back_button = QPushButton("BACK")
        self.back_button.setStyleSheet(f"""QPushButton{{
                                       background-color: #dc6331;
                                       font-family: {self.font_family};
                                       font-size: 40px; 
                                       color: white;
        }}""")
        self.layout1.addWidget(self.back_button)
        self.back_button.clicked.connect(lambda: self.back_toGame())
        
    def load_fonts(self):
        self.font_id = QFontDatabase.addApplicationFont("Z_custom_fonts/Jersey15-Regular.ttf")
        self.font_id2 = QFontDatabase.addApplicationFont("Z_custom_fonts/PixelifySans-VariableFont_wght.ttf")

        self.font_family = QFontDatabase.applicationFontFamilies(self.font_id)[0]
        self.custom_font = QFont(self.font_family)
        self.custom_font.setBold(True)

        self.font_family2 = QFontDatabase.applicationFontFamilies(self.font_id2)[0]
        self.custom_font2 = QFont(self.font_family2)
        self.custom_font2.setBold(False)
    
    def back_toGame(self):
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
    
    window = SecondScene()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()