import sys
import threading
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from time import sleep as delay

class PlayerAnimate(QWidget):
    move_event = pyqtSignal(QPoint) # class attr of move event
    positionUpdated = pyqtSignal(int, int)
    scene_changed = pyqtSignal() # signal for the scene change
    dead_finish = pyqtSignal()

    """
    This class is a player animation class inherited from the QWidget. It manages player animation
    using a sprite sheet and allows movement in the x-direction using the 'A' and 'D' keys.
    """
    
    def __init__(self, speed=0.09, parent=None):
        super(PlayerAnimate, self).__init__(parent)
        self.setGeometry(0,600,200,300)
        #self.setFixedSize(QSize(200,300))
        #self.move(0,800)
        self.current_x = self.x()
        self.current_y = self.y()
        self.hold = False
        self.direction = None
        self.is_jumping = False
        self.velocity = 0  # vertical speed
        self.y_pos = 40 # Starting ground level

        self.speed = speed
        self.can_move = True
        self.is_dead = False

        # Player sprite
        self.sprite = QPixmap(r"Sprites\Walk.png")
        self.sprite_width = 128
        self.sprite_height = 128
        self.current_frame = 0

        self.x_pos = 0  # Starting x position
        self.widget_x_pos = 0
        
        # The QLabel to display the sprite
        self.sprite_lab = QLabel(self)
        self.sprite_lab.setScaledContents(False)
        self.sprite_lab.move(self.x_pos, self.y_pos)
    
        # dead sprite
        self.dead_sprite = QPixmap(r"Sprites\Dead.png")
        self.dead_sprite_width = 128
        self.dead_sprite_height = 128
        self.dead_frame = 0
        self.max_dead_frames = 4 

        #### The player collider ##### (for collisions)
        self.player_collider = QRect(self.x_pos, self.y_pos, self.sprite_width, self.sprite_height)
        #self.obstacle = QRect(300, 40, 100, 100)

        # Animation timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_sprite)
        self.update_sprite()

        # Movement timer
        self.move_timer = QTimer(self)
        self.move_timer.timeout.connect(self.move_sprite)

        # dead timer
        self.dead_timer = QTimer(self)
        self.dead_timer.timeout.connect(self.update_dead_sprite)
    
    def dead_start(self):
        self.is_dead = True
        self.dead_timer.start(200)
        self.can_move = False
        QTimer.singleShot(300, self.dead_finish.emit)
        

    def update_sprite(self):
        self.x_dir = self.current_frame * self.sprite_width
        self.y_dir = 0

        self.frame = self.sprite.copy(self.x_dir, self.y_dir, self.sprite_width, self.sprite_height)

        # Flip the sprite if moving left
        if self.direction == "left":
            transform = QTransform().scale(-1, 1)
            self.frame = self.frame.transformed(transform)

        resize_sprite = self.frame.scaled(self.sprite_width * 2, self.sprite_height * 2)
        self.sprite_lab.setPixmap(resize_sprite)

        self.current_frame += 1
        if self.current_frame >= 5:
            self.current_frame = 0

    def keyPressEvent(self, event):
        if self.is_dead:
            return
        
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

            if self.y_pos >= 40: 
                self.y_pos = 40  
                self.velocity = 0 
                self.is_jumping = False  

            self.sprite_lab.move(self.x_pos, self.y_pos)
            delay(0.02)  # the jump speed

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
        
        # Stop when reach the amximm frame
        if self.dead_frame >= self.max_dead_frames:
            self.dead_frame = 0 
            self.dead_timer.stop() 

if __name__ == "__main__":
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    window = PlayerAnimate()
    window.show()
    app.exec()