from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import sys
import random

class TitlePage(QMainWindow):
    def __init__(self, plr_data=None, parent=None, *args, **kwargs):
        super(TitlePage, self).__init__(parent, *args, **kwargs)
        self.setWindowTitle("Fisherman Chronicles")
        self.showFullScreen()
        
        self.plr_data = plr_data
        print(f"PLAYER DATA IN TITLE PAGE: \n{self.plr_data}")

        # custom fonts (get the font)
        self.font_id = QFontDatabase.addApplicationFont("Z_custom_fonts\Jersey15-Regular.ttf")
        self.font_id2 = QFontDatabase.addApplicationFont("Z_custom_fonts\PixelifySans-VariableFont_wght.ttf")

        # The central widget and layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)  # specify the central widget
    
        # The stack widget for switching pages
        self.stack_widget = QStackedWidget(self.central_widget)
        self.stack_widget.setFixedSize(QSize(self.width(), self.height()))

        # Background label
        self.pixmap = QPixmap(r"H_images\img_login\night_time.png")
        self.label = QLabel(self.central_widget)
        self.label.setGeometry(0, 0, self.width(), self.height())
        self.label.setPixmap(self.pixmap)
        self.label.setScaledContents(True)

        # Call the functions
        self.components()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.fish_swim)
        self.timer.start(2000)  # spawn every 0.5 sec

        self.shark_timer = QTimer(self)
        self.shark_timer.timeout.connect(self.shark_swim)
        self.shark_timer.start(2500)  # spawn every 0.5 sec

        # Show the window 
        self.show()
    
    # set the player data (get, set method)
    def set_player_data(self, plr_data):
        self.plr_data = plr_data
        print(f"Plr data: {self.plr_data}")

    def components(self):
        # The custom font execution
        font_family = QFontDatabase.applicationFontFamilies(self.font_id)[0] 
        custom_font = QFont(font_family) 
        custom_font.setBold(True)

        font_family2 = QFontDatabase.applicationFontFamilies(self.font_id2)[0] 
        custom_font2 = QFont(font_family2) 
        custom_font2.setBold(False)

        # Title label
        self.title_layout = QHBoxLayout()
        self.title_lab = QLabel(text="Fisherman Chronicles")
        self.title_lab.setFixedSize(QSize(1400, 300))
        self.title_lab.setFont(custom_font)
        self.title_lab.setStyleSheet("""color: white;
                                       margin-top: 50px;
                                       font-size: 150px;
                                       width: 200px;
                                       background-color: rgb(22, 48, 125); 
                                       border: 5px outset #51f4ff;
                                       font-weight: bold;""")
        self.title_lab.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_layout.addWidget(self.title_lab)
        self.main_layout.addLayout(self.title_layout)

        # set the opacity of title label
        self.opacity = QGraphicsOpacityEffect(self)
        self.title_lab.setGraphicsEffect(self.opacity)
        self.animate_title()

        self.btns_names = ["Play", "Options", "Exit"]
        self.obj_name = ["play", "options", "exit"]

        # Create and add buttons to the layout
        self.btn_layouts = QVBoxLayout()
        self.btn_layouts.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        self.main_layout.addLayout(self.btn_layouts)

        for i in range(len(self.btns_names)):
            self.btn = QPushButton(self.btns_names[i])
            self.btn.setFont(custom_font2)
            self.btn.setFixedSize(QSize(400, 150))
            self.btn.setObjectName(self.obj_name[i])
            self.btn_layouts.addWidget(self.btn)

            if self.obj_name[i] == "exit":
                self.btn.clicked.connect(self.exitting_program)
            elif self.obj_name[i] == "play":
                self.btn.clicked.connect(self.play_game)
            elif self.obj_name[i] == "options":
                self.btn.clicked.connect(self.go_options)

        # Apply the stylesheet for all buttons at once (apply it to the self components)
        self.setStyleSheet("""
            QPushButton#play {
                background-color: #1fab00;
                border: 4px outset green;
                color: white;
                font-size: 50px;
                font-weight: bold;
                text-transform: uppercase;
                text-align: center;
                margin-top:20px;
                border-radius: 10px;
            }

            QPushButton#options {
                background-color: #8d8d8d;
                border: 4px outset gray;
                color: white;
                font-size: 50px;
                font-weight: bold;
                text-transform: uppercase;
                text-align: center;
                margin-top:20px;
                border-radius: 10px;
            }

            QPushButton#exit {
                background-color: #9d364b;
                border: 4px outset red;
                color: white;
                font-size: 50px;
                font-weight: bold;
                text-transform: uppercase;
                text-align: center;
                margin-top:20px;
                border-radius: 10px;
            }

            QPushButton#play:hover {
                background-color: green;
            }

            QPushButton#options:hover {
                background-color: #707070;
            }

            QPushButton#exit:hover {
                background-color: #cc0066;
            }
        """)

    def exitting_program(self):
        answer = QMessageBox.information(self, "Exit?", "Do you want to exit the program",
                                          QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)

        if answer == QMessageBox.StandardButton.Ok:
            self.fading = QPropertyAnimation(self, b"windowOpacity")
            self.fading.setDuration(800)  
            self.fading.setStartValue(1)  
            self.fading.setEndValue(0)  

            self.fading.finished.connect(QApplication.quit)  # exit program when animation ends
            self.fading.start()

    def login_page(self):
        from A_Title import login # import inside the method
        self.setEnabled(False)
        login.main()  # call the method from login page (the player data will be passed to the __init__ )
        self.setEnabled(True)

    def play_game(self):
        """Importing inside the method prevent circular import"""
        from A_Title.choosemode import ChooseMode  # Import the ChooseMode class 

        print(f"\n\n\n{self.plr_data}")

        if self.plr_data is None:
            self.login_page()
        
        else:
            self.timer.stop()
            self.shark_timer.stop()
            self.central_widget.hide() 

            if not hasattr(self, "choose_mode_widget"):
                self.choose_mode_widget = ChooseMode(plr_data=self.plr_data, title="Choose Mode")

            self.stack_widget.addWidget(self.choose_mode_widget)  # Add ChooseMode to the stack
            self.stack_widget.setCurrentWidget(self.choose_mode_widget)  # Switch to ChooseMode
            self.choose_mode_widget.show()  # show the choose mode page
            self.setCentralWidget(self.stack_widget)

    ### call the option page
    def go_options(self):
        print("options clicked")
        from Script.change_name import LoginWindow
        self.change_name_window = LoginWindow()
        self.change_name_window.show()

    def animate_title(self):
        self.title_animate = QPropertyAnimation(self.opacity, b"opacity")
        self.title_animate.setDuration(1500)
        self.title_animate.setStartValue(0)  # transparent
        self.title_animate.setEndValue(1)   # opaque (we can see it 100%)
        self.title_animate.start()

    def fish_swim(self):  # The Gif animation using QMovie
        self.anglerfish = QLabel(self.central_widget)  
        self.mov = QMovie("Z_Enemies/anglerfish.gif")

        self.anglerfish.setMovie(self.mov)
        self.mov.start()

        self.anglerfish.setFixedSize(QSize(300, 250))
        self.anglerfish.setScaledContents(True)
        self.anglerfish.move(0, 700)

        self.anglerfish.show()

        # AFish animations
        random_anim = [QEasingCurve.Type.BezierSpline, QEasingCurve.Type.Linear]
        self.angler_anim = QPropertyAnimation(self.anglerfish, b"pos")
        self.angler_anim.setEasingCurve(random.choice(random_anim))  
        self.angler_anim.setEndValue(QPoint(self.width(), random.randint(650, 1200))) 
        self.angler_anim.setDuration(1800)  
        self.angler_anim.start()
        
        # Clear the fish
        self.clear_fish = QTimer(self)
        self.clear_fish.setSingleShot(True)
        self.clear_fish.timeout.connect(self.anglerfish.clear)
        self.clear_fish.start(2000)

    def shark_swim(self):  # The image label animation using QPixmap
        self.shark_load = QPixmap("Z_Enemies/shark1.png")
        self.shark_lab = QLabel(self.central_widget)
        self.shark_lab.setPixmap(self.shark_load)
        self.shark_lab.setScaledContents(True)
        self.shark_lab.setFixedSize(QSize(200, 200))
        self.shark_lab.move(1400, random.randint(0, self.height() - 200))

        self.shark_lab.show()

        # Animations
        anims = [QEasingCurve.Type.BezierSpline, QEasingCurve.Type.Linear]
        self.shark_anim = QPropertyAnimation(self.shark_lab, b"pos")
        self.shark_anim.setEasingCurve(random.choice(anims))  
        self.shark_anim.setEndValue(QPoint(-300, random.randint(0, self.height() - 200))) 
        self.shark_anim.setDuration(2500)  
        self.shark_anim.start()

        self.clear_shark = QTimer(self)
        self.clear_shark.setSingleShot(True)
        self.clear_shark.timeout.connect(self.clear_shark_fish)
        self.clear_shark.start(2490)

    def clear_shark_fish(self):
        if self.shark_lab is not None:
            try: # This method will handle runtime error
                if self.shark_lab.isVisible():
                    self.shark_lab.hide()
                    self.central_widget.layout().removeWidget(self.shark_lab)
                    self.shark_lab.deleteLater()
            except RuntimeError:
                pass
            finally:
                self.shark_lab = None  

def main(player_data):
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    win = TitlePage(plr_data=player_data) # pass player data from main to class
    win.show()
    app.exec()

if __name__ == "__main__":
    main("data")
