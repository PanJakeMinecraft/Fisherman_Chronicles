from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
import sys
from time import sleep as delay
from G_CustomWidgets.FishType import FishWidget
from G_CustomWidgets.DataVis import DataVisualization
import csv

class Color(QWidget):
    def __init__(self, color_name):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color_name))
        self.setPalette(palette)

class FishInformation(QMainWindow):
    def __init__(self, parent=None, plr_data=None, **kwargs):
        super(FishInformation, self).__init__(parent, **kwargs)
        self.setWindowTitle("Fisherman Chronicles")
        self.showFullScreen()
        self.plr_data = plr_data
        
        # maxiumum colum per row
        self.max_cols = 3

        # previous state from DSA
        self.undo_stack = QUndoStack()

        # ALL FISH list
        self.all_fish = {
            "Cat Fish": (r"H_images\Fish_infoImg\catfish.png", 350, 220),
            "Tilapia": (r"H_images\Fish_infoImg\tilapia.png", 320, 220),
            "Koi": (r"H_images\Fish_infoImg\koi.png", 270, 220),
            "Snakehead Fish": (r"H_images\Fish_infoImg\snakeheadFish.png", 270, 220),
            "Salmon": (r"H_images\Fish_infoImg\salmon.png", 350, 220),
            "Eel": (r"H_images\Fish_infoImg\eel.png", 350, 220),
            "Electic Eel": (r"H_images\Fish_infoImg\electric_eel.png", 350, 220),
            "Angler Fish": (r"H_images\Fish_infoImg\angler_fish.png", 350, 220),
        }

        # the central widget and the main layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        
        self.main_layout = QHBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        self.central_widget.setStyleSheet("background-color: #1c0040")

        # stacked widget
        self.stack_widget = QStackedWidget(self.central_widget)
        self.stack_widget.setFixedSize(QSize(self.width(), self.height()))

        ####### MENUBAR STYLE
        self.setStyleSheet(""" 
        QMenuBar {
            background-color: #007ACC;
            color: white;
            font-size: 14px;
            font-family: Tahoma;
            padding: 10px;
            font-weight: bold;
        }
        QMenuBar::item {
            background: transparent;
            padding: 5px 15px;
            margin: 2px;
        }
        QMenuBar::item:selected {  /* Hover effect */
            background: #00045d;
        }
        QMenu {
            background-color: #222;
            color: white;
            border: 1px solid #555;
        }
        QMenu::item {
            padding: 5px 20px;
            background-color: #555;
            font-family: Tahoma;
            font-size: 12px;
            padding: 15px;
        }
        QMenu::item:selected {
            background-color: #000000;
        }""")

        # call the methods
        self.load_fonts()
        self.create_menus()
        self.contextMenu_create()
        self.create_layouts()
        self.create_widgets()
        self.add_fish()
    

    #### MENUBAR
    def create_menus(self):
        self.menu_bar = self.menuBar()
        self.menu_bar.setNativeMenuBar(False)

        # add the menus
        self.file_menu = self.menu_bar.addMenu("File")
        self.edit_menu = self.menu_bar.addMenu("Edit")
        self.color_theme = self.menu_bar.addMenu("Color Themes")

        # file menus
        self.fileName_ls = []
        file_ls = ["New", "Open", "Screenshot"]
        for i in range(len(file_ls)):
            self.file_action = QAction(file_ls[i], self)
            self.file_menu.addAction(self.file_action)
            self.fileName_ls.append(self.file_action)
            self.file_action.triggered.connect(lambda event, file_menu=file_ls[i]: self.FileMenu_method(file_menu))       

        # Edit
        self.EditName_ls = []
        edit_ls = ["Undo", "Reset"]
        for i in range(len(edit_ls)):
            self.edit_action = QAction(edit_ls[i], self)
            self.edit_menu.addAction(self.edit_action)
            self.EditName_ls.append(self.edit_action)
            self.edit_action.triggered.connect(lambda event, edit=edit_ls[i]: self.editingMenu(edit))
        
        # color theme
        self.ThemeName_ls = []
        theme_ls = ["Dark theme", "Light Theme"]
        for i in range(len(theme_ls)):
            self.color_action = QAction(theme_ls[i], self)
            self.color_theme.addAction(self.color_action)
            self.ThemeName_ls.append(self.color_action)

    def load_fonts(self):
        self.font_id = QFontDatabase.addApplicationFont("Z_custom_fonts/Jersey15-Regular.ttf")
        self.font_id2 = QFontDatabase.addApplicationFont("Z_custom_fonts/PixelifySans-VariableFont_wght.ttf")

        self.font_family = QFontDatabase.applicationFontFamilies(self.font_id)[0]
        self.custom_font = QFont(self.font_family)
        self.custom_font.setBold(True)

        self.font_family2 = QFontDatabase.applicationFontFamilies(self.font_id2)[0]
        self.custom_font2 = QFont(self.font_family2)
        self.custom_font2.setBold(False)

    ##### CONTEXT MENU
    def contextMenu_create(self):
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContext_menu)

    def showContext_menu(self, event):
        self.context_menu = QMenu(self)

        if self.fileName_ls:
            self.filecontextmenu = self.context_menu.addMenu("File")
            for i in range(len(self.fileName_ls)):
                self.file_context_action = self.filecontextmenu.addAction(self.fileName_ls[i])
        
        if self.EditName_ls:
            self.editcontextMenu = self.context_menu.addMenu("Edit")
            for j in range(len(self.EditName_ls)):
                self.edit_context_action = self.editcontextMenu.addAction(self.EditName_ls[j])

        if self.ThemeName_ls:
            self.themecontextmenu = self.context_menu.addMenu("Color Theme")
            for k in range(len(self.ThemeName_ls)):
                self.theme_context_action = self.themecontextmenu.addAction(self.ThemeName_ls[k])
        
        # get the mouse pos
        action = self.context_menu.exec(self.mapToGlobal(event))

    def create_layouts(self):
        """
        Creating the layouts and put it into the main layout. However, each layout
        will contains it own individual QWidget() and each widget will have a fixed size
        """
        self.nav_widget = QWidget()
        self.nav_widget.setStyleSheet("background-color: #290054; padding: 0px;")
        self.nav_layout = QVBoxLayout(self.nav_widget)
        self.nav_widget.setFixedWidth(400)
        self.nav_widget.setLayout(self.nav_layout)
        self.main_layout.addWidget(self.nav_widget)

        self.group_information = QVBoxLayout()

        self.search_res_widget = QWidget()
        self.search_res_widget.setStyleSheet("background-color: #5d006e")
        self.res_layout = QVBoxLayout()
        self.search_res_widget.setFixedHeight(100)
        self.search_res_widget.setLayout(self.res_layout)
        self.group_information.addWidget(self.search_res_widget)

        self.scrollbar = QScrollArea()
        self.scrollbar.setStyleSheet("")
        self.scrollbar.setWidgetResizable(True)  
        
        self.info_widget = QWidget()
        # The scrollbar styling
        self.scrollbar.setStyleSheet("""
                            QScrollBar:vertical {
                                border: none;
                                background: #2b2b2b; 
                                width: 15px; 
                                margin: 5px 0 5px 0;
                            }
                            
                            QScrollBar::handle:vertical {
                                background: #6A5ACD; 
                                min-height: 30px;
                                border-radius: 5px;
                            }
                            
                            QScrollBar::handle:vertical:hover {
                                background: #836FFF;  
                            }

                            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                                background: none;
                                height: 0px;
                            }

                            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                                background: none;
                            }

                            QScrollBar:horizontal {
                                border: none;
                                background: #2b2b2b;
                                height: 10px;
                                margin: 0px 5px 0px 5px;
                                border-radius: 5px;
                            }
                            
                            QScrollBar::handle:horizontal {
                                background: #6A5ACD;
                                min-width: 30px;
                                border-radius: 5px;
                            }
                            
                            QScrollBar::handle:horizontal:hover {
                                background: #836FFF;
                            }

                            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                                background: none;
                                width: 0px;
                            }

                            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                                background: none;
                            }
                        """)
        self.info_layout = QGridLayout(self.info_widget)
        self.info_layout.setContentsMargins(15, 15, 15, 15)
        self.info_layout.setHorizontalSpacing(10)

        self.scrollbar.setWidget(self.info_widget)
        self.group_information.addWidget(self.scrollbar) 
        self.main_layout.addLayout(self.group_information)

    ################ CREATE THE WIDGETS
    def create_widgets(self):
        """
        This class will create the basic widgets which will have within 
        this page. All widget and some styling will be here will be here
        """
        
        self.searchWidget = QWidget()
        self.searchWidget.setStyleSheet("background-color: #290054")
        self.searchWidget.setFixedHeight(60)
        self.search_barLayout = QHBoxLayout(self.searchWidget)
        self.search_barLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.search_lab = QLabel("SEARCH: ")
        self.search_lab.setStyleSheet(f"""QLabel{{
                                      color: white;
                                      font-family: {self.font_family};
                                      font-size: 30px;
                                      margin-top: 20px;
                                    }}""")
        
        self.search_lab.setObjectName("searchbar")
        self.search_line = QLineEdit()
        self.search_line.setFixedSize(QSize(260,50))
        self.search_line.setAlignment(Qt.AlignmentFlag.AlignJustify)
        self.search_line.setStyleSheet(f"""QLineEdit{{
                                       font-family: {self.font_family};
                                       color: white;
                                       background-color: #040078;
                                       border: 1px solid white;
                                       font-size: 25px; 
                                       margin-top: 10px;
                                       margin-top: 20px;
                                    }}
                                    
                                    QLineEdit:focus{{
                                    border: 2px solid white;
                                    background-color: #0d0044;
                                    }}""")
        ##### Signal for search line
        self.search_line.returnPressed.connect(lambda: self.show_result()) 

        self.search_barLayout.addWidget(self.search_lab)
        self.search_barLayout.addWidget(self.search_line)
        self.nav_layout.addWidget(self.searchWidget, alignment= Qt.AlignmentFlag.AlignTop)
    
        self.stat_calc = QPushButton("Stat Calculation")
        self.stat_calc.setIcon(QIcon(r"H_images\Edu_image\stat_calc.png"))
        self.stat_calc.setIconSize(QSize(60,60))
        self.stat_calc.setFixedWidth(400)
        self.nav_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.stat_calc.setStyleSheet(f"""QPushButton{{
                                     font-family: {self.font_family};
                                     font-size: 30px;
                                     color: white;
                                     background-color: #f99e21;
                                     height: 150px;
                                     margin-top: 25px;
                                     border: 3px solid white;
                                }}

                                QPushButton:hover{{
                                background-color: orange;
                                }}""")
        self.nav_layout.addWidget(self.stat_calc, alignment=Qt.AlignmentFlag.AlignLeft)
        self.stat_calc.clicked.connect(lambda: self.showStat_window())

        self.favorite = QPushButton("Favorite")
        self.favorite.setIcon(QIcon(r"H_images\Edu_image\star.png"))
        self.favorite.setIconSize(QSize(60,60))
        self.favorite.setFixedWidth(400)
        self.favorite.setStyleSheet(f"""QPushButton{{
                                     font-family: {self.font_family};
                                     font-size: 30px;
                                     color: white;
                                     background-color: #f99e21;
                                     height: 150px;
                                     border: 3px solid white;
                                }}""")
        self.nav_layout.addWidget(self.favorite, alignment=Qt.AlignmentFlag.AlignLeft)
        
        self.alphabetical_order = QPushButton("A-Z")
        self.alphabetical_order.setIcon(QIcon(r"H_images\Edu_image\alphabet.png"))
        self.alphabetical_order.setIconSize(QSize(60,60))
        self.alphabetical_order.setFixedWidth(400)
        self.alphabetical_order.setStyleSheet(f"""QPushButton{{
                                     font-family: {self.font_family};
                                     font-size: 30px;
                                     color: white;
                                     background-color: #f99e21;
                                     height: 150px;
                                     border: 3px solid white;
                                }}""")
        self.nav_layout.addWidget(self.alphabetical_order, alignment=Qt.AlignmentFlag.AlignLeft)
        self.alphabetical_order.clicked.connect(lambda: self.sort_fish())

        self.back_btn = QPushButton("BACK")
        self.back_btn.setFixedWidth(400)
        self.back_btn.setStyleSheet(f"""QPushButton{{
                                     font-family: {self.font_family};
                                     font-size: 40px;
                                     color: white;
                                     background-color: #a10f01;
                                     height: 150px;
                                     border: 3px solid white;
                                }}""")
        self.nav_layout.addWidget(self.back_btn, alignment=Qt.AlignmentFlag.AlignBottom)
        self.back_btn.clicked.connect(lambda: self.go_back())

        self.nav_layout.setContentsMargins(0, 0, 0, 0)

        # Add the widget to result layout (empty QLabel)
        self.result_emp = QLabel("Search Results: ")
        self.result_emp.setStyleSheet(f"""QLabel{{
                                      background-color: #5d006e;
                                      color: white;
                                      font-family: {self.font_family};
                                      font-size: 30px;
                                      font-weight: bold;
                                    }}""")
        self.res_layout.addWidget(self.result_emp)
    
    ############### SHOW STAT CALCULATE WINDOW
    def showStat_window(self):
        # clear the window
        self.clearWidget()
        self.stat_window = DataVisualization(self.info_widget)
        self.stat_window.show()
    

    ##### BACK TO PREVIOUS PAGE
    def go_back(self):
        from C_EducationMode.choose_education import EducationChoose
            
        if hasattr(self, 'context_menu') and self.context_menu.isVisible():
            self.context_menu.close()
            
        if not hasattr(self, "edu"):
            self.edu = EducationChoose(plr_data= self.plr_data)
        
        self.menu_bar.hide()
        self.stack_widget.addWidget(self.edu)
        self.stack_widget.setCurrentWidget(self.edu)
        self.edu.show()
        self.central_widget.hide()
        self.setCentralWidget(self.stack_widget)

    ########################### MENUBAR FUNCTIONS
    # reset menu
    def editingMenu(self, edit):
        print(edit)
        if edit == "Reset":
            self.search_line.clear()
            self.result_emp.setText("Search Results: ")
            self.clearWidget()
            self.add_fish()

            if hasattr(self, "stat_window"):
                self.stat_window.deleteLater()

        elif edit == "Undo":
            self.undo_stack.undo()

    def FileMenu_method(self, file_menu):
        file_menu = file_menu.lower()
        print(file_menu)
        
        if file_menu == "open":
            msg = QMessageBox.question(self, "open file", "Are you sure you want\nto open your file",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
            if msg == QMessageBox.StandardButton.Yes:
                path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*);;Text Files (*.txt);;Image Files (*.png *.jpg *.bmp)")
                if path:
                    print("File opening")
                else:
                    print("cannot find path, cannot open")
            else:
                print("Not opening the file")
        
        elif file_menu == "screenshot":
            screen = QApplication.primaryScreen()
            screenshot = screen.grabWindow(0)
            
            screenshot_file = "/tmp/screenshot.png" 
            screenshot.save(screenshot_file, "PNG")
            
            self.screenshot_window = ScreenShotWindow(screenshot_file)
            self.screenshot_window.show()
            
        elif file_menu == "new":
            self.text_edit = TextEditWindow()
            self.text_edit.show()
    

    ######################### ADD FISH TO WIDGET (THIs IS THE DEFAULT, NOT SEACH YET)
    def add_fish(self):
        self.info_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        from G_CustomWidgets.FishType import FishWidget
        
        # FISH WIDGETS
        self.catfish = FishWidget(fish_name="Cat Fish", fish_image=r"H_images\Fish_infoImg\catfish.png", image_width=350, image_height=220)
        self.tilapia = FishWidget(fish_name="Tilapia", fish_image=r"H_images\Fish_infoImg\tilapia.png", image_width=320, image_height=220)
        self.koi = FishWidget(fish_name="Koi", fish_image=r"H_images\Fish_infoImg\koi.png", image_width=270, image_height=220)
        self.snake_head_fish = FishWidget(fish_name="Snakehead Fish", fish_image=r"H_images\Fish_infoImg\snakeheadFish.png", image_width=270, image_height=220)
        self.salmon = FishWidget(fish_name="Salmon", fish_image=r"H_images\Fish_infoImg\salmon.png", image_width=350, image_height=220)
        self.eel = FishWidget(fish_name="Eel", fish_image=r"H_images\Fish_infoImg\eel.png", image_width=350, image_height=220)
        self.electric_eel = FishWidget(fish_name="Electric Eel", fish_image=r"H_images\Fish_infoImg\electric_eel.png", image_width=350, image_height=220)
        self.anglerfish = FishWidget(fish_name="Angler Fish", fish_image=r"H_images\Fish_infoImg\angler_fish.png", image_width=350, image_height=220)

        # add FISH into layout
        self.info_layout.addWidget(self.catfish, 0, 0)
        self.info_layout.addWidget(self.tilapia, 0, 1)
        self.info_layout.addWidget(self.koi, 0, 2)
        self.info_layout.addWidget(self.snake_head_fish, 1,0)
        self.info_layout.addWidget(self.salmon, 1, 1)
        self.info_layout.addWidget(self.eel, 1, 2)
        self.info_layout.addWidget(self.electric_eel, 2, 0)
        self.info_layout.addWidget(self.anglerfish, 2, 1)


    def show_result(self): ############# SEARCH FISH
        self.searchShow = self.search_line.text()
        self.searching = self.search_line.text().lower().strip()
        self.result_emp.setText("Search Results: " + self.searchShow)
        
        # clear widget every time when search
        self.clearWidget()
    
        if self.searching == "":
            self.add_fish()  

        else: ### For this method, I ask chat gpt for the idea and finally, I implemented into my method
            filtered = {}
            for fish_name, (fish_image, image_width, image_height) in self.all_fish.items():
                if self.searching in fish_name.lower():
                    filtered[fish_name] = (fish_image, image_width, image_height)
            
            for i, (fish_name, (fish_image, image_width, image_height)) in enumerate(filtered.items()):
                row = i // self.max_cols
                col = i % self.max_cols

                fish_widget = FishWidget(fish_name=fish_name, fish_image=fish_image, image_width=image_width, image_height=image_height)
                self.info_layout.addWidget(fish_widget, row, col)

    ###### SORT FISH BY alphetically
    def sort_fish(self):
        sorting_fish = dict(self.all_fish)

        if hasattr(self, "stat_window"):
            self.stat_window.deleteLater()

        self.clearWidget()

        for i, (fish_name, (fish_image, image_width, image_height)) in enumerate(sorted(sorting_fish.items())):
            row = i // self.max_cols
            col = i % self.max_cols
            
            fish_widget = FishWidget(fish_name=fish_name, fish_image=fish_image, image_width=image_width, image_height=image_height)
            self.info_layout.addWidget(fish_widget, row, col)

    #### CLEAR THE FISH WIDGETS
    # This method prevent the shifting, clear from bottom to top
    def clearWidget(self):
        for i in reversed(range(self.info_layout.count())):
            widget = self.info_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()


############### SCreen shot window
class ScreenShotWindow(QMainWindow):
    def __init__(self, screenshot, *args, **kwargs):
        super(ScreenShotWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("Screenshot")
        
        self.label = QLabel(self)
        self.pixmap = QPixmap(screenshot)
        self.label.setPixmap(self.pixmap)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setScaledContents(True)
        
        layout = QVBoxLayout()
        layout.addWidget(self.label)
    
        self.widget = QWidget()
        self.widget.setLayout(layout)
        self.setCentralWidget(self.widget)
    
        width = 500  
        height = 350  
        self.resize(width, height)
        self.setFixedSize(width, height)

    def contextMenuEvent(self, event): # built in context menu function
        self.context = QMenu(self)
        self.save_action = QAction("Save", self)
        self.save_action.triggered.connect(self.save_screenshot)
        self.context.addAction(self.save_action)

        self.context.exec(event.globalPos())

    def save_screenshot(self):
        folder = QFileDialog.getExistingDirectory(self, "select save folder")
        if folder:
            path = f"{folder}/screenshot.png"

            if self.pixmap.save(path, "PNG"): # save it as PNG
                QMessageBox.information(self, "saved", "Screenshot save")
            else:
                QMessageBox.critical(self, "ERROR", "ERORR:\nScreen shot cannot save")

##### TEXT EDIT WINDOW
class TextEditWindow(QWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super(TextEditWindow, self).__init__(parent, *args, **kwargs)
        self.setWindowTitle("TextEdit window")
        self.setStyleSheet("""QWidget{background-color: #1c006f; color: white;}""")
        self.load_fonts()

        layout = QVBoxLayout()

        self.text =  QTextEdit(self)
        self.text.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.text.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self.text.setStyleSheet(f"""
            QTextEdit {{
                background-color: #1e1e2f; 
                color: #e6e6e6; 
                border: 2px solid #6A5ACD; 
                border-radius: 10px; 
                padding: 10px;
                font-size: 30px;
                font-family: {self.font_family};
            }}

            QTextEdit:hover {{
                border: 2px solid #836FFF;
            }}

            QTextEdit QScrollBar:vertical {{
                border: none;
                background: white;
                width: 10px;
                margin: 5px 5px 5px 5px;
            }}

            QTextEdit QScrollBar::handle:vertical {{
                background: #eda8ff;
                min-height: 30px;
                border-radius: 5px;
            }}

            QTextEdit QScrollBar::handle:vertical:hover {{
                background: #e16eff;
            }}

            QTextEdit QScrollBar::add-line:vertical, QTextEdit QScrollBar::sub-line:vertical {{
                background: none;
                border: none;
            }}
        """)
        layout.addWidget(self.text)

        self.submit_button = QPushButton("Submit")
        self.submit_button.setStyleSheet(f"""QPushButton{{
                                         background-color: #faad07;
                                         color: white;
                                         border: 1px solid white;
                                         font-family: {self.font_family};
                                         font-size: 32px;
                                        }}

                                        QPushButton:hover{{
                                        background-color: #d49100;
                                        }}""")
        
        layout.addWidget(self.submit_button)
        self.submit_button.clicked.connect(lambda: self.text_conversion())

        self.returnbutton = QPushButton("CLOSE")
        self.returnbutton.setStyleSheet(f"""QPushButton{{
                                         background-color: #ab1c00;
                                         color: white;
                                         border: 1px solid white;
                                         font-family: {self.font_family};
                                         font-size: 32px;
                                        }}

                                        QPushButton:hover{{
                                        background-color: #d49100;
                                        }}""")
        
        layout.addWidget(self.returnbutton)
        self.returnbutton.clicked.connect(lambda: self.close())

        self.setLayout(layout)
        self.setFixedSize(QSize(400,300))

    def text_conversion(self): # save to txt filr
        print(self.text.toPlainText())
        
        texting = self.text.toPlainText()
        if not texting.strip():
            QMessageBox.information(self, "EMPTY text", "Text cannot be empty")
            return
        
        folder = QFileDialog.getExistingDirectory(self, "Select Folder to Save")
        if folder:
            patth = f"{folder}\save_text.txt"
            with open(patth, "w") as file:
                file.write(texting)
            
            print("The file is saved")
            self.close()

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
    
    window = FishInformation()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()