"""
V3.5: Statistics and Search Panel Widget
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QLineEdit, QFrame
)
from PyQt6.QtCore import pyqtSignal, Qt
from datetime import datetime


class StatsPanel(QWidget):
    """Collapsible statistics and search panel"""
    
    # Signals
    search_changed = pyqtSignal(str)  # Emits search text
    filter_changed = pyqtSignal(str)  # Emits filter type
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.collapsed = False
        self.current_filter = "All"
        self.setup_ui()
    
    def setup_ui(self):
        """Setup panel UI"""
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Header with collapse button
        header_layout = QHBoxLayout()
        header_layout.addWidget(QLabel("📊 Session Stats"))
        
        self.collapse_btn = QPushButton("▼")
        self.collapse_btn.setMaximumWidth(30)
        self.collapse_btn.clicked.connect(self.toggle_collapse)
        header_layout.addWidget(self.collapse_btn)
        layout.addLayout(header_layout)
        
        # Collapsible content
        self.content = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 5, 0, 5)
        
        # Report name label
        self.report_label = QLabel("Report: Not set")
        self.report_label.setStyleSheet("font-weight: bold; color: #2563eb;")
        content_layout.addWidget(self.report_label)
        
        # Stats display
        self.stats_label = QLabel("No data")
        self.stats_label.setStyleSheet("color: #6b7280; font-size: 11px;")
        self.stats_label.setWordWrap(True)
        content_layout.addWidget(self.stats_label)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("background-color: #e5e7eb;")
        content_layout.addWidget(separator)
        
        # Search box
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("🔍"))
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search entries...")
        self.search_box.textChanged.connect(self.on_search)
        search_layout.addWidget(self.search_box)
        content_layout.addLayout(search_layout)
        
        # Filter buttons
        content_layout.addWidget(QLabel("📑 Filter by type:"))
        
        self.filter_buttons = {}
        filter_layout = QVBoxLayout()
        filter_layout.setSpacing(3)
        
        for filter_type in ["All", "Web", "App", "Mobile", "Other"]:
            btn = QPushButton(f"{filter_type} (0)")
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, t=filter_type: self.on_filter(t))
            if filter_type == "All":
                btn.setChecked(True)
            self.filter_buttons[filter_type] = btn
            filter_layout.addWidget(btn)
        
        content_layout.addLayout(filter_layout)
        
        self.content.setLayout(content_layout)
        layout.addWidget(self.content)
        
        self.setLayout(layout)
    
    def update_stats(self, entries, metadata):
        """Update statistics display"""
        count = len(entries)
        
        # Count by type
        type_counts = {
            "web": 0, 
            "app": 0, 
            "mobile": 0, 
            "other": 0
        }
        
        for entry in entries:
            entry_type = getattr(entry, 'location_type', 'other')
            if entry_type in type_counts:
                type_counts[entry_type] += 1
            else:
                type_counts['other'] += 1
        
        # Calculate duration
        if entries and len(entries) > 1:
            first = entries[-1]  # Oldest
            last = entries[0]    # Newest
            duration = self.calculate_duration(first.timestamp, last.timestamp)
        else:
            duration = "0 sec"
        
        # Update labels
        report_title = getattr(metadata, 'report_title', 'Overlay Annotator Report')
        self.report_label.setText(f"📝 {report_title}")
        
        created_date = getattr(metadata, 'created', 'Unknown')
        if created_date and created_date != 'Unknown':
            created_str = self.format_date(created_date)
        else:
            created_str = "Unknown"
        
        self.stats_label.setText(
            f"📸 Screenshots: {count}\n"
            f"📅 Created: {created_str}\n"
            f"⏱️  Duration: {duration}"
        )
        
        # Update filter buttons
        self.filter_buttons["All"].setText(f"All ({count})")
        self.filter_buttons["Web"].setText(f"Web ({type_counts['web']})")
        self.filter_buttons["App"].setText(f"App ({type_counts['app']})")
        self.filter_buttons["Mobile"].setText(f"Mobile ({type_counts['mobile']})")
        self.filter_buttons["Other"].setText(f"Other ({type_counts['other']})")
    
    def calculate_duration(self, start_iso, end_iso):
        """Calculate duration between two ISO timestamps"""
        try:
            start = datetime.fromisoformat(start_iso.replace('Z', '+00:00'))
            end = datetime.fromisoformat(end_iso.replace('Z', '+00:00'))
            delta = end - start
            
            days = delta.days
            hours = delta.seconds // 3600
            minutes = (delta.seconds % 3600) // 60
            
            if days > 0:
                return f"{days}d {hours}h"
            elif hours > 0:
                return f"{hours}h {minutes}m"
            elif minutes > 0:
                return f"{minutes}m"
            else:
                return f"{delta.seconds}s"
        except:
            return "Unknown"
    
    def format_date(self, iso_str):
        """Format ISO date to readable string"""
        try:
            dt = datetime.fromisoformat(iso_str.replace('Z', '+00:00'))
            return dt.strftime("%Y-%m-%d")
        except:
            return "Unknown"
    
    def toggle_collapse(self):
        """Collapse/expand panel"""
        self.collapsed = not self.collapsed
        self.content.setVisible(not self.collapsed)
        self.collapse_btn.setText("▶" if self.collapsed else "▼")
    
    def on_search(self, text):
        """Handle search text change"""
        self.search_changed.emit(text)
    
    def on_filter(self, filter_type):
        """Handle filter button click"""
        # Uncheck other buttons
        for btn_type, btn in self.filter_buttons.items():
            btn.setChecked(btn_type == filter_type)
        
        self.current_filter = filter_type
        self.filter_changed.emit(filter_type)
