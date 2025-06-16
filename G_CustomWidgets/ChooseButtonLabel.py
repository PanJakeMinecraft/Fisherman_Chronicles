from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from sys import argv

class ChooseButton(QWidget):
    def __init__(self, txt, icon_path=None, parent=None):
        super(ChooseButton, self).__init__(parent) 
        self.setObjectName(txt.lower().replace(" ", "_"))
        self.txt = txt
        self.icon_path = icon_path
        
        # Load custom fonts
        self.font_id = QFontDatabase.addApplicationFont("Z_custom_fonts/Jersey15-Regular.ttf")
        self.font_id2 = QFontDatabase.addApplicationFont("Z_custom_fonts/PixelifySans-VariableFont_wght.ttf")

        self.font_family = QFontDatabase.applicationFontFamilies(self.font_id)[0]
        self.custom_font = QFont(self.font_family)
        self.custom_font.setBold(True)

        self.font_family2 = QFontDatabase.applicationFontFamilies(self.font_id2)[0]
        self.custom_font2 = QFont(self.font_family2)
        self.custom_font2.setBold(False)

        self.btn = QPushButton(self)
        self.btn.setObjectName("btn") 
        self.add_shadow(self.btn)

        if self.icon_path:
            self.btn.setIcon(QIcon(self.icon_path))
            self.btn.setIconSize(QSize(300,400)) 

        self.label = QLabel(self.txt, self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        self.label.setFixedSize(QSize(380,80))

        self.layouts_ = QVBoxLayout(self)
        self.layouts_.addWidget(self.btn)
        self.setLayout(self.layouts_)

        self.subLayout = QHBoxLayout()
        self.subLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subLayout.addWidget(self.label)
        self.layouts_.addLayout(self.subLayout)

        self.setStyleSheet(f"""
            QPushButton#btn {{
                background-color: #092664;
                font-family: {self.font_family2};
                font-size: 30px;
                color: white;
                margin: 20px;
                width: 280px;
                height: 270px;
                padding: 20px;
                text-align: center;
                border: 7px double #d0d0d0;
                font-weight: bold;
                position: relative;
            }}

            QPushButton#btn:hover {{
                background-color: #001b49;
            }}

            QPushButton#btn:pressed {{
                background-color: #001537;
            }}

            QLabel {{
                color: white;
                font-size: 70px;
                font-family: {self.font_family};
                font-weight: bold;
                background-color: #2396ff;
                border: 3px groove black;
                text-align: center;
            }}
            
            QLabel:hover{{
                background-color: #257ccc;
            }}
        """)

    def add_shadow(self, widget):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(5) 
        shadow.setXOffset(8)  
        shadow.setYOffset(8) 
        shadow.setColor(QColor(0, 47, 144, 100)) 
        widget.setGraphicsEffect(shadow)