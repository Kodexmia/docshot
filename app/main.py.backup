#!/usr/bin/env python3
"""
Overlay Annotator v2 - Main Entry Point
Launch with global hotkey support (Ctrl+Alt+S)
"""
from pathlib import Path
import sys
import faulthandler
import os

# Enable faulthandler for C-level crash traces
faulthandler.enable(sys.stderr)

# Force software rendering on Windows to avoid GPU driver issues
os.environ.setdefault("QT_OPENGL", "software")

from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import QObject, pyqtSignal, QTimer

try:
    from pyqthotkey import QHotkey
    HOTKEY_AVAILABLE = True
except ImportError:
    print("Warning: pyqthotkey not installed. Install with: pip install pyqthotkey")
    HOTKEY_AVAILABLE = False

from app.ui.main_window import MainWindow
from app.ui.capture_overlay import CaptureOverlay
from app.core.logger import setup_logging, exception_hook, log_exception

ROOT = Path(__file__).resolve().parent


class OverlayAnnotatorApp:
    def __init__(self):
        # Setup logging first
        self.logger, self.log_file = setup_logging()
        self.logger.info("Initializing application...")
        
        try:
            self.app = QApplication(sys.argv)
            self.root = ROOT
            self.main_window = MainWindow(
                project_root=self.root, 
                logger=self.logger,
                app_instance=self  # Pass self so MainWindow can call show_capture_overlay
            )
            self.capture_overlay = None
            self.hk_capture = None
            
            self.logger.info("Application initialized successfully")
            
        except Exception as e:
            self.logger.error("Failed to initialize application", exc_info=True)
            raise
        
    def show_capture_overlay(self):
        """Show the transparent capture overlay"""
        try:
            self.logger.info("Showing capture overlay...")
            if self.capture_overlay is None:
                self.capture_overlay = CaptureOverlay(
                    on_region_selected=self.main_window.handle_captured_region,
                    logger=self.logger
                )
            self.capture_overlay.start_capture()
        except Exception as e:
            self.logger.error("Error showing capture overlay", exc_info=True)
            log_exception(self.logger)
            QMessageBox.critical(
                None,
                "Capture Error",
                f"Failed to start capture:\n{str(e)}\n\nCheck log file:\n{self.log_file}"
            )
    
    def register_hotkey(self):
        """Register system-wide hotkey using QHotkey (Qt-safe)"""
        if not HOTKEY_AVAILABLE:
            self.logger.warning("QHotkey not available - hotkey disabled")
            print("\n" + "=" * 60)
            print("WARNING: Global hotkey not available!")
            print("Install pyqthotkey: pip install pyqthotkey")
            print("Use the 'Capture' button instead")
            print("=" * 60 + "\n")
            return
        
        try:
            self.logger.info("Registering global hotkey (Ctrl+Alt+S)...")
            
            # Create QHotkey instance with parent
            self.hk_capture = QHotkey("Ctrl+Alt+S", parent=self.main_window, register=True)
            
            # Connect to slot via QTimer for thread safety
            self.hk_capture.activated.connect(
                lambda: QTimer.singleShot(0, self.show_capture_overlay)
            )
            
            self.logger.info("Hotkey registered successfully - Ctrl+Alt+S active")
            
        except Exception as e:
            self.logger.error("Failed to register hotkey", exc_info=True)
            print(f"\nWarning: Could not register hotkey: {e}")
            print("Use the 'Capture' button instead\n")
    
    def run(self):
        """Launch the application"""
        try:
            self.register_hotkey()
            self.main_window.show()
            
            print("=" * 60)
            print("Overlay Annotator running...")
            if HOTKEY_AVAILABLE:
                print("Press Ctrl+Alt+S to capture screen region")
            else:
                print("Use 'Capture' button to capture screen region")
            print(f"Log file: {self.log_file}")
            print("=" * 60)
            
            self.logger.info("Application running - entering event loop")
            return self.app.exec()
            
        except Exception as e:
            self.logger.critical("Application error", exc_info=True)
            log_exception(self.logger)
            return 1


if __name__ == "__main__":
    # Install global exception handler
    sys.excepthook = exception_hook
    
    try:
        app = OverlayAnnotatorApp()
        exit_code = app.run()
        sys.exit(exit_code)
    except Exception as e:
        print(f"\nFATAL ERROR: {e}")
        print("Check log file in ~/overlay_annotator_logs/")
        import traceback
        traceback.print_exc()
        sys.exit(1)
