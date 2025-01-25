import json
import os
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QMessageBox, QHBoxLayout
)
from PyQt5.QtGui import QFont

USER_DATA_FILE = "users.json"

# Ensure the data file exists
if not os.path.exists(USER_DATA_FILE):
    with open(USER_DATA_FILE, "w") as f:
        json.dump({}, f)

class LoginRegisterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Speak Now - Login & Register")
        self.setGeometry(300, 200, 400, 300)
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.show_main_screen()
        self.setLayout(self.layout)

    def show_main_screen(self):
        self.clear_screen()

        title_label = QLabel("Welcome to Speak Now!")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50; margin-bottom: 20px;")
        self.layout.addWidget(title_label)

        self.login_button = QPushButton("Login")
        self.register_button = QPushButton("Register")

        self.login_button.setStyleSheet("padding: 10px; font-size: 14px;")
        self.register_button.setStyleSheet("padding: 10px; font-size: 14px;")

        self.login_button.clicked.connect(self.open_login_screen)
        self.register_button.clicked.connect(self.open_register_screen)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.login_button)
        button_layout.addWidget(self.register_button)

        self.layout.addLayout(button_layout)

    def open_register_screen(self):
        self.clear_screen()

        title_label = QLabel("Create an Account")
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setStyleSheet("color: #3498db; margin-bottom: 15px;")
        self.layout.addWidget(title_label)

        self.username_field = QLineEdit(self)
        self.username_field.setPlaceholderText("Enter Username")
        self.password_field = QLineEdit(self)
        self.password_field.setPlaceholderText("Enter Password")
        self.password_field.setEchoMode(QLineEdit.Password)

        self.username_field.setStyleSheet("padding: 8px; font-size: 12px;")
        self.password_field.setStyleSheet("padding: 8px; font-size: 12px;")

        self.register_btn = QPushButton("Register")
        self.register_btn.setStyleSheet("padding: 10px; font-size: 14px; background-color: #27ae60; color: white;")
        self.register_btn.clicked.connect(self.register_user)

        self.layout.addWidget(self.username_field)
        self.layout.addWidget(self.password_field)
        self.layout.addWidget(self.register_btn)

    def open_login_screen(self):
        self.clear_screen()

        title_label = QLabel("Login to Speak Now")
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setStyleSheet("color: #e67e22; margin-bottom: 15px;")
        self.layout.addWidget(title_label)

        self.username_field = QLineEdit(self)
        self.username_field.setPlaceholderText("Enter Username")
        self.password_field = QLineEdit(self)
        self.password_field.setPlaceholderText("Enter Password")
        self.password_field.setEchoMode(QLineEdit.Password)

        self.username_field.setStyleSheet("padding: 8px; font-size: 12px;")
        self.password_field.setStyleSheet("padding: 8px; font-size: 12px;")

        self.login_btn = QPushButton("Login")
        self.login_btn.setStyleSheet("padding: 10px; font-size: 14px; background-color: #2980b9; color: white;")
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

        try:
            with open(USER_DATA_FILE, "r") as f:
                users = json.load(f)
        except json.JSONDecodeError:
            users = {}

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

        try:
            with open(USER_DATA_FILE, "r") as f:
                users = json.load(f)
        except json.JSONDecodeError:
            users = {}

        if username in users and users[username] == password:
            self.show_message("Success", f"Welcome, {username}!", "info")
            self.open_main_screen(username)
        else:
            self.show_message("Login Error", "Invalid username or password!", "warning")
            self.show_main_screen()

    def open_main_screen(self, username):
        try:
            subprocess.Popen(["python3", "main.py", username])  # Running in a separate process
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

if __name__ == "__main__":
    app = QApplication([])
    window = LoginRegisterApp()
    window.show()
    app.exec_()