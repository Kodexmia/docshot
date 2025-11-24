#!/usr/bin/env python3
"""
DocShot v3.6.2 - Diagnostic Test
Run this to see what's failing
"""
import sys
import traceback

print("=" * 60)
print("DocShot v3.6.2 CLEAN - Diagnostic Test")
print("=" * 60)
print()

# Test 1: Python version
print("Test 1: Python Version")
print(f"  Version: {sys.version}")
print(f"  ✅ Python OK")
print()

# Test 2: Required modules
print("Test 2: Import Dependencies")
required = [
    'PyQt6',
    'PyQt6.QtWidgets',
    'PyQt6.QtCore',
    'PyQt6.QtGui',
    'PIL',
    'mss',
    'pydantic',
    'jinja2',
    'markdown',
]

for module in required:
    try:
        __import__(module)
        print(f"  ✅ {module}")
    except ImportError as e:
        print(f"  ❌ {module} - NOT INSTALLED")
        print(f"     {e}")

print()

# Test 3: Optional hotkey
print("Test 3: Optional Modules")
try:
    import pyqthotkey
    print("  ✅ pyqthotkey (hotkeys will work)")
except ImportError:
    print("  ⚠️  pyqthotkey not installed (hotkeys disabled, but app will work)")

print()

# Test 4: App modules
print("Test 4: DocShot Modules")
sys.path.insert(0, '.')

modules = [
    'app',
    'app.main',
    'app.core.models',
    'app.core.storage',
    'app.core.logger',
    'app.ui.main_window',
    'app.ui.capture_overlay',
    'app.ui.annotation_canvas',
]

for module in modules:
    try:
        __import__(module)
        print(f"  ✅ {module}")
    except Exception as e:
        print(f"  ❌ {module}")
        print(f"     Error: {e}")
        traceback.print_exc()

print()

# Test 5: Try creating MainWindow
print("Test 5: Create MainWindow")
try:
    from PyQt6.QtWidgets import QApplication
    from app.ui.main_window import MainWindow
    from pathlib import Path
    
    app = QApplication(sys.argv)
    window = MainWindow(
        project_root=Path('.'),
        logger=None,
        app_instance=None
    )
    print("  ✅ MainWindow created successfully")
    print()
    print("=" * 60)
    print("✅ ALL TESTS PASSED!")
    print("=" * 60)
    print()
    print("DocShot should work. Try running:")
    print("  python -m app.main")
    sys.exit(0)
    
except Exception as e:
    print(f"  ❌ Failed to create MainWindow")
    print()
    print("=" * 60)
    print("❌ ERROR FOUND!")
    print("=" * 60)
    print()
    print(f"Error: {e}")
    print()
    print("Full traceback:")
    traceback.print_exc()
    print()
    print("Please send this error message!")
    sys.exit(1)
