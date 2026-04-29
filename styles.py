"""
Modern UI Styles and Themes for Project Manager
"""

# Color Palette - Green Theme for GEMPHIL Technologies, Inc.
COLORS = {
    'primary': '#1B5E20',      # Deep Green (Primary)
    'primary_light': '#2E7D32', # Medium-Dark Green
    'secondary': '#388E3C',    # Medium Green
    'success': '#4CAF50',      # Bright Green
    'danger': '#EF4444',       # Red
    'warning': '#F59E0B',      # Amber
    'dark_bg': '#0D3817',      # Very Dark Green
    'light_bg': '#80d15a',     # Light Green Background
    'white': '#FFFFFF',
    'text_dark': '#0D3817',    # Dark Green
    'text_light': '#4B5563',   # Medium-Light Green
    'border': '#C8E6C9',       # Light Green Border
    'hover': '#43A047',        # Hover Green
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
        background-color: {COLORS['hover']};
    }}
    
    QPushButton#deleteBtn {{
        background-color: {COLORS['danger']};
    }}
    
    QPushButton#deleteBtn:hover {{
        background-color: #DC2626;
    }}
    
    QTableWidget {{
        background-color: {COLORS['white']};
        alternate-background-color: #F5FFF7;
        gridline-color: #C8E6C9;
        border: 1px solid {COLORS['border']};
        border-radius: 4px;
    }}
    
    QTableWidget::item {{
        padding: 8px;
        border-right: 1px solid {COLORS['border']};
        border-bottom: 1px solid {COLORS['border']};
    }}
    
    QTableWidget::item:selected {{
        background-color: {COLORS['primary_light']};
        color: {COLORS['white']};
        border-right: 1px solid {COLORS['primary']};
        border-bottom: 1px solid {COLORS['primary']};
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
        background-color: {COLORS['hover']};
    }}
    
    QPushButton:pressed {{
        background-color: {COLORS['secondary']};
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
