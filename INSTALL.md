# Installation Guide

## System Requirements

### Minimum Requirements
- **OS:** Windows 10/11, macOS 10.14+, or Linux (Ubuntu 20.04+)
- **Python:** 3.8 or higher
- **RAM:** 4 GB
- **Disk Space:** 100 MB for application + space for screenshots
- **Display:** 1280x720 minimum resolution

### Recommended Requirements
- **Python:** 3.10 or higher
- **RAM:** 8 GB or more
- **Display:** 1920x1080 or higher

## Installation Methods

### Method 1: Quick Install (Recommended)

#### Windows
```cmd
# Download or clone the repository
git clone https://github.com/yourusername/docshot.git
cd docshot

# Install dependencies
pip install -r requirements.txt

# Run the application
start.bat
```

#### macOS
```bash
# Download or clone the repository
git clone https://github.com/yourusername/docshot.git
cd docshot

# Install dependencies
pip3 install -r requirements.txt

# Run the application
chmod +x start.sh
./start.sh
```

#### Linux
```bash
# Download or clone the repository
git clone https://github.com/yourusername/docshot.git
cd docshot

# Install dependencies (may need sudo)
pip3 install -r requirements.txt

# Run the application
chmod +x start.sh
./start.sh
```

---

### Method 2: Virtual Environment (Isolated Install)

Using a virtual environment keeps the application isolated from your system Python.

#### Windows
```cmd
# Clone repository
git clone https://github.com/yourusername/docshot.git
cd docshot

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
python -m app.main
```

#### macOS/Linux
```bash
# Clone repository
git clone https://github.com/yourusername/docshot.git
cd docshot

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run application
python -m app.main
```

---

### Method 3: Manual Installation

If you prefer to install dependencies manually:

```bash
pip install PyQt6
pip install mss
pip install Pillow
pip install pydantic
pip install jinja2
pip install markdown
```

Then run:
```bash
python -m app.main
```

---

## Verification

After installation, verify everything works:

```bash
# Check Python version (should be 3.8+)
python --version

# Check installed packages
pip list | grep -E "PyQt6|Pillow|pydantic|jinja2"

# Run the application
python -m app.main
```

The application window should appear with:
- "New Session" button
- "Capture" button
- Empty entry list

---

## Troubleshooting Installation

### Issue: "pip not found"

**Solution:**
- Windows: Add Python to PATH during installation
- macOS: Use `pip3` instead of `pip`
- Linux: Install python3-pip: `sudo apt install python3-pip`

### Issue: "PyQt6 installation fails"

**Solution for Linux:**
```bash
# Install system dependencies first
sudo apt-get update
sudo apt-get install python3-pyqt6 libgl1

# Then try pip install again
pip3 install -r requirements.txt
```

### Issue: "Permission denied"

**Solution:**
```bash
# Use --user flag
pip install --user -r requirements.txt

# Or use virtual environment (recommended)
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: "ModuleNotFoundError: No module named 'app'"

**Solution:**
Make sure you're running from the overlay_annotator directory:
```bash
cd docshot
python -m app.main  # Note the -m flag
```

### Issue: "ImportError: cannot import name 'X' from 'PyQt6'"

**Solution:**
```bash
# Upgrade PyQt6 to latest version
pip install --upgrade PyQt6
```

---

## Platform-Specific Notes

### Windows
- Run as administrator if you have permission issues
- Disable antivirus temporarily if it blocks the application
- Use Command Prompt or PowerShell
- Windows Defender may flag on first run (allow it)

### macOS
- Grant screen recording permission in System Preferences > Security & Privacy
- May need to "Allow apps downloaded from anywhere" in Security settings
- Use Terminal application

### Linux
- May need X11 libraries: `sudo apt install libxcb-xinerama0`
- Wayland users: Some features may require X11 session
- Ubuntu/Debian: `sudo apt install python3-pyqt6 python3-pil`
- Fedora: `sudo dnf install python3-PyQt6 python3-pillow`

---

## Post-Installation Setup

### First Launch

1. Application starts and creates folders:
   - `~/overlay_annotator_v3/sessions/` (session storage)
   - `~/overlay_annotator_logs/` (application logs)

2. Click "New Session" to create your first session

3. Click "Capture" to test screenshot functionality

### Configuration

No configuration file needed - all settings are managed through the UI.

### Updates

To update to the latest version:

```bash
cd docshot
git pull origin main
pip install --upgrade -r requirements.txt
```

---

## Uninstallation

### Remove Application
```bash
# Navigate to parent folder
cd ..

# Remove application folder
rm -rf docshot  # Linux/macOS
# Or: rmdir /s docshot  # Windows
```

### Remove Data
```bash
# Remove sessions and logs
rm -rf ~/overlay_annotator_v3
rm -rf ~/overlay_annotator_logs
```

### Remove Python Packages
```bash
# If using virtual environment, just delete venv folder
rm -rf venv

# If installed globally, uninstall packages
pip uninstall PyQt6 mss Pillow pydantic jinja2 markdown
```

---

## Support

If you encounter issues during installation:

1. Check the [Troubleshooting](#troubleshooting-installation) section above
2. Ensure all system requirements are met
3. Check application logs in `~/overlay_annotator_logs/`
4. Open an issue on GitHub with:
   - Your operating system and version
   - Python version (`python --version`)
   - Full error message
   - Steps you've tried

---

## Next Steps

After successful installation:

1. Read the [README.md](README.md) for usage instructions
2. Try the Quick Start guide
3. Experiment with annotation tools
4. Export your first report

---

**Happy Documenting! 📸**

*DocShot - Screenshot. Annotate. Document.*
