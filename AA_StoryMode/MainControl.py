from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from abc import ABC, abstractmethod
import sys

"""The abstract class window will be used for further implementation within the program"""
class AbstractMainWin(QMainWindow):
    def __init__(self, **kwargs):
        super(AbstractMainWin, self).__init__(**kwargs)
        self.setWindowTitle("Fisherman Chronicles")
        self.showFullScreen()

        # Load custom fonts and set the custom fonts
        self.font_id = QFontDatabase.addApplicationFont("Z_custom_fonts/Jersey15-Regular.ttf")
        self.font_id2 = QFontDatabase.addApplicationFont("Z_custom_fonts/PixelifySans-VariableFont_wght.ttf")

        self.font_family = QFontDatabase.applicationFontFamilies(self.font_id)[0]
        self.custom_font = QFont(self.font_family)
        self.custom_font.setBold(True)

        self.font_family2 = QFontDatabase.applicationFontFamilies(self.font_id2)[0]
        self.custom_font2 = QFont(self.font_family2)
        self.custom_font2.setBold(False)

        # central widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Create the stack layout
        self.stacking = QStackedWidget(self.central_widget)
        self.stacking.setFixedSize(QSize(self.width(), self.height()))

    @abstractmethod
    def add_pages(self):
        """ Adding the page to the program"""
        pass

    @abstractmethod
    def switch_pages(self, index):
        pass

class MainWindow(AbstractMainWin): # Pass the abstract class window to this class
    def __init__(self, plr_data=None, title=None, parent=None, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        self.plr_data = plr_data
        print(f"\n\n\nPLR DATA IN PROLOGUE\n{self.plr_data}")
        self.add_pages()

    def add_pages(self):
        # import inside prevent circular import
        from AA_StoryMode.Prologue import Prologue

        # page 1 (the prologue page)
        self.page1 = Prologue(plr_data= self.plr_data)
        self.stacking.addWidget(self.page1)
        self.stacking.setCurrentWidget(self.page1)
        self.page1.show()
        self.central_widget.hide()
        self.setCentralWidget(self.stacking)

    def switch_pages(self, index):
        pass

def main():
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
