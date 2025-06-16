from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import sys

class AnimateCharacterWindow(QWidget):
    """
    - This class contains the basic text animation.
    - Text is stored in a string and will be displayed by using `self.text[:self.index + 1]` to display 1 letter at a time.
    """

    # Class method showing signal whether animation is complete
    animation_finished = pyqtSignal()

    def __init__(self, opacity=255, width=1200, height=800, background_color=(0, 0, 0), parent=None, **kwargs):
        super(AnimateCharacterWindow, self).__init__(parent, **kwargs)
        self.opacity = opacity

        self.setFixedSize(QSize(width, height))

        self.font_id = QFontDatabase.addApplicationFont("Z_custom_fonts/Jersey15-Regular.ttf")
        self.font_id2 = QFontDatabase.addApplicationFont("Z_custom_fonts/PixelifySans-VariableFont_wght.ttf")

        self.font_family = QFontDatabase.applicationFontFamilies(self.font_id)[0]
        self.custom_font = QFont(self.font_family)
        self.custom_font.setBold(True)

        self.font_family2 = QFontDatabase.applicationFontFamilies(self.font_id2)[0]
        self.custom_font2 = QFont(self.font_family2)
        self.custom_font2.setBold(False)

        self.setStyleSheet(f"""
                           background: rgba({background_color[0]}, {background_color[1]}, {background_color[2]}, {self.opacity});
                           border-radius: 7px;
                           """)

        self.label = QLabel("", self)
        self.label.setStyleSheet(f"""
                                 QLabel{{
                                 font-family: {self.font_family};
                                 font-size: 40px;
                                 color: white;
                                 padding: 10px;
                                 line-height: 1.5;
                                 }}""")
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)  
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.isRunning = False
        self.text = ""  
        self.index = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_text)
        self.speed = 30 

        self.animation_finished.connect(self.start_next_animation)

    def animate_text(self, text):
        if self.isRunning:
            return 
        self.text = text
        self.index = 0
        self.label.setStyleSheet(f"""
                                QLabel{{
                                font-family: {self.font_family};
                                font-size: 40px;
                                color: white;
                                padding: 10px;
                                line-height: 1.5;
                                }}""")
        self.update()
        self.isRunning = True 
        self.timer.start(self.speed)

    def update_text(self):
        if self.index < len(self.text):
            self.curr = self.text[:self.index + 1]
            self.label.setText(self.curr)
            self.index += 1
        else:
            self.timer.stop()  
            self.isRunning = False  
            self.animation_finished.emit()  

    def start_next_animation(self):
        if hasattr(self, "next_animation_text"):
            self.animate_text(self.next_animation_text)
            del self.next_animation_text

    def set_next_animation(self, text):
        self.next_animation_text = text

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.isRunning:
                self.label.setText(self.text)
                self.isRunning = False
                self.timer.stop()  
            elif hasattr(self, "next_animation_text"):
                self.start_next_animation()

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            event.accept()  
            if not self.isRunning:  
                if hasattr(self, "next_animation_text"):
                    self.start_next_animation()
                else:
                    self.animation_finished.emit()

if __name__ == "__main__":
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    window = AnimateCharacterWindow(opacity=100, background_color=(0, 0, 0))
    window.set_next_animation("sdfdsfdfdsfsdfdsfds\nsdfodsfjodjfdfjdsodjoj\nsdofjdsjfod")
    window.start_next_animation()
    window.show()
    app.exec()