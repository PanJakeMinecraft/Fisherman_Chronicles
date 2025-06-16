from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import sys
from time import sleep as delay
import threading
import random
import math

######### Class colors will be use for testing the layouts inside the widgets
class Color(QWidget):
    def __init__(self, color_name):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color_name))
        self.setPalette(palette)


############# THE GAME CLASS (GAME WINDOW)
class FishAttack(QMainWindow):
    """
    The fish attack class is the main window of the program. This contains the class of the fish and the class of 
    the player. However, if the player want the gane to begin, they need to click
    the checkbox, and after the checkbox is being clicked, the signals will make
    the game start

    The game:
    - Contains fish class
    - Contains player class
    - Contains victory and defeat pages
    """
    def __init__(self, plr_data=None, parent=None, background=None, **kwargs):
        super(FishAttack, self).__init__(**kwargs)
        self.setWindowTitle("Fish attack")
        self.showFullScreen()

        if background is None:
            self.background = rf"H_images\FishAttacks\beach.png"
        else:
            self.background = background

        self.plr_data = plr_data
        print(f"\n\n\nPLR DATA IN FISH ATTACK:\n{self.plr_data}")

        # central widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # The layouts
        self.main_layout = QVBoxLayout(self.central_widget) 
        self.central_widget.setLayout(self.main_layout)

        self.middle_vbox = QVBoxLayout()
        self.main_layout.addLayout(self.middle_vbox)

        # The stacking widgets
        self.stacking = QStackedWidget(self.central_widget)
        self.stacking.setFixedSize(QSize(self.width(), self.height()))

        # call the methods
        self.font_load()
        self.sceneryComp()
        self.loading_page()

        # Add the bottom layout
        self.bottom_vbox = QVBoxLayout() 
        self.main_layout.addLayout(self.bottom_vbox) 

    def font_load(self):
        self.font_id = QFontDatabase.addApplicationFont("Z_custom_fonts/Jersey15-Regular.ttf")
        self.font_id2 = QFontDatabase.addApplicationFont("Z_custom_fonts/PixelifySans-VariableFont_wght.ttf")

        self.font_family = QFontDatabase.applicationFontFamilies(self.font_id)[0]
        self.custom_font = QFont(self.font_family)
        self.custom_font.setBold(True)

        self.font_family2 = QFontDatabase.applicationFontFamilies(self.font_id2)[0]
        self.custom_font2 = QFont(self.font_family2)
        self.custom_font2.setBold(False)

    def sceneryComp(self):
        self.bg_load = QPixmap(fr"{self.background}")
        self.bg_image = QLabel(self.central_widget)
        self.bg_image.setGeometry(0, 0, self.width(), self.height())
        self.bg_image.setPixmap(self.bg_load)
        self.bg_image.setScaledContents(True)

        # send the bg to the back
        self.bg_image.lower()

    def loading_page(self):
        self.bg_image.hide()
        self.setStyleSheet("background-color: black;")
        # Set the layout for the QLabel
        self.load_label = QLabel("Loading.")
        self.load_label.setStyleSheet(f"""QLabel{{
                                      font-family: {self.font_family2};
                                      font-size: 120px;
                                      color: white;
                                      font-weight: bold;
                                      padding: 10px;
                                      }}""")
        self.load_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.middle_vbox.addWidget(self.load_label)

        # Add the timer to QLabel (animate the dot)
        self.dot_count = 1
        self.load_lab_timer = QTimer(self)
        self.load_lab_timer.timeout.connect(lambda: self.update_the_text())
        self.load_lab_timer.start(400)

        # The QCheckbutton, create it inside the QWidget
        cck_widget = QWidget()
        cck_widget.setStyleSheet("background-color: transparent;")
        cck_widget.setFixedSize(QSize(700,100))
        self.middle_vbox.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.cck_layout = QHBoxLayout(cck_widget)
        self.ready_cck = QCheckBox("Click to start the game")
        self.ready_cck.setStyleSheet(f"""
            QCheckBox {{
                font-family: {self.font_family};
                font-size: 60px;
                color: white;
                spacing: 8px;
                margin-left: 100px; /*Add the margin to make it little off center*/
            }}

            QCheckBox::indicator {{
                width: 20px;
                height: 20px;
                border-radius: 5px;
                border: 2px solid #37bcff;
                background-color: transparent;
            }}

            QCheckBox::indicator:checked {{
                background-color: #00d523;
                border: 2px solid #37bcff;
            }}

            QCheckBox::indicator:hover{{
                background-color: #00d523;
            }}
        """)

        self.cck_layout.addWidget(self.ready_cck)
        self.middle_vbox.addWidget(cck_widget)

        # connect the cck signals
        self.ready_cck.stateChanged.connect(lambda state: self.game_begin(state))

    def update_the_text(self):
        self.dot_count = (self.dot_count % 3) + 1  
        self.load_label.setText(f"Loading{'.' * self.dot_count}")
    
    #STARTING THE GAME
    def game_begin(self, state):
        if self.ready_cck.isChecked():
            print("Game Start", f"CheckState = {state}")

            # Stop load timer
            self.load_lab_timer.stop()

            # Clear the label and cck 
            self.load_label.hide()
            self.ready_cck.setDisabled(True)
            self.ready_cck.hide()

            # Count down 
            self.countdown = 3
            self.load_label.setStyleSheet(f"font-size: 300px; color: white; font-family: {self.font_family2}")
            self.load_label.setText(str(self.countdown))
            self.load_label.show()

            self.countdown_timer = QTimer(self)
            self.countdown_timer.timeout.connect(lambda: self.update_countdown())
            self.countdown_timer.start(1000)

        else:
            print("Not starting", f"CheckState = {state}")
    
    def update_countdown(self):
        self.countdown -= 1
        self.load_label.setText(str(self.countdown))

        if self.countdown == 0:
            self.load_lab_timer.stop()
            self.load_label.hide()
            self.setStyleSheet("background: transparent;")
            self.bg_image.show()

            # Call another method
            self.fish_attack_game()
    
    ################ LOADING PLAYER AND FISH
    def fish_attack_game(self):
        """
        Load the player, and add the wall collision logic to the player using
        .move_event.connect(self.moving_handle) 
        """
        ### PLAYER LOAD
        self.player = PlayerAnimate(self, plr_data= self.plr_data)
        self.player.setStyleSheet("background-color: transparent; margin-bottom: 0px;")
        self.player.setFixedSize(QSize(250,500))
        self.player.move(0,600)
        self.player.setParent(self.central_widget) # Set the player layer on the main widget
        self.player.show()
        self.player.setFocus() 
        #self.player.move_event.connect(self.moving_handle) 

        #### FISH LOAD (load the fish gif)
        self.enemyFish = FishEnemy(self, plr_data=self.plr_data)
        self.enemyFish.setStyleSheet("background: transparent; margin-bottom: 0px;")
        self.enemyFish.setFixedSize(QSize(400,320))
        self.enemyFish.move(1150,750)
        self.enemyFish.setParent(self.central_widget)
        self.enemyFish.show()

        ########## When the fish is dead
        if self.enemyFish.health <= 0:
            print("Victory")
        
        if self.player.health <= 0:
            print("Defeat")
    
    def check_collision(self):
        player_pos = self.player.pos()
        screen_width = self.width()
        screen_height = self.height()

        ######## FOR THE COLLISION, I ask chatbot for the solution and modify into my version
        if player_pos.x() <= 10:  
            return True, "left"
        if player_pos.x() + self.player.width() >= screen_width - 10:  
            return True, "right"
        if player_pos.y() <= 10: 
            return True, "top"
        if player_pos.y() + self.player.height() >= screen_height - 10:  
            return True, "bottom"
        
        return False, ""

    def moving_handle(self, new_pos):
        collided, direction = self.check_collision()
        
        if collided:
            print(f"player hit {direction} side")
            
            if direction == "left" and new_pos.x() < self.player.x():
                new_pos.setX(10)  
            elif direction == "right" and new_pos.x() > self.player.x():
                new_pos.setX(self.width() - self.player.width() - 10) 
            elif direction == "top" and new_pos.y() < self.player.y():
                new_pos.setY(10) 
            elif direction == "bottom" and new_pos.y() > self.player.y():
                new_pos.setY(self.height() - self.player.height() - 10)

        self.player.move(new_pos)

    def display_defeat(self):
        self.dead_text = QLabel("DEFEAT")
        self.dead_text.setStyleSheet(f"""QLabel{{
                                     background-color: transparent;
                                     color: white;
                                     font-family: {self.font_family};
                                     font-size: 120px;
        }}""")
        self.dead_text.move(400, 300)

    ## This will allow player to click anywhere on the screen to attack instead of clicking the sprite
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if not self.player.attack_cooldown.isActive():  # When cooldown is not active
                self.player.attack_frame = 0
                self.player.is_attacking = True
                self.player.update_attack_sprite()
                self.player.attack_timer.start(100)
                self.player.attack_cooldown.start(500)



################## THE PLAYER CLASS 
class PlayerAnimate(QWidget):
    move_event = pyqtSignal(QPoint)

    def __init__(self, speed=0.09, plr_data = None, parent=None):
        super(PlayerAnimate, self).__init__(parent)
        self.setGeometry(0, 600, 200, 500)
        self.hold = False
        self.direction = None
        self.is_jumping = False
        self.is_attacking = False
        self.velocity = 0  
        self.health = 100
        self.y_pos = 150  
        self.plr_data = plr_data

        self.speed = speed
        self.can_move = True
        self.can_attack = True
        self.defeat_shown = False 

        self.font_id = QFontDatabase.addApplicationFont("Z_custom_fonts/Jersey15-Regular.ttf")
        self.font_id2 = QFontDatabase.addApplicationFont("Z_custom_fonts/PixelifySans-VariableFont_wght.ttf")

        self.font_family = QFontDatabase.applicationFontFamilies(self.font_id)[0]
        self.custom_font = QFont(self.font_family)
        self.custom_font.setBold(True)

        self.font_family2 = QFontDatabase.applicationFontFamilies(self.font_id2)[0]
        self.custom_font2 = QFont(self.font_family2)
        self.custom_font2.setBold(False)
        # Player sprite (walking)
        self.sprite = QPixmap(r"Sprites\Walk.png")
        self.sprite_width = 128
        self.sprite_height = 128
        self.current_frame = 0

        # Attack sprites
        self.attack_sprite = QPixmap(r"Sprites\Attack_2.png")
        self.attack_width = 128
        self.attack_height = 128
        self.attack_frame = 0
        self.attack_max_frames = 3  

        self.x_pos = 0  # Starting x position
        self.widget_x_pos = 0

        # The QLabel to display the sprite
        self.sprite_lab = QLabel(self)
        self.sprite_lab.setScaledContents(False)
        self.sprite_lab.move(self.x_pos, self.y_pos)

        #### The player collider ##### (for collisions)
        self.player_collider = QRect(self.x_pos, self.y_pos, 250, 250) # (posx, posy, width, height)
        
        # The player healthbar
        self.display_healthbar()

        # Animation timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_sprite)
        self.update_sprite()

        self.move_timer = QTimer(self)
        self.move_timer.timeout.connect(self.move_sprite)

        ##################### THE PLAYER DAMAGE TIMER ########################
        """
        In this part, I can't really make the fish to attack player, so I decided to call the 
        use the take_damage method in the class and take the damage out from the player
        (After the player reaches 0, the dead animation will appear)
        """
        self.random_damage = random.randint(1, 3)
        self.damage_timer = QTimer(self)
        self.damage_timer.timeout.connect(lambda: self.take_damage(self.random_damage))
        self.damage_timer.start(1200) 
       ####################################################################

        # Dead sprite
        self.dead_sprite = QPixmap(r"Sprites\Dead.png")
        self.dead_sprite_width = 128
        self.dead_sprite_height = 128
        self.dead_frame = 0
        self.max_dead_frames = 4 
        self.direction = "left"

        self.dead_timer = QTimer(self)
        self.dead_timer.timeout.connect(self.update_dead_sprite)
     
        # Attack cool down timer
        self.attack_timer = QTimer(self)
        self.attack_timer.timeout.connect(self.update_attack_sprite)

        self.attack_cooldown = QTimer(self)
        self.attack_cooldown.timeout.connect(self.reset_attack)

    ################# PAINT THE PLAYER COLLIDER ###################
    '''
    def paintEvent(self, a0):
        painter = QPainter(self)
        pen = QPen(Qt.GlobalColor.red)
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawRect(self.player_collider)
    '''
    
    def update_sprite(self):
        if self.health == 0: 
            self.update_dead_sprite() # when player dead
            self.dead_timer.start(200)

            # clear healthbar
            self.curr_health.clear()
            self.total_health.clear()
            self.total_health.hide()
            self.curr_health.hide()
            
            #self.dead_timer.timeout.connect(self.show_defeat)

        else:
            if self.is_attacking:
                self.update_attack_sprite()
            else:
                self.update_walk_sprite()

    def show_defeat(self):
        if self.defeat_shown and not hasattr(self, "defeat_shown_once"):
            self.defeat_shown_once = True
            self.defeat = DefeatPage(parent=self, plr_data=self.plr_data)
            
            if hasattr(self, "fish_attk") and self.fish_attk is not None:
                if hasattr(self.fish_attk, "stacking"):
                    self.fish_attk.stacking.addWidget(self.defeat)
                    self.fish_attk.stacking.setCurrentWidget(self.defeat)

                if hasattr(self.fish_attk, "central_widget") and self.fish_attk.central_widget is not None:
                    self.fish_attk.central_widget.hide()

                self.fish_attk.setCentralWidget(self.fish_attk.stacking)

            self.defeat.show()
            self.hide()

    def update_walk_sprite(self):
        self.x_dir = self.current_frame * self.sprite_width
        self.y_dir = 0

        self.frame = self.sprite.copy(self.x_dir, self.y_dir, self.sprite_width, self.sprite_height)

        if self.direction == "left":
            transform = QTransform().scale(-1, 1)
            self.frame = self.frame.transformed(transform)

        resize_sprite = self.frame.scaled(self.sprite_width * 2, self.sprite_height * 2)
        self.sprite_lab.setPixmap(resize_sprite)

        self.current_frame += 1
        if self.current_frame >= 5:
            self.current_frame = 0
    
    def update_attack_sprite(self):
        if self.health == 0:
            return 
         
        if not self.can_attack:
            return
        
        if self.attack_frame >= self.attack_max_frames:
            self.attack_timer.stop() 
            self.attack_cooldown.start(500) 
            self.is_attacking = False  # Stop attacking animation
            
        else:
            self.x_dir = self.attack_frame * self.attack_width
            self.y_dir = 0

            self.frame = self.attack_sprite.copy(self.x_dir, self.y_dir, self.attack_width, self.attack_height)

            if self.direction == "left":
                transform = QTransform().scale(-1, 1)
                self.frame = self.frame.transformed(transform)

            resize_sprite = self.frame.scaled(self.attack_width * 2, self.attack_height * 2)
            self.sprite_lab.setPixmap(resize_sprite)

            self.attack_frame += 1

    def update_dead_sprite(self):
        self.x_dir = self.dead_frame * self.dead_sprite_width
        self.y_dir = 0 
        
        self.frame = self.dead_sprite.copy(self.x_dir, self.y_dir, self.dead_sprite_width, self.dead_sprite_height)

        if self.direction == "left":
            transform = QTransform().scale(-1, 1)  
            self.frame = self.frame.transformed(transform)

        resize_sprite = self.frame.scaled(self.dead_sprite_width * 2, self.dead_sprite_height * 2)
        self.sprite_lab.setPixmap(resize_sprite)
        self.dead_frame += 1
        
        if self.dead_frame >= self.max_dead_frames:
            self.dead_frame = 0 
            self.dead_timer.stop() 
        
        if not self.defeat_shown:
            self.defeat_shown = True
            QTimer.singleShot(4000, self.show_defeat)

    def reset_attack(self):
        self.attack_frame = 0
        self.attack_cooldown.stop()  # stop cooldown, player can attack again
    
    '''
    def mousePressEvent(self, event):
        self.enemyFish = FishEnemy(self)
        if event.button() == Qt.MouseButton.LeftButton:
            if not self.attack_cooldown.isActive():  # When cooldown is not active
                self.attack_frame = 0
                self.is_attacking = True
                self.update_attack_sprite()
                self.attack_timer.start(100)
                self.attack_cooldown.start(500)
    '''

    def keyPressEvent(self, event):
        if self.health == 0:
            return  # Don't move if dead

        if event.key() == Qt.Key.Key_D and not self.hold:
            self.hold = True
            self.direction = "right"
            if not self.timer.isActive():
                self.timer.start(30)
            if not self.move_timer.isActive():
                self.move_timer.start(10)

        elif event.key() == Qt.Key.Key_A and not self.hold:
            self.hold = True
            self.direction = "left"
            if not self.timer.isActive():
                self.timer.start(30)
            if not self.move_timer.isActive():
                self.move_timer.start(10)

        elif event.key() == Qt.Key.Key_Space and not self.is_jumping:
            self.velocity = -15
            self.is_jumping = True
            threading.Thread(target=self.jump, daemon=True).start()

    def keyReleaseEvent(self, event):
        if event.key() in [Qt.Key.Key_D, Qt.Key.Key_A]:
            self.hold = False
            self.move_timer.stop()
            self.timer.stop()

    def move_sprite(self):
        if self.health == 0:
            return  # Don't move if dead

        if not self.can_move:
            return
        
        self.player_collider.moveTo(self.x_pos, self.y_pos)

        if self.direction == "right":
            if self.x_pos + self.sprite_width * 2 < self.width():
                self.x_pos += 3
            else:
                self.widget_x_pos += 3
                self.move(self.widget_x_pos, 600)
        elif self.direction == "left":
            if self.x_pos > 0:
                self.x_pos -= 3
            else:
                self.widget_x_pos -= 3
                self.move(self.widget_x_pos, 600)

        new_pos = QPoint(self.x_pos, self.y_pos)
        self.sprite_lab.move(new_pos)

        self.move_event.emit(new_pos)

    def jump(self):
        while self.is_jumping:
            self.velocity += 1
            self.y_pos += self.velocity

            if self.y_pos >= 150:
                self.y_pos = 150
                self.velocity = 0
                self.is_jumping = False

            self.sprite_lab.move(self.x_pos, self.y_pos)
            self.total_health.move(self.x_pos, self.y_pos - 20)
            self.curr_health.move(self.x_pos, self.y_pos - 20)

            delay(0.02)  # the jump speed

    def display_healthbar(self):
        self.total_health = QLabel(self)
        self.total_health.setStyleSheet("background-color: red; border: 2px solid black;")
        self.total_health.setGeometry(self.x_pos + 20, self.y_pos, 220, 20)

        self.curr_health = QLabel(self)
        self.curr_health.setStyleSheet("background-color: #27ce00;")
        self.curr_health.setGeometry(self.x_pos + 20, self.y_pos, 220, 20)

        self.set_health(100)

    def set_health(self, value):
        self.health = value
        if value < 0:
            value = 0
        elif value > 100:
            value = 100

        self.curr_health.setFixedWidth(int(220 * (value / 100)))

    def take_damage(self, dmg):
        if self.health == 0:
            return
        
        current_health = int((self.curr_health.width() / 220) * 100)
        new_health = current_health - dmg

        if new_health < 0:
            new_health = 0

        self.set_health(new_health)

        if self.health == 0:
            self.die()

    def die(self):
        self.can_move = False
        self.timer.stop() 
        self.move_timer.stop()
        self.damage_timer.stop()
        self.update_sprite()  # call the update sprite, and it will show dead animation


############### THE FISH Class ############## the fish enemy class
class FishEnemy(QWidget):
    def __init__(self, player, parent=None, plr_data =None):
        super(FishEnemy, self).__init__(parent)
        self.setGeometry(0, 600, 400, 300)
        self.player = player
        self.plr_data = plr_data

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
        self.attack_cool.setInterval(500)
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

        rd_weight = [1, 1, 1, 1]

        self.select_fish = random.choices(self.fish_gif, weights=rd_weight)[0]
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
            self.player = PlayerAnimate(self)
            if event.button() == Qt.MouseButton.LeftButton:
                if not self.player.attack_cooldown.isActive(): 
                    self.player.attack_frame = 0
                    self.player.is_attacking = True
                    self.player.update_attack_sprite()
                    self.player.attack_timer.start(100)
                    self.player.attack_cooldown.start(500)

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
        damage = random.randint(5, 10) # Random damage make from player
        self.take_damage(damage)

    def take_damage(self, dmg):
        if self.health == 0: 
            return
        
        new_health = self.health - dmg
        if new_health <= 0:
            new_health = 0

        self.health_set(new_health)

        if self.health == 0:
            print("The fish is dead, fish will fade in 1 second")
            self.dead_fish() 

            # Fade the fish away and stop the animated gif 
            self.health_bg.hide()
            self.fish_curr_health.hide()

            self.fish_lab.hide()
            self.show_victory() # show victory page
            print(f"Victory function called!")
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
    
    ##### SHOW THE VICTORY PAGE
    def show_victory(self):
        if not hasattr(self, "victory_shown") or not self.victory_shown:  
            self.victory_shown = True  
            self.victory = VictoryPage(parent=self, plr_data=self.plr_data)
            
            if hasattr(self, "fish_attk") and self.fish_attk is not None:
                if hasattr(self.fish_attk, "stacking") and self.fish_attk.stacking is not None:
                    self.fish_attk.stacking.addWidget(self.victory)
                    self.fish_attk.stacking.setCurrentWidget(self.victory)

                if hasattr(self.fish_attk, "central_widget") and self.fish_attk.central_widget is not None:
                    self.fish_attk.central_widget.hide()

                self.fish_attk.setCentralWidget(self.fish_attk.stacking)

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

###################### DEFEAT PAGE
class DefeatPage(QMainWindow):
    def __init__(self, parent=None, plr_data=None):
        super(DefeatPage, self).__init__(parent)
        self.showFullScreen()
        self.plr_data = plr_data

        print(f"DEFEAT PAGE: {self.plr_data}")

        self.font_id = QFontDatabase.addApplicationFont("Z_custom_fonts/Jersey15-Regular.ttf")
        self.font_id2 = QFontDatabase.addApplicationFont("Z_custom_fonts/PixelifySans-VariableFont_wght.ttf")

        self.font_family = QFontDatabase.applicationFontFamilies(self.font_id)[0]
        self.custom_font = QFont(self.font_family)
        self.custom_font.setBold(True)

        self.font_family2 = QFontDatabase.applicationFontFamilies(self.font_id2)[0]
        self.custom_font2 = QFont(self.font_family2)
        self.custom_font2.setBold(False)

        self.setStyleSheet("background-color: black")

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Create the "DEFEAT" label
        self.defeat = QLabel("DEFEAT", self)
        self.defeat.setStyleSheet(f"""QLabel {{
                                      font-family: {self.font_family};
                                      font-size: 300px;
                                      color: red;
                                    }}""")
        self.defeat.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # back button
        self.back_button = QPushButton("Back", self)
        self.back_button.setStyleSheet(f"""QPushButton{{
                                       font-family: {self.font_family};
                                       font-size: 50px;
                                       color: white;
                                       background-color: #bd3e3e;
                                       width: 100px;
                                       height: 60px;
                                    }}

                                    QPushButton::hover{{
                                       background-color: #a02f2f;
                                    }}
        """)
        self.back_button.clicked.connect(lambda: self.click_back())

        self.central_layout = QVBoxLayout(self.central_widget)
        #self.central_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.central_layout.addWidget(self.defeat)
        self.central_layout.addWidget(self.back_button)
        self.central_widget.setLayout(self.central_layout)
    
    def click_back(self):  #### Click the button to go back to choosemode page
        from A_Title.choosemode import ChooseMode

        self.setStyleSheet("background-color: none;")  
        if hasattr(self, 'central_widget') and self.central_widget is not None:
            self.central_widget.hide()  

        if not hasattr(self, "choosing"):
            self.choosing = ChooseMode(plr_data=self.plr_data)

        self.main_wind = FishAttack(parent=self, plr_data=self.plr_data)  # We still need this to set the layout correctly
        self.main_wind.stacking.addWidget(self.choosing)
        self.main_wind.stacking.setCurrentWidget(self.choosing)

        self.setCentralWidget(self.main_wind.stacking)
        self.choosing.show()
        self.main_wind.hide()

######################### VICTORY PAGE
class VictoryPage(QMainWindow):
    def __init__(self, parent=None, plr_data=None):
        super(VictoryPage, self).__init__(parent)
        self.showFullScreen()
        self.plr_data = plr_data

        print(f"DEFEAT PAGE: {self.plr_data}")

        self.font_id = QFontDatabase.addApplicationFont("Z_custom_fonts/Jersey15-Regular.ttf")
        self.font_id2 = QFontDatabase.addApplicationFont("Z_custom_fonts/PixelifySans-VariableFont_wght.ttf")

        self.font_family = QFontDatabase.applicationFontFamilies(self.font_id)[0]
        self.custom_font = QFont(self.font_family)
        self.custom_font.setBold(True)

        self.font_family2 = QFontDatabase.applicationFontFamilies(self.font_id2)[0]
        self.custom_font2 = QFont(self.font_family2)
        self.custom_font2.setBold(False)

        self.setStyleSheet("background-color: black")

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Create the "DEFEAT" label
        self.defeat = QLabel("VICTORY!", self)
        self.defeat.setStyleSheet(f"""QLabel {{
                                      font-family: {self.font_family};
                                      font-size: 300px;
                                      color: #ffd800;
                                    }}""")
        self.defeat.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # back button
        self.back_button = QPushButton("Back", self)
        self.back_button.setStyleSheet(f"""QPushButton{{
                                       font-family: {self.font_family};
                                       font-size: 50px;
                                       color: white;
                                       background-color: #bd3e3e;
                                       width: 100px;
                                       height: 60px;
                                    }}

                                    QPushButton::hover{{
                                       background-color: #a02f2f;
                                    }}
        """)
        self.back_button.clicked.connect(lambda: self.click_back())

        self.central_layout = QVBoxLayout(self.central_widget)
        #self.central_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.central_layout.addWidget(self.defeat)
        self.central_layout.addWidget(self.back_button)
        self.central_widget.setLayout(self.central_layout)

    def click_back(self):  #### Click the button to go back to choosemode page
        from A_Title.choosemode import ChooseMode

        self.setStyleSheet("background-color: none;")  
        if hasattr(self, 'central_widget') and self.central_widget is not None:
            self.central_widget.hide()  

        if not hasattr(self, "choosing"):
            self.choosing = ChooseMode(plr_data=self.plr_data)

        self.main_wind = FishAttack(parent=self, plr_data=self.plr_data)  # We still need this to set the layout correctly
        self.main_wind.stacking.addWidget(self.choosing)
        self.main_wind.stacking.setCurrentWidget(self.choosing)

        self.setCentralWidget(self.main_wind.stacking)
        self.choosing.show()
        self.main_wind.hide()

def main():
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    window = FishAttack()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()