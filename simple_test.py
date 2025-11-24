"""Simple test to see if DocShot can start"""
import sys
import traceback

print("Testing DocShot v3.6.2...")
print("=" * 60)

try:
    print("1. Importing PyQt6...")
    from PyQt6.QtWidgets import QApplication
    print("   ✅ PyQt6 OK")
    
    print("2. Creating QApplication...")
    app = QApplication(sys.argv)
    print("   ✅ QApplication OK")
    
    print("3. Importing MainWindow...")
    from app.ui.main_window import MainWindow
    print("   ✅ MainWindow import OK")
    
    print("4. Creating MainWindow...")
    from pathlib import Path
    window = MainWindow(
        project_root=Path('.'),
        logger=None,
        app_instance=None
    )
    print("   ✅ MainWindow created OK")
    
    print("5. Showing window...")
    window.show()
    print("   ✅ Window shown")
    
    print()
    print("SUCCESS! DocShot should be running now.")
    print("Close the window to exit.")
    print("=" * 60)
    
    sys.exit(app.exec())
    
except Exception as e:
    print()
    print("=" * 60)
    print("ERROR!")
    print("=" * 60)
    print(f"Error: {e}")
    print()
    print("Full traceback:")
    traceback.print_exc()
    print()
    print("=" * 60)
    input("Press Enter to exit...")
    sys.exit(1)
