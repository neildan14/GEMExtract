"""
Modern UI Styles and Themes for Project Manager
"""

# Color Palette
COLORS = {
    'primary': '#1E3A8A',      # Deep Blue
    'primary_light': '#3B82F6', # Bright Blue
    'secondary': '#0F766E',    # Teal
    'success': '#10B981',      # Green
    'danger': '#EF4444',       # Red
    'warning': '#F59E0B',      # Amber
    'dark_bg': '#0F172A',      # Very Dark Blue
    'light_bg': '#F8FAFC',     # Light Gray-Blue
    'white': '#FFFFFF',
    'text_dark': '#1E293B',    # Dark Slate
    'text_light': '#64748B',   # Medium Slate
    'border': '#E2E8F0',       # Light Border
    'hover': '#3B82F6',        # Hover Blue
}

# Main Application Stylesheet
MAIN_STYLESHEET = f"""
    QMainWindow {{
        background-color: {COLORS['light_bg']};
    }}
    
    QWidget {{
        background-color: {COLORS['light_bg']};
        color: {COLORS['text_dark']};
    }}
    
    QPushButton {{
        background-color: {COLORS['primary']};
        color: {COLORS['white']};
        border: none;
        border-radius: 6px;
        padding: 8px 16px;
        font-weight: bold;
        font-size: 11pt;
        min-height: 36px;
        margin: 4px 2px;
    }}
    
    QPushButton:hover {{
        background-color: {COLORS['primary_light']};
    }}
    
    QPushButton:pressed {{
        background-color: {COLORS['secondary']};
    }}
    
    QPushButton#addBtn {{
        background-color: {COLORS['success']};
    }}
    
    QPushButton#addBtn:hover {{
        background-color: #059669;
    }}
    
    QPushButton#deleteBtn {{
        background-color: {COLORS['danger']};
    }}
    
    QPushButton#deleteBtn:hover {{
        background-color: #DC2626;
    }}
    
    QTableWidget {{
        background-color: {COLORS['white']};
        alternate-background-color: #F1F5F9;
        gridline-color: #CBD5E1;
        border: 1px solid {COLORS['border']};
        border-radius: 4px;
    }}
    
    QTableWidget::item {{
        padding: 5px;
        border-right: 1px solid #E2E8F0;
        border-bottom: 1px solid #E2E8F0;
    }}
    
    QTableWidget::item:selected {{
        background-color: {COLORS['primary_light']};
        color: {COLORS['white']};
        border-right: 1px solid #2563EB;
        border-bottom: 1px solid #2563EB;
    }}
    
    QHeaderView::section {{
        background-color: {COLORS['primary']};
        color: {COLORS['white']};
        padding: 12px 8px;
        border: none;
        border-right: 1px solid rgba(255, 255, 255, 0.2);
        font-weight: bold;
        font-size: 10pt;
        min-height: 40px;
    }}
    
    QHeaderView::section:last {{
        border-right: none;
    }}
    
    QLineEdit {{
        background-color: {COLORS['white']};
        border: 1px solid {COLORS['border']};
        border-radius: 4px;
        padding: 8px;
        font-size: 10pt;
        selection-background-color: {COLORS['primary']};
    }}
    
    QLineEdit:focus {{
        border: 2px solid {COLORS['primary_light']};
    }}
    
    QLabel {{
        color: {COLORS['text_dark']};
        font-size: 10pt;
        font-weight: 500;
    }}
    
    QMessageBox {{
        background-color: {COLORS['light_bg']};
    }}
    
    QMessageBox QLabel {{
        color: {COLORS['text_dark']};
    }}
    
    QMessageBox QPushButton {{
        min-width: 60px;
    }}
    
    QScrollArea {{
        background-color: {COLORS['white']};
        border: 1px solid {COLORS['border']};
        border-radius: 4px;
    }}
"""

# Login Dialog Stylesheet
LOGIN_STYLESHEET = f"""
    QDialog {{
        background-color: {COLORS['primary']};
    }}
    
    QLabel#titleLabel {{
        color: {COLORS['white']};
        font-size: 18pt;
        font-weight: bold;
        margin-bottom: 10px;
    }}
    
    QLabel#infoLabel {{
        color: rgba(255, 255, 255, 0.8);
        font-size: 9pt;
    }}
    
    QLineEdit {{
        background-color: rgba(255, 255, 255, 0.9);
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-radius: 6px;
        padding: 10px;
        font-size: 10pt;
        color: {COLORS['text_dark']};
        selection-background-color: {COLORS['primary_light']};
    }}
    
    QLineEdit:focus {{
        border: 2px solid {COLORS['white']};
        background-color: {COLORS['white']};
    }}
    
    QPushButton {{
        background-color: {COLORS['success']};
        color: {COLORS['white']};
        border: none;
        border-radius: 6px;
        padding: 10px;
        font-weight: bold;
        font-size: 11pt;
        min-height: 40px;
    }}
    
    QPushButton:hover {{
        background-color: #059669;
    }}
    
    QPushButton:pressed {{
        background-color: #047857;
    }}
"""

# Dialog Stylesheet
DIALOG_STYLESHEET = f"""
    QDialog {{
        background-color: {COLORS['light_bg']};
    }}
    
    QLineEdit {{
        background-color: {COLORS['white']};
        border: 1px solid {COLORS['border']};
        border-radius: 4px;
        padding: 8px;
        font-size: 10pt;
        selection-background-color: {COLORS['primary']};
    }}
    
    QLineEdit:focus {{
        border: 2px solid {COLORS['primary_light']};
    }}
    
    QLabel {{
        color: {COLORS['text_dark']};
        font-size: 10pt;
        font-weight: 500;
        margin-top: 8px;
    }}
    
    QPushButton {{
        background-color: {COLORS['primary']};
        color: {COLORS['white']};
        border: none;
        border-radius: 6px;
        padding: 8px 16px;
        font-weight: bold;
        font-size: 10pt;
        min-height: 36px;
        min-width: 80px;
    }}
    
    QPushButton:hover {{
        background-color: {COLORS['primary_light']};
    }}
    
    QPushButton:pressed {{
        background-color: {COLORS['secondary']};
    }}
    
    QPushButton#cancelBtn {{
        background-color: {COLORS['text_light']};
    }}
    
    QPushButton#cancelBtn:hover {{
        background-color: {COLORS['text_dark']};
    }}
    
    QScrollArea {{
        background-color: {COLORS['white']};
        border: 1px solid {COLORS['border']};
        border-radius: 4px;
    }}
"""
