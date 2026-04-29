import sqlite3
import os
import shutil
from datetime import datetime
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox, QScrollArea,
                             QWidget, QFrame, QFileDialog)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from styles import DIALOG_STYLESHEET

class AddEditRecordDialog(QDialog):
    """Dialog for adding or editing a record in the database."""
    
    def __init__(self, parent=None, record_id=None):
        """
        Initialize the dialog.
        
        Args:
            parent: Parent widget
            record_id: If provided, loads and allows editing of existing record
        """
        super().__init__(parent)
        self.record_id = record_id
        self.setWindowTitle("Add New Record" if not record_id else "Edit Record")
        self.setFixedSize(550, 700)
        self.setStyleSheet(DIALOG_STYLESHEET)
        
        # Center the dialog
        self.move(150, 100)
        
        # Create UI
        self.init_ui()
        
        # If editing, load existing data
        if record_id:
            self.load_record_data()
    
    def init_ui(self):
        """Initialize the UI components."""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(15)
        
        # Title
        title_label = QLabel("Add New Record" if not self.record_id else "Edit Record Details")
        title_label.setStyleSheet("font-size: 14pt; font-weight: bold; color: #1B5E20;")
        main_layout.addWidget(title_label)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("background-color: #C8E6C9; height: 2px;")
        main_layout.addWidget(separator)
        
        # Create a scrollable area for the form
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: 1px solid #C8E6C9;
                border-radius: 4px;
                background-color: #F1F8F4;
            }
            QScrollBar:vertical {
                width: 10px;
                background-color: #F5FFF7;
            }
            QScrollBar::handle:vertical {
                background-color: #A5D6A7;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #81C784;
            }
        """)
        
        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        form_layout.setSpacing(15)
        form_layout.setContentsMargins(15, 15, 15, 15)
        
        # Define field labels and create input fields
        self.fields = {}
        field_names = [
            'NO', 'CLIENT', 'LOCATION', 'CURRENCY', 'PROGRESS', 
            'IMAGE_PATH', 'PROJECT', 'GEMPHIL_DEVICE', 
            'DETAILS', 'CONTACT_PERSON', 'EMAIL'
        ]
        
        for field_name in field_names:
            # Format label text (capitalize and replace underscores with spaces)
            label_text = field_name.replace('_', ' ').title()
            
            label = QLabel(label_text)
            label.setStyleSheet("font-weight: 500; color: #1E293B;")
            
            form_layout.addWidget(label)
            
            # Special handling for IMAGE_PATH field
            if field_name == 'IMAGE_PATH':
                # Create a custom layout for image field with browse button
                image_layout = QHBoxLayout()
                image_layout.setSpacing(8)
                
                input_field = QLineEdit()
                input_field.setPlaceholderText("Select an image file...")
                input_field.setMinimumHeight(32)
                input_field.setReadOnly(True)  # Read-only since file picker will populate it
                image_layout.addWidget(input_field)
                
                browse_button = QPushButton("📁 Browse")
                browse_button.setMaximumWidth(100)
                browse_button.setCursor(Qt.CursorShape.PointingHandCursor)
                browse_button.clicked.connect(self.browse_image_file)
                image_layout.addWidget(browse_button)
                
                clear_button = QPushButton("✕ Clear")
                clear_button.setMaximumWidth(80)
                clear_button.setCursor(Qt.CursorShape.PointingHandCursor)
                clear_button.clicked.connect(lambda: input_field.clear())
                image_layout.addWidget(clear_button)
                
                form_layout.addLayout(image_layout)
                
                self.fields[field_name] = input_field
            else:
                input_field = QLineEdit()
                input_field.setPlaceholderText(f"Enter {label_text.lower()}")
                input_field.setMinimumHeight(32)
                
                form_layout.addWidget(input_field)
                self.fields[field_name] = input_field
        
        form_layout.addStretch()
        scroll.setWidget(form_widget)
        main_layout.addWidget(scroll)
        
        # Separator
        separator2 = QFrame()
        separator2.setFrameShape(QFrame.Shape.HLine)
        separator2.setStyleSheet("background-color: #C8E6C9; height: 2px;")
        main_layout.addWidget(separator2)
        
        # Button layout
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        button_layout.setContentsMargins(0, 10, 0, 0)
        
        self.save_button = QPushButton("Save Record")
        self.save_button.setMinimumHeight(40)
        self.save_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.save_button.clicked.connect(self.save_record)
        button_layout.addWidget(self.save_button)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setObjectName("cancelBtn")
        self.cancel_button.setMinimumHeight(40)
        self.cancel_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)
        
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)
    
    def load_record_data(self):
        """Load existing record data into the form fields."""
        try:
            conn = sqlite3.connect("data/app_database.db", timeout=10.0)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT NO, CLIENT, LOCATION, CURRENCY, PROGRESS, IMAGE_PATH, 
                       PROJECT, GEMPHIL_DEVICE, DETAILS, CONTACT_PERSON, EMAIL 
                FROM records WHERE id = ?
            """, (self.record_id,))
            record = cursor.fetchone()
            conn.close()
            
            if record:
                field_names = [
                    'NO', 'CLIENT', 'LOCATION', 'CURRENCY', 'PROGRESS', 
                    'IMAGE_PATH', 'PROJECT', 'GEMPHIL_DEVICE', 
                    'DETAILS', 'CONTACT_PERSON', 'EMAIL'
                ]
                for idx, field_name in enumerate(field_names):
                    self.fields[field_name].setText(str(record[idx]) if record[idx] else "")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load record: {str(e)}")
    
    def browse_image_file(self):
        """Open file picker to select an image file."""
        try:
            # Create images folder if it doesn't exist
            images_dir = "data/images"
            if not os.path.exists(images_dir):
                os.makedirs(images_dir)
            
            # Open file picker
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Select Image File",
                "",
                "Image Files (*.png *.jpg *.jpeg *.bmp *.gif);;All Files (*)"
            )
            
            if not file_path:
                return
            
            # Generate unique filename to avoid conflicts
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_")
            original_name = os.path.basename(file_path)
            unique_filename = timestamp + original_name
            
            # Copy image to data/images folder
            destination_path = os.path.join(images_dir, unique_filename)
            shutil.copy2(file_path, destination_path)
            
            # Store relative path in the field
            relative_path = os.path.join(images_dir, unique_filename)
            self.fields['IMAGE_PATH'].setText(relative_path)
            
            QMessageBox.information(self, "Success", f"Image loaded: {original_name}")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load image: {str(e)}")
    
    
    def save_record(self):
        """Save the record to the database."""
        try:
            # Collect data from all fields
            data = {
                field_name: self.fields[field_name].text().strip() 
                for field_name in self.fields
            }
            
            # Basic validation
            if not data['CLIENT']:
                QMessageBox.warning(self, "Validation Error", "Client field cannot be empty")
                self.fields['CLIENT'].setFocus()
                return
            
            conn = sqlite3.connect("data/app_database.db", timeout=10.0)
            cursor = conn.cursor()
            
            if self.record_id:
                # Update existing record
                cursor.execute("""
                    UPDATE records 
                    SET NO = ?, CLIENT = ?, LOCATION = ?, CURRENCY = ?, PROGRESS = ?, 
                        IMAGE_PATH = ?, PROJECT = ?, GEMPHIL_DEVICE = ?, 
                        DETAILS = ?, CONTACT_PERSON = ?, EMAIL = ?
                    WHERE id = ?
                """, (
                    data['NO'], data['CLIENT'], data['LOCATION'], data['CURRENCY'],
                    data['PROGRESS'], data['IMAGE_PATH'], data['PROJECT'], data['GEMPHIL_DEVICE'],
                    data['DETAILS'], data['CONTACT_PERSON'], data['EMAIL'],
                    self.record_id
                ))
                message = "✓ Record updated successfully!"
            else:
                # Insert new record
                cursor.execute("""
                    INSERT INTO records 
                    (NO, CLIENT, LOCATION, CURRENCY, PROGRESS, IMAGE_PATH, PROJECT, 
                     GEMPHIL_DEVICE, DETAILS, CONTACT_PERSON, EMAIL)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    data['NO'], data['CLIENT'], data['LOCATION'], data['CURRENCY'],
                    data['PROGRESS'], data['IMAGE_PATH'], data['PROJECT'], data['GEMPHIL_DEVICE'],
                    data['DETAILS'], data['CONTACT_PERSON'], data['EMAIL']
                ))
                message = "✓ Record added successfully!"
            
            conn.commit()
            conn.close()
            
            QMessageBox.information(self, "Success", message)
            self.accept()  # Close dialog with success
            
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", f"Failed to save record: {str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
