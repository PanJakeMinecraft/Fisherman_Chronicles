from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from abc import ABC, abstractmethod
import sys
from G_CustomWidgets.TextAnim import AnimateCharacterWindow
from Sprites.Player import PlayerAnimate
from time import sleep as delay

class FourthScene(QMainWindow):
    def __init__(self, parent=None, plr_data=None, **kwargs):
        super(FourthScene, self).__init__(parent)
        self.setWindowTitle("Fisherman Chronicles")
        self.showFullScreen()

        self.plr_data = plr_data

        # central widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.setStyleSheet("background-color: black;")

        # stack widget
        self.stack_widget = QStackedWidget(self.central_widget)
        self.stack_widget.setFixedSize(QSize(self.width(), self.height()))

        self.bg_load = QPixmap(fr"H_images\story_img\scene10.png")
        self.bg_image = QLabel(self.central_widget)
        self.bg_image.setGeometry(0, 0, self.width(), self.height())
        self.bg_image.setPixmap(self.bg_load)
        self.bg_image.setScaledContents(True)

        # Call the methods
        self.load_fonts()
        self.__widgets_comp()
        self.first_text()

        self.attack_timer = QTimer(self)
        self.attack_timer.timeout.connect(self.attack_fish)
        self.total_time = 30 
        self.attack_counter = 0
        self.timer_ended = False

        ############# THE TIMER PROGRESSBAR
        self.timer_bar = QProgressBar(self.central_widget)
        self.timer_bar.setGeometry(0, 0, self.width(), 50)
        self.timer_bar.setMaximum(self.total_time)
        self.timer_bar.setValue(self.total_time)
        self.timer_bar.setValue(self.total_time)
        self.timer_bar.setTextVisible(True) 
        self.timer_bar.setFormat("Time Left: %v s") 
        self.timer_bar.setStyleSheet("""QProgressBar{
                                    border: 2px solid black;
                                    border-radius: 5px;
                                    background-color: #444444;
                                    color: white;
                                    font-size: 30px;
                                    font-family: Tahoma;
                                    text-align: center;
                                    font-weight: bold;
                                    }
                                     
                                     QProgressBar::chunk{
                                     background-color: #55FF55;
                                     width: 20px;
                                     }""") 

        self.timer_bar.hide()

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
    
    ############## ANIMATED TEXT AND QUESTS
    def first_text(self):
        self.bg_image.hide()

        self.t1 = AnimateCharacterWindow(opacity=100, background_color=(0, 0, 0))
        self.t1.animation_finished.connect(self.second_text)  # Connect to text2() directly
        self.t1.set_next_animation(""" 
        As I reached the end of the cave, I looked outside, I wasnt 
        at that sea anymore. It was on the other side of the cave. 
        It was a grass mountain. 
        """)
        self.t1.start_next_animation()
        self.vbox.addWidget(self.t1)

    def second_text(self):
        self.bg_image.hide()
        self.t1.hide()

        self.t2 = AnimateCharacterWindow(opacity=100, background_color=(0, 0, 0))
        self.t2.animation_finished.connect(self.load_fish)  # Connect to text2() directly
        self.t2.set_next_animation(""" 
        I look around with confusion. The wind was blowing fast,
        As the old man said to me to give him 3 fish. I need to go fishing
        """)
        self.t2.start_next_animation()
        self.vbox.addWidget(self.t2)


    def load_fish(self):
        self.bg_image.show()
        self.t2.hide()

        if not hasattr(self, "player"):
            self.timer_bar.show()
            from Z_Enemies.fishEnemy import FishEnemy

            self.player = PlayerAnimate(self)
            self.player.setStyleSheet("background-color: transparent; margin-bottom: 0px;")
            self.player.move(0, 600)
            self.player.setParent(self.central_widget)
            self.player.show()
            self.player.setFocus()

            # Call the fish enemy class and input the parameters
            self.fish_enemy = FishEnemy(self, plr_data=self.plr_data, random_weight=[0, 1, 1, 1])
            self.fish_enemy.setStyleSheet("background: transparent; margin-bottom: 0px;")
            self.fish_enemy.setFixedSize(QSize(400, 320))
            self.fish_enemy.move(1150, 750)
            self.fish_enemy.setParent(self.central_widget)
            self.fish_enemy.show()

            self.fish_enemy.fish_died.connect(self.fish_is_dead)

            self.attack_counter = 0
            self.attack_timer.start(1000)  

    def attack_fish(self):
        if self.timer_ended:
            self.time_endin() 
            return

        self.attack_counter += 1
        self.timer_bar.setValue(self.total_time - self.attack_counter)

        if self.attack_counter >= self.total_time:
            self.end_attack()

    def time_endin(self):
        self.timer_bar.hide()
        print("OUT OF TIME<<<< no fish is spawned")
        self.destroy_fish() 

    def end_attack(self):
        self.attack_timer.stop()  
        self.timer_ended = True  
        print("Attack phase ended. No more fish spawning.")
        self.time_endin()  
        
        # create the fade widget (this widget will be inside the central widget)
        self.fade_widget = QWidget(self.central_widget)
        self.fade_widget.setStyleSheet("background-color: black;")
        self.fade_widget.setGeometry(0, 0, self.central_widget.width(), self.central_widget.height())
        self.fade_widget.show()

        """
        For this, I set the opacity as QGraphicsOpacityEffect and add the efefct to
        the fade widget. Then I create te animation using QPropertyAnimation to set
        the opacity using b'opacity' (this will change the screen opacity)
        - Finally, set the time and connect to another method when the animation finish running
        """
        self.opacity = QGraphicsOpacityEffect()
        self.fade_widget.setGraphicsEffect(self.opacity)

        self.fade_anim = QPropertyAnimation(self.opacity, b"opacity")
        self.fade_anim.setDuration(2000)
        self.fade_anim.setStartValue(0)
        self.fade_anim.setEndValue(1)
        self.fade_anim.setEasingCurve(QEasingCurve.Type.OutQuad)
        self.fade_anim.finished.connect(self.third_text)

        self.fade_anim.start()

    def destroy_fish(self):
        if hasattr(self, "fish_enemy"):
            self.fish_enemy.deleteLater() 

    def spawn_new_fish(self):
        if self.timer_ended:  
            return

        if hasattr(self, "fish_enemy"):
            self.fish_enemy.deleteLater()  

        from Z_Enemies.fishEnemy import FishEnemy
        self.fish_enemy = FishEnemy(self, plr_data=self.plr_data, random_weight=[0, 0, 1, 1])
        self.fish_enemy.setStyleSheet("background: transparent; margin-bottom: 0px;")
        self.fish_enemy.setFixedSize(QSize(400, 320))
        self.fish_enemy.move(1150, 750)
        self.fish_enemy.setParent(self.central_widget)
        self.fish_enemy.show()

        self.fish_enemy.fish_died.connect(self.fish_is_dead)

    def fish_is_dead(self):
        if not self.timer_ended:  
            print("The fish died")
            self.spawn_new_fish()  
    
    #################### TEXT animation continues
    def third_text(self):
        self.fade_widget.hide()
        self.bg_image.hide()
        self.t3 = AnimateCharacterWindow(opacity=100, background_color=(0, 0, 0))
        self.t3.animation_finished.connect(self.fourth_text)  # Connect to text2() directly
        self.t3.set_next_animation(""" 
        "I should bring the fish back to the old man but I've lost"
        ... 
        ...
        ...
                                   
        "Where could I be?"
        """)
        self.t3.start_next_animation()
        self.vbox.addWidget(self.t3)

    def fourth_text(self):
        self.t3.hide()
        self.bg_image.hide()
        self.t4 = AnimateCharacterWindow(opacity=100, background_color=(0, 0, 0))
        self.t4.animation_finished.connect(self.fifth_text)  # Connect to text2() directly
        self.t4.set_next_animation(""" 
        "You have reached the heart of the island (the grass mountain)"

        The middle of the land surface slowly cracked opens making fisherman 
        fall down under the surface.                        
        """)
        self.t4.start_next_animation()
        self.vbox.addWidget(self.t4)

    def fifth_text(self):
        self.t4.hide()
        self.bg_image.hide()

        # Change the background
        self.bg_load = QPixmap(fr"H_images\story_img\scene4.png")
        self.bg_image = QLabel(self.central_widget)
        self.bg_image.setGeometry(0, 0, self.width(), self.height())
        self.bg_image.setPixmap(self.bg_load)
        self.bg_image.setScaledContents(True)

        self.t5 = AnimateCharacterWindow(opacity=100, background_color=(0, 0, 0))
        self.t5.animation_finished.connect(self.boss_appear)  # Connect to text2() directly
        self.t5.set_next_animation("""  
        As I reached the underground surface, I saw something like a strange
        monster fish. Is it the anglerfish??
        .
        .
        .
        
        Once the notion took old, the fisherman could wait no longer.
        He holds back the fishing rod in his hand and ready to attack.
        """)
        self.t5.start_next_animation()
        self.vbox.addWidget(self.t5)
    
    def boss_appear(self):
        self.t5.hide()
        self.bg_image.show()

        # set the fade widget and fade in and out
        self.fade_widget = QWidget(self.central_widget)
        self.fade_widget.setStyleSheet("background-color: black;")
        self.fade_widget.setGeometry(0, 0, self.central_widget.width(), self.central_widget.height())
        self.fade_widget.show()

        self.opacity = QGraphicsOpacityEffect()
        self.fade_widget.setGraphicsEffect(self.opacity)

        self.fade_anim = QPropertyAnimation(self.opacity, b"opacity")
        self.fade_anim.setDuration(2500)
        self.fade_anim.setStartValue(0)
        self.fade_anim.setEndValue(1)
        self.fade_anim.setEasingCurve(QEasingCurve.Type.InQuad)

        # SET the fading direction (this will make the fade backward)
        self.fade_anim.setDirection(QPropertyAnimation.Direction.Backward)
        self.fade_anim.start()
        print("The anglerfish is spawn")

        # load the fish boss and player again
        self.fade_widget.hide()
        self.player.hide()
        self.player = PlayerAnimate(self)
        self.player.setFixedSize(QSize(250,500))
        self.player.setStyleSheet("background-color: transparent; margin-bottom: 0px;")
        self.player.move(0, 600)
        self.player.setParent(self.central_widget)
        self.player.show()
        self.player.setFocus()

        self.load_fish_boss()
        self.escape_theFish() # laod the objective 
        QTimer.singleShot(3000, self.dead_sequence)
        self.player.dead_finish.connect(self.dead_txt1) # connect signals

    def dead_sequence(self):
        self.fade_white()
        self.player.dead_start()

    def fade_white(self):
        self.white_widget = QWidget(self.central_widget)
        self.white_widget.setStyleSheet("background-color: white;")
        self.white_widget.setGeometry(0,0, self.central_widget.width(), self.central_widget.height())
        self.white_widget.show()

        self.white_op = QGraphicsOpacityEffect()
        self.white_widget.setGraphicsEffect(self.white_op)

        self.white_anim = QPropertyAnimation(self.white_op, b"opacity")
        self.white_anim.setDuration(2500)
        self.white_anim.setStartValue(0)
        self.white_anim.setEndValue(1)
        self.white_anim.setEasingCurve(QEasingCurve.Type.InQuad)
        self.white_anim.start()

    def load_fish_boss(self):
        from Z_Enemies.fishBoss import FishBoss
        self.boss = FishBoss(self, plr_data=self.plr_data, random_weight=[1,0,0,0])
        self.boss.setStyleSheet("background: transparent; margin-bottom: 0px;")
        self.boss.setFixedSize(QSize(1000, 800))
        self.boss.move(1150, 600)
        self.boss.setParent(self.central_widget)
        self.boss.show()

    def escape_theFish(self):
        self.obj_lab = QLabel("Objective: Escape the Anglerfish")
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
        self.vbox.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
        self.vbox.addWidget(self.obj_lab)

    def dead_txt1(self):
        print("Dead text shown")

        self.obj_lab.hide()
        self.bg_image.hide()
        self.boss.health_bg.hide()
        self.boss.fish_curr_health.hide()

        # wait for 2 seconds and show the text
        QTimer.singleShot(2000, self.dead_txt11)
    
    def dead_txt11(self):
        QTimer.singleShot(1500, self.hiding)

        self.dead1 = AnimateCharacterWindow(opacity=100, background_color=(0, 0, 0))
        self.dead1.animation_finished.connect(self.dead_txt2)  # Connect to text2() directly
        self.dead1.set_next_animation(""" 
        "I'm not dead yet!" the fisherman vision slowly faded white
        
                                      
        The fisherman fell to his hand and knee, he tried to stand up 
        but saddly, it was too late. 
        "No! No!!!!! I can't die yet"
                                      
        The fisherman screamed with sadness and depression. He screamed
        until no tear was left. However, he could not return    
        """)
        self.dead1.start_next_animation()
        self.vbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.vbox.addWidget(self.dead1)

    def dead_txt2(self):
        self.dead1.hide()
        self.dead2 = AnimateCharacterWindow(opacity=100, background_color=(0, 0, 0))
        self.dead2.animation_finished.connect(self.dead_txt3)  # Connect to text2() directly
        self.dead2.set_next_animation(""" 
        Eventually, he rise his head up a bit.
        .
        .
        .
        Finally, I realized that
        "I'm just a normal fisherman who enjoys fishing"
        "It's really felt blank in my mind."
        
        "Nothing exist at this moment"
        "Alone in this dimension"
        "No people, no air, especially, nothing"
                                      
        "Simply me alone in this world"
        """)
        self.dead2.start_next_animation()
        self.vbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.vbox.addWidget(self.dead2)

    def dead_txt3(self):
        self.dead2.hide()
        self.white_widget.hide()

        # change the bg image
        self.bg_load = QPixmap(fr"H_images\choose_modes\choosemode.png")
        self.bg_image = QLabel(self.central_widget)
        self.bg_image.setGeometry(0, 0, self.width(), self.height())
        self.bg_image.setPixmap(self.bg_load)
        self.bg_image.setScaledContents(True)
        self.bg_image.show()

        self.dead3 = AnimateCharacterWindow(opacity=100, background_color=(0, 0, 0))
        self.dead3.animation_finished.connect(self.show_endPage)  # Connect to text2() directly
        self.dead3.set_next_animation(""" 
        I woke up again in the middle of the grassland at night, everything
        was alright, but I can't remember anything about the past anymore, 
                                      
        but there is one thing that I can remember..

        “... I still a legendary fisherman”

        """)
        self.dead3.start_next_animation()
        self.vbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.vbox.addWidget(self.dead3)

    def hiding(self):
        self.player.hide()
        self.boss.hide()

    def show_endPage(self):
        print("Showing ending page")
        if not hasattr(self, "endpage"):
            self.endpage = EndPage(plr_data=self.plr_data)
        
        self.setStyleSheet("background-color: none;")
        self.stack_widget.addWidget(self.endpage)
        self.stack_widget.setCurrentWidget(self.endpage)
        self.endpage.show()
        self.setCentralWidget(self.stack_widget)

class EndPage(QMainWindow):
    def __init__(self, parent=None, plr_data=None):
        super(EndPage, self).__init__(parent)
        self.showFullScreen()
        self.plr_data = plr_data

        print("Player data inside the end page: {}".format(self.plr_data))

        self.load_fonts()
        self.setStyleSheet("background-color: black")

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout1 = QVBoxLayout()
        self.central_widget.setLayout(self.layout1)

        # stack widget
        self.stack_widget = QStackedWidget(self.central_widget)
        self.stack_widget.setFixedSize(QSize(self.width(), self.height()))

        self.layout1.setContentsMargins(0, 0, 0, 0)
        self.layout1.setSpacing(5)
        
        self.labelend = QLabel("THE END")
        self.custom_font.setPointSize(80) 
        self.labelend.setFont(self.custom_font)
        self.labelend.setStyleSheet(f"""QLabel{{
                                        font-family: {self.font_family};
                                        font-weight: bold;
                                        font-size: 300px;
                                        color: #ffc356;
                                        padding: 0px;
                                        margin: 0px;
                                        line-height: 30px;
        }}""")
        self.labelend.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout1.addWidget(self.labelend)

        self.cont = QLabel("To be continue... ")
        self.cont.setStyleSheet(f"""QLabel{{
                                    font-family: {self.font_family};
                                    font-weight: bold;
                                    font-size: 40px;
                                    color: yellow;
                                    padding: 5px;
                                    margin: 0x;
        }}""")
        self.cont.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        self.cont.setFixedHeight(45)
        self.cont.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout1.addWidget(self.cont)

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
        from A_Title.choosemode import ChooseMode

        if not hasattr(self, "choosemode"):
            self.choosemode = ChooseMode(plr_data=self.plr_data)
        
        self.setStyleSheet("background-color: none;")
        self.stack_widget.addWidget(self.choosemode)
        self.stack_widget.setCurrentWidget(self.choosemode)
        self.choosemode.show()
        self.setCentralWidget(self.stack_widget)

def main():
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    window = EndPage()
    window.show()
    app.exec()