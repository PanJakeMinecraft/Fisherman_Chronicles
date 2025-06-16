from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import sys
import locale
import json
from A_Title.login import PlayerData
import os 
import matplotlib.pyplot as plt
import numpy as np

# Change the progressbar number to arabic number
QLocale.setDefault(QLocale(QLocale.English, QLocale.UnitedStates))

class Color(QWidget):
    def __init__(self, color_name):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color_name))
        self.setPalette(palette)

class QuizUI(QWidget):
    def __init__(self, plr_data=None):
        super().__init__()
        self.init_ui()
        self.answers = ["Shark", [False,True,True,False], True, "ichthyology", "puffer", True, "fishing", "coelacanth", "Vertebrates", "Cartilage"]
        self.correctAns = []
        self.incorrectAns = []
        self.quizNo = 1

        self.plr = plr_data
        print(f"\n\nPLR DATA IN QUIZ: {self.plr}")

        # stack widget
        self.stacking = QStackedWidget(self)
        self.stacking.setFixedSize(QSize(self.width(), self.height()))

    def init_ui(self):

        self.pgbar = Progressbar() # Call the progressbar method
        self.main_layout = QVBoxLayout()

        self.quiz_layout = QGridLayout()
        self.main_layout.addLayout(self.quiz_layout)
        self.main_layout.setStretch(1, 16) 

        self.bottom_layout = QHBoxLayout()
        self.main_layout.addLayout(self.bottom_layout)
        self.main_layout.setStretch(2, 5)
        self.bottom_layout.addWidget(self.pgbar)

        self.setStyleSheet(""" 
                            QLabel{
                           color: #0f0061;
                           font: Tahoma;
                           font-size: 35px;
                           font-weight: bold;
                           margin-left: 25px;
                           } 

                           QPushButton{
                           font-family: Tahoma;
                           font-weight: bold;
                           background-color: #61d4e4;
                           width: 200px;
                           height: 60px;
                           border: 2px inset blue;
                           }
                           
                           QPushButton:hover{
                           background-color: #52b1bf;
                           }
                           
                           QPushButton#submit{
                           background-color: #ff658b;
                           font-family: Tahoma;
                           font-weight: bold;
                           height: 30px;
                           border: 2px solid #950024;
                           }

                           QPushButton#submit:hover{
                           background-color: #dd3d53;
                           }

                            QLineEdit {
                            font-family: Tahoma;
                            font-size: 18px;
                            color: #2c3e50;
                            background-color: #ecf0f1;
                            border: 2px solid #3498db;
                            border-radius: 8px;
                            padding: 5px;
                            font-family: Tahoma;
                            font-weight: bold;
                            font-size: 22px;
                            selection-background-color: #3498db;
                            margin: 30px;
                            }

                           QLineEdit:focus{
                           border-color: #3498db;
                           }

                            QLineEdit {
                            font-family: Tahoma;
                            font-size: 18px;
                            color: #2c3e50;
                            background-color: #ecf0f1;
                            border: 2px solid #3498db;
                            border-radius: 8px;
                            padding: 5px;
                            font-family: Tahoma;
                            font-weight: bold;
                            font-size: 22px;
                            selection-background-color: #3498db;
                            margin: 30px;
                            }

                           QLineEdit:focus{
                           border-color: #3498db;
                           }

                            QProgressBar {
                            font-family: Tahoma;
                            font-size: 20px;
                            text-align: center;
                            border: 2px solid #555;
                            border-radius: 10px;
                            background-color: #eee;
                            color: black;
                            width: 400px;
                           
                            }
                            QProgressBar::chunk {
                                background-color: #5ec634;
                                border-radius: 8px;
                            }
                           
                           QRadioButton {
                            font-family: Tahoma;
                            font-size: 18px;
                            font-weight: bold;
                            color: #34495e;
                            padding: 5px;
                        }

                        QRadioButton::indicator { /*when not check*/
                            width: 20px;
                            height: 20px;
                            border-radius: 10px;
                            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                                stop:0 #f3ceff, stop:1 #f3ceff);                                                                                                                                        
                            border: 2px solid black;
                        }

                        QRadioButton::indicator:checked { /*When radiobutton check*/
                            background: qradialgradient(cx:0.5, cy:0.5, radius: 0.6, 
                                fx:0.5, fy:0.5, stop:0 #aa0000, stop:1 #aa0000);
                            border: 2px solid black;
                        }
                           
                        QCheckBox {
                        font-family: Tahoma;
                        font-size: 18px;
                        color: white;
                        spacing: 8px;
                        color: black;                                                                                                               
                        }

                        QCheckBox::indicator {
                        width: 20px;
                        height: 20px;
                        border-radius: 5px;
                        border: 2px solid blue;
                        background-color: transparent;
                        }
                           
                        QCheckBox::indicator:checked {
                        background-color: #bb0000;
                        border: 2px solid blue;
                        }   
                           
                        QPushButton#next{
                           background-color: #ec8148;
                           border: 2px inset red;
                           border-radius: 6px;
                        }
                        QPushButton#next:hover{
                           background-color: #ca7548;
                        }
                           """)
        ###################################################
        

        ##################################################

        self.setLayout(self.main_layout)

    def create_txtFile(self, user_data, score):
        username = user_data["name"]
        folder = "users"
        filename = os.path.join(folder, f"{username}.txt")
        os.makedirs(folder, exist_ok=True)
        print(username)

        # Read file and write the score inside the file
        trial_num = 1
        if os.path.exists(filename):
            with open(filename, "r") as file:
                lines = file.readlines()
                trial_num = sum(1 for line in lines if line.startswith("Score")) + 1 

        with open(filename, "a") as file: # USE A FOR APPEND
            file.write(f"Score{trial_num}: {score}\n")
   
    def create_graph(self):
        """
        For this, I make it read the file again and then use the score and trials 
        for plotting the bar graph in a separate window.
        """
        username = self.plr["name"]
        folder = "users"
        filename = os.path.join(folder, f"{username}.txt")
        
        if not os.path.exists(filename):
            print("File not found.")
            return
        
        trials = []
        scores = []

        with open(filename, "r") as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith("Score"):
                    trial_num = int(line.split(":")[0].replace("Score", "").strip())
                    score = int(line.split(":")[1].strip())
                    trials.append(trial_num)
                    scores.append(score)

        fig, (plt1, plt2) = plt.subplots(1, 2, figsize=(12, 6))

        plt1.bar(trials, scores, color="#d993ff")
        plt1.set_title("Player Performance (Bar Graph)")
        plt1.set_xlabel("Trials")
        plt1.set_ylabel("Score")
        plt1.set_ylim(0, 10)  

        plt2.scatter(trials, scores, color= "#d993ff", marker="o")
        plt2.set_title("Player Performance (Scatter Plot)")
        plt2.set_xlabel("Trials")
        plt2.set_ylabel("Score")
        plt2.set_ylim(0, 10)

        plt.tight_layout()
        plt.show() 

    def nextQuiz(self):
        for i in reversed(range(self.quiz_layout.count())): 
            self.quiz_layout.itemAt(i).widget().setParent(None)

        self.qText = QLabel(self)
        self.quiz_layout.addWidget(self.qText, 0, 0, 1, 3)

        if self.quizNo == 1:
            self.qText.setText("1) What is this fish?")
            img = QLabel(self)
            pixmap = QPixmap("H_images\shark2.jpg")  
            resized_pixmap = pixmap.scaled(950, 700)
            img.setPixmap(resized_pixmap)
            img.setAlignment(Qt.AlignmentFlag.AlignLeft)
            btn1 = QPushButton(self)
            btn1.setText("Shark")
            btn2 = QPushButton(self)
            btn2.setText("Salmon")
            btn3 = QPushButton(self)
            btn3.setText("Tuna")
            btn4 = QPushButton(self)
            btn4.setText("Swordfish")
            self.quiz_layout.addWidget(img, 1, 1, 1, 4)
            self.quiz_layout.addWidget(btn1, 2, 0, 1, 2)
            self.quiz_layout.addWidget(btn2, 2, 2, 1, 2) 
            self.quiz_layout.addWidget(btn3, 3, 0, 1, 2)
            self.quiz_layout.addWidget(btn4, 3, 2, 1, 2)
            btn1.clicked.connect(lambda: self.submit_answer("Shark"))
            btn2.clicked.connect(lambda: self.submit_answer("Salmon"))
            btn3.clicked.connect(lambda: self.submit_answer("Tuna"))
            btn4.clicked.connect(lambda: self.submit_answer("Swordfish"))
        elif self.quizNo == 2:
            self.qText.setText("2) What are the important habitats for many salmon species? (2 answers)")
            cb1 = QCheckBox(self)
            cb1.setText("Paldea")
            cb2 = QCheckBox(self)
            cb2.setText("Freshwater streams")
            cb3 = QCheckBox(self)
            cb3.setText("Freshwater estuaries")
            cb4 = QCheckBox(self)
            cb4.setText("Kalos")
            submit_btn = QPushButton(self)
            submit_btn.setText("Submit")
            submit_btn.setObjectName("submit")
            submit_btn.clicked.connect(lambda: self.submit_answer([cb1.isChecked(),cb2.isChecked(),cb3.isChecked(),cb4.isChecked()]))
            self.quiz_layout.addWidget(cb1, 1, 0, 1, 2)
            self.quiz_layout.addWidget(cb2, 1, 2, 1, 2) 
            self.quiz_layout.addWidget(cb3, 2, 0, 1, 2)
            self.quiz_layout.addWidget(cb4, 2, 2, 1, 2)
            self.quiz_layout.addWidget(submit_btn, 3, 0, 1, 3)
        elif self.quizNo == 3:
            self.qText.setText("3) To which family do most goldfish belong?")
            rd1 = QRadioButton(self)
            rd1.setText("Tuna family")
            rd2 = QRadioButton(self)
            rd2.setText("Salmon family")
            rd3 = QRadioButton(self)
            rd3.setText("Shark family")
            rd4 = QRadioButton(self)
            rd4.setText("Carp family")
            submit_btn = QPushButton(self)
            submit_btn.setObjectName("submit")
            submit_btn.setText("Submit")
            submit_btn.clicked.connect(lambda: self.submit_answer(rd4.isChecked()))
            self.quiz_layout.addWidget(rd1, 1, 0, 1, 2)
            self.quiz_layout.addWidget(rd2, 1, 2, 1, 2) 
            self.quiz_layout.addWidget(rd3, 2, 0, 1, 2)
            self.quiz_layout.addWidget(rd4, 2, 2, 1, 2)
            self.quiz_layout.addWidget(submit_btn, 3, 0, 1, 3)
        elif self.quizNo == 4:
            self.qText.setText("4) What is the name for the scientific study of fish?")
            btn1 = QPushButton(self)
            btn1.setText("oncology")
            btn2 = QPushButton(self)
            btn2.setText("entomology")
            btn3 = QPushButton(self)
            btn3.setText("ichthyology")
            btn4 = QPushButton(self)
            btn4.setText("ornithology")
            self.quiz_layout.addWidget(btn1, 1, 0, 1, 2)
            self.quiz_layout.addWidget(btn2, 1, 2, 1, 2) 
            self.quiz_layout.addWidget(btn3, 2, 0, 1, 2)
            self.quiz_layout.addWidget(btn4, 2, 2, 1, 2)
            btn1.clicked.connect(lambda: self.submit_answer("oncology"))
            btn2.clicked.connect(lambda: self.submit_answer("entomology"))
            btn3.clicked.connect(lambda: self.submit_answer("ichthyology"))
            btn4.clicked.connect(lambda: self.submit_answer("ornithology"))
        elif self.quizNo == 5:
            self.qText.setText("5) Which of these fish is dangerous to eat and is called fugu (フグ) in Japan?")
            btn1 = QPushButton(self)
            btn1.setText("puffer")
            btn2 = QPushButton(self)
            btn2.setText("pomfret")
            btn3 = QPushButton(self)
            btn3.setText("barracuda")
            btn4 = QPushButton(self)
            btn4.setText("piranha")
            self.quiz_layout.addWidget(btn1, 1, 0, 1, 2)
            self.quiz_layout.addWidget(btn2, 1, 2, 1, 2) 
            self.quiz_layout.addWidget(btn3, 2, 0, 1, 2)
            self.quiz_layout.addWidget(btn4, 2, 2, 1, 2)
            btn1.clicked.connect(lambda: self.submit_answer("puffer"))
            btn2.clicked.connect(lambda: self.submit_answer("pomfret"))
            btn3.clicked.connect(lambda: self.submit_answer("barracuda"))
            btn4.clicked.connect(lambda: self.submit_answer("piranha"))
        elif self.quizNo == 6:
            self.qText.setText("6) What is the name of the organs used by fish to obtain oxygen from water?")
            rd1 = QRadioButton(self)
            rd1.setText("abdominal pores")
            rd2 = QRadioButton(self)
            rd2.setText("gills")
            rd3 = QRadioButton(self)
            rd3.setText("fins")
            rd4 = QRadioButton(self)
            rd4.setText("swim bladders")
            submit_btn = QPushButton(self)
            submit_btn.setObjectName("submit")
            submit_btn.setText("Submit")
            submit_btn.clicked.connect(lambda: self.submit_answer(rd2.isChecked()))
            self.quiz_layout.addWidget(rd1, 1, 0, 1, 2)
            self.quiz_layout.addWidget(rd2, 1, 2, 1, 2) 
            self.quiz_layout.addWidget(rd3, 2, 0, 1, 2)
            self.quiz_layout.addWidget(rd4, 2, 2, 1, 2)
            self.quiz_layout.addWidget(submit_btn, 3, 0, 1, 3)
        elif self.quizNo == 7:
            self.qText.setText("7) What is the thai word 'ตกปลา' in English?")
            textbox = QLineEdit(self)
            textbox.setFixedSize(QSize(1000,120))
            submit_btn = QPushButton(self)
            submit_btn.setText("Submit")
            submit_btn.setObjectName("submit")
            submit_btn.clicked.connect(lambda: self.submit_answer(textbox.text().lower().strip()))
            self.quiz_layout.addWidget(textbox, 1, 0, 2, 2)
            self.quiz_layout.addWidget(submit_btn, 2, 0, 1, 2)
        elif self.quizNo == 8:
            self.qText.setText("8) Which of these fish is known as a living fossil?")
            btn1 = QPushButton(self)
            btn1.setText("angelfish")
            btn2 = QPushButton(self)
            btn2.setText("puffer")
            btn3 = QPushButton(self)
            btn3.setText("catfish")
            btn4 = QPushButton(self)
            btn4.setText("coelacanth")
            self.quiz_layout.addWidget(btn1, 1, 0, 1, 2)
            self.quiz_layout.addWidget(btn2, 1, 2, 1, 2) 
            self.quiz_layout.addWidget(btn3, 2, 0, 1, 2)
            self.quiz_layout.addWidget(btn4, 2, 2, 1, 2)
            btn1.clicked.connect(lambda: self.submit_answer("angelfish"))
            btn2.clicked.connect(lambda: self.submit_answer("puffer"))
            btn3.clicked.connect(lambda: self.submit_answer("catfish"))
            btn4.clicked.connect(lambda: self.submit_answer("coelacanth"))
        elif self.quizNo == 9:
            self.qText.setText("9) Fish are...")
            btn1 = QPushButton(self)
            btn1.setText("Vertebrates")
            btn2 = QPushButton(self)
            btn2.setText("Invertebrates")
            self.quiz_layout.addWidget(btn1, 1, 0, 1, 2)
            self.quiz_layout.addWidget(btn2, 1, 2, 1, 2)
            btn1.clicked.connect(lambda: self.submit_answer("Vertebrates"))
            btn2.clicked.connect(lambda: self.submit_answer("Invertebrates"))
        elif self.quizNo == 10:
            self.qText.setText("10) The skeleton of a shark is made of...")
            btn1 = QPushButton(self)
            btn1.setText("Bone")
            btn2 = QPushButton(self)
            btn2.setText("Cartilage")
            self.quiz_layout.addWidget(btn1, 1, 0, 1, 2)
            self.quiz_layout.addWidget(btn2, 1, 2, 1, 2)
            btn1.clicked.connect(lambda: self.submit_answer("Bone"))
            btn2.clicked.connect(lambda: self.submit_answer("Cartilage"))
        else:
            self.pgbar.hide()
            print(f"Correct Answers: {self.correctAns}")
            print(f"Incorrect Answers: {self.incorrectAns}")

            # Create a new txt file
            self.correct_answers = len(self.correctAns)
            self.create_txtFile(self.plr, self.correct_answers)

            # show the correct and incorrect answers
            self.correct = QLabel()
            self.correct.setText(f"You got: {len(self.correctAns)} / {len(self.correctAns) + len(self.incorrectAns)}")
            self.correct.setStyleSheet("color: red; font-family: Tahoma; font-size: 100px; font-weight: bold;")
            self.quiz_layout.addWidget(self.correct, 0,1,1,1)
            
            self.create_graph()

            # Go to next mode
            self.to_next_mode = QPushButton("Return")
            self.to_next_mode.setObjectName("next")
            self.to_next_mode.clicked.connect(self.go_back)
            self.quiz_layout.addWidget(self.to_next_mode, 1,1)
            
            # Add the money to playerData
            self.plr["money"] += 10 * int(len(self.correctAns))
            self.plr["exp"] += 2 * int(len(self.correctAns))
            
            print(self.plr["money"])
            print(self.plr["exp"])

            # Save and update the player data with money and exp (call the login method)
            try: 
                PlayerData.save_data(self.plr["name"], self.plr) 
                print("Success") 
            except Exception as e:
                print(f"Error saving player data: {e}")

    def go_back(self):
        from C_EducationMode.choose_education import EducationChoose
        
        if not hasattr(self, "choosing"):
            self.choosing = EducationChoose(plr_data=self.plr)

        self.hide()
        self.close()
        self.choosing.show()

    def submit_answer(self, answer):
        correctAnswer = self.answers[self.quizNo-1]
        print(str(self.quizNo)+")", answer, answer==correctAnswer)
        if answer == correctAnswer:
            self.correctAns.append(self.quizNo)
        else:
            self.incorrectAns.append(self.quizNo)
        self.pgbar.updatebar()
        self.quizNo += 1
        self.nextQuiz()

class Progressbar(QMainWindow):
    def __init__(self):
        super(Progressbar, self).__init__()
        self.max_q = 10

        self.setWindowTitle("Progressbar")
        self.setFixedSize(QSize(400, 100))

        self.bar = QProgressBar(self)
        self.bar.setRange(0, self.max_q) 
        self.bar.setValue(0) 

        layout = QVBoxLayout(self)
        layout.addWidget(self.bar)
        self.setLayout(layout)
        self.value = 0 

    def updatebar(self):
        if self.value < self.max_q:
            self.value += 1
            self.bar.setValue(self.value) 

class MainWindow(QWidget):  # Change from QMainWindow to QWidget
    def __init__(self, plr_data=None):
        super().__init__()
        self.plr_data = plr_data 
        self.setWindowTitle("Fish Quiz")
        self.showFullScreen()

        quizUI = QuizUI(plr_data=self.plr_data)
        layout = QVBoxLayout(self)
        layout.addWidget(quizUI)
        quizUI.nextQuiz()

def main(plr_data=None):
    app = QApplication(sys.argv)
    window = MainWindow(plr_data=plr_data)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()