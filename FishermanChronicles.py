import tkinter as tk
from tkinter.ttk import *
from tkinter import messagebox, ttk
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import sys
from A_Title.login import RegisterSys
from A_Title import login
from A_Title.choosemode import ChooseMode
from A_Title import choosemode
from C_EducationMode import choose_education
from AA_StoryMode import MainControl
from C_EducationMode import FishQuiz
from B_FishAttack import FishAttack
from AA_StoryMode import Prologue
from Fish_Tic_Tac import tictac
from AA_StoryMode import Scene1
from AA_StoryMode import Scene2
from AA_StoryMode import Scene3
from AA_StoryMode import Scene4
from Z_Enemies import fishBoss
from C_EducationMode import FishBook

class FishermanChronicles:
    def __init__(self):
        super(FishermanChronicles, self).__init__()
        
        # Load the main method of the login
        login.main()

        """s
        self.root = tk.Tk()
     d  RegisterSys(self.root,700,720)
        self.root.mainloop()

        # Using this method, the login background image will not successfully load
        # This method will create a new root within this page
        """

if __name__ == "__main__":
    FishermanChronicles()