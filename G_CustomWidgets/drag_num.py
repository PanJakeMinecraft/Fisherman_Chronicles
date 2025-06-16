from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import sys

class ArrangeNum(QWidget):
    # Make a signal that will emit the correct order
    correct_signal = pyqtSignal()

    def __init__(self, parent=None):
        super(ArrangeNum, self).__init__(parent)
        self.setFixedSize(QSize(550, 700))
        self.setWindowTitle("Drag and drop")

        self.setStyleSheet("background-color: transparent")
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom)
        self.setLayout(self.main_layout)

        # call the methods (load fonts)
        self.load_fonts()

        # Direction text
        self.label = QLabel("Rearrange the numbers\n   From low to high")
        self.label.setStyleSheet(f"color: white; padding: 10px; font-family: {self.font_family}; font-size: 40px;")
        self.label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.label)

        # Call the create buttons
        self.create_buttons(bg_color="#ff9a0b")

    def load_fonts(self):
        self.font_id = QFontDatabase.addApplicationFont("Z_custom_fonts/Jersey15-Regular.ttf")
        self.font_id2 = QFontDatabase.addApplicationFont("Z_custom_fonts/PixelifySans-VariableFont_wght.ttf")

        self.font_family = QFontDatabase.applicationFontFamilies(self.font_id)[0]
        self.custom_font = QFont(self.font_family)
        self.custom_font.setBold(True)

        self.font_family2 = QFontDatabase.applicationFontFamilies(self.font_id2)[0]
        self.custom_font2 = QFont(self.font_family2)
        self.custom_font2.setBold(False)
    
    def create_buttons(self, bg_color=None):
        self.btn_nums = ["100", "50", "399", "999", "250", "10"]
        self.buttons = []

        for i in range(len(self.btn_nums)):
            btn = ButtonDrag(self.btn_nums[i], self)
            self.main_layout.addWidget(btn)
            self.buttons.append(btn)

    def reorder_buttons(self, dragged_btn, target):
        idx_dragg = self.buttons.index(dragged_btn)
        idx_target = self.buttons.index(target)
        
        self.buttons.insert(idx_target, self.buttons.pop(idx_dragg))

        # Refresh the main layout so that we will not see the overlap
        for x in self.buttons:
            self.main_layout.removeWidget(x)
        for x in self.buttons:
            self.main_layout.addWidget(x)

        # Call the check correct method
        self.check_correct()

    def check_correct(self):
        """
        The player need to order the number from low to high vertically
        This method will check whether the number is being ordered correctly?
        """
        values = []
        for k in self.buttons:
            print(int(k.text()))
            values.append(int(k.text()))  

        sorted_values = sorted(values) # sort thr values
        
        if values == sorted_values:
            print("Correct!") 
            self.correct_signal.emit()

class ButtonDrag(QPushButton):
    def __init__(self, text, parent):
        super(ButtonDrag, self).__init__(text, parent)
        self.parent = parent
        
        # load the fonts for button style
        self.load_fonts()

        self.setStyleSheet(f"""QPushButton {{
                                background-color: #3498db; 
                                color: white;
                                font-size: 16px;
                                font-weight: bold;
                                border: 2px solid #d0dbff;
                                border-radius: 8px;
                                padding: 8px 16px;
                                font-family: {self.font_family};
                                font-size: 30px;   
                                margin: 3px;
                                width: 200px;
                                height: 60px;    
                            }}

                            QPushButton:hover {{
                                background-color: #2980b9; 
                            }}

                            QPushButton:pressed {{
                                background-color: #1f669b;
                                border: 2px solid #1c5a87;
                            }}
                        """)
        
        self.setAcceptDrops(True) # Make the button dropable

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            drag = QDrag(self)
            mime_data = QMimeData() # QMimedata can be use for dragging functionalities
            mime_data.setText(self.text())
            drag.setMimeData(mime_data)

            # Use grab method to show grab effect
            grab = self.grab()
            drag.setPixmap(grab)
            drag.exec(Qt.DropAction.MoveAction)
    
    def dragEnterEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        dragged_txt = event.mimeData().text()
        dragged_btn = event.source()

        if dragged_btn and dragged_btn != self:
            self.parent.reorder_buttons(dragged_btn, self)
            dragged_btn.setStyleSheet(f"""QPushButton {{
                                        background-color: #2ecc71; 
                                        color: white;
                                        font-size: 16px;
                                        font-weight: bold;
                                        border: 2px solid #27ae60;
                                        border-radius: 8px;
                                        padding: 8px 16px;
                                        font-family: {self.font_family};
                                        font-size: 30px;   
                                        margin: 3px;
                                        width: 200px;
                                        height: 60px;    
                                    }}""")
        
        event.accept()

    def load_fonts(self):
        self.font_id = QFontDatabase.addApplicationFont("Z_custom_fonts/Jersey15-Regular.ttf")
        self.font_id2 = QFontDatabase.addApplicationFont("Z_custom_fonts/PixelifySans-VariableFont_wght.ttf")

        self.font_family = QFontDatabase.applicationFontFamilies(self.font_id)[0]
        self.custom_font = QFont(self.font_family)
        self.custom_font.setBold(True)

        self.font_family2 = QFontDatabase.applicationFontFamilies(self.font_id2)[0]
        self.custom_font2 = QFont(self.font_family2)
        self.custom_font2.setBold(False)

def main():
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    window = ArrangeNum()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()