"""
Entry editor dialog for editing existing entries
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QTextEdit, QComboBox, QPushButton, QFormLayout, QSpinBox,
    QDialogButtonBox, QGroupBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from app.core.models import Entry


class EntryEditorDialog(QDialog):
    """Dialog for editing entry details and number"""
    
    def __init__(self, entry: Entry, entry_number: int, parent=None):
        super().__init__(parent)
        self.entry = entry
        self.original_number = entry_number
        self.new_number = entry_number
        
        self.setWindowTitle(f"Edit Entry #{entry_number}")
        self.setMinimumWidth(600)
        self.setMinimumHeight(500)
        
        self.setup_ui()
        self.load_entry_data()
    
    def setup_ui(self):
        """Setup the dialog UI"""
        layout = QVBoxLayout(self)
        
        # Entry Number Section
        number_group = QGroupBox("Entry Number")
        number_layout = QHBoxLayout()
        
        number_layout.addWidget(QLabel("Entry #:"))
        self.spin_number = QSpinBox()
        self.spin_number.setMinimum(1)
        self.spin_number.setMaximum(9999)
        self.spin_number.setValue(self.original_number)
        self.spin_number.setToolTip("Change the entry number (affects display order)")
        number_layout.addWidget(self.spin_number)
        
        number_layout.addWidget(QLabel("Current: "))
        self.lbl_current = QLabel(f"#{self.original_number}")
        self.lbl_current.setStyleSheet("color: #666; font-weight: bold;")
        number_layout.addWidget(self.lbl_current)
        
        number_layout.addStretch()
        number_group.setLayout(number_layout)
        layout.addWidget(number_group)
        
        # Entry Details Section
        details_group = QGroupBox("Entry Details")
        form_layout = QFormLayout()
        
        # Title
        self.txt_title = QLineEdit()
        self.txt_title.setPlaceholderText("Enter a descriptive title...")
        form_layout.addRow("Title:", self.txt_title)
        
        # Details (quick summary)
        self.txt_details = QTextEdit()
        self.txt_details.setMaximumHeight(80)
        self.txt_details.setPlaceholderText("Quick summary (2-3 lines)...")
        form_layout.addRow("Details:", self.txt_details)
        
        # Location Type
        self.combo_location_type = QComboBox()
        self.combo_location_type.addItems([
            "Web", "App", "Mobile", "Desktop", "Other"
        ])
        form_layout.addRow("Type:", self.combo_location_type)
        
        # Location URL
        self.txt_location_url = QLineEdit()
        self.txt_location_url.setPlaceholderText("https://example.com or /path/to/file")
        form_layout.addRow("Location:", self.txt_location_url)
        
        # Layout
        self.combo_layout = QComboBox()
        self.combo_layout.addItems(["image-left", "image-top"])
        form_layout.addRow("Layout:", self.combo_layout)
        
        details_group.setLayout(form_layout)
        layout.addWidget(details_group)
        
        # Notes Section
        notes_group = QGroupBox("Notes")
        notes_layout = QVBoxLayout()
        
        self.txt_notes = QTextEdit()
        self.txt_notes.setPlaceholderText("Detailed notes, observations, steps...")
        notes_layout.addWidget(self.txt_notes)
        
        notes_group.setLayout(notes_layout)
        layout.addWidget(notes_group)
        
        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | 
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        # Info label
        info_label = QLabel(
            "💡 Tip: Changing the entry number will reorder entries in exports"
        )
        info_label.setStyleSheet("color: #0078d4; font-style: italic; padding: 8px;")
        layout.addWidget(info_label)
    
    def load_entry_data(self):
        """Load entry data into form fields"""
        self.txt_title.setText(self.entry.title)
        self.txt_details.setPlainText(self.entry.details if self.entry.details else "")
        self.txt_notes.setPlainText(self.entry.notes if self.entry.notes else "")
        self.txt_location_url.setText(self.entry.location_url if self.entry.location_url else "")
        
        # Set location type
        location_type = self.entry.location_type if self.entry.location_type else "other"
        location_type_capitalized = location_type.capitalize() if location_type != "other" else "Other"
        index = self.combo_location_type.findText(location_type_capitalized)
        if index >= 0:
            self.combo_location_type.setCurrentIndex(index)
        
        # Set layout
        layout = self.entry.layout if hasattr(self.entry, 'layout') else "image-left"
        index = self.combo_layout.findText(layout)
        if index >= 0:
            self.combo_layout.setCurrentIndex(index)
    
    def get_updated_entry(self):
        """Get the entry with updated values
        
        Returns:
            tuple: (updated_entry, new_number)
        """
        # Update entry fields
        self.entry.title = self.txt_title.text()
        self.entry.details = self.txt_details.toPlainText()
        self.entry.notes = self.txt_notes.toPlainText()
        self.entry.location_url = self.txt_location_url.text()
        self.entry.location_type = self.combo_location_type.currentText().lower()
        
        if hasattr(self.entry, 'layout'):
            self.entry.layout = self.combo_layout.currentText()
        
        self.new_number = self.spin_number.value()
        
        return self.entry, self.new_number


class QuickRenumberDialog(QDialog):
    """Quick dialog for just renumbering entries"""
    
    def __init__(self, total_entries: int, parent=None):
        super().__init__(parent)
        self.total_entries = total_entries
        
        self.setWindowTitle("Renumber All Entries")
        self.setMinimumWidth(400)
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the dialog UI"""
        layout = QVBoxLayout(self)
        
        # Info
        info = QLabel(
            f"Reset all entry numbers to sequential order (1-{self.total_entries})\n\n"
            "This will renumber all entries based on their current order."
        )
        info.setWordWrap(True)
        layout.addWidget(info)
        
        # Options
        form = QFormLayout()
        
        self.spin_start = QSpinBox()
        self.spin_start.setMinimum(1)
        self.spin_start.setMaximum(9999)
        self.spin_start.setValue(1)
        self.spin_start.setToolTip("Starting number for renumbering")
        form.addRow("Start from:", self.spin_start)
        
        layout.addLayout(form)
        
        # Preview
        preview_group = QGroupBox("Preview")
        preview_layout = QVBoxLayout()
        
        preview_text = QLabel(
            f"Entry 1 → #{self.spin_start.value()}\n"
            f"Entry 2 → #{self.spin_start.value() + 1}\n"
            f"Entry 3 → #{self.spin_start.value() + 2}\n"
            "..."
        )
        preview_text.setStyleSheet("font-family: monospace; color: #666;")
        self.preview_label = preview_text
        preview_layout.addWidget(preview_text)
        
        preview_group.setLayout(preview_layout)
        layout.addWidget(preview_group)
        
        # Update preview when start changes
        self.spin_start.valueChanged.connect(self.update_preview)
        
        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    def update_preview(self, value):
        """Update the preview text"""
        self.preview_label.setText(
            f"Entry 1 → #{value}\n"
            f"Entry 2 → #{value + 1}\n"
            f"Entry 3 → #{value + 2}\n"
            "..."
        )
    
    def get_start_number(self):
        """Get the starting number"""
        return self.spin_start.value()
