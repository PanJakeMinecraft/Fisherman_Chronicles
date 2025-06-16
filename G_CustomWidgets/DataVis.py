from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from sys import argv
import os
import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib import style
from matplotlib.ticker import MaxNLocator

class DataVisualization(QWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super(DataVisualization, self).__init__(parent, *args, **kwargs)
        self.setWindowTitle("Data Visualize")
        self.setFixedSize(1270, 880)

        # make bg visiible when calling in another class
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("background-color: #230046;")

        ############# the layouts creation
        self.main_layout = QHBoxLayout(self)
        self.setLayout(self.main_layout)

        self.vbox = QVBoxLayout()

        self.super_lefttop_layout = QVBoxLayout()
        self.super_lefttop_widget = QWidget(self)
        self.super_lefttop_widget.setLayout(self.super_lefttop_layout)
        self.super_lefttop_widget.setFixedSize(QSize(250,80))
        self.super_lefttop_widget.setStyleSheet("background-color: #3c0091")
        self.vbox.addWidget(self.super_lefttop_widget, alignment= Qt.AlignmentFlag.AlignTop)
     
        self.lefttop_layout = QVBoxLayout()
        self.lefttop_widget = QWidget(self)
        self.lefttop_widget.setLayout(self.lefttop_layout)
        self.lefttop_widget.setFixedSize(QSize(250,450))
        self.lefttop_widget.setStyleSheet("background-color: #3c0091")
        self.vbox.addWidget(self.lefttop_widget, alignment= Qt.AlignmentFlag.AlignTop)
     
        self.leftbottom_layout = QFormLayout()
        self.leftbottom_widget = QWidget(self)
        self.leftbottom_widget.setLayout(self.leftbottom_layout) 
        self.leftbottom_widget.setFixedSize(QSize(250, 320))
        self.leftbottom_widget.setStyleSheet("background-color: #490091;")
        self.vbox.addWidget(self.leftbottom_widget, alignment=Qt.AlignmentFlag.AlignTop)
        
        self.main_layout.addLayout(self.vbox)

        self.leftmain_layout = QHBoxLayout()
        self.leftmain_widget = QWidget(self)
        self.leftmain_widget.setLayout(self.leftmain_layout)
        self.leftmain_widget.setFixedSize(QSize(500, 900)) 
        self.leftmain_widget.setStyleSheet("background-color: #1c0042;")
        self.main_layout.addWidget(self.leftmain_widget, alignment=Qt.AlignmentFlag.AlignCenter)

        self.rightmain_layout = QHBoxLayout()
        self.rightmain_widget = QWidget(self)
        self.rightmain_widget.setLayout(self.rightmain_layout)
        self.rightmain_widget.setFixedSize(QSize(500, 900))  
        self.rightmain_widget.setStyleSheet("background-color: #1c0042")
        self.main_layout.addWidget(self.rightmain_widget, alignment=Qt.AlignmentFlag.AlignCenter)

        # Load custom fonts
        self.load_fonts()
        self.create_widgets()

    def create_widgets(self):
        self.browse_btn = QPushButton("Browse CSV files")
        self.browse_btn.setStyleSheet(f"""QPushButton{{
                                      background-color: #00cc07;
                                      color: white;
                                      font-family: {self.font_family};
                                      font-size: 35px;
                                      border: 2px solid white;
                                      padding: 5px;    
                                    }}
                                    
                                    QPushButton:hover{{
                                    background-color: #009b06;
                                    }}""")
        self.super_lefttop_layout.addWidget(self.browse_btn)
        self.browse_btn.clicked.connect(lambda: self.browse_csv())

        self.chooseLabel = QLabel("Choose X and Y values")
        self.chooseLabel.setStyleSheet(f"""QLabel{{
                                       color: white;
                                       font-family: {self.font_family};
                                       font-size: 25px;  
                                       margin-top: 10px;
                                       margin-bottom: 10px;
        }}""")
        self.leftbottom_layout.addRow(self.chooseLabel)

        self.plot_graphbtn = QPushButton("Create Graphs")
        self.plot_graphbtn.setStyleSheet(f"""QPushButton{{
                                      background-color: #f29e04;
                                      color: white;
                                      font-family: {self.font_family};
                                      font-size: 35px;
                                      border: 2px solid white;
                                      padding: 5px;    
                                      margin-top: 10px;
                                    }}
                                    
                                    QPushButton:hover{{
                                    background-color: #dd7000;
                                    }}""")

        self.combox = QLabel("x values")
        self.comboy = QLabel("y values")
        self.combox.setStyleSheet(f"color: white; font-family: {self.font_family}; font-size: 22px; margin-bottom: 15px;")
        self.comboy.setStyleSheet(f"color: white; font-family: {self.font_family}; font-size: 22px; margin-bottom: 15px;")

        self.combo_x = QComboBox()
        self.combo_y = QComboBox()     
        self.combo_x.setStyleSheet("background-color: white;")
        self.combo_y.setStyleSheet("background-color: white;")

        self.leftbottom_layout.addRow(self.combox, self.combo_x)
        self.leftbottom_layout.addRow(self.comboy, self.combo_y)
        
        self.leftbottom_layout.addRow(self.plot_graphbtn)
        self.plot_graphbtn.clicked.connect(lambda: self.plot_click())

        # call the function
        self.load_headers()
        self.combo_x.currentIndexChanged.connect(self.update_display)
        self.combo_y.currentIndexChanged.connect(self.update_display)
    
    def plot_click(self):
        self.update_display()

    def load_fonts(self):
        self.font_id = QFontDatabase.addApplicationFont("Z_custom_fonts/Jersey15-Regular.ttf")
        self.font_id2 = QFontDatabase.addApplicationFont("Z_custom_fonts/PixelifySans-VariableFont_wght.ttf")

        self.font_family = QFontDatabase.applicationFontFamilies(self.font_id)[0]
        self.custom_font = QFont(self.font_family)
        self.custom_font.setBold(True)

        self.font_family2 = QFontDatabase.applicationFontFamilies(self.font_id2)[0]
        self.custom_font2 = QFont(self.font_family2)
        self.custom_font2.setBold(False)

###### CLEAR THE WIDGET CSV WIDGET contains
    def clear_csv(self):
        for i in range(self.lefttop_layout.count()):
            widget = self.lefttop_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater() 

##### BROWSE LOAD AND DISPLAY CSV FILES               
    def browse_csv(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)")
        
        if filename:
            self.clear_csv()
            self.load_csv(filename)
            
    def load_csv(self, filename):
        if os.path.exists(filename):
            with open(filename, newline="") as csvfile:
                reader = csv.reader(csvfile) 
                rows = list(reader)  
                
                if rows:
                    headers = rows[0] 
                    self.headers = headers 
                    self.data = rows[1:]  
        
                    self.load_headers()

                data = "\n".join([", ".join(row) for row in rows])
                self.display_csv(data) 

    
    def display_csv(self, data):
        self.cont = QWidget()
        grid_layout = QGridLayout(self.cont)
        grid_layout.setSpacing(0) 

        rows = data.split("\n")
        
        # This is for the head row (first row)
        headers = rows[0].split(",")  
        for col_index, header in enumerate(headers): # iterate through the column (header col) names
            label = QLabel(header.strip()) 
            label.setStyleSheet(f"color: white; font-family: {self.font_family}; font-size: 18px; background-color: #350097; text-align: center; padding: 5px;")
            grid_layout.addWidget(label, 0, col_index + 1)  

        for row_index, row in enumerate(rows[0:], start=1): # iterate through the row datas
            values = row.split(",")
            for col_index, value in enumerate(values):
                if (row_index + col_index) % 2 == 0:
                    cell_color = "#350097"
                else:
                    cell_color = "#26006D"
                
                # This will create label for every cell and add it in grid layout
                label = QLabel(str(value).strip()) 
                label.setStyleSheet(f"color: white; font-family: {self.font_family}; font-size: 16px; background-color: {cell_color}; text-align: center; padding: 5px;")
                grid_layout.addWidget(label, row_index, col_index + 1) 
        
        self.scrollbar = QScrollArea()
        self.scrollbar.setWidget(self.cont)
        self.scrollbar.setWidgetResizable(True) 
        
        self.scrollbar.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scrollbar.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.lefttop_layout.addWidget(self.scrollbar)
        self.scrollbar.setFixedSize(250, 450)

        self.scrollbar.setStyleSheet("""
            QScrollBar:vertical {
                background: #42005e;
                width: 20px;
                border-radius: 6px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar:horizontal {
                background: #3c0061;
                height: 12px;
                width: 20px;
                border-radius: 6px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: #cc00cc;
                border-radius: 6px;
                width: 20px;
            }
            QScrollBar::handle:horizontal {
                background: #cc00cc;
                width: 20px;
                border-radius: 6px;
            }
        """)

######## LOAD CSV FILE HEADER
    """
    These functions contains the load header, update header and select dispay
    This will work with the combobox. When select the following item. It will show
    the selected item on the QWidget, the top left widget
    """
    def clear_display(self):
        for i in range(self.lefttop_layout.count()):
            widget = self.lefttop_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

    def load_headers(self):
        if hasattr(self, "headers"):
            self.combo_x.clear()
            self.combo_y.clear()
            self.combo_x.addItems(self.headers)
            self.combo_y.addItems(self.headers)

            self.combo_x.setCurrentIndex(-1)
            self.combo_y.setCurrentIndex(-1)

            self.combo_x.currentIndexChanged.connect(self.update_display)
            self.combo_y.currentIndexChanged.connect(self.update_display)
   
    def select_display(self, x_column, y_column):
        self.clear_display()

        self.x_col = self.combo_x.currentText()
        self.y_col = self.combo_y.currentText()

        # Combine the X and Y columns into a display format
        dataCombine = ""
        for x, y in zip(x_column, y_column):
            dataCombine += f"{x}\t{y}\n"

        text = f"{self.x_col}\t{self.y_col}:\n{dataCombine}"

        self.data_label = QLabel(text)
        self.data_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.data_label.setStyleSheet(f"color: white; font-family: {self.font_family}; font-size: 18px;")
        self.lefttop_layout.addWidget(self.data_label, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

    def update_display(self):
        x_idx = self.combo_x.currentIndex()
        y_idx = self.combo_y.currentIndex()

        if x_idx != -1 and y_idx != -1:
            x = [row[x_idx] for row in self.data]
            y = [row[y_idx] for row in self.data]

            self.clear_plot(self.leftmain_layout)
            self.clear_plot(self.rightmain_layout)

            self.select_display(x, y)
            
            x_col = self.combo_x.currentText()
            y_col = self.combo_y.currentText()

            self.plot_bar(x, y, x_col, y_col)
            self.plot_scatter(x, y, x_col, y_col)
        else:
            self.clear_display()

    def plot_bar(self, x_column, y_column, x_col, y_col):
        figure = plt.figure(figsize=(5, 3))
        ax = figure.add_subplot(111)

        ax.bar(x_column, y_column, color="teal", edgecolor="black", linewidth=1.5)
        ax.set_title(f"Bar Graph of {x_col} & {y_col}", fontsize=14, fontweight='bold', color='darkviolet')
        ax.set_xlabel(x_col, fontsize=12, fontweight="bold", color="indigo")
        ax.set_ylabel(y_col, fontsize=12, fontweight="bold", color="indigo")
        ax.tick_params(axis="both", which="major", labelsize=10, direction='in', length=6, width=1.2)

        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        self.add_graph(figure, self.leftmain_layout)

    def plot_scatter(self, x_column, y_column, x_col, y_col):
        figure = plt.figure(figsize=(5, 3))
        ax = figure.add_subplot(111)

        ax.scatter(x_column, y_column, color="orangered", s=50, edgecolor="black", alpha=0.7)
        ax.set_title(f"Scatter Plot of {x_col} & {y_col}", fontsize=14, fontweight='bold', color='darkviolet')
        ax.set_xlabel(x_col, fontsize=12, fontweight="bold", color="indigo")
        ax.set_ylabel(y_col, fontsize=12, fontweight="bold", color="indigo")

        ax.tick_params(axis="both", which="major", labelsize=10, direction="in", length=6, width=1.2)
        self.add_graph(figure, self.rightmain_layout)

    def add_graph(self, figure, layout):
        self.canvas = FigureCanvas(figure)
        layout.addWidget(self.canvas)
        self.canvas.draw()

    def clear_plot(self, layout):
        for i in range(layout.count()):
            widget = layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

if __name__ == "__main__":
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication(argv)
    
    window = DataVisualization()
    window.show()
    app.exec()