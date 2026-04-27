import sys
import sqlite3
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTableWidget, 
                             QTableWidgetItem, QVBoxLayout, QHBoxLayout, QWidget, 
                             QPushButton, QMessageBox, QLabel, QFrame, QCheckBox, QFileDialog,
                             QComboBox, QDialog, QScrollArea, QLineEdit, QTableWidgetItem as TableItem)
from PyQt6.QtCore import Qt
import bcrypt
from login_ui import LoginWindow
from forms import AddEditRecordDialog
from styles import MAIN_STYLESHEET
from database import initialize_database, create_default_admin
from data_manager import import_excel, export_excel

class ColumnSelectionDialog(QDialog):
    """Dialog for selecting which columns to export"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Columns to Export")
        self.setGeometry(100, 100, 400, 500)
        self.setStyleSheet("""
            QDialog {
                background-color: #F8FAFC;
            }
            QLabel {
                color: #1E3A8A;
            }
            QCheckBox {
                color: #334155;
                padding: 5px;
            }
            QPushButton {
                background-color: #3B82F6;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1E40AF;
            }
        """)
        
        # Column options
        self.column_options = [
            ('NO', 'No.'),
            ('CLIENT', 'Client'),
            ('LOCATION', 'Location'),
            ('CURRENCY', 'Currency'),
            ('PROGRESS', 'Progress'),
            ('IMAGE_PATH', 'Image'),
            ('PROJECT', 'Project'),
            ('GEMPHIL_DEVICE', 'Gemphil Device'),
            ('DETAILS', 'Details'),
            ('CONTACT_PERSON', 'Contact Person'),
            ('EMAIL', 'Email')
        ]
        
        self.init_ui()
        self.selected_columns = []
    
    def init_ui(self):
        """Initialize the dialog UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("Select Columns to Export:")
        title.setStyleSheet("font-size: 14pt; font-weight: bold; color: #1E3A8A; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Scrollable area for checkboxes
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: 1px solid #CBD5E1; border-radius: 4px; }")
        
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(8)
        scroll_layout.setContentsMargins(10, 10, 10, 10)
        
        # Create checkboxes
        self.checkboxes = {}
        for col_db, col_display in self.column_options:
            checkbox = QCheckBox(col_display)
            checkbox.setChecked(True)  # All selected by default
            self.checkboxes[col_db] = checkbox
            scroll_layout.addWidget(checkbox)
        
        scroll_layout.addStretch()
        scroll_area.setWidget(scroll_widget)
        layout.addWidget(scroll_area)
        
        # Button layout
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        # Select All button
        select_all_btn = QPushButton("✓ Select All")
        select_all_btn.clicked.connect(self.select_all)
        button_layout.addWidget(select_all_btn)
        
        # Deselect All button
        deselect_all_btn = QPushButton("✗ Deselect All")
        deselect_all_btn.clicked.connect(self.deselect_all)
        button_layout.addWidget(deselect_all_btn)
        
        button_layout.addStretch()
        
        # OK button
        ok_btn = QPushButton("✓ OK")
        ok_btn.setMinimumWidth(100)
        ok_btn.clicked.connect(self.accept_selection)
        button_layout.addWidget(ok_btn)
        
        # Cancel button
        cancel_btn = QPushButton("✗ Cancel")
        cancel_btn.setMinimumWidth(100)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #EF4444;
            }
            QPushButton:hover {
                background-color: #DC2626;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
    
    def select_all(self):
        """Select all checkboxes"""
        for checkbox in self.checkboxes.values():
            checkbox.setChecked(True)
    
    def deselect_all(self):
        """Deselect all checkboxes"""
        for checkbox in self.checkboxes.values():
            checkbox.setChecked(False)
    
    def accept_selection(self):
        """Get selected columns and close dialog"""
        self.selected_columns = [col for col, checkbox in self.checkboxes.items() if checkbox.isChecked()]
        
        if not self.selected_columns:
            QMessageBox.warning(self, "Selection Error", "Please select at least one column to export")
            return
        
        self.accept()
    
    def get_selected_columns(self):
        """Return list of selected column database names"""
        return self.selected_columns

class AdminCredentialDialog(QDialog):
    """Dialog for verifying admin credentials"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Admin Verification Required")
        self.setGeometry(150, 150, 350, 200)
        self.setStyleSheet("""
            QDialog {
                background-color: #F8FAFC;
            }
            QLabel {
                color: #1E3A8A;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #CBD5E1;
                border-radius: 4px;
                background-color: white;
            }
            QPushButton {
                background-color: #3B82F6;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1E40AF;
            }
        """)
        self.verified = False
        self.init_ui()
    
    def init_ui(self):
        """Initialize the dialog UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("⚠️ Admin verification required for this action")
        title.setStyleSheet("font-weight: bold; color: #DC2626;")
        layout.addWidget(title)
        
        # Username
        layout.addWidget(QLabel("Admin Username:"))
        self.username_input = QLineEdit()
        self.username_input.setMinimumHeight(50)
        layout.addWidget(self.username_input)
        
        # Password
        layout.addWidget(QLabel("Admin Password:"))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMinimumHeight(50)
        self.password_input.returnPressed.connect(self.verify_credentials)
        layout.addWidget(self.password_input)
        
        layout.addSpacing(10)
        
        # Button layout
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        verify_btn = QPushButton("✓ Verify")
        verify_btn.setMinimumWidth(100)
        verify_btn.clicked.connect(self.verify_credentials)
        button_layout.addWidget(verify_btn)
        
        cancel_btn = QPushButton("✗ Cancel")
        cancel_btn.setMinimumWidth(100)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #EF4444;
            }
            QPushButton:hover {
                background-color: #DC2626;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
    
    def verify_credentials(self):
        """Verify admin credentials"""
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Please enter both username and password")
            return
        
        try:
            conn = sqlite3.connect("data/app_database.db")
            cursor = conn.cursor()
            cursor.execute("SELECT password_hash, role FROM users WHERE username = ?", (username,))
            result = cursor.fetchone()
            conn.close()
            
            if result:
                password_hash, role = result
                if bcrypt.checkpw(password.encode(), password_hash) and role.lower() == 'admin':
                    self.verified = True
                    self.accept()
                else:
                    QMessageBox.warning(self, "Verification Failed", "Invalid credentials or user is not admin")
            else:
                QMessageBox.warning(self, "Verification Failed", "User not found")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Verification error: {str(e)}")

class ManageUsersDialog(QDialog):
    """Dialog for managing users (admin only)"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("👥 Manage Users")
        self.setGeometry(100, 100, 600, 500)
        self.setStyleSheet("""
            QDialog {
                background-color: #F8FAFC;
            }
            QLabel {
                color: #1E3A8A;
            }
            QLineEdit, QComboBox {
                padding: 8px;
                border: 1px solid #CBD5E1;
                border-radius: 4px;
                background-color: white;
                min-height: 35px;
            }
            QTableWidget {
                border: 1px solid #CBD5E1;
                gridline-color: #E2E8F0;
            }
            QPushButton {
                background-color: #3B82F6;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1E40AF;
            }
        """)
        self.init_ui()
        self.load_users()
    
    def init_ui(self):
        """Initialize the dialog UI"""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Add User Section
        add_section = QLabel("➕ Add New User:")
        add_section.setStyleSheet("font-weight: bold; color: #1E3A8A; font-size: 11pt;")
        main_layout.addWidget(add_section)
        
        add_layout = QHBoxLayout()
        add_layout.setSpacing(10)
        
        self.new_username_input = QLineEdit()
        self.new_username_input.setPlaceholderText("Username")
        add_layout.addWidget(self.new_username_input)
        
        self.new_password_input = QLineEdit()
        self.new_password_input.setPlaceholderText("Password")
        self.new_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        add_layout.addWidget(self.new_password_input)
        
        self.new_role_combo = QComboBox()
        self.new_role_combo.addItems(["admin", "user"])
        add_layout.addWidget(self.new_role_combo)
        
        add_btn = QPushButton("Add User")
        add_btn.clicked.connect(self.add_user)
        add_layout.addWidget(add_btn)
        
        main_layout.addLayout(add_layout)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("background-color: #E2E8F0;")
        main_layout.addWidget(separator)
        
        # Users Table Section
        table_label = QLabel("👤 Existing Users:")
        table_label.setStyleSheet("font-weight: bold; color: #1E3A8A; font-size: 11pt;")
        main_layout.addWidget(table_label)
        
        # Users table
        self.users_table = QTableWidget()
        self.users_table.setColumnCount(4)
        self.users_table.setHorizontalHeaderLabels(['Username', 'Role', 'Change Role', 'Delete'])
        self.users_table.horizontalHeader().setStretchLastSection(False)
        self.users_table.setSelectionBehavior(self.users_table.SelectionBehavior.SelectRows)
        self.users_table.setAlternatingRowColors(True)
        main_layout.addWidget(self.users_table)
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        main_layout.addWidget(close_btn)
    
    def load_users(self):
        """Load users from database"""
        try:
            conn = sqlite3.connect("data/app_database.db")
            cursor = conn.cursor()
            cursor.execute("SELECT id, username, role FROM users ORDER BY username")
            users = cursor.fetchall()
            conn.close()
            
            self.users_table.setRowCount(len(users))
            for row_idx, (user_id, username, role) in enumerate(users):
                # Username
                username_item = QTableWidgetItem(username)
                username_item.setData(1001, user_id)
                self.users_table.setItem(row_idx, 0, username_item)
                
                # Role
                role_item = QTableWidgetItem(role)
                self.users_table.setItem(row_idx, 1, role_item)
                
                # Change Role button
                change_role_btn = QPushButton("Change")
                change_role_btn.clicked.connect(lambda checked, rid=user_id, rn=username: self.change_role_dialog(rid, rn))
                self.users_table.setCellWidget(row_idx, 2, change_role_btn)
                
                # Delete button
                delete_btn = QPushButton("Delete")
                delete_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #EF4444;
                    }
                    QPushButton:hover {
                        background-color: #DC2626;
                    }
                """)
                delete_btn.clicked.connect(lambda checked, rid=user_id, rn=username: self.delete_user(rid, rn))
                self.users_table.setCellWidget(row_idx, 3, delete_btn)
            
            # Adjust column widths
            self.users_table.resizeColumnsToContents()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load users: {str(e)}")
    
    def add_user(self):
        """Add a new user"""
        username = self.new_username_input.text().strip()
        password = self.new_password_input.text()
        role = self.new_role_combo.currentText()
        
        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Please enter username and password")
            return
        
        try:
            conn = sqlite3.connect("data/app_database.db")
            cursor = conn.cursor()
            
            # Check if user exists
            cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
            if cursor.fetchone():
                QMessageBox.warning(self, "Duplicate User", "Username already exists")
                conn.close()
                return
            
            # Hash password and insert
            password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                          (username, password_hash, role))
            conn.commit()
            conn.close()
            
            QMessageBox.information(self, "Success", f"User '{username}' added successfully")
            self.new_username_input.clear()
            self.new_password_input.clear()
            self.load_users()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add user: {str(e)}")
    
    def change_role_dialog(self, user_id, username):
        """Show dialog to change user role"""
        # Determine current role
        try:
            conn = sqlite3.connect("data/app_database.db")
            cursor = conn.cursor()
            cursor.execute("SELECT role FROM users WHERE id = ?", (user_id,))
            current_role = cursor.fetchone()[0]
            conn.close()
            
            new_role = "user" if current_role.lower() == "admin" else "admin"
            
            reply = QMessageBox.question(
                self,
                "Change User Role",
                f"Change {username}'s role from '{current_role}' to '{new_role}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                conn = sqlite3.connect("data/app_database.db")
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET role = ? WHERE id = ?", (new_role, user_id))
                conn.commit()
                conn.close()
                
                QMessageBox.information(self, "Success", f"Role changed to '{new_role}'")
                self.load_users()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to change role: {str(e)}")
    
    def delete_user(self, user_id, username):
        """Delete a user"""
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete user '{username}'?\nThis action cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                conn = sqlite3.connect("data/app_database.db")
                cursor = conn.cursor()
                cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
                conn.commit()
                conn.close()
                
                QMessageBox.information(self, "Success", f"User '{username}' deleted")
                self.load_users()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete user: {str(e)}")

class MainWindow(QMainWindow):
    def __init__(self, role):
        super().__init__()
        self.role = role
        self.setWindowTitle(f"Project Manager - {role.capitalize()}")
        self.setGeometry(50, 50, 1200, 750)
        self.setStyleSheet(MAIN_STYLESHEET)
        
        # Sort state tracking
        self.sort_column = None
        self.sort_ascending = True
        
        # Main Layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(15, 15, 15, 15)
        self.layout.setSpacing(12)
        
        # Header Section
        header_layout = QHBoxLayout()
        header_layout.setSpacing(10)
        
        title_label = QLabel("Project Records")
        title_label.setStyleSheet("font-size: 16pt; font-weight: bold; color: #1E3A8A;")
        header_layout.addWidget(title_label)
        
        role_badge = QLabel(f"Role: {role.upper()}")
        role_badge.setStyleSheet("""
            background-color: #E0F2FE;
            color: #0369A1;
            padding: 4px 12px;
            border-radius: 12px;
            font-weight: 500;
            font-size: 9pt;
        """)
        header_layout.addStretch()
        header_layout.addWidget(role_badge)
        
        self.layout.addLayout(header_layout)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("background-color: #E2E8F0;")
        self.layout.addWidget(separator)

        # Filter Section
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(10)
        
        filter_label = QLabel("🔍 Filters:")
        filter_label.setStyleSheet("font-weight: bold; color: #1E3A8A;")
        filter_layout.addWidget(filter_label)
        
        # Create filter dropdowns for key categories
        self.client_filter = QComboBox()
        self.client_filter.addItem("All Clients")
        self.client_filter.currentIndexChanged.connect(self.apply_filters)
        filter_layout.addWidget(QLabel("Client:"))
        filter_layout.addWidget(self.client_filter)
        
        self.location_filter = QComboBox()
        self.location_filter.addItem("All Locations")
        self.location_filter.currentIndexChanged.connect(self.apply_filters)
        filter_layout.addWidget(QLabel("Location:"))
        filter_layout.addWidget(self.location_filter)
        
        self.currency_filter = QComboBox()
        self.currency_filter.addItem("All Currencies")
        self.currency_filter.currentIndexChanged.connect(self.apply_filters)
        filter_layout.addWidget(QLabel("Currency:"))
        filter_layout.addWidget(self.currency_filter)
        
        self.progress_filter = QComboBox()
        self.progress_filter.addItem("All Progress")
        self.progress_filter.currentIndexChanged.connect(self.apply_filters)
        filter_layout.addWidget(QLabel("Progress:"))
        filter_layout.addWidget(self.progress_filter)
        
        filter_layout.addStretch()
        
        clear_filters_btn = QPushButton("Clear Filters")
        clear_filters_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        clear_filters_btn.clicked.connect(self.clear_filters)
        filter_layout.addWidget(clear_filters_btn)
        
        self.layout.addLayout(filter_layout)

        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("background-color: #E2E8F0;")
        self.layout.addWidget(separator)

        # Search Bar for real-time alphabetical filtering
        search_layout = QHBoxLayout()
        search_layout.setSpacing(10)
        
        search_label = QLabel("🔎 Search:")
        search_label.setStyleSheet("font-weight: bold; color: #1E3A8A;")
        search_layout.addWidget(search_label)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search across all columns...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 8px 12px;
                border: 1px solid #CBD5E1;
                border-radius: 4px;
                background-color: white;
                color: #334155;
            }
            QLineEdit:focus {
                border: 2px solid #3B82F6;
            }
        """)
        self.search_input.textChanged.connect(self.on_search_text_changed)
        search_layout.addWidget(self.search_input)
        
        clear_search_btn = QPushButton("✕ Clear Search")
        clear_search_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        clear_search_btn.clicked.connect(self.clear_search)
        search_layout.addWidget(clear_search_btn)
        
        search_layout.addStretch()
        self.layout.addLayout(search_layout)

        # Separator
        separator2 = QFrame()
        separator2.setFrameShape(QFrame.Shape.HLine)
        separator2.setStyleSheet("background-color: #E2E8F0;")
        self.layout.addWidget(separator2)

        # Table Widget
        self.table = QTableWidget()
        self.table.setColumnCount(11)  # 11 data columns (no checkbox)
        self.table.setHorizontalHeaderLabels(['No.', 'Client', 'Location', 'Currency', 
                                              'Progress', 'Image', 'Project', 
                                              'Gemphil Device', 'Details', 'Contact', 'Email'])
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(self.table.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(self.table.SelectionMode.MultiSelection)
        self.table.horizontalHeader().setStretchLastSection(True)
        
        # Make header taller with better spacing
        self.table.horizontalHeader().setDefaultSectionSize(100)
        self.table.horizontalHeader().setSectionResizeMode(self.table.horizontalHeader().ResizeMode.Interactive)
        self.table.horizontalHeader().setMinimumHeight(48)
        
        # Connect header click signal for column sorting
        self.table.horizontalHeader().sectionClicked.connect(self.on_header_click)
        
        # Enable gridlines for clear column/row division
        self.table.setShowGrid(True)
        self.table.setGridStyle(Qt.PenStyle.SolidLine)
        
        # Set row height for better visibility AND allow resizing
        self.table.verticalHeader().setDefaultSectionSize(32)
        self.table.verticalHeader().setVisible(True)  # <-- Changed to True to allow users to adjust row heights
        self.table.verticalHeader().setSectionResizeMode(self.table.verticalHeader().ResizeMode.Interactive)
        
        self.layout.addWidget(self.table)

        # Button layout for CRUD actions
        button_layout1 = QHBoxLayout()
        button_layout1.setSpacing(10)
        
        self.add_btn = QPushButton("➕ Add Record")
        self.add_btn.setObjectName("addBtn")
        self.add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.add_btn.clicked.connect(self.add_record)
        button_layout1.addWidget(self.add_btn)
        
        self.edit_btn = QPushButton("✏️ Edit Record")
        self.edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.edit_btn.clicked.connect(self.edit_record)
        button_layout1.addWidget(self.edit_btn)
        
        self.delete_btn = QPushButton("🗑️ Delete Record")
        self.delete_btn.setObjectName("deleteBtn")
        self.delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.delete_btn.clicked.connect(self.delete_record)
        button_layout1.addWidget(self.delete_btn)
        
        self.refresh_btn = QPushButton("🔄 Refresh")
        self.refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.refresh_btn.clicked.connect(self.load_data)
        button_layout1.addWidget(self.refresh_btn)
        
        # Select All and Deselect All buttons
        self.select_all_btn = QPushButton("✅ Select All")
        self.select_all_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.select_all_btn.clicked.connect(self.table.selectAll)
        button_layout1.addWidget(self.select_all_btn)
        
        self.deselect_all_btn = QPushButton("❌ Deselect All")
        self.deselect_all_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.deselect_all_btn.clicked.connect(self.table.clearSelection)
        button_layout1.addWidget(self.deselect_all_btn)
        
        button_layout1.addStretch()
        self.layout.addLayout(button_layout1)
        
        # Button layout for data management
        button_layout2 = QHBoxLayout()
        button_layout2.setSpacing(10)
        
        self.import_btn = QPushButton("📥 Import Excel")
        self.import_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.import_btn.clicked.connect(self.import_data)
        button_layout2.addWidget(self.import_btn)
        
        self.export_btn = QPushButton("📤 Export Excel")
        self.export_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.export_btn.clicked.connect(self.export_data)
        button_layout2.addWidget(self.export_btn)
        
        button_layout2.addStretch()
        
        self.manage_users_btn = QPushButton("👥 Manage Users")
        self.manage_users_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.manage_users_btn.clicked.connect(self.manage_users)
        self.manage_users_btn.setEnabled(False)  # Disabled until admin login
        button_layout2.addWidget(self.manage_users_btn)
        
        self.layout.addLayout(button_layout2)
        
        # Enable Manage Users button if admin
        if role.lower() == 'admin':
            self.manage_users_btn.setEnabled(True)

        self.load_data()

    def load_data(self):
        """Fetch data from database and populate table"""
        try:
            conn = sqlite3.connect("data/app_database.db")
            cursor = conn.cursor()
            
            # Populate filter options (get unique values)
            self.populate_filter_options(cursor)
            
            # Build filter query
            query = "SELECT id, NO, CLIENT, LOCATION, CURRENCY, PROGRESS, IMAGE_PATH, PROJECT, GEMPHIL_DEVICE, DETAILS, CONTACT_PERSON, EMAIL FROM records WHERE 1=1"
            params = []
            
            # Apply filters
            if self.client_filter.currentText() != "All Clients":
                query += " AND CLIENT = ?"
                params.append(self.client_filter.currentText())
            
            if self.location_filter.currentText() != "All Locations":
                query += " AND LOCATION = ?"
                params.append(self.location_filter.currentText())
            
            if self.currency_filter.currentText() != "All Currencies":
                query += " AND CURRENCY = ?"
                params.append(self.currency_filter.currentText())
            
            if self.progress_filter.currentText() != "All Progress":
                query += " AND PROGRESS = ?"
                params.append(self.progress_filter.currentText())
            
            # Apply sorting
            if self.sort_column is not None:
                # Map column index to database column name
                column_map = {
                    0: "NO",
                    1: "CLIENT",
                    2: "LOCATION",
                    3: "CURRENCY",
                    4: "PROGRESS",
                    5: "IMAGE_PATH",
                    6: "PROJECT",
                    7: "GEMPHIL_DEVICE",
                    8: "DETAILS",
                    9: "CONTACT_PERSON",
                    10: "EMAIL"
                }
                
                # Columns that should be sorted numerically
                numeric_columns = {"NO", "PROJECT", "GEMPHIL_DEVICE"}
                
                sort_column = column_map.get(self.sort_column, "id")
                sort_order = "ASC" if self.sort_ascending else "DESC"
                
                # Use CAST to NUMERIC for numeric columns to ensure proper numeric sorting
                if sort_column in numeric_columns:
                    query += f" ORDER BY CAST({sort_column} AS NUMERIC) {sort_order}"
                else:
                    query += f" ORDER BY {sort_column} {sort_order}"
            else:
                query += " ORDER BY id ASC"
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            conn.close()

            self.table.setRowCount(len(rows))
            for row_idx, row_data in enumerate(rows):
                record_id = row_data[0]  # First column is the id
                
                # Display data columns (no checkbox column)
                for col_idx, col_data in enumerate(row_data[1:], start=0):
                    item = QTableWidgetItem(str(col_data) if col_data else "")
                    item.setData(1001, record_id)  # Store record_id as custom data
                    self.table.setItem(row_idx, col_idx, item)
            
            # Reset search filter after loading data
            self.search_input.blockSignals(True)
            self.search_input.clear()
            self.search_input.blockSignals(False)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load data: {str(e)}")
    
    def populate_filter_options(self, cursor):
        """Populate filter dropdowns with unique values from database"""
        try:
            # Get unique clients
            cursor.execute("SELECT DISTINCT CLIENT FROM records WHERE CLIENT IS NOT NULL AND CLIENT != '' ORDER BY CLIENT")
            clients = [row[0] for row in cursor.fetchall()]
            self.client_filter.blockSignals(True)
            current_client = self.client_filter.currentText()
            self.client_filter.clear()
            self.client_filter.addItem("All Clients")
            self.client_filter.addItems(clients)
            if current_client in clients or current_client == "All Clients":
                self.client_filter.setCurrentText(current_client)
            self.client_filter.blockSignals(False)
            
            # Get unique locations
            cursor.execute("SELECT DISTINCT LOCATION FROM records WHERE LOCATION IS NOT NULL AND LOCATION != '' ORDER BY LOCATION")
            locations = [row[0] for row in cursor.fetchall()]
            self.location_filter.blockSignals(True)
            current_location = self.location_filter.currentText()
            self.location_filter.clear()
            self.location_filter.addItem("All Locations")
            self.location_filter.addItems(locations)
            if current_location in locations or current_location == "All Locations":
                self.location_filter.setCurrentText(current_location)
            self.location_filter.blockSignals(False)
            
            # Get unique currencies
            cursor.execute("SELECT DISTINCT CURRENCY FROM records WHERE CURRENCY IS NOT NULL AND CURRENCY != '' ORDER BY CURRENCY")
            currencies = [row[0] for row in cursor.fetchall()]
            self.currency_filter.blockSignals(True)
            current_currency = self.currency_filter.currentText()
            self.currency_filter.clear()
            self.currency_filter.addItem("All Currencies")
            self.currency_filter.addItems(currencies)
            if current_currency in currencies or current_currency == "All Currencies":
                self.currency_filter.setCurrentText(current_currency)
            self.currency_filter.blockSignals(False)
            
            # Get unique progress values
            cursor.execute("SELECT DISTINCT PROGRESS FROM records WHERE PROGRESS IS NOT NULL AND PROGRESS != '' ORDER BY PROGRESS")
            progress_values = [row[0] for row in cursor.fetchall()]
            self.progress_filter.blockSignals(True)
            current_progress = self.progress_filter.currentText()
            self.progress_filter.clear()
            self.progress_filter.addItem("All Progress")
            self.progress_filter.addItems(progress_values)
            if current_progress in progress_values or current_progress == "All Progress":
                self.progress_filter.setCurrentText(current_progress)
            self.progress_filter.blockSignals(False)
        except Exception as e:
            print(f"Error populating filters: {str(e)}")
    
    def apply_filters(self):
        """Apply filters and reload data"""
        self.load_data()
    
    def clear_filters(self):
        """Clear all filters"""
        self.client_filter.setCurrentIndex(0)
        self.location_filter.setCurrentIndex(0)
        self.currency_filter.setCurrentIndex(0)
        self.progress_filter.setCurrentIndex(0)
        self.load_data()
    
    def on_header_click(self, column_index):
        """Handle header click for column sorting"""
        # If clicking the same column, toggle ascending/descending
        if self.sort_column == column_index:
            self.sort_ascending = not self.sort_ascending
        else:
            self.sort_column = column_index
            self.sort_ascending = True
        
        # Reload data with new sort order
        self.load_data()
        
        # Update header appearance to show sort direction
        self.update_header_appearance()
    
    def update_header_appearance(self):
        """Update header appearance to indicate sort direction"""
        header = self.table.horizontalHeader()
        column_labels = ['No.', 'Client', 'Location', 'Currency', 
                        'Progress', 'Image', 'Project', 
                        'Gemphil Device', 'Details', 'Contact', 'Email']
        
        for i, label in enumerate(column_labels):
            if i == self.sort_column:
                # Add indicator to show sort direction
                arrow = "▲" if self.sort_ascending else "▼"
                self.table.horizontalHeaderItem(i).setText(f"{label} {arrow}")
            else:
                self.table.horizontalHeaderItem(i).setText(label)
    
    def on_search_text_changed(self, search_text):
        """Handle real-time search filtering across all columns"""
        search_text = search_text.lower().strip()
        
        for row in range(self.table.rowCount()):
            # Check if any cell in this row contains the search text
            match_found = False
            
            if not search_text:
                # If search is empty, show all rows
                match_found = True
            else:
                for col in range(self.table.columnCount()):
                    item = self.table.item(row, col)
                    if item and search_text in item.text().lower():
                        match_found = True
                        break
            
            # Show or hide row based on match
            self.table.setRowHidden(row, not match_found)
    
    def clear_search(self):
        """Clear search input"""
        self.search_input.clear()
    
    def add_record(self):
        """Open dialog to add a new record"""
        dialog = AddEditRecordDialog(self)
        if dialog.exec():
            self.load_data()  # Refresh table after save
    
    def edit_record(self):
        """Open dialog to edit the selected record"""
        # Get all selected rows
        selected_rows = self.table.selectionModel().selectedRows()
        
        if not selected_rows:
            QMessageBox.warning(self, "Selection Error", "Please select a row to edit")
            return
        
        if len(selected_rows) > 1:
            QMessageBox.warning(self, "Multiple Selection Error", "Please select only one row to edit")
            return
        
        # Get the record_id from the first (and only) selected row
        row = selected_rows[0].row()
        item = self.table.item(row, 0)
        record_id = item.data(1001)  # Retrieve custom data
        
        dialog = AddEditRecordDialog(self, record_id=record_id)
        if dialog.exec():
            self.load_data()  # Refresh table after save
    
    def delete_record(self):
        """Delete the selected record(s) - supports multi-select with RBAC"""
        # Get all selected rows
        selected_rows = self.table.selectionModel().selectedRows()
        
        if not selected_rows:
            QMessageBox.warning(self, "Selection Error", "Please select at least one record to delete")
            return
        
        # Collect record IDs and client names
        record_ids = []
        client_names = []
        
        for model_index in selected_rows:
            row = model_index.row()
            item = self.table.item(row, 0)
            record_id = item.data(1001)
            client_name = self.table.item(row, 1).text()  # Column 1 is Client (no checkbox column)
            record_ids.append(record_id)
            client_names.append(client_name)
        
        # RBAC Check: If not admin, require admin verification
        if self.role.lower() != 'admin':
            # Show admin credential verification dialog
            admin_dialog = AdminCredentialDialog(self)
            if not admin_dialog.exec() or not admin_dialog.verified:
                QMessageBox.warning(self, "Access Denied", "Admin verification failed. Deletion cancelled.")
                return
        
        # Confirmation dialog
        if len(record_ids) == 1:
            confirm_msg = f"Are you sure you want to delete the record for '{client_names[0]}'?\nThis action cannot be undone."
            title = "Confirm Deletion"
        else:
            confirm_msg = f"Are you sure you want to delete {len(record_ids)} records?\n\n{', '.join(client_names[:5])}"
            if len(client_names) > 5:
                confirm_msg += f"\n... and {len(client_names) - 5} more"
            confirm_msg += "\n\nThis action cannot be undone."
            title = f"Confirm Deletion of {len(record_ids)} Records"
        
        reply = QMessageBox.question(
            self, 
            title, 
            confirm_msg,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                conn = sqlite3.connect("data/app_database.db")
                cursor = conn.cursor()
                
                # Delete all selected records
                for record_id in record_ids:
                    cursor.execute("DELETE FROM records WHERE id = ?", (record_id,))
                
                conn.commit()
                conn.close()
                
                deleted_count = len(record_ids)
                msg = f"Successfully deleted {deleted_count} record" if deleted_count == 1 else f"Successfully deleted {deleted_count} records"
                QMessageBox.information(self, "Success", msg + "!")
                self.load_data()  # Refresh table
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete record(s): {str(e)}")
    
    def import_data(self):
        """Import data from Excel file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Import Excel File", 
            "", 
            "Excel Files (*.xlsx *.xls);;All Files (*)"
        )
        
        if not file_path:
            return
        
        result = import_excel(file_path)
        
        if result['success']:
            QMessageBox.information(self, "Import Successful", result['message'])
            self.load_data()  # Refresh table
        else:
            QMessageBox.warning(self, "Import Failed", result['message'])
    
    def export_data(self):
        """Export data to Excel file - shows column selection dialog"""
        # Show column selection dialog
        column_dialog = ColumnSelectionDialog(self)
        if column_dialog.exec() != QDialog.DialogCode.Accepted:
            return  # User cancelled
        
        selected_columns = column_dialog.get_selected_columns()
        
        # Get selected rows
        selected_rows = self.table.selectionModel().selectedRows()
        
        # Collect record IDs to export
        record_ids_to_export = []
        
        if not selected_rows:
            # Handle "No selection" case: ask to export all visible
            reply = QMessageBox.question(
                self, 
                "Export Options", 
                "No rows selected. Would you like to export ALL visible rows?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel,
                QMessageBox.StandardButton.Cancel
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                # Export all visible rows (skip hidden rows from search filter)
                for row_idx in range(self.table.rowCount()):
                    # Skip hidden rows (filtered by search)
                    if not self.table.isRowHidden(row_idx):
                        item = self.table.item(row_idx, 0)
                        if item:
                            record_ids_to_export.append(item.data(1001))
                export_mode = f"All {len(record_ids_to_export)} visible rows"
            elif reply == QMessageBox.StandardButton.No:
                QMessageBox.information(self, "Selection Required", "Please select specific rows and try again.")
                return
            else:
                return  # Cancelled
        else:
            # Export only selected rows (in table order)
            for model_index in selected_rows:
                row = model_index.row()
                item = self.table.item(row, 0)
                record_id = item.data(1001)
                record_ids_to_export.append(record_id)
            export_mode = f"Selected {len(record_ids_to_export)} rows"
        
        if not record_ids_to_export:
            QMessageBox.warning(self, "Export Error", "No records to export")
            return
        
        save_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Excel File",
            "export.xlsx",
            "Excel Files (*.xlsx)"
        )
        
        if not save_path:
            return
        
        # Export with preserve_order=True to maintain table sort/filter order
        result = export_excel(record_ids=record_ids_to_export, selected_columns=selected_columns, save_path=save_path, preserve_order=True)
        
        if result['success']:
            QMessageBox.information(self, "Export Successful", f"Successfully exported {export_mode}:\n{result['message']}")
        else:
            QMessageBox.warning(self, "Export Failed", result['message'])
    
    def manage_users(self):
        """Open user management dialog - admin only"""
        if self.role.lower() != 'admin':
            QMessageBox.warning(self, "Access Denied", "Only administrators can manage users")
            return
        
        dialog = ManageUsersDialog(self)
        dialog.exec()

if __name__ == "__main__":
    # Initialize database before starting the app
    if not os.path.exists('data'):
        os.makedirs('data')
    
    initialize_database()
    create_default_admin()
    
    app = QApplication(sys.argv)
    login = LoginWindow()
    if login.exec():
        main_win = MainWindow(login.user_role)
        main_win.show()
        sys.exit(app.exec())