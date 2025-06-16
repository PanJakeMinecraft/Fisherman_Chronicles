import sys
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from functools import partial
import cv2
import numpy as np

COLORS = ["white", "black", "#5ec623", "#f5d00e", "#0e51f5", "#ada5f9", "#00aefe", "#498600", "#025900", "#b91800", "#9000bb", "#fb6700", "#fb00e1", "#fcb9f5"]

class Canvas(QLabel):
    def __init__(self):
        super().__init__()
        self.pen_color = QColor("black")  # Default color
        self.pen_width = 5  # Default pen width
        canvas = QPixmap(1000, 700)  
        canvas.fill(Qt.GlobalColor.white)
        self.setPixmap(canvas)
        self.last_x, self.last_y = None, None

    def init_canvas(self):
        canvas = QPixmap(1000, 700)
        canvas.fill(Qt.GlobalColor.white)
        self.setPixmap(canvas)

    # Set the pen color
    def set_pen_color(self, color):
        self.pen_color = QColor(color)
    
    # create the eraser 
    def set_eraser(self):
        canvas = QPixmap(1000, 700)  
        canvas.fill(Qt.GlobalColor.white)
        self.setPixmap(canvas)

    def mouseMoveEvent(self, e):
        if self.last_x is None:  # Start drawing when mouse is moved
            self.last_x = int(e.position().x())
            self.last_y = int(e.position().y())
            return
        
        canvas = self.pixmap()
        painter = QPainter(canvas)
        pen = QPen(self.pen_color, self.pen_width)  # Use current pen color and width
        painter.setPen(pen)
        painter.drawLine(self.last_x, self.last_y, int(e.position().x()), int(e.position().y()))
        painter.end()
        self.setPixmap(canvas)

        # Update the last position
        self.last_x = int(e.position().x())
        self.last_y = int(e.position().y())

    def mouseReleaseEvent(self, e):
        self.last_x = None
        self.last_y = None

    ############ Check whether player meet the requirement quest?
    
    def get_image(self):
        return self.pixmap().toImage()
    
    def display_success(self):
        canvas = self.pixmap()
        painter = QPainter(canvas)
        painter.setFont(QFont("Tahoma", 40, QFont.Weight.Bold))
        painter.setPen(QColor("Green"))
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "Success")
        painter.end()
        self.setPixmap(canvas)  
        self.update() 

    def try_again(self):
        canvas = self.pixmap()
        painter = QPainter(canvas)
        painter.setFont(QFont("Tahoma", 40, QFont.Weight.Bold))
        painter.setPen(QColor("Red"))
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "Try again")
        painter.end()
        self.setPixmap(canvas)  
        self.update() 

class QPaletteButton(QPushButton):
    def __init__(self, color):
        super().__init__()
        self.setFixedSize(40, 40)
        self.setStyleSheet(f"background-color: {color};")
        self.color = color

class Main(QWidget):
    success_signal = pyqtSignal()
    def __init__(self, parent = None):
        super(Main, self).__init__(parent)
        self.setWindowTitle("Drawing Application")

        self.setStyleSheet("background-color: white;")

        # call the canvas class
        self.canvas = Canvas()
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)  

        bottom_layout = QHBoxLayout()
        self.add_palette_buttons(bottom_layout)

        # Add Eraser Button
        eraser_button = QPushButton("Clear")
        eraser_button.setFixedSize(QSize(100, 50))
        eraser_button.setStyleSheet(
                                    """
                                    font-family: Tahoma;
                                    font-weight: bold;
                                    font-size: 16px;
                                    """
        )
        eraser_button.clicked.connect(self.canvas.set_eraser)
        bottom_layout.addWidget(eraser_button)

        submit_button = QPushButton("Submit")
        submit_button.setFixedSize(QSize(100,50))
        submit_button.setStyleSheet("""QPushButton{
                                    background-color: #ffc356;
                                    font-family: Tahoma;
                                    font-weight: bold;
                                    font-size: 16px;
                                    }""")
        bottom_layout.addWidget(submit_button)
        submit_button.clicked.connect(lambda: self.submit_answer())

        layout.addLayout(bottom_layout) 
        self.setLayout(layout)

    def add_palette_buttons(self, layout):
        for c in COLORS:
            b = QPushButton()
            b.setFixedSize(40, 40)
            b.setStyleSheet(f"background-color: {c};")
            b.clicked.connect(partial(self.canvas.set_pen_color, c))
            layout.addWidget(b)

    def submit_answer(self):
        if self.is_rectangle(): # WHEN IT IS RECTANGLE (IF PLAYER DRAW RECTANGLE)
            print("Success")
            self.canvas.display_success()
            QTimer.singleShot(1400, self.emit_signal)
        else:
            print("Not success, not rectangle")
            self.canvas.try_again()

    def emit_signal(self):
        self.success_signal.emit()
   
    ##### Check whether player draws a rectangle
    def is_rectangle(self): # This function, I have idea from the chatgpt (but I modify it into my function)
        """
        This function will check whether the player draw rectangle or not
        If player draw rectangle it will return True

        SPECIFICALLY
        - It will access the image from the canvas using get_image()
        - Get the raw pixel data using .bit().asarray() from the image
        - Convert the byte into numpy array using np.frombuffer() and reshape it                      
        - convert to grayscale
        - Use canny edge detection method to detect the edges
        - Find the image contours using cv2.findCountour() 
        - cv2.RETR_EXTERNAL: Only retrieves the external contours (outermost shapes).
        - cv2.CHAIN_APPROX_SIMPLE: Approximates the contours to save memory by removing 
        redundant points (especially for rectangular shapes).

        - approximate the countour where 0.02 * cv2.arcLength(contour, True)
        will be the accuracy detection
        - Check wiether the approximation have 4 edges

        """
        image = self.canvas.get_image() 
        buffer = image.bits().asarray(image.width() * image.height() * 4)
        img_array = np.frombuffer(buffer, dtype=np.uint8).reshape((image.height(), image.width(), 4))
        grayscale = cv2.cvtColor(img_array, cv2.COLOR_BGRA2GRAY)
        edges = cv2.Canny(grayscale, 50, 100)
        
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 0.08 * cv2.arcLength(contour, True), True)
            if len(approx) == 4:
                return True  
        return False

def main():
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    window = Main()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()