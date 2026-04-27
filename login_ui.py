import sqlite3
import bcrypt
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
from PyQt6.QtCore import Qt
from styles import LOGIN_STYLESHEET

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Project Manager - Login")
        self.setFixedSize(420, 520)
        self.setStyleSheet(LOGIN_STYLESHEET)
        
        # Center the window
        self.move(100, 100)
        
        # Main layout with padding
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 60, 40, 40)
        layout.setSpacing(15)
        
        # Title
        title_label = QLabel("Project Manager")
        title_label.setObjectName("titleLabel")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setMinimumHeight(40)
        layout.addWidget(title_label)
        
        # Subtitle
        info_label = QLabel("Secure Access Portal")
        info_label.setObjectName("infoLabel")
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info_label)
        
        layout.addSpacing(20)
        
        # Username Label
        username_label = QLabel("Username")
        username_label.setStyleSheet("color: rgba(255, 255, 255, 0.9);")
        layout.addWidget(username_label)
        
        # Username Input
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setMinimumHeight(45)
        layout.addWidget(self.username_input)
        
        # Password Label
        password_label = QLabel("Password")
        password_label.setStyleSheet("color: rgba(255, 255, 255, 0.9);")
        layout.addWidget(password_label)
        
        # Password Input
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMinimumHeight(45)
        layout.addWidget(self.password_input)
        
        layout.addSpacing(20)
        
        # Login Button
        self.login_button = QPushButton("Sign In")
        self.login_button.clicked.connect(self.check_login)
        self.login_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.login_button.setMinimumHeight(48)
        layout.addWidget(self.login_button)
        
        layout.addStretch()
        
        # Footer info
        footer_label = QLabel("Demo: admin / admin123")
        footer_label.setObjectName("infoLabel")
        footer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(footer_label)
        
        self.setLayout(layout)
        self.user_role = None # Store role after success
        
        # Allow Enter key to login
        self.password_input.returnPressed.connect(self.check_login)

    def check_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Validation Error", "Please enter both username and password")
            return
        
        conn = sqlite3.connect("data/app_database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT password_hash, role FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        conn.close()
        
        if result and bcrypt.checkpw(password.encode('utf-8'), result[0]):
            self.user_role = result[1] # Save the role (e.g., 'admin')
            self.accept() # Close dialog with success
        else:
            QMessageBox.warning(self, "Authentication Failed", "Invalid username or password")