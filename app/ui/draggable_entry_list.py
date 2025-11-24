"""
Draggable entry list widget for reordering entries
"""
from PyQt6.QtWidgets import QListWidget, QListWidgetItem, QMessageBox
from PyQt6.QtCore import Qt, pyqtSignal


class DraggableEntryList(QListWidget):
    """QListWidget with drag-and-drop reordering support"""
    
    # Signal emitted when order changes
    order_changed = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Enable drag and drop
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        
        # Visual feedback
        self.setStyleSheet("""
            QListWidget {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 4px;
            }
            QListWidget::item {
                padding: 8px;
                border: 1px solid transparent;
                border-radius: 3px;
                margin: 2px;
            }
            QListWidget::item:selected {
                background-color: #0078d4;
                color: white;
                border: 1px solid #005a9e;
            }
            QListWidget::item:hover:!selected {
                background-color: #f0f0f0;
                border: 1px solid #ccc;
            }
        """)
    
    def dropEvent(self, event):
        """Handle drop event and emit signal"""
        super().dropEvent(event)
        # Order has changed, emit signal
        self.order_changed.emit()
    
    def get_entry_ids(self):
        """Extract entry IDs from list items in current order
        
        Returns:
            list: List of entry IDs in display order
        """
        entry_ids = []
        for i in range(self.count()):
            item = self.item(i)
            text = item.text()
            # Extract ID from format: "#1 - Title" or just "Title"
            if text.startswith('#'):
                try:
                    # Format: "#index - Title"
                    idx = int(text.split(' - ')[0].replace('#', ''))
                    entry_ids.append(idx - 1)  # Convert to 0-based index
                except:
                    pass
        return entry_ids
    
    def keyPressEvent(self, event):
        """Handle keyboard shortcuts for reordering"""
        current_row = self.currentRow()
        
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            if event.key() == Qt.Key.Key_Up and current_row > 0:
                # Move item up
                self.move_item(current_row, current_row - 1)
                event.accept()
                return
            elif event.key() == Qt.Key.Key_Down and current_row < self.count() - 1:
                # Move item down
                self.move_item(current_row, current_row + 1)
                event.accept()
                return
        
        super().keyPressEvent(event)
    
    def move_item(self, from_row, to_row):
        """Move an item from one row to another
        
        Args:
            from_row: Source row index
            to_row: Destination row index
        """
        if from_row < 0 or from_row >= self.count():
            return
        if to_row < 0 or to_row >= self.count():
            return
        
        # Take item from source
        item = self.takeItem(from_row)
        
        # Insert at destination
        self.insertItem(to_row, item)
        
        # Keep selection
        self.setCurrentRow(to_row)
        
        # Emit order changed signal
        self.order_changed.emit()
