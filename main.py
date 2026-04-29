import sys
import sqlite3
import os
import bcrypt
import shutil                  # <-- Added for backups
from datetime import datetime  # <-- Added for backups
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTableWidget, 
                             QTableWidgetItem, QVBoxLayout, QHBoxLayout, QWidget, 
                             QPushButton, QMessageBox, QLabel, QFrame, QCheckBox, QFileDialog,
                             QComboBox, QDialog, QScrollArea, QLineEdit, QHeaderView)
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QPixmap, QIcon, QDesktopServices, QColor

# --- Matplotlib for Dashboard Analytics ---
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

# Local Modules
from login_ui import LoginWindow
from forms import AddEditRecordDialog
from styles import MAIN_STYLESHEET, COLORS
from database import initialize_database, create_default_admin
from data_manager import import_excel, export_excel

# --- Helper Dialogs ---

class ColumnSelectionDialog(QDialog):
    """Dialog for selecting which columns to export"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Export Options")
        self.setGeometry(100, 100, 400, 550)
        self.setStyleSheet(f"""
            QDialog {{ background-color: {COLORS['light_bg']}; }}
            QLabel {{ color: {COLORS['text_dark']}; font-weight: bold; }}
            QCheckBox {{ color: #334155; padding: 5px; }}
            QPushButton {{ background-color: {COLORS['primary']}; color: white; border: none; padding: 8px 16px; border-radius: 4px; font-weight: bold; }}
            QPushButton:hover {{ background-color: {COLORS['primary_light']}; }}
            QPushButton#actionBtn {{ background-color: #64748B; padding: 6px 12px; font-size: 10pt; }}
            QPushButton#actionBtn:hover {{ background-color: #475569; }}
        """)
        
        self.column_options = [
            ('NO', 'No.'), ('CLIENT', 'Client'), ('LOCATION', 'Location'),
            ('CURRENCY', 'Currency'), ('PROGRESS', 'Progress'), ('IMAGE_PATH', 'Image'),
            ('PROJECT', 'Project'), ('GEMPHIL_DEVICE', 'Gemphil Device'),
            ('DETAILS', 'Details'), ('CONTACT_PERSON', 'Contact Person'), ('EMAIL', 'Email')
        ]
        
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Select Columns to Export:"))
        
        actions_layout = QHBoxLayout()
        select_all_btn = QPushButton("✓ Select All")
        select_all_btn.setObjectName("actionBtn")
        select_all_btn.clicked.connect(self.select_all)
        
        deselect_all_btn = QPushButton("✗ Deselect All")
        deselect_all_btn.setObjectName("actionBtn")
        deselect_all_btn.clicked.connect(self.deselect_all)
        
        actions_layout.addWidget(select_all_btn)
        actions_layout.addWidget(deselect_all_btn)
        actions_layout.addStretch()
        layout.addLayout(actions_layout)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        self.checkboxes = {}
        for col_db, col_display in self.column_options:
            checkbox = QCheckBox(col_display)
            checkbox.setChecked(False) 
            self.checkboxes[col_db] = checkbox
            scroll_layout.addWidget(checkbox)
            
        scroll_area.setWidget(scroll_widget)
        layout.addWidget(scroll_area)
        
        options_layout = QVBoxLayout()
        self.sort_client_cb = QCheckBox("Sort alphabetically by Client")
        self.sort_client_cb.setStyleSheet(f"font-weight: bold; color: {COLORS['text_dark']}; margin-top: 5px;")
        options_layout.addWidget(self.sort_client_cb)
        layout.addLayout(options_layout)
        
        btn_layout = QHBoxLayout()
        ok_btn = QPushButton("Confirm Export")
        ok_btn.clicked.connect(self.accept)
        btn_layout.addWidget(ok_btn)
        layout.addLayout(btn_layout)

    def select_all(self):
        for cb in self.checkboxes.values():
            cb.setChecked(True)
            
    def deselect_all(self):
        for cb in self.checkboxes.values():
            cb.setChecked(False)

    def get_selected_columns(self):
        return [col for col, checkbox in self.checkboxes.items() if checkbox.isChecked()]
        
    def is_sort_by_client(self):
        return self.sort_client_cb.isChecked()

class AdminCredentialDialog(QDialog):
    """Admin verification dialog"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Admin Verification Required")
        self.setStyleSheet(f"""
            QDialog {{ background-color: {COLORS['light_bg']}; }}
            QLabel {{ color: {COLORS['text_dark']}; font-weight: bold; }}
            QLineEdit {{ padding: 8px; border: 1px solid #CBD5E1; border-radius: 4px; background-color: white; }}
            QPushButton {{ background-color: {COLORS['primary']}; color: white; border: none; padding: 8px 16px; border-radius: 4px; font-weight: bold; }}
        """)
        self.verified = False
        
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Admin Username:"))
        self.username_input = QLineEdit()
        layout.addWidget(self.username_input)
        
        layout.addWidget(QLabel("Admin Password:"))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.returnPressed.connect(self.verify_credentials)
        layout.addWidget(self.password_input)
        
        verify_btn = QPushButton("Verify")
        verify_btn.clicked.connect(self.verify_credentials)
        layout.addWidget(verify_btn)
    
    def verify_credentials(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        try:
            conn = sqlite3.connect("data/app_database.db", timeout=10.0)
            cursor = conn.cursor()
            cursor.execute("SELECT password_hash, role FROM users WHERE username = ?", (username,))
            result = cursor.fetchone()
            conn.close()
            
            if result and bcrypt.checkpw(password.encode(), result[0]) and result[1].lower() == 'admin':
                self.verified = True
                self.accept()
            else:
                QMessageBox.warning(self, "Verification Failed", "Invalid credentials or user is not admin")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Verification error: {str(e)}")

class ManageUsersDialog(QDialog):
    """Dialog for managing users (admin only)"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Manage Users")
        self.setGeometry(100, 100, 600, 500)
        
        self.setStyleSheet(f"""
            QDialog {{ background-color: {COLORS['light_bg']}; }}
            QLabel {{ color: {COLORS['text_dark']}; font-weight: bold; }}
            QLineEdit, QComboBox {{ padding: 8px; border: 1px solid #CBD5E1; border-radius: 4px; background-color: white; }}
            QPushButton {{ background-color: {COLORS['primary']}; color: white; border: none; padding: 8px 16px; border-radius: 4px; font-weight: bold; }}
            QPushButton:hover {{ background-color: {COLORS['primary_light']}; }}
        """)
        self.init_ui()
        self.load_users()
    
    def init_ui(self):
        main_layout = QVBoxLayout(self)
        
        add_layout = QHBoxLayout()
        self.new_username_input = QLineEdit()
        self.new_username_input.setPlaceholderText("Username")
        self.new_username_input.setMaxLength(30)
        add_layout.addWidget(self.new_username_input)
        
        self.new_password_input = QLineEdit()
        self.new_password_input.setPlaceholderText("Password")
        self.new_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.new_password_input.setMaxLength(50)
        add_layout.addWidget(self.new_password_input)
        
        self.new_role_combo = QComboBox()
        self.new_role_combo.addItems(["admin", "user"])
        add_layout.addWidget(self.new_role_combo)
        
        add_btn = QPushButton("Add User")
        add_btn.clicked.connect(self.add_user)
        add_layout.addWidget(add_btn)
        
        main_layout.addWidget(QLabel("➕ Add New User:"))
        main_layout.addLayout(add_layout)
        
        self.users_table = QTableWidget()
        self.users_table.setColumnCount(4)
        self.users_table.setHorizontalHeaderLabels(['Username', 'Role', 'Change Role', 'Delete'])
        self.users_table.horizontalHeader().setStretchLastSection(True)
        main_layout.addWidget(QLabel("👤 Existing Users:"))
        main_layout.addWidget(self.users_table)
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        main_layout.addWidget(close_btn)
        
    def load_users(self):
        conn = sqlite3.connect("data/app_database.db", timeout=10.0)
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, role FROM users ORDER BY username")
        users = cursor.fetchall()
        conn.close()
        
        self.users_table.setRowCount(len(users))
        self.users_table.verticalHeader().setDefaultSectionSize(50)
        
        for row_idx, (user_id, username, role) in enumerate(users):
            item = QTableWidgetItem(username)
            item.setData(1001, user_id)
            self.users_table.setItem(row_idx, 0, item)
            self.users_table.setItem(row_idx, 1, QTableWidgetItem(role))
            
            cell_btn_style = "margin: 4px; padding: 6px; border-radius: 4px; font-weight: bold; color: white; border: none;"
            
            change_btn = QPushButton("Change")
            change_btn.setStyleSheet(f"background-color: {COLORS['primary']}; {cell_btn_style}")
            change_btn.clicked.connect(lambda checked, rid=user_id, rn=username: self.change_role(rid, rn))
            self.users_table.setCellWidget(row_idx, 2, change_btn)
            
            del_btn = QPushButton("Delete")
            del_btn.setStyleSheet(f"background-color: #EF4444; {cell_btn_style}")
            del_btn.clicked.connect(lambda checked, rid=user_id, rn=username: self.delete_user(rid, rn))
            self.users_table.setCellWidget(row_idx, 3, del_btn)
            
            self.users_table.setRowHeight(row_idx, 70)

    def add_user(self):
        username = self.new_username_input.text().strip()
        password = self.new_password_input.text()
        role = self.new_role_combo.currentText()
        
        # --- Validation Checks ---
        if not username or not password: 
            QMessageBox.warning(self, "Validation Error", "Both username and password are required.")
            return
            
        if len(username) < 4:
            QMessageBox.warning(self, "Validation Error", "Username must be at least 4 characters long.")
            return
            
        if not username.isalnum():
            QMessageBox.warning(self, "Validation Error", "Username can only contain letters and numbers (no spaces).")
            return
            
        if len(password) < 8:
            QMessageBox.warning(self, "Validation Error", "Password must be at least 8 characters long.")
            return
        
        conn = sqlite3.connect("data/app_database.db", timeout=10.0)
        cursor = conn.cursor()
        
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            QMessageBox.warning(self, "Error", "Username already exists. Please choose a different one.")
            conn.close()
            return
            
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)", (username, hashed, role))
        conn.commit()
        conn.close()
        
        QMessageBox.information(self, "Success", f"User '{username}' has been successfully created.")
        
        self.new_username_input.clear()
        self.new_password_input.clear()
        self.load_users()

    def change_role(self, user_id, username):
        conn = sqlite3.connect("data/app_database.db", timeout=10.0)
        cursor = conn.cursor()
        cursor.execute("SELECT role FROM users WHERE id = ?", (user_id,))
        current_role = cursor.fetchone()[0]
        new_role = "user" if current_role.lower() == "admin" else "admin"
        
        msg = f"Change {username}'s role from '{current_role}' to '{new_role}'?\n\nThis will change their permissions in the system."
        if QMessageBox.question(
            self, 
            "Confirm Role Change", 
            msg,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        ) == QMessageBox.StandardButton.Yes:
            cursor.execute("UPDATE users SET role = ? WHERE id = ?", (new_role, user_id))
            conn.commit()
            QMessageBox.information(self, "Success", f"{username}'s role changed to {new_role}.")
            self.load_users()
        conn.close()

    def delete_user(self, user_id, username):
        msg = f"Are you sure you want to delete the user '{username}'?\n\nThis action cannot be undone and they will lose access to the system."
        if QMessageBox.critical(
            self, 
            "Confirm User Deletion", 
            msg,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        ) == QMessageBox.StandardButton.Yes:
            conn = sqlite3.connect("data/app_database.db", timeout=10.0)
            conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Success", f"User '{username}' has been deleted.")
            self.load_users()

# --- Core Data Management Dialog ---

class DataTableDialog(QDialog):
    def __init__(self, role, parent=None):
        super().__init__(parent)
        self.role = role
        self.setWindowTitle("Data Manager")
        self.resize(1100, 700)
        
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowMaximizeButtonHint | Qt.WindowType.WindowMinimizeButtonHint)
        
        self.setStyleSheet(f"""
            QDialog {{ background-color: {COLORS['light_bg']}; }}
            QTableWidget {{ background-color: white; alternate-background-color: #F5FFF7; }}
            QLabel {{ color: {COLORS['text_dark']}; font-weight: bold; }}
            QPushButton {{ background-color: {COLORS['primary']}; color: white; border-radius: 4px; padding: 6px 12px; font-weight: bold; border: none; }}
            QPushButton:hover {{ background-color: {COLORS['primary_light']}; }}
            QLineEdit, QComboBox {{ padding: 6px; border: 1px solid #CBD5E1; border-radius: 4px; color: {COLORS['text_dark']}; }}
        """)
        
        self.sort_column = None
        self.sort_ascending = True
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(15, 15, 15, 15)
        self.layout.setSpacing(12)
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        # Filters
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(12)
        filter_layout.setContentsMargins(0, 10, 0, 10)
        filter_layout.addWidget(QLabel("🔍 Filters:"))
        
        self.client_filter = QComboBox()
        self.client_filter.addItem("All Clients")
        self.client_filter.setMinimumHeight(32)
        self.client_filter.currentIndexChanged.connect(self.load_data)
        filter_layout.addWidget(QLabel("Client:"))
        filter_layout.addWidget(self.client_filter)
        
        self.location_filter = QComboBox()
        self.location_filter.addItem("All Locations")
        self.location_filter.setMinimumHeight(32)
        self.location_filter.currentIndexChanged.connect(self.load_data)
        filter_layout.addWidget(QLabel("Location:"))
        filter_layout.addWidget(self.location_filter)
        
        self.currency_filter = QComboBox()
        self.currency_filter.addItem("All Currencies")
        self.currency_filter.setMinimumHeight(32)
        self.currency_filter.currentIndexChanged.connect(self.load_data)
        filter_layout.addWidget(QLabel("Currency:"))
        filter_layout.addWidget(self.currency_filter)
        
        self.progress_filter = QComboBox()
        self.progress_filter.addItem("All Progress")
        self.progress_filter.setMinimumHeight(32)
        self.progress_filter.currentIndexChanged.connect(self.load_data)
        filter_layout.addWidget(QLabel("Progress:"))
        filter_layout.addWidget(self.progress_filter)
        
        clear_btn = QPushButton("Clear Filters")
        clear_btn.setMinimumHeight(32)
        clear_btn.clicked.connect(self.clear_filters)
        filter_layout.addWidget(clear_btn)
        filter_layout.addStretch()
        self.layout.addLayout(filter_layout)
        
        # Search
        search_layout = QHBoxLayout()
        search_layout.setSpacing(12)
        search_layout.setContentsMargins(0, 5, 0, 5)
        search_layout.addWidget(QLabel("🔎 Search:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search across all columns...")
        self.search_input.setMinimumHeight(32)
        self.search_input.textChanged.connect(self.on_search_text_changed)
        search_layout.addWidget(self.search_input)
        self.layout.addLayout(search_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(11)
        self.table.setHorizontalHeaderLabels(['No.', 'Client', 'Location', 'Currency', 'Progress', 'Image', 'Project', 'Gemphil Device', 'Details', 'Contact', 'Email'])
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.MultiSelection)
        
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().sectionClicked.connect(self.on_header_click)
        
        for col in range(11):
            self.table.setColumnWidth(col, 100)
        
        self.table.setWordWrap(True)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.table.verticalHeader().setDefaultSectionSize(50)
        
        # --- NEW: Connect double click to open files/links ---
        self.table.cellDoubleClicked.connect(self.on_cell_double_clicked)
        # -----------------------------------------------------
        
        self.layout.addWidget(self.table)
        
        # Actions
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)
        
        add_btn = QPushButton("➕ Add")
        add_btn.clicked.connect(self.add_record)
        add_btn.setMinimumHeight(40)
        
        edit_btn = QPushButton("✏️ Edit")
        edit_btn.clicked.connect(self.edit_record)
        edit_btn.setMinimumHeight(40)
        
        del_btn = QPushButton("🗑️ Delete")
        del_btn.clicked.connect(self.delete_record)
        del_btn.setMinimumHeight(40)
        del_btn.setStyleSheet("background-color: #EF4444;")
        
        import_btn = QPushButton("📥 Import")
        import_btn.clicked.connect(self.import_data)
        import_btn.setMinimumHeight(40)
        
        export_btn = QPushButton("📤 Export")
        export_btn.clicked.connect(self.export_data)
        export_btn.setMinimumHeight(40)
        
        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(edit_btn)
        btn_layout.addWidget(del_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(import_btn)
        btn_layout.addWidget(export_btn)
        self.layout.addLayout(btn_layout)

    def load_data(self):
        try:
            conn = sqlite3.connect("data/app_database.db", timeout=10.0)
            cursor = conn.cursor()
            
            self.populate_filter_options(cursor)
            
            query = "SELECT id, NO, CLIENT, LOCATION, CURRENCY, PROGRESS, IMAGE_PATH, PROJECT, GEMPHIL_DEVICE, DETAILS, CONTACT_PERSON, EMAIL FROM records WHERE 1=1"
            params = []
            
            if self.client_filter.currentText() != "All Clients":
                query += " AND CLIENT = ?"; params.append(self.client_filter.currentText())
            if self.location_filter.currentText() != "All Locations":
                query += " AND LOCATION = ?"; params.append(self.location_filter.currentText())
            if self.currency_filter.currentText() != "All Currencies":
                query += " AND CURRENCY = ?"; params.append(self.currency_filter.currentText())
            if self.progress_filter.currentText() != "All Progress":
                query += " AND PROGRESS = ?"; params.append(self.progress_filter.currentText())
                
            if self.sort_column is not None:
                col_map = {0:"NO", 1:"CLIENT", 2:"LOCATION", 3:"CURRENCY", 4:"PROGRESS", 5:"IMAGE_PATH", 6:"PROJECT", 7:"GEMPHIL_DEVICE", 8:"DETAILS", 9:"CONTACT_PERSON", 10:"EMAIL"}
                sort_col = col_map.get(self.sort_column, "id")
                order = "ASC" if self.sort_ascending else "DESC"
                if sort_col in {"NO", "PROJECT", "GEMPHIL_DEVICE"}:
                    query += f" ORDER BY CAST({sort_col} AS NUMERIC) {order}"
                else:
                    query += f" ORDER BY {sort_col} {order}"
            else:
                query += " ORDER BY id ASC"
                
            cursor.execute(query, params)
            rows = cursor.fetchall()
            conn.close()
            
            self.table.setRowCount(len(rows))
            for row_idx, row_data in enumerate(rows):
                record_id = row_data[0]
                for col_idx, col_data in enumerate(row_data[1:]):
                    text_val = str(col_data) if col_data else ""
                    item = QTableWidgetItem(text_val)
                    item.setData(1001, record_id)
                    
                    # --- NEW: Style links to look clickable ---
                    # Check if it's the Image column (idx 5) OR if the text is a web link
                    if text_val and (col_idx == 5 or text_val.startswith('http') or text_val.startswith('www.')):
                        item.setForeground(QColor("#2563EB")) # Standard link blue
                        font = item.font()
                        font.setUnderline(True)
                        item.setFont(font)
                        item.setToolTip("Double-click to open file/link")
                    # ------------------------------------------
                    
                    self.table.setItem(row_idx, col_idx, item)
            
            self.update_header_appearance()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load data: {str(e)}")

    def populate_filter_options(self, cursor):
        def update_combo(combo, col_name, default_text):
            cursor.execute(f"SELECT DISTINCT {col_name} FROM records WHERE {col_name} IS NOT NULL AND {col_name} != '' ORDER BY {col_name}")
            items = [r[0] for r in cursor.fetchall()]
            combo.blockSignals(True)
            curr = combo.currentText()
            combo.clear(); combo.addItem(default_text); combo.addItems(items)
            if curr in items or curr == default_text: combo.setCurrentText(curr)
            combo.blockSignals(False)

        update_combo(self.client_filter, "CLIENT", "All Clients")
        update_combo(self.location_filter, "LOCATION", "All Locations")
        update_combo(self.currency_filter, "CURRENCY", "All Currencies")
        update_combo(self.progress_filter, "PROGRESS", "All Progress")

    def clear_filters(self):
        self.client_filter.setCurrentIndex(0)
        self.location_filter.setCurrentIndex(0)
        self.currency_filter.setCurrentIndex(0)
        self.progress_filter.setCurrentIndex(0)
        self.load_data()

    def on_search_text_changed(self, text):
        text = text.lower().strip()
        for row in range(self.table.rowCount()):
            match = not text or any(text in self.table.item(row, col).text().lower() for col in range(self.table.columnCount()))
            self.table.setRowHidden(row, not match)

    def on_cell_double_clicked(self, row, col):
        """Opens local files or web links when a cell is double-clicked."""
        item = self.table.item(row, col)
        if not item: return
        
        path = item.text().strip()
        if not path: return
        
        # 1. Handle Web Links (Google Drive, websites, etc.)
        if path.startswith('http://') or path.startswith('https://') or path.startswith('www.'):
            # Ensure it has http:// if they only typed www.
            url = path if path.startswith('http') else 'http://' + path
            QDesktopServices.openUrl(QUrl(url))
            return
            
        # 2. Handle Local Files (Images, PDFs, Excel files, etc.)
        # We check if it's the Image column (col 5) or if it looks like a file path
        if col == 5 or "\\" in path or "/" in path:
            # Convert to absolute path so Windows knows exactly where it is
            abs_path = os.path.abspath(path)
            
            if os.path.exists(abs_path):
                # Open the file in its default Windows application
                QDesktopServices.openUrl(QUrl.fromLocalFile(abs_path))
            else:
                QMessageBox.warning(
                    self, 
                    "File Not Found", 
                    f"Could not find the file on this computer or network:\n\n{abs_path}"
                )

    def on_header_click(self, col):
        self.sort_ascending = not self.sort_ascending if self.sort_column == col else True
        self.sort_column = col
        self.load_data()

    def update_header_appearance(self):
        labels = ['No.', 'Client', 'Location', 'Currency', 'Progress', 'Image', 'Project', 'Gemphil Device', 'Details', 'Contact', 'Email']
        for i, label in enumerate(labels):
            if i == self.sort_column:
                self.table.horizontalHeaderItem(i).setText(f"{label} {'▲' if self.sort_ascending else '▼'}")
            else:
                self.table.horizontalHeaderItem(i).setText(label)

    def add_record(self):
        if AddEditRecordDialog(self).exec(): self.load_data()

    def edit_record(self):
        selected = self.table.selectionModel().selectedRows()
        if not selected or len(selected) > 1:
            QMessageBox.warning(self, "Selection", "Please select exactly one row to edit.")
            return
        record_id = self.table.item(selected[0].row(), 0).data(1001)
        if AddEditRecordDialog(self, record_id=record_id).exec(): self.load_data()

    def delete_record(self):
        selected = self.table.selectionModel().selectedRows()
        if not selected: 
            QMessageBox.warning(self, "No Selection", "Please select at least one record to delete.")
            return
        
        if self.role.lower() != 'admin':
            dlg = AdminCredentialDialog(self)
            if not dlg.exec() or not dlg.verified: 
                QMessageBox.warning(self, "Verification Failed", "Admin verification required to delete records.")
                return
        
        num_records = len(selected)
        if num_records == 1:
            client = self.table.item(selected[0].row(), 1).text()
            msg = f"Are you sure you want to delete this record?\n\nClient: {client}\n\nThis action cannot be undone."
        else:
            msg = f"Are you sure you want to delete {num_records} records?\n\nThis action cannot be undone."
        
        reply = QMessageBox.critical(
            self, 
            "Confirm Deletion", 
            msg,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                conn = sqlite3.connect("data/app_database.db", timeout=10.0)
                for model_index in selected:
                    record_id = self.table.item(model_index.row(), 0).data(1001)
                    conn.execute("DELETE FROM records WHERE id = ?", (record_id,))
                conn.commit()
                conn.close()
                QMessageBox.information(self, "Success", f"{num_records} record(s) deleted successfully.")
                self.load_data()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete records: {str(e)}")

    def import_data(self):
        path, _ = QFileDialog.getOpenFileName(self, "Import Excel", "", "Excel Files (*.xlsx *.xls)")
        if path:
            res = import_excel(path)
            if res['success']: QMessageBox.information(self, "Success", res['message'])
            else: QMessageBox.warning(self, "Failed", res['message'])
            self.load_data()

    def export_data(self):
        dlg = ColumnSelectionDialog(self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            cols = dlg.get_selected_columns()
            sort_by_client = dlg.is_sort_by_client()
            
            if not cols:
                return QMessageBox.warning(self, "Export Error", "No columns selected to export.")
                
            selected = self.table.selectionModel().selectedRows()
            
            if selected:
                rows_to_export = [m.row() for m in selected]
            else:
                rows_to_export = [r for r in range(self.table.rowCount()) if not self.table.isRowHidden(r)]
            
            if sort_by_client:
                def get_client_text(row_idx):
                    item = self.table.item(row_idx, 1)
                    return item.text().lower() if item else ""
                rows_to_export.sort(key=get_client_text)
                
            ids = [self.table.item(r, 0).data(1001) for r in rows_to_export]
            
            if not ids: return QMessageBox.warning(self, "Error", "No records to export.")
            
            path, _ = QFileDialog.getSaveFileName(self, "Export", "export.xlsx", "Excel (*.xlsx)")
            if path:
                res = export_excel(record_ids=ids, selected_columns=cols, save_path=path, preserve_order=True)
                QMessageBox.information(self, "Export", res['message'] if res['success'] else f"Failed: {res['message']}")


# --- Dashboard Window ---

# --- Dashboard Window ---

class MainWindow(QMainWindow):
    def __init__(self, role):
        super().__init__()
        self.role = role
        self.logged_out = False 
        
        self.setWindowTitle("GEMExtract Dashboard")
        # Bumped height to 550 to give the chart more room to breathe
        self.setFixedSize(850, 550) 
        self.setStyleSheet(MAIN_STYLESHEET)
        
        central = QWidget()
        self.setCentralWidget(central)
        
        # We use a horizontal layout to split the dashboard (Left: Data/Chart, Right: Actions)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(30)
        
        # --- LEFT PANEL: Text, Logo & Analytics ---
        left_layout = QVBoxLayout()
        left_layout.setSpacing(10) # Tighter vertical spacing
        
        # 1. LOGO
        self.logo_label = QLabel()
        logo_path = os.path.join("data", "images", "Gemphil.png")
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            
            # 1. CHANGE THIS: Increase the width (e.g., from 80 to 150)
            scaled_pixmap = pixmap.scaledToWidth(400, Qt.TransformationMode.SmoothTransformation)
            
            self.logo_label.setPixmap(scaled_pixmap)
            self.logo_label.setAlignment(Qt.AlignmentFlag.AlignLeft) 
            
            # 2. CHANGE THIS: Increase the maximum height to match your new width 
            # so the layout doesn't cut off the bottom of the larger image
            self.logo_label.setMaximumHeight(400) 
        
        left_layout.addWidget(self.logo_label)
        
        # 2. GREETING
        greeting = QLabel(f"Welcome back, {role.capitalize()}!")
        greeting.setStyleSheet(f"font-size: 20pt; font-weight: bold; color: {COLORS['text_dark']};")
        greeting.setMaximumHeight(40) # Prevents stretching
        left_layout.addWidget(greeting)
        
        # 3. STATS
        self.stats_label = QLabel()
        self.stats_label.setStyleSheet("font-size: 14pt; color: #64748B; background: #E2E8F0; padding: 15px; border-radius: 8px;")
        self.stats_label.setMaximumHeight(60) # Prevents stretching
        left_layout.addWidget(self.stats_label)
        
        # 4. CHART CANVAS
        self.figure = Figure(dpi=100) # Removed fixed figsize to let layout control it
        self.figure.patch.set_facecolor(COLORS['light_bg']) 
        self.canvas = FigureCanvasQTAgg(self.figure)
        # By setting stretch=1, ALL empty vertical space is given exclusively to the chart
        left_layout.addWidget(self.canvas, stretch=1) 
        
        
        # --- RIGHT PANEL: Action Buttons ---
        right_layout = QVBoxLayout()
        right_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        view_btn = QPushButton("📊 View Data Manager")
        view_btn.setMinimumHeight(60)
        view_btn.clicked.connect(self.open_data_manager)
        right_layout.addWidget(view_btn)
        
        quick_actions_layout = QHBoxLayout()
        import_btn = QPushButton("📥 Quick Import")
        import_btn.setMinimumHeight(45)
        import_btn.clicked.connect(self.quick_import)
        quick_actions_layout.addWidget(import_btn)
        
        export_btn = QPushButton("📤 Quick Export")
        export_btn.setMinimumHeight(45)
        export_btn.clicked.connect(self.quick_export)
        quick_actions_layout.addWidget(export_btn)
        right_layout.addLayout(quick_actions_layout)
        
        if self.role == 'admin':
            manage_btn = QPushButton("👥 Manage Users")
            manage_btn.setMinimumHeight(50)
            manage_btn.clicked.connect(self.manage_users)
            right_layout.addWidget(manage_btn)
            
            backup_btn = QPushButton("💾 Backup Database")
            backup_btn.setMinimumHeight(50)
            backup_btn.setStyleSheet("background-color: #F59E0B;") 
            backup_btn.clicked.connect(self.backup_database)
            right_layout.addWidget(backup_btn)
            
        logout_btn = QPushButton("🚪 Logout")
        logout_btn.setMinimumHeight(50)
        logout_btn.setStyleSheet("background-color: #EF4444;")
        logout_btn.clicked.connect(self.process_logout) 
        right_layout.addWidget(logout_btn)
        
        main_layout.addLayout(left_layout, stretch=2)
        main_layout.addLayout(right_layout, stretch=1)
        
        self.update_dashboard_data()

    def update_dashboard_data(self):
        """Updates both the total records label and the visual chart"""
        try:
            conn = sqlite3.connect("data/app_database.db", timeout=10.0)
            cursor = conn.cursor()
            
            count = cursor.execute("SELECT COUNT(*) FROM records").fetchone()[0]
            self.stats_label.setText(f"Total Records: {count}")
            
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.set_facecolor(COLORS['light_bg']) 
            
            cursor.execute('''
                SELECT CLIENT, COUNT(*) as count 
                FROM records 
                WHERE CLIENT IS NOT NULL AND TRIM(CLIENT) != '' 
                GROUP BY CLIENT 
                ORDER BY count DESC 
                LIMIT 5
            ''')
            results = cursor.fetchall()
            conn.close()
            
            if not results:
                ax.text(0.5, 0.5, "No client data available to graph.", 
                        ha='center', va='center', fontsize=12, color=COLORS['text_dark'])
                ax.axis('off')
            else:
                clients = [r[0][:15] + ('...' if len(r[0]) > 15 else '') for r in results]
                counts = [r[1] for r in results]
                
                clients.reverse()
                counts.reverse()
                
                bars = ax.barh(clients, counts, color=COLORS['primary'])
                ax.set_title('Top 5 Clients', fontsize=14, fontweight='bold', color=COLORS['text_dark'], pad=15)
                ax.tick_params(colors=COLORS['text_dark'], labelsize=10)
                
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.spines['bottom'].set_visible(False)
                ax.spines['left'].set_color(COLORS['text_dark'])
                ax.xaxis.set_visible(False) 
                
                for bar in bars:
                    width = bar.get_width()
                    ax.text(width + 0.1, bar.get_y() + bar.get_height()/2, 
                            f'{int(width)}', ha='left', va='center', 
                            color=COLORS['text_dark'], fontweight='bold')
                            
                # --- NEW FIX: Explicitly set margins so nothing is ever cut off ---
                self.figure.subplots_adjust(left=0.35, right=0.90, top=0.85, bottom=0.05)
                
            self.canvas.draw()
            
        except Exception as e:
            print(f"Chart Error: {e}")

    def open_data_manager(self):
        dialog = DataTableDialog(self.role, self)
        dialog.exec()
        self.update_dashboard_data()

    def manage_users(self):
        ManageUsersDialog(self).exec()

    def quick_import(self):
        path, _ = QFileDialog.getOpenFileName(self, "Quick Import Excel", "", "Excel Files (*.xlsx *.xls)")
        if path:
            res = import_excel(path)
            if res['success']: 
                QMessageBox.information(self, "Success", res['message'])
                self.update_dashboard_data()
            else: 
                QMessageBox.warning(self, "Failed", res['message'])

    def quick_export(self):
        dlg = ColumnSelectionDialog(self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            cols = dlg.get_selected_columns()
            sort_by_client = dlg.is_sort_by_client()
            
            if not cols:
                return QMessageBox.warning(self, "Export Error", "No columns selected to export.")
                
            try:
                conn = sqlite3.connect("data/app_database.db", timeout=10.0)
                count = conn.execute("SELECT COUNT(*) FROM records").fetchone()[0]
                conn.close()
                if count == 0:
                    return QMessageBox.warning(self, "Error", "No records available to export.")
            except: pass
                
            path, _ = QFileDialog.getSaveFileName(self, "Quick Export", "export.xlsx", "Excel (*.xlsx)")
            if path:
                if sort_by_client:
                    conn = sqlite3.connect("data/app_database.db", timeout=10.0)
                    cursor = conn.cursor()
                    cursor.execute("SELECT id FROM records ORDER BY CLIENT COLLATE NOCASE ASC")
                    record_ids = [r[0] for r in cursor.fetchall()]
                    conn.close()
                    res = export_excel(record_ids=record_ids, selected_columns=cols, save_path=path, preserve_order=True)
                else:
                    res = export_excel(record_ids=None, selected_columns=cols, save_path=path)
                
                if res['success']:
                    QMessageBox.information(self, "Export", res['message'])
                else:
                    QMessageBox.warning(self, "Export Failed", f"Failed: {res['message']}")

    def backup_database(self):
        """Creates a timestamped copy of the database file."""
        try:
            backup_dir = "data/backups"
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
                
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"backup_{timestamp}.db"
            backup_path = os.path.join(backup_dir, backup_filename)
            
            source_db = "data/app_database.db"
            if os.path.exists(source_db):
                shutil.copy2(source_db, backup_path)
                QMessageBox.information(
                    self, 
                    "Backup Successful", 
                    f"Database safely backed up!\n\nSaved as: {backup_filename}\nLocation: {backup_path}"
                )
            else:
                QMessageBox.warning(self, "Backup Failed", "The main database file could not be found.")
                
        except Exception as e:
            QMessageBox.critical(self, "Backup Error", f"An error occurred during backup:\n{str(e)}")

    def process_logout(self):
        confirm = QMessageBox.question(
            self, 
            "Confirm Logout", 
            "Are you sure you want to log out?", 
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if confirm == QMessageBox.StandardButton.Yes:
            self.logged_out = True
            self.close()


# --- Entry Point ---

if __name__ == "__main__":
    # --- NEW: Force the app to always look in the correct folder ---
    if getattr(sys, 'frozen', False):
        # If running as a compiled .exe
        os.chdir(os.path.dirname(sys.executable))
    else:
        # If running as a Python script
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
    # ---------------------------------------------------------------

    if not os.path.exists('data'):
        os.makedirs('data')
    
    initialize_database()
    create_default_admin()
    
    app = QApplication(sys.argv)
    
    # Set the global window icon
    icon_path = os.path.join("data", "images", "Logo.ico")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    
    while True:
        login = LoginWindow()
        if login.exec() == QDialog.DialogCode.Accepted:
            main_win = MainWindow(login.user_role)
            main_win.show()
            app.exec()
            
            if main_win.logged_out:
                continue
            else:
                break 
        else:
            break 
            
    sys.exit(0)