"""
Transparent full-screen overlay for region selection
"""
from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtCore import Qt, QRect, QPoint, pyqtSignal
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor, QPixmap
from mss import mss
from PIL import Image
from typing import Callable, Optional
import logging

# Module logger
logger = logging.getLogger('OverlayAnnotator.CaptureOverlay')


class CaptureOverlay(QWidget):
    """Full-screen transparent overlay for capturing screen regions"""
    
    def __init__(self, on_region_selected: Callable, logger=None):
        super().__init__()
        self.on_region_selected = on_region_selected
        self.logger = logger
        self.selection_start: Optional[QPoint] = None
        self.selection_end: Optional[QPoint] = None
        self.screenshot: Optional[QPixmap] = None
        self.is_selecting = False
        
        if self.logger:
            self.logger.debug("CaptureOverlay initialized")
        
        # Setup window properties
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint | 
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # CRITICAL FIX: Set geometry to cover ALL screens, not just fullscreen on primary
        # Get virtual desktop geometry (all monitors combined)
        from PyQt6.QtWidgets import QApplication
        desktop = QApplication.primaryScreen().virtualGeometry()
        self.setGeometry(desktop)
        
        # Set cursor
        self.setCursor(Qt.CursorShape.CrossCursor)
        
    def start_capture(self):
        """Capture screen and show overlay"""
        # CRITICAL FIX: Capture screen FIRST (before showing overlay)
        # This prevents the overlay from being captured in the screenshot
        self.capture_screen()
        
        # Small delay to ensure capture is complete
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(100, self._show_overlay)
    
    def _show_overlay(self):
        """Show the overlay after capture"""
        # CRITICAL FIX: Re-apply geometry right before showing
        # Sometimes Qt resets it to primary screen only
        from PyQt6.QtWidgets import QApplication
        desktop = QApplication.primaryScreen().virtualGeometry()
        self.setGeometry(desktop)
        
        print(f"Overlay geometry: {desktop.x()}, {desktop.y()}, {desktop.width()}x{desktop.height()}")
        
        self.show()
        self.raise_()
        self.activateWindow()
    
    def capture_screen(self):
        """Capture full screen using mss - ALL MONITORS"""
        try:
            from PyQt6.QtCore import QBuffer, QIODevice
            from io import BytesIO
            
            with mss() as sct:
                # CRITICAL FIX: Capture ALL monitors (monitor 0 = all screens combined)
                monitor = sct.monitors[0]  # 0 = All monitors as one virtual screen
                screenshot = sct.grab(monitor)
                
                # Convert to PIL Image
                img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
                
                # Validate image
                if img.width == 0 or img.height == 0:
                    print("Error: Invalid image dimensions")
                    return
                
                print(f"Captured ALL monitors: {img.width}x{img.height}")
                
                # Convert PIL to QPixmap using in-memory buffer (no file system!)
                byte_array = BytesIO()
                img.save(byte_array, format='PNG')
                byte_array.seek(0)
                
                # Load directly from bytes
                self.screenshot = QPixmap()
                self.screenshot.loadFromData(byte_array.read())
                
                # Validate QPixmap loaded successfully
                if self.screenshot.isNull():
                    print("Error: Failed to load QPixmap")
                    return
                
                print(f"QPixmap loaded: {self.screenshot.width()}x{self.screenshot.height()}")
                    
        except Exception as e:
            print(f"Error capturing screen: {e}")
            import traceback
            traceback.print_exc()
    
    def mousePressEvent(self, event):
        """Start region selection"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.selection_start = event.pos()
            self.selection_end = event.pos()
            self.is_selecting = True
            self.update()
    
    def mouseMoveEvent(self, event):
        """Update region selection"""
        if self.is_selecting:
            self.selection_end = event.pos()
            self.update()
    
    def mouseReleaseEvent(self, event):
        """Finish region selection"""
        if event.button() == Qt.MouseButton.LeftButton and self.is_selecting:
            self.is_selecting = False
            self.selection_end = event.pos()
            
            # Calculate selected region
            if self.selection_start and self.selection_end:
                x1 = min(self.selection_start.x(), self.selection_end.x())
                y1 = min(self.selection_start.y(), self.selection_end.y())
                x2 = max(self.selection_start.x(), self.selection_end.x())
                y2 = max(self.selection_start.y(), self.selection_end.y())
                
                # Crop the screenshot
                if self.screenshot and x2 > x1 and y2 > y1:
                    cropped = self.screenshot.copy(x1, y1, x2 - x1, y2 - y1)
                    
                    # Convert QPixmap to PIL Image using in-memory buffer (no temp file!)
                    from PyQt6.QtCore import QBuffer, QIODevice
                    from io import BytesIO
                    
                    buffer = QBuffer()
                    buffer.open(QIODevice.OpenModeFlag.WriteOnly)
                    cropped.save(buffer, "PNG")
                    
                    pil_img = Image.open(BytesIO(buffer.data()))
                    
                    # Pass to callback
                    self.on_region_selected(pil_img)
            
            # Close overlay
            self.close()
            self.reset()
    
    def keyPressEvent(self, event):
        """Handle escape key to cancel"""
        if event.key() == Qt.Key.Key_Escape:
            self.close()
            self.reset()
    
    def reset(self):
        """Reset selection state"""
        self.selection_start = None
        self.selection_end = None
        self.is_selecting = False
        self.screenshot = None
    
    def paintEvent(self, event):
        """Draw semi-transparent overlay and selection rectangle"""
        painter = QPainter(self)
        
        # Draw dark semi-transparent background
        painter.fillRect(self.rect(), QColor(0, 0, 0, 120))
        
        # Draw selection rectangle if active
        if self.selection_start and self.selection_end:
            x1 = min(self.selection_start.x(), self.selection_end.x())
            y1 = min(self.selection_start.y(), self.selection_end.y())
            x2 = max(self.selection_start.x(), self.selection_end.x())
            y2 = max(self.selection_start.y(), self.selection_end.y())
            
            selection_rect = QRect(x1, y1, x2 - x1, y2 - y1)
            
            # Clear the selected area (show underlying screenshot)
            painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Clear)
            painter.fillRect(selection_rect, Qt.GlobalColor.transparent)
            painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceOver)
            
            # Draw border around selection
            pen = QPen(QColor(0, 150, 255), 2, Qt.PenStyle.SolidLine)
            painter.setPen(pen)
            painter.drawRect(selection_rect)
            
            # Draw dimension label
            if x2 - x1 > 0 and y2 - y1 > 0:
                dimension_text = f"{x2 - x1} × {y2 - y1}"
                painter.setPen(QColor(255, 255, 255))
                painter.drawText(x1 + 5, y1 - 5, dimension_text)
