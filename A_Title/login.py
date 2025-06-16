import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import json
import os
import tkinter.font as tkFont
import sys
from PIL import Image, ImageTk

class PlayerData:
    def __init__(self):
        super(PlayerData, self).__init__()
       
    def default_data(self):
        return {
            "name": "",
            "password": "",
            "health": 100,
            "money": 0,
            "exp": 0,
            "equipped_weapon": "fishing_rod",
            "weapons" : {
                "fishing_rod": {"dmg": 2, "attack_speed": 2, "rarity": 1},
                "wooden_stick": {"dmg": 2, "attack_speed": 1, "rarity": 1}
            },
            "inventory": {
                "weapons" : {
                    "fishing_rod": {"dmg": 2, "attack_speed": 2, "rarity": 1},
                    "wooden_stick": {"dmg": 2, "attack_speed": 1, "rarity": 1}
                },
                "potions": {
                    "heath_potion": {"quantity": 1, "heal_amount": 10},
                    "mana_potion": {"quantity": 1, "restore_amount": 5},
                },
                "fish": [],
            },
        }

    @staticmethod
    def file_path(username): 
        """The username parameter passed from the signup method"""
        user_folder = r"C:\Users\ACE\OneDrive\Fisherman_Chronicles\users"
        if not os.path.exists(user_folder):
            os.makedirs(user_folder) # create directory from the user_folder
        else:
            return os.path.join(user_folder, f"{username}_data.json")
    
    @classmethod
    def load_data(cls, username):
        try:
            with open(cls.file_path(username), "r") as file:
                return json.load(file)
        except FileNotFoundError: # when file not exist
            return None

    @classmethod
    def save_data(cls, username, data):
        with open(cls.file_path(username), 'w') as file:
            json.dump(data, file, indent=4)

    @classmethod
    def username_exists(cls, username):
        return os.path.exists(cls.file_path(username))
    
class RegisterSys:
    def __init__(self, root, width, height):
        super(RegisterSys, self).__init__()
        # Check all the available fonts
        '''
        fonts = tkFont.families()
        print("Availble fonts in tkinter")
        for i in range(len(fonts)):
            print(f"{i+1}: {fonts[i]}")
        print("\n\n\n")'
        '''
        
        self.root = root  
        self.frame = None 
        self.root.geometry(f"{str(width)}x{str(height)}")
        self.root.config(bg="#320077")
        self.root.resizable(False, False)
        self.root.attributes("-fullscreen", True)

        img = r"H_images\img_login\castle.png" 
        
        self.bg_image = Image.open(img)
        self.castle_img = ImageTk.PhotoImage(self.bg_image.resize((1800,1000)))  

        # The image label
        self.img_label = tk.Label(self.root, image=self.castle_img, border=0)
        self.img_label.place(x=0, y =-200)

        # Start the login frame
        self.login_frame()
  
    def login_frame(self):
        if self.frame:
            self.frame.destroy()
        self.root.title("Login Page")
        self.frame = Login(self.root)
        self.frame.pack()  

    def signup_frame(self):
        if self.frame:
            self.frame.destroy()
        self.root.title("Signup Page")
        self.frame = Signup(self.root)
        self.frame.pack() 

    def destroy_root(self):
        self.root.destroy()

class Signup(tk.Frame):
    def __init__(self, root):
        super(Signup, self).__init__(root)
        self.root = root
        self.__widgets_comp()

    def __widgets_comp(self):
        self.signup_frame = tk.Frame(self.root, bg ="#203aa1", relief= "solid", border=2, highlightbackground= "white", highlightcolor="black", highlightthickness=2)
        self.signup_frame.pack(pady=(500,0), padx = 0, fill="both", expand=True)
        self.label = tk.Label(self.signup_frame, 
                              text="SIGN UP",
                              bg = "#203aa1",
                              fg = "white",
                              font= ("Trebuchet MS", 50, "bold")).pack(pady = (30,30))
        
        self.inner_signup_frame = tk.Frame(self.signup_frame, bg ="#203aa1", border = 0)
        self.inner_signup_frame.pack(fill = "x")
        
        self.signup_user_label = tk.Label(self.inner_signup_frame,
                                          text="Name: ", 
                                          font=("Leelawadee", 25, "bold"),
                                          bg = "#203aa1",
                                          fg = "white").grid(row=0, column=0, padx = (230,5))
        self.signup_user_var = tk.StringVar()
        self.signup_ent = tk.Entry(self.inner_signup_frame, 
                                    font=("Leelawadee", 25), 
                                    width=40, 
                                    bg= "#0e336d",
                                    fg="white", 
                                    insertbackground="white", 
                                    border=0,
                                    highlightbackground="#979797", 
                                    highlightcolor="#979797", 
                                    highlightthickness=1,
                                    textvariable=self.signup_user_var)  # Binding StringVar
        self.signup_ent.grid(row=0, column=1, padx=5, pady = 10)
        self.signup_ent.bind("<FocusIn>", lambda event: event.widget.config(bg ="#17185f"))
        self.signup_ent.bind("<FocusOut>", lambda event: event.widget.config(bg ="#0e336d"))

        self.signup_pass_label = tk.Label(self.inner_signup_frame,
                                          text="Password: ", 
                                          font=("Leelawadee", 25, "bold"),
                                          bg = "#203aa1",
                                          fg = "white").grid(row=1, column=0, padx = (280,5))
        self.signup_pass_var = tk.StringVar()  
        self.signup_pass_ent = tk.Entry(self.inner_signup_frame, 
                                         font=("Leelawadee", 25), 
                                         width=40, 
                                         bg= "#0e336d",
                                         fg="white", 
                                         insertbackground="white", 
                                         border=0,
                                         highlightbackground="#979797", 
                                         highlightcolor="#979797", 
                                         highlightthickness=1,
                                         show="*",
                                         textvariable=self.signup_pass_var)  # Binding StringVar
        self.signup_pass_ent.grid(row=1, column=1, padx=5, pady =10)
        self.signup_pass_ent.bind("<FocusIn>", lambda event: event.widget.config(bg ="#17185f"))
        self.signup_pass_ent.bind("<FocusOut>", lambda event: event.widget.config(bg ="#0e336d"))

        self.signup_confirm_label = tk.Label(self.inner_signup_frame,
                                             text="Confirm Password: ", 
                                             font=("Leelawadee", 25, "bold"),
                                             bg = "#203aa1",
                                             fg = "white").grid(row=2, column=0, padx = (150,5))
        self.signup_confirm_var = tk.StringVar()  
        self.signup_confirm_ent = tk.Entry(self.inner_signup_frame, 
                                            font=("Leelawadee", 25), 
                                            width=40, 
                                            bg= "#0e336d",
                                            fg="white", 
                                            insertbackground="white", 
                                            border=0,
                                            highlightbackground="#979797", 
                                            highlightcolor="#979797", 
                                            highlightthickness=1,
                                            show="*",
                                            textvariable=self.signup_confirm_var)  # Binding StringVar
        self.signup_confirm_ent.grid(row=2, column=1, padx=5, pady =10)
        self.signup_confirm_ent.bind("<FocusIn>", lambda event: event.widget.config(bg ="#17185f"))
        self.signup_confirm_ent.bind("<FocusOut>", lambda event: event.widget.config(bg ="#0e336d"))

        self.create_acc_btn = tk.Button(self.signup_frame,
                                        width=50,
                                        height=2,
                                        border=0,
                                        bg="#e300de",
                                        fg="white",
                                        relief="solid",
                                        font=("Leelawadee", 18, "bold"),
                                        text="Create Account",
                                        command= self.signing_up)  
        self.create_acc_btn.pack(pady=(35,5))
        self.create_acc_btn.bind("<Enter>", lambda event: event.widget.config(bg ="#af00ab"))
        self.create_acc_btn.bind("<Leave>", lambda event: event.widget.config(bg ="#e300de"))
        
        self.have_acc = tk.Label(self.signup_frame,
                                 text="Already have Account",
                                 bg = "#203aa1",
                                 fg = "white",
                                 cursor="hand2",
                                 font= ("Yu Gothic", 18, "bold underline"))
        self.have_acc.pack(pady = 30)
        self.have_acc.bind("<Button-1>", lambda e: self.call_login())

    def __validate(self, user, pwd, con_pwd):
        """
        Check whether the length of username is valid
        check whether the password == confirm password
        Check whether the player data already exist or not from getting from JSON
        If not exist, save the data into user folder
        """
        if len(user) < 3 or len(user) > 20:
            messagebox.showerror("Invalid Username", "Username must be between 3 and 20 characters.")
            return False
        
        if pwd != con_pwd:
            messagebox.showerror("Unmatched Password", "Passwords do not match.")
            return False
        
        return True
        
    def signing_up(self):
        user = self.signup_user_var.get().strip()
        pwd = self.signup_pass_var.get().strip()
        con_pwd = self.signup_confirm_var.get().strip()

        if self.__validate(user, pwd, con_pwd):
            if PlayerData.username_exists(user):
                messagebox.showerror("Username Exists", "Username already exists.")
            else:
                # Save the player data to JSON file
                player_data = PlayerData()
                data = player_data.default_data()
                data["name"] = user
                data["password"] = pwd
                PlayerData.save_data(user, data) # transfer the player data into JSON
                messagebox.showinfo("Success", "Account created")

                # clear the entrybox fields
                self.signup_ent.delete(0, tk.END)
                self.signup_pass_ent.delete(0, tk.END)
                self.signup_confirm_ent.delete(0, tk.END)

                # Call the login frame
                self.call_login()

    def call_login(self):
        self.signup_frame.destroy()
        self.frame = Login(self.root) 

class Login(tk.Frame):  # The login frame (inherited from frame class)
    def __init__(self, root):
        super(Login, self).__init__(root)
        self.root = root
        self.__widgets_comp()

    def __widgets_comp(self):
        self.login_frame = tk.Frame(self.root, bg="#283144", relief= "solid", border=2, highlightbackground= "white", highlightcolor="black", highlightthickness=2)
        self.login_frame.pack(pady=(500, 0), padx=0, fill="both", expand=True)

        self.label = tk.Label(self.login_frame, 
                              text="User Login",
                              bg="#283144",
                              fg="white",
                              font=("Trebuchet MS", 50, "bold"))
        self.label.pack(pady=(30, 30))

        self.inner_login_frame = tk.Frame(self.login_frame, bg="#283144", border=0)
        self.inner_login_frame.pack(fill="x")

        self.login_name_frame = tk.Frame(self.login_frame, bg="#283144", border=0)
        self.login_name_frame.pack(fill="x")

        self.login_user_label = tk.Label(self.login_name_frame,
                                         text="Name: ", 
                                         font=("Leelawadee", 25, "bold"),
                                         bg="#283144",
                                         fg="white")
        self.login_user_label.pack(side="left", padx=(320,0), pady=10)


        self.login_user_var = tk.StringVar()
        self.login_ent = tk.Entry(self.login_name_frame, 
                                  font=("Leelawadee", 25), 
                                  width=40, 
                                  bg="#2a2a4c",
                                  fg="white", 
                                  insertbackground="white", 
                                  border=0,
                                  highlightbackground="#979797", 
                                  highlightcolor="#979797", 
                                  highlightthickness=1,
                                  textvariable=self.login_user_var)
        self.login_ent.pack(side="left", padx=(60,0), pady=10)

        self.login_ent.bind("<FocusIn>", lambda event: event.widget.config(bg ="#17185f"))
        self.login_ent.bind("<FocusOut>", lambda event: event.widget.config(bg ="#2a2a4c"))
    
        self.inner_login_frame2 = tk.Frame(self.login_frame, bg="#283144", border=0)
        self.inner_login_frame2.pack(fill="x")

        self.login_pass_label = tk.Label(self.inner_login_frame2,
                                         text="Password: ", 
                                         font=("Leelawadee", 25, "bold"),
                                         bg="#283144",
                                         fg="white")
        self.login_pass_label.pack(side="left", padx=(320,0), pady=15)

        self.login_pass_var = tk.StringVar()
        self.login_pass_ent = tk.Entry(self.inner_login_frame2, 
                                       font=("Leelawadee", 25), 
                                       width=40, 
                                       bg="#2a2a4c",
                                       fg="white", 
                                       insertbackground="white", 
                                       border=0,
                                       highlightbackground="#979797", 
                                       highlightcolor="#979797", 
                                       highlightthickness=1,
                                       show="*",
                                       textvariable=self.login_pass_var)
        self.login_pass_ent.pack(side="left", padx=(5,0), pady=15)
        self.login_pass_ent.bind("<FocusIn>", lambda event: event.widget.config(bg ="#17185f"))
        self.login_pass_ent.bind("<FocusOut>", lambda event: event.widget.config(bg ="#2a2a4c"))

        self.innerframe = tk.Frame(self.login_frame, bg = "#283144")
        self.innerframe.pack(fill="x")
        self.remember = tk.Checkbutton(self.innerframe,
                                       text= "Remember me",
                                       bg = "#283144",
                                       borderwidth=0,
                                       fg = "white",
                                       selectcolor="magenta",
                                       font = ("Leelawadee", 15))
        self.remember.pack(side="left", padx=(180, 100), pady=10)

        self.forgot_pass = tk.Label(self.innerframe,
                                    bg = "#283144",
                                    fg = "white",
                                    font= ("Leelawadee", 15),
                                    text= "Forgot password?")
        self.forgot_pass.pack(side="right", pady= 15, padx = (5,100))
    

        self.login_btn = tk.Button(self.login_frame,
                                   width=50,
                                   height=2,
                                   border=0,
                                   bg="#e300de",
                                   fg="white",
                                   relief="solid",
                                   font=("Leelawadee", 18, "bold"),
                                   text="Login",
                                   command=self.logging_in)
        self.login_btn.pack(pady=(15, 15))
        self.login_btn.bind("<Enter>", lambda event: event.widget.config(bg="#af00ab"))
        self.login_btn.bind("<Leave>", lambda event: event.widget.config(bg="#e300de"))

        self.new_acc_lab = tk.Label(self.login_frame,
                                    text="Create New Account",
                                    fg = "white",
                                    bg = "#283144",
                                    font = ("Yu Gothic", 18, "bold underline"),
                                    cursor= "hand2")
        self.new_acc_lab.pack(pady = (20,0))
        self.new_acc_lab.bind("<Button-1>", lambda e: self.call_sign_up())

    def logging_in(self):
        from A_Title import title_page
        from A_Title.title_page import TitlePage # this will prevent circular import (import inside the method)

        """
        get username and password from textvariable
        Checkk the username and password
        """
        user = self.login_user_var.get().strip()
        pwd = self.login_pass_var.get().strip()

        plr_data = PlayerData.load_data(user) # load the player data

        if plr_data is None:
            messagebox.showerror("Login Failed", "Username not found.")
            return

        stored_pwd = plr_data.get("password", None)  
        if stored_pwd is None:
            messagebox.showerror("Login Failed", "Password not set for this user.")
            return

        if pwd == stored_pwd:
            # delete the entry fields
            self.login_ent.delete(0, tk.END)
            self.login_pass_ent.delete(0, tk.END)
            
            # clear frame and destroy root
            self.clear_frame()
            RegisterSys.destroy_root(self)

            # pass the data to title page (passing the data) 
            title_page.main(plr_data)

        else:
            messagebox.showerror("Login Failed", "Incorrect password or username")

    def call_sign_up(self):
        self.login_frame.destroy()
        self.frame = Signup(self.root) # call the sign up page

    def clear_frame(self):
        self.login_frame.destroy()

def main():
    root = tk.Tk() 
    app = RegisterSys(root,700,720) 
    root.mainloop() 

if __name__ == "__main__":
    main()