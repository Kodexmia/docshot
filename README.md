# DocShot

**Screenshot. Annotate. Document.**

Professional screenshot annotation tool for documentation, bug reports, and visual communication. Built for developers, QA engineers, and technical writers.

![Version](https://img.shields.io/badge/version-3.6.4-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

## ✨ Features

### Core Functionality
- **Global Screen Capture** - Capture any area of your screen with click and drag
- **Annotation Tools** - Arrow, box, pen, and text tools with customizable colors
- **Session Management** - Organize screenshots into named sessions
- **Search & Filter** - Real-time search across titles, notes, and locations
- **Type Filtering** - Filter by Web, App, Mobile, Desktop, or Other
- **Professional Reports** - Export to HTML or Markdown with beautiful formatting

### Advanced Features
- **Structured Metadata** - Add titles, details, location info, and notes to each capture
- **Custom Report Naming** - Name your reports for easy organization
- **Session Statistics** - Track screenshot count, creation date, and more
- **Multiple Export Formats** - HTML (beautiful gradient design) and Markdown
- **Aspect Ratio Preservation** - Screenshots display without distortion
- **High-Quality Rendering** - Anti-aliased annotations and smooth scaling

## 💼 Perfect For

- **📝 Documentation** - Create visual guides and tutorials
- **🐛 Bug Reports** - Capture and annotate issues with context
- **👨‍🏫 Training** - Build step-by-step instructions
- **🔍 Code Reviews** - Highlight specific code sections
- **💬 Communication** - Visual explanations for teams
- **📊 Presentations** - Professional screenshot collections
- **✅ QA Testing** - Document test cases and results

## 📸 Screenshots

### Main Interface
Clean, intuitive interface with session management and statistics.

### Annotation Tools
Four powerful tools: Arrow, Box, Pen, and Text annotations.

### Beautiful Exports
Professional HTML reports with gradient headers, color-coded badges, and responsive design.

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

#### Windows
```bash
# 1. Clone the repository
git clone https://github.com/yourusername/docshot.git
cd docshot

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the application
start.bat
```

#### macOS/Linux
```bash
# 1. Clone the repository
git clone https://github.com/yourusername/docshot.git
cd docshot

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the application
./start.sh
# Or: python -m app.main
```

### First Use

1. **Create a Session**
   - Click "New Session" button
   - Choose a folder location
   - Give your session a name

2. **Capture a Screenshot**
   - Click "Capture" button (or press Ctrl+Alt+S)
   - Click and drag to select screen area
   - Release to capture

3. **Annotate**
   - Use the floating toolbar to select tools
   - Add arrows, boxes, text, or freehand drawings
   - Click ✓ to save or ✕ to cancel

4. **Add Details**
   - Enter a title for your screenshot
   - Add quick details (optional)
   - Specify location type (Web, App, Mobile, etc.)
   - Add full notes if needed
   - Click "Save Entry"

5. **Export Report**
   - Click "Export Report"
   - Choose HTML or Markdown format
   - Open the generated report in your browser or text editor

## 📚 Usage Guide

### Annotation Tools

#### Arrow Tool (A)
Draw arrows to point to specific elements.
- Click where arrow should start
- Drag to where it should point
- Release to place

#### Box Tool (B)
Draw rectangles to highlight areas.
- Click to set one corner
- Drag to opposite corner
- Release to place

#### Pen Tool (P)
Freehand drawing for custom annotations.
- Click and drag to draw
- Release to finish

#### Text Tool (T)
Add text labels to your screenshots.
- Click where text should appear
- Enter text in the dialog
- Text appears with white background

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Ctrl+Alt+S` | Capture screenshot |
| `A` | Select Arrow tool |
| `B` | Select Box tool |
| `P` | Select Pen tool |
| `T` | Select Text tool |
| `Ctrl+S` | Save annotation |
| `Esc` | Cancel annotation |

### Organization

#### Sessions
Each session is a folder containing:
- `images/` - Your captured screenshots
- `metadata/` - Entry data and session info
- `_templates/` - Export templates

#### Metadata Structure
- **Title** - Short description of the screenshot
- **Details** - Quick summary (2-3 lines)
- **Location Type** - Web, App, Mobile, Desktop, or Other
- **Location URL** - URL or file path
- **Notes** - Detailed information

#### Search & Filter
- **Search** - Real-time search across all text fields
- **Filter by Type** - Show only Web, App, Mobile, Desktop, or Other entries
- **Combine** - Use search and filter together for precise results

### Export Formats

#### HTML
Beautiful, professional reports with:
- Gradient header with session information
- Color-coded location badges (blue=web, pink=app, green=mobile)
- Structured fields with icons
- Responsive layout
- Print-friendly styling
- Clickable URLs

#### Markdown
Clean, text-based reports with:
- Numbered entries
- Structured sections
- Image references
- Easy to convert to other formats

## 🔧 Configuration

### Default Settings
- Screenshots saved as high-quality JPEGs (95% quality)
- Default annotation color: Red
- Default line width: 3 pixels
- Default layout: Image on left, text on right

### Session Location
- Windows: `Documents/Cyber Securi/overlay_annotator_v3/sessions/`
- macOS/Linux: `~/overlay_annotator_v3/sessions/`

### Logs
Application logs are saved to:
- Windows: `C:\Users\YourName\overlay_annotator_logs\`
- macOS/Linux: `~/overlay_annotator_logs/`

## 🛠️ Troubleshooting

### Application Won't Start

**Problem:** Import errors or missing dependencies

**Solution:**
```bash
pip install --upgrade -r requirements.txt
```

### Capture Not Working

**Problem:** Screen capture overlay doesn't appear

**Solution:**
1. Check that no other screen capture tool is running
2. Try clicking the Capture button instead of using hotkey
3. Check logs for errors: `~/overlay_annotator_logs/`

### Annotations Not Appearing

**Problem:** Tools selected but annotations don't show

**Solution:**
1. Ensure toolbar is visible (floating window)
2. Try selecting tool again
3. Check that you're clicking within the image area

### Export Fails

**Problem:** Error when exporting report

**Solution:**
1. Ensure session has at least one entry
2. Check that session folder has write permissions
3. Try exporting to a different location

## 🏗️ Architecture

### Technology Stack
- **PyQt6** - GUI framework
- **Pillow (PIL)** - Image processing
- **Pydantic** - Data validation
- **Jinja2** - Template engine
- **mss** - Fast screenshot capture

### Project Structure
```
docshot/
├── app/
│   ├── core/
│   │   ├── models.py          # Data models
│   │   ├── storage.py         # Session management
│   │   └── _templates/        # Export templates
│   └── ui/
│       ├── main_window.py     # Main application window
│       ├── capture_overlay.py # Screenshot capture
│       ├── annotation_canvas.py # Annotation tools
│       ├── annotation_toolbar.py # Tool selection
│       └── stats_panel.py     # Statistics display
├── requirements.txt           # Python dependencies
├── start.bat                 # Windows launcher
└── start.sh                  # macOS/Linux launcher
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/docshot.git
cd docshot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run in development mode
python -m app.main
```

### Coding Standards
- Follow PEP 8 style guidelines
- Add docstrings to all functions
- Include type hints where appropriate
- Test changes thoroughly before submitting PR

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- PyQt6 for the excellent GUI framework
- Python community for amazing libraries
- All contributors who help improve this tool

## 📮 Support

For issues, feature requests, or questions:
- Open an issue on GitHub
- Check existing issues for solutions
- Include log files when reporting bugs

## 🗺️ Roadmap

### Planned Features
- [ ] Integrated toolbar (not floating)
- [ ] Highlighting tool (semi-transparent rectangles)
- [ ] Line thickness control
- [ ] Color picker for annotations
- [ ] Undo/redo for individual annotations
- [ ] Copy/paste annotations
- [ ] Annotation templates
- [ ] Dark mode
- [ ] Multi-monitor support
- [ ] Cloud sync

### Version History
- **v3.5.3** - Current stable version
  - Fixed text annotation crash
  - Removed broken blur tool
  - Fixed image aspect ratio distortion
  - Improved stability and error handling

- **v3.5.2** - Bug fixes
  - Fixed session.json loading crash
  - Improved data validation

- **v3.5.1** - Compatibility fixes
  - Made new fields optional for backward compatibility

- **v3.5.0** - Major feature release
  - Added structured metadata fields
  - Implemented real-time search
  - Added type filtering
  - Enhanced HTML export with beautiful design
  - Custom report naming

---

**DocShot - Making Documentation Visual** 📸✨

*Built for developers, by developers*
