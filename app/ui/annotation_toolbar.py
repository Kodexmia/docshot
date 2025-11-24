from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QToolButton, QColorDialog, 
    QInputDialog, QLabel, QVBoxLayout
)
from PyQt6.QtCore import Qt, QPoint, pyqtSignal
from PyQt6.QtGui import QIcon, QColor, QPalette, QPixmap, QPainter, QBrush
from app.ui.annotation_canvas import ToolType


class AnnotationToolbar(QWidget):
    """Floating toolbar with annotation tools"""
    
    tool_selected = pyqtSignal(ToolType, QColor, int)
    save_requested = pyqtSignal()
    cancel_requested = pyqtSignal()
    text_requested = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_color = QColor(255, 0, 0)  # Red
        self.current_width = 3
        
        # Window setup for floating toolbar
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint | 
            Qt.WindowType.Tool |
            Qt.WindowType.FramelessWindowHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.setup_ui()
        self.apply_style()
        
        # Make draggable
        self.dragging = False
        self.drag_position = QPoint()
    
    def setup_ui(self):
        """Create toolbar UI"""
        layout = QHBoxLayout()
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)
        
        # Tool buttons
        self.tool_buttons = {}
        
        tools = [
            (ToolType.ARROW, "➔", "Arrow (A)"),
            (ToolType.BOX, "▭", "Box (B)"),
            (ToolType.PEN, "✎", "Pen (P)"),
            (ToolType.TEXT, "T", "Text (T)"),
            # BLUR removed in V3.5.3 - was causing crashes
        ]
        
        for tool, icon, tooltip in tools:
            btn = QToolButton()
            btn.setText(icon)
            btn.setToolTip(tooltip)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, t=tool: self.select_tool(t))
            btn.setMinimumSize(40, 40)
            self.tool_buttons[tool] = btn
            layout.addWidget(btn)
        
        # Default to arrow
        self.tool_buttons[ToolType.ARROW].setChecked(True)
        
        # Separator
        separator = QLabel("|")
        separator.setStyleSheet("color: #666; font-size: 20px;")
        layout.addWidget(separator)
        
        # Color picker button
        self.color_btn = QToolButton()
        self.color_btn.setText("●")
        self.color_btn.setToolTip("Color")
        self.color_btn.clicked.connect(self.pick_color)
        self.color_btn.setMinimumSize(40, 40)
        self.update_color_button()
        layout.addWidget(self.color_btn)
        
        # Separator
        separator2 = QLabel("|")
        separator2.setStyleSheet("color: #666; font-size: 20px;")
        layout.addWidget(separator2)
        
        # Undo button
        undo_btn = QToolButton()
        undo_btn.setText("↶")
        undo_btn.setToolTip("Undo")
        undo_btn.setMinimumSize(40, 40)
        layout.addWidget(undo_btn)
        self.undo_btn = undo_btn
        
        # Save button
        save_btn = QToolButton()
        save_btn.setText("✓")
        save_btn.setToolTip("Save (Ctrl+S)")
        save_btn.clicked.connect(self.save_requested.emit)
        save_btn.setMinimumSize(40, 40)
        layout.addWidget(save_btn)
        
        # Cancel button
        cancel_btn = QToolButton()
        cancel_btn.setText("✕")
        cancel_btn.setToolTip("Cancel (Esc)")
        cancel_btn.clicked.connect(self.cancel_requested.emit)
        cancel_btn.setMinimumSize(40, 40)
        layout.addWidget(cancel_btn)
        
        self.setLayout(layout)
    
    def apply_style(self):
        """Apply modern island-style appearance"""
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(40, 40, 40, 230);
                border-radius: 8px;
                padding: 4px;
            }
            QToolButton {
                background-color: rgba(60, 60, 60, 180);
                color: white;
                border: 2px solid rgba(80, 80, 80, 150);
                border-radius: 6px;
                font-size: 18px;
                font-weight: bold;
                padding: 4px;
            }
            QToolButton:hover {
                background-color: rgba(80, 80, 80, 200);
                border: 2px solid rgba(100, 150, 255, 200);
            }
            QToolButton:checked {
                background-color: rgba(0, 120, 215, 220);
                border: 2px solid rgba(100, 180, 255, 255);
            }
            QLabel {
                color: #999;
                background: transparent;
                border: none;
            }
        """)
    
    def select_tool(self, tool: ToolType):
        """Select a tool and emit signal"""
        # Uncheck all other buttons
        for t, btn in self.tool_buttons.items():
            btn.setChecked(t == tool)
        
        # Text tool is handled differently - just emit the tool selection
        # The canvas will handle showing the dialog when user clicks
        self.tool_selected.emit(tool, self.current_color, self.current_width)
    
    def request_text_input(self):
        """Show text input dialog - called by canvas after click"""
        # Create dialog with proper styling
        dialog = QInputDialog(self)
        dialog.setWindowTitle("Add Text")
        dialog.setLabelText("Enter text to add:")
        dialog.setInputMode(QInputDialog.InputMode.TextInput)
        
        # CRITICAL FIX: Force light background with dark text
        dialog.setStyleSheet("""
            QInputDialog {
                background-color: white;
            }
            QLabel {
                color: black;
                font-size: 12px;
                background: transparent;
            }
            QLineEdit {
                background-color: white;
                color: black;
                border: 1px solid #ccc;
                padding: 5px;
                font-size: 12px;
            }
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                padding: 6px 20px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
        """)
        
        ok = dialog.exec()
        text = dialog.textValue()
        
        if ok and text:
            return text
        return None
    
    def pick_color(self):
        """Open color picker with light theme"""
        dialog = QColorDialog(self.current_color, self)
        dialog.setWindowTitle("Pick Color")
        
        # CRITICAL FIX: Comprehensive light theme for ALL color picker widgets
        dialog.setStyleSheet("""
            /* Main dialog */
            QColorDialog {
                background-color: #f0f0f0;
            }
            
            /* All widgets default to light */
            QWidget {
                background-color: #f0f0f0;
                color: black;
            }
            
            /* Labels */
            QLabel {
                color: black;
                background: transparent;
                font-size: 11px;
            }
            
            /* Input fields */
            QLineEdit, QSpinBox {
                background-color: white;
                color: black;
                border: 1px solid #ccc;
                padding: 3px;
                selection-background-color: #0078d4;
                selection-color: white;
            }
            
            /* Buttons */
            QPushButton {
                background-color: #e0e0e0;
                color: black;
                border: 1px solid #999;
                padding: 6px 16px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
            }
            QPushButton:pressed {
                background-color: #c0c0c0;
            }
            
            /* OK/Cancel buttons - special styling */
            QDialogButtonBox QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
            }
            QDialogButtonBox QPushButton:hover {
                background-color: #005a9e;
            }
            
            /* Color squares grid */
            QColorShower {
                background-color: white;
                border: 1px solid #999;
            }
            
            /* Luminosity picker */
            QColorLuminancePicker {
                background-color: white;
                border: 1px solid #999;
            }
            
            /* Color picker area */
            QColorPicker {
                background-color: white;
                border: 1px solid #999;
            }
            
            /* Group boxes */
            QGroupBox {
                background-color: #f0f0f0;
                color: black;
                border: 1px solid #ccc;
                margin-top: 6px;
                padding-top: 10px;
            }
            QGroupBox::title {
                color: black;
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
            }
        """)
        
        if dialog.exec():
            color = dialog.selectedColor()
            if color.isValid():
                self.current_color = color
                self.update_color_button()
                # Re-emit current tool with new color
                current_tool = self.get_current_tool()
                if current_tool:
                    self.tool_selected.emit(current_tool, self.current_color, self.current_width)
    
    def update_color_button(self):
        """Update color button appearance"""
        self.color_btn.setStyleSheet(f"""
            QToolButton {{
                background-color: {self.current_color.name()};
                color: white;
                border: 2px solid white;
                border-radius: 6px;
                font-size: 24px;
                font-weight: bold;
            }}
            QToolButton:hover {{
                border: 2px solid #0078d7;
            }}
        """)
    
    def get_current_tool(self) -> ToolType:
        """Get currently selected tool"""
        for tool, btn in self.tool_buttons.items():
            if btn.isChecked():
                return tool
        return ToolType.ARROW
    
    def mousePressEvent(self, event):
        """Start dragging toolbar"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
    
    def mouseMoveEvent(self, event):
        """Drag toolbar"""
        if self.dragging:
            self.move(event.globalPosition().toPoint() - self.drag_position)
    
    def mouseReleaseEvent(self, event):
        """Stop dragging"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
