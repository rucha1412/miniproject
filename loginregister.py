import json
import os
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox

USER_DATA_FILE = "users.json"

# Ensure the data file exists
if not os.path.exists(USER_DATA_FILE):
    with open(USER_DATA_FILE, "w") as f:
        json.dump({}, f)

class loginregister(QWidget):
    def _init_(self):
        super()._init_()
        self.setWindowTitle("Login and Register")
        self.setGeometry(300, 200, 400, 300)
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.show_main_screen()
        self.setLayout(self.layout)

    def show_main_screen(self):
        self.clear_screen()

        self.title_label = QLabel("Welcome to Speak Now!")
        self.layout.addWidget(self.title_label)

        self.login_button = QPushButton("Login")
        self.register_button = QPushButton("Register")

        self.login_button.clicked.connect(self.open_login_screen)
        self.register_button.clicked.connect(self.open_register_screen)

        self.layout.addWidget(self.login_button)
        self.layout.addWidget(self.register_button)

    def open_register_screen(self):
        self.clear_screen()

        self.title_label = QLabel("Register")
        self.layout.addWidget(self.title_label)

        self.username_field = QLineEdit(self)
        self.username_field.setPlaceholderText("Enter Username")
        self.password_field = QLineEdit(self)
        self.password_field.setPlaceholderText("Enter Password")
        self.password_field.setEchoMode(QLineEdit.Password)

        self.register_btn = QPushButton("Register")
        self.register_btn.clicked.connect(self.register_user)

        self.layout.addWidget(self.username_field)
        self.layout.addWidget(self.password_field)
        self.layout.addWidget(self.register_btn)

    def open_login_screen(self):
        self.clear_screen()

        self.title_label = QLabel("Login")
        self.layout.addWidget(self.title_label)

        self.username_field = QLineEdit(self)
        self.username_field.setPlaceholderText("Enter Username")
        self.password_field = QLineEdit(self)
        self.password_field.setPlaceholderText("Enter Password")
        self.password_field.setEchoMode(QLineEdit.Password)

        self.login_btn = QPushButton("Login")
        self.login_btn.clicked.connect(self.login_user)

        self.layout.addWidget(self.username_field)
        self.layout.addWidget(self.password_field)
        self.layout.addWidget(self.login_btn)

    def register_user(self):
        username = self.username_field.text().strip()
        password = self.password_field.text().strip()

        if not username or not password:
            self.show_message("Registration Error", "Username and password cannot be empty!", "warning")
            return

        with open(USER_DATA_FILE, "r") as f:
            users = json.load(f)

        if username in users:
            self.show_message("Registration Error", "Username already exists!", "warning")
        else:
            users[username] = password
            with open(USER_DATA_FILE, "w") as f:
                json.dump(users, f)

            self.show_message("Success", "Registration successful! Please login.", "info")
            self.show_main_screen()

    def login_user(self):
        username = self.username_field.text().strip()
        password = self.password_field.text().strip()

        with open(USER_DATA_FILE, "r") as f:
            users = json.load(f)

        if username in users and users[username] == password:
            self.show_message("Success", f"Welcome, {username}!", "info")
            self.open_main_screen(username)
        else:
            self.show_message("Login Error", "Invalid username or password! Redirecting to the main screen.", "warning")
            self.show_main_screen()

    def open_main_screen(self, username):
        try:

            # Use subprocess.Popen to run main.py with the username as an argument
            subprocess.Popen(["python3", "main.py", username])  # Running in a separate process
            #self.close()  # Close the current login/register window
            #process.wait()
        except Exception as e:
            self.show_message("Error", f"Failed to open the Speak Now application: {e}", "warning")

    def clear_screen(self):
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def show_message(self, title, message, icon):
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(message)
        if icon == "info":
            msg.setIcon(QMessageBox.Information)
        elif icon == "warning":
            msg.setIcon(QMessageBox.Warning)
        msg.exec_()

if _name_ == "_main_":
    app = QApplication([])
    window = loginregister()
    window.show()
    app.exec_()