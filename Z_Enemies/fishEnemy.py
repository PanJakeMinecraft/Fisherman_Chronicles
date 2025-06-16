from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import sys
from time import sleep as delay
import threading
import random
import math

class FishEnemy(QWidget):
    fish_died = pyqtSignal() # Fish dead signals

    def __init__(self, player, parent=None, plr_data =None, random_weight=None):
        super(FishEnemy, self).__init__(parent)
        self.setGeometry(0, 600, 400, 300)
        self.player = player
        self.plr_data = plr_data

        # Random weight
        if random_weight is None:
             self.rd_weight = [0, 0, 0, 1]
        else:
            self.rd_weight = random_weight

        self.x_pos = 0
        self.y_pos = 0
        self.fish_speed = 2
        self.victory_shown = False

        ## Test damage timerr
        '''
        self.damage_timer = QTimer(self)
        self.damage_timer.timeout.connect(lambda: self.take_damage(20))
        self.damage_timer.start(500)  

        self.damage_amount = 3  
        self.health = 100  
        '''

        ########## The fish collider
        self.fish_collider = QRect(self.x_pos, self.y_pos, self.width() + 20, self.height() + 5)
        self.attack_cool = QTimer(self)
        self.attack_cool.setInterval(100)
        self.attack_cool.setSingleShot(True)
        self.attack_cool.timeout.connect(self.reset_attackTimer)  
        
        # Attack Timer (triggers attack every 3-5 seconds)
        self.attack_timer = QTimer(self)
        self.attack_timer.timeout.connect(self.attack_player)
        self.start_attack_timer()

        # Call the methods
        self.animate_fish()
        self.attatch_healthbar()
        self.health_set(self.health)
        self.animate_fish_horizontal()

    def update_collider(self): # Call the method to create collider
         self.fish_collider = QRect(self.x_pos, self.y_pos, self.width() + 20, self.height() + 5)

    ############ PAINT THE COLLIDER
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QColor(255, 0, 0)) 
        painter.setBrush(QColor(0, 0, 255, 50)) 
        painter.drawRect(self.fish_collider) 

    def reset_attackTimer(self):
        pass

    def animate_fish(self):
        # fish images and mov (will be use for randomize)
        self.fish_gif = [
            r"Z_Enemies\anglerfish.gif",
            r"Z_Enemies\sharkman.gif",
            r"Z_Enemies\frog.gif",
            r"Z_Enemies\fish3.gif",
        ]


        self.select_fish = random.choices(self.fish_gif, weights=self.rd_weight)[0]
        self.fish_lab = QLabel(self)
        self.fish_lab.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.fish_mov = QMovie(self.select_fish)
        self.fish_lab.setMovie(self.fish_mov)

        if self.select_fish == r"Z_Enemies\frog.gif":
            self.fish_lab.setFixedSize(QSize(500, 400))
            self.fish_lab.setAlignment(Qt.AlignmentFlag.AlignCenter)
            print("Set the size to 800, 600")

        elif self.select_fish == r"Z_Enemies\fish3.gif":
            self.fish_lab.setFixedSize(QSize(400,300))
            print("Set the size to 400, 300")

        else:
            self.fish_lab.setFixedSize(QSize(400,350))
            print("Set the size to 400, 350")

        self.fish_lab.setScaledContents(True)
        self.fish_mov.start()
        self.fish_lab.show()

    ################ FISH MOVE
    def animate_fish_horizontal(self):
        screen_width = self.screen().availableGeometry().width() - 450
        self.start_pos = QPointF(screen_width, self.y_pos + 700)
        self.end_pos = QPointF(self.x_pos, self.y_pos + 700) 
        self.fish_mov.start()

        self.fish_collider = QRect(self.x(), self.y(), self.width() + 20, self.height() + 5)

        if self.select_fish in [r"Z_Enemies\anglerfish.gif", r"Z_Enemies\sharkman.gif"]:
            self.flip_image(True) 

        if self.select_fish in [r"Z_Enemies\frog.gif", r"Z_Enemies\fish3.gif"]:
            self.flip_image(False)  

        self.animation = QPropertyAnimation(self, b"pos")
        self.animation.setStartValue(self.start_pos)
        self.animation.setEndValue(self.end_pos)
        self.animation.setDuration(5000)  
        self.animation.setLoopCount(1) 
        self.animation.setEasingCurve(QEasingCurve.Type.Linear)  

        self.animation.finished.connect(self.reverse_animation) 
        self.animation.start()

    def reverse_animation(self):
        self.start_pos, self.end_pos = self.end_pos, self.start_pos

        if self.select_fish in [r"Z_Enemies\anglerfish.gif", r"Z_Enemies\sharkman.gif"]:
            self.flip_image(False)  

        if self.select_fish in [r"Z_Enemies\frog.gif", r"Z_Enemies\fish3.gif"]:
            self.flip_image(True)  
        self.fish_collider.moveTo(self.x(), self.y())

        self.animation.setStartValue(self.start_pos)
        self.animation.setEndValue(self.end_pos)
        self.animation.start()
        self.animation.finished.connect(self.animate_fish_horizontal)  

    def flip_image(self, flip: bool):
        if flip:
            if hasattr(self, "normal_movie") and self.normal_movie is not None:
                self.normal_movie.stop()

            if not hasattr(self, "flipped_movie") or self.flipped_movie is None:
                self.flipped_movie = QMovie(self.select_fish)
                self.flipped_movie.frameChanged.connect(self.update_flip)
                self.flipped_movie.start()

            self.fish_lab.setMovie(self.flipped_movie)  
        else:
            if hasattr(self, "flipped_movie") and self.flipped_movie is not None:
                self.flipped_movie.stop()

            if not hasattr(self, "normal_movie") or self.normal_movie is None:
                self.normal_movie = QMovie(self.select_fish)
                self.normal_movie.frameChanged.connect(self.normal_fish)
                self.normal_movie.start()

            self.fish_lab.setMovie(self.normal_movie)

        self.fish_lab.movie().start() 

    def normal_fish(self):  
        if self.normal_movie:
            frame = self.normal_movie.currentPixmap()
            self.fish_lab.setPixmap(frame)  

    def update_flip(self): 
        if self.flipped_movie:
            frame = self.flipped_movie.currentPixmap()
            transform = QTransform().scale(-1, 1) 
            flipped_frame = frame.transformed(transform)
            self.fish_lab.setPixmap(flipped_frame)

    def mousePressEvent(self, event: QMouseEvent):
            if event.button() == Qt.MouseButton.LeftButton:
                    if not self.attack_cool.isActive():
                        self.apply_random_damage()
                        self.attack_cool.start()

    ############ When fish attack player
    def start_attack_timer(self):
        attack_interval = random.randint(100, 150)
        self.attack_timer.start(attack_interval)

    def attack_player(self):
        pass

    def attatch_healthbar(self):
        self.health_bg = QLabel(self)
        self.health_bg.setStyleSheet("background-color: #79000f; border: 1px solid black;")
        self.health_bg.setGeometry(self.fish_lab.x() - 5, self.fish_lab.y() + 20, self.fish_lab.width() + 10, 30)  # Add padding for the border
        self.health_bg.show()

        self.fish_curr_health = QLabel(self)
        self.fish_curr_health.setGeometry(self.fish_lab.x(), self.fish_lab.y() + 20, self.fish_lab.width(), 30)
        self.fish_curr_health.setStyleSheet("background-color: #007a39; border: 1px solid black;")
        self.fish_curr_health.show()

        self.health_set(100)

    def apply_random_damage(self):
        damage = random.randint(1, 3) # Random damage make from player
        self.take_damage(damage)

    def take_damage(self, dmg):
        if self.health == 0: 
            return
        
        new_health = self.health - dmg
        if new_health <= 0:
            new_health = 0

        self.health_set(new_health)

        if self.health <= 0:
            print("The fish is dead, fish will fade in 1 second")
            self.dead_fish() 

            # THIS SIGNAL WILL WORK WHEN FISH IS DEAD (It can be use for another class calling)
            self.fish_died.emit()

            # Fade the fish away and stop the animated gif 
            self.health_bg.hide()
            self.fish_curr_health.hide()

            self.fish_lab.hide()
            print(f"Fish is dead")
            ###########################
            ########################## YOu can call other function 
            #self.damage_timer.stop()  

    def health_set(self, value):
        self.health = value
        if self.health < 0:
            self.health = 0
            self.dead_fish()
        elif self.health > 100:
            self.health = 100
        
        new_width = int(self.health_bg.width() * (self.health / 100))
        self.fish_curr_health.setFixedWidth(new_width)
    
    def dead_fish(self):
        opacity_effect = QGraphicsOpacityEffect(self.fish_lab)
        self.fish_lab.setGraphicsEffect(opacity_effect)
        dead_anim = QPropertyAnimation(opacity_effect, b"opacity")
        dead_anim.setStartValue(1.0)
        dead_anim.setEndValue(0.0)
        dead_anim.setDuration(100)
        dead_anim.setEasingCurve(QEasingCurve.Type.InCurve)
        self.fish_mov.stop()

        dead_anim.finished.connect(self.stop_dead_anim)
        dead_anim.start()

    def stop_dead_anim(self):
        self.fish_mov.stop()
        self.health_bg.hide()
        self.fish_curr_health.hide()
        self.fish_lab.hide()

if __name__ == "__main__":
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication([])
    
    window = FishEnemy()
    window.show()
    app.exec()