import sys
import json
import os
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox
)
class PlayerData:
    @staticmethod
    def file_path(username): 
        user_folder = r"C:\Users\ACE\OneDrive\Fisherman_Chronicles\users"
        if not os.path.exists(user_folder):
            os.makedirs(user_folder)
        return os.path.join(user_folder, f"{username}_data.json")
    @classmethod
    def load_data(cls, username):
        try:
            with open(cls.file_path(username), "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return None
    @classmethod
    def save_data(cls, username, data):
        with open(cls.file_path(username), 'w') as file:
            json.dump(data, file, indent=4)
    @classmethod
    def username_exists(cls, username):
        return os.path.exists(cls.file_path(username))
    
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("User Login")
        self.setGeometry(100, 100, 300, 200)
        self.layout = QVBoxLayout()
        self.username_label = QLabel("Username:")
        self.layout.addWidget(self.username_label)
        self.username_input = QLineEdit()
        self.layout.addWidget(self.username_input)
        self.password_label = QLabel("Password:")
        self.layout.addWidget(self.password_label)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.password_input)
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login)
        self.layout.addWidget(self.login_button)
        self.setLayout(self.layout)
    
    def login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        player_data = PlayerData.load_data(username)
        if player_data is None:
            QMessageBox.warning(self, "Login Failed", "Username not found.")
            return
        if player_data.get("password") != password:
            QMessageBox.warning(self, "Login Failed", "Incorrect password.")
            return
        QMessageBox.information(self, "Login Successful", f"Welcome, {username}!")
        self.edit_username_window = EditUsernameWindow(username) # pass the current username 
        self.edit_username_window.show()
        self.close()

class EditUsernameWindow(QWidget):
    def __init__(self, current_username):
        super().__init__()
        self.current_username = current_username
        self.setWindowTitle("Edit Username")
        self.setGeometry(100, 100, 300, 200)
        self.layout = QVBoxLayout()
        self.current_username_label = QLabel(f"Current Username: {self.current_username}")
        self.layout.addWidget(self.current_username_label)
        self.new_username_label = QLabel("New Username:")
        self.layout.addWidget(self.new_username_label)
        self.new_username_input = QLineEdit()
        self.layout.addWidget(self.new_username_input)
        self.password_label = QLabel("Password:")
        self.layout.addWidget(self.password_label)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.layout.addWidget(self.password_input)
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_username)
        self.layout.addWidget(self.save_button)
        self.setLayout(self.layout)

    def save_username(self):
        new_username = self.new_username_input.text().strip()
        password = self.password_input.text().strip()
        if not new_username:
            QMessageBox.warning(self, "Error", "Please enter a new username.")
            return
        
        player_data = PlayerData.load_data(self.current_username)
        if player_data is None or player_data.get("password") != password:
            QMessageBox.warning(self, "Error", "Incorrect password.")
            return
        
        # Update the username in the JSON file and rename the file
        old_file_path = PlayerData.file_path(self.current_username)
        new_file_path = PlayerData.file_path(new_username)
        player_data["name"] = new_username
        PlayerData.save_data(new_username, player_data)  # Save with the new username
        os.remove(old_file_path)  # Remove the old file
        QMessageBox.information(self, "Success", f"Username changed to: {new_username}")
        self.close()

def main():
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec())
if __name__ == "__main__":
    main()