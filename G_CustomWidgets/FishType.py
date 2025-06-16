from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import sys
from time import sleep as delay

class FishWidget(QWidget):
    def __init__(self, fish_name, fish_image, image_width, image_height, parent=None, *args, **kwargs):
        super(FishWidget, self).__init__(parent, *args, **kwargs)
        self.setFixedSize(QSize(400,400))

        self.fish_name = fish_name
        self.fish_image = fish_image
        self.img_width = image_width
        self.img_height = image_height

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("background-color: #4b00a7; margin: 10px;")

        # main layout
        self.layout1 = QVBoxLayout()
        self.setLayout(self.layout1)

        # call the methods
        self.load_fonts()
        self.style_components()

    def style_components(self):
        self.fish_imageLab = QLabel()
        self.fish_imageLab.setFixedSize(QSize(self.img_width, self.img_height))
        self.fish_imageLab.setScaledContents(True)

        self.fish_pixmap = QPixmap(self.fish_image)
        self.fish_imageLab.setPixmap(self.fish_pixmap)
        self.fish_imageLab.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)
        self.layout1.addWidget(self.fish_imageLab)

        #### FISH TXT
        self.fish_text = QLabel(self.fish_name)
        self.fish_text.setStyleSheet(f"""QLabel{{
                                     background-color: #e229ff;
                                     color: white;
                                     font-family: {self.font_family};
                                     font-size: 50px;
                                     border-radius: 10px;
                                }}""")
        self.fish_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.layout1.addWidget(self.fish_text)

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
    
    window = FishWidget(fish_name="Cat Fish", fish_image=r"H_images\Fish_infoImg\catfish.png", image_width=320, image_height=270)
    window.show()
    app.exec()

if __name__ == "__main__":
    main()