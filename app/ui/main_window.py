"""
Main application window with session management (V3.5.4)
"""
from pathlib import Path
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QFileDialog, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QTextEdit, QComboBox, QListWidget, 
    QSplitter, QMessageBox, QStatusBar, QLineEdit, QFrame,
    QToolButton, QMenu, QDialog  # V3.5.4: For reordering and editing
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QKeySequence, QShortcut
from PIL import Image

from app.core.storage import SessionStore
from app.core.models import Entry, ImageModel
from app.ui.annotation_canvas import AnnotationCanvas, ToolType
from app.ui.annotation_toolbar import AnnotationToolbar
from app.ui.stats_panel import StatsPanel  # V3.5
from app.ui.draggable_entry_list import DraggableEntryList  # V3.5.4
from app.ui.entry_editor import EntryEditorDialog, QuickRenumberDialog  # V3.5.4


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self, project_root: Path, logger=None, app_instance=None):
        super().__init__()
        self.setWindowTitle("DocShot v3.6")
        self.resize(1400, 900)
        self.project_root = project_root
        self.logger = logger
        self.app_instance = app_instance  # Reference to OverlayAnnotatorApp
        self.session_path = None
        self.store = None
        self.annotation_toolbar = None
        self.current_filter = "All"  # V3.5: Track current filter
        
        if self.logger:
            self.logger.debug("MainWindow initializing...")
        
        self.setup_ui()
        self.setup_shortcuts()
        self.show_welcome_message()
    
    def setup_ui(self):
        """Setup main UI components"""
        # Left panel: Session and entry list
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        
        # Session controls
        self.btn_new_session = QPushButton("📁 New Session")
        self.btn_new_session.clicked.connect(self.choose_session_folder)
        left_layout.addWidget(self.btn_new_session)
        
        self.btn_capture = QPushButton("📷 Capture (Ctrl+Alt+S)")
        self.btn_capture.clicked.connect(self.trigger_capture)
        self.btn_capture.setEnabled(False)
        left_layout.addWidget(self.btn_capture)
        
        # V3.5: Stats Panel
        self.stats_panel = StatsPanel(self)
        self.stats_panel.search_changed.connect(self.on_search_changed)
        self.stats_panel.filter_changed.connect(self.on_filter_changed)
        left_layout.addWidget(self.stats_panel)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("background-color: #ccc;")
        left_layout.addWidget(separator)
        
        left_layout.addWidget(QLabel("Entries:"))
        
        # V3.5.4: Use draggable list for reordering
        self.entry_list = DraggableEntryList()
        self.entry_list.itemClicked.connect(self.load_entry)
        self.entry_list.itemDoubleClicked.connect(self.edit_selected_entry)  # V3.5.4: Double-click to edit
        self.entry_list.order_changed.connect(self.on_entry_order_changed)  # V3.5.4: Handle reordering
        
        # V3.5.4: Context menu for right-click
        self.entry_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.entry_list.customContextMenuRequested.connect(self.show_entry_context_menu)
        
        left_layout.addWidget(self.entry_list)
        
        # V3.5.4: Entry management buttons
        entry_buttons = QHBoxLayout()
        
        self.btn_edit_entry = QPushButton("✏️ Edit")
        self.btn_edit_entry.setToolTip("Edit selected entry (or double-click)")
        self.btn_edit_entry.clicked.connect(self.edit_selected_entry)
        
        self.btn_renumber = QPushButton("🔢 Renumber")
        self.btn_renumber.setToolTip("Reset all entry numbers sequentially")
        self.btn_renumber.clicked.connect(self.renumber_all_entries)
        
        self.btn_delete_entry = QPushButton("🗑️ Delete")
        self.btn_delete_entry.setToolTip("Delete selected entry")
        self.btn_delete_entry.clicked.connect(self.delete_selected_entry)
        
        entry_buttons.addWidget(self.btn_edit_entry)
        entry_buttons.addWidget(self.btn_renumber)
        entry_buttons.addWidget(self.btn_delete_entry)
        
        left_layout.addLayout(entry_buttons)
        
        # V3.5.4: Reorder buttons (for keyboard users)
        reorder_layout = QHBoxLayout()
        self.btn_move_up = QToolButton()
        self.btn_move_up.setText("▲")
        self.btn_move_up.setToolTip("Move Up (Ctrl+Up)")
        self.btn_move_up.clicked.connect(self.move_entry_up)
        
        self.btn_move_down = QToolButton()
        self.btn_move_down.setText("▼")
        self.btn_move_down.setToolTip("Move Down (Ctrl+Down)")
        self.btn_move_down.clicked.connect(self.move_entry_down)
        
        reorder_layout.addWidget(QLabel("Reorder:"))
        reorder_layout.addWidget(self.btn_move_up)
        reorder_layout.addWidget(self.btn_move_down)
        reorder_layout.addStretch()
        
        left_layout.addLayout(reorder_layout)
        
        # Export button
        self.btn_export = QPushButton("📤 Export Report")
        self.btn_export.clicked.connect(self.export_report)
        self.btn_export.setEnabled(False)
        left_layout.addWidget(self.btn_export)
        
        left_panel.setLayout(left_layout)
        
        # Center panel: Canvas
        center_panel = QWidget()
        center_layout = QVBoxLayout()
        
        # CRITICAL FIX: Set main window as canvas parent so text tool can call back
        self.canvas = AnnotationCanvas(parent=self)
        center_layout.addWidget(self.canvas)
        
        # Annotation controls
        controls_layout = QHBoxLayout()
        
        self.btn_show_toolbar = QPushButton("🎨 Show Toolbar")
        self.btn_show_toolbar.clicked.connect(self.show_annotation_toolbar)
        self.btn_show_toolbar.setEnabled(False)
        controls_layout.addWidget(self.btn_show_toolbar)
        
        self.btn_undo = QPushButton("↶ Undo")
        self.btn_undo.clicked.connect(self.canvas.undo_last)
        self.btn_undo.setEnabled(False)
        controls_layout.addWidget(self.btn_undo)
        
        self.btn_clear = QPushButton("🗑 Clear")
        self.btn_clear.clicked.connect(self.canvas.clear_annotations)
        self.btn_clear.setEnabled(False)
        controls_layout.addWidget(self.btn_clear)
        
        controls_layout.addStretch()
        center_layout.addLayout(controls_layout)
        
        center_panel.setLayout(center_layout)
        
        # Right panel: Metadata (V3.5: Enhanced with split notes)
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        
        # V3.5: Report Name
        right_layout.addWidget(QLabel("📝 Report Name:"))
        self.report_name_edit = QLineEdit()
        self.report_name_edit.setPlaceholderText("e.g., Q4 Security Audit")
        right_layout.addWidget(self.report_name_edit)
        
        # Separator
        separator2 = QFrame()
        separator2.setFrameShape(QFrame.Shape.HLine)
        separator2.setStyleSheet("background-color: #ccc;")
        right_layout.addWidget(separator2)
        
        # Layout
        right_layout.addWidget(QLabel("Layout:"))
        self.layout_select = QComboBox()
        self.layout_select.addItems(["image-left", "image-top"])
        right_layout.addWidget(self.layout_select)
        
        # Title
        right_layout.addWidget(QLabel("📌 Title:"))
        self.title_edit = QTextEdit()
        self.title_edit.setPlaceholderText("Enter title...")
        self.title_edit.setMaximumHeight(60)
        right_layout.addWidget(self.title_edit)
        
        # V3.5: Details (NEW)
        right_layout.addWidget(QLabel("📋 Details:"))
        self.details_edit = QTextEdit()
        self.details_edit.setPlaceholderText("Quick summary (2-3 lines)...")
        self.details_edit.setMaximumHeight(60)
        right_layout.addWidget(self.details_edit)
        
        # V3.5: Location (NEW)
        right_layout.addWidget(QLabel("📍 Location:"))
        location_layout = QHBoxLayout()
        location_layout.addWidget(QLabel("Type:"))
        self.location_type_combo = QComboBox()
        self.location_type_combo.addItems(["Web Page", "Desktop App", "Mobile", "Other"])
        location_layout.addWidget(self.location_type_combo)
        right_layout.addLayout(location_layout)
        
        self.location_url_edit = QLineEdit()
        self.location_url_edit.setPlaceholderText("URL or app path (e.g., https://example.com)")
        right_layout.addWidget(self.location_url_edit)
        
        # Notes (kept, but smaller)
        right_layout.addWidget(QLabel("📝 Notes:"))
        self.notes_edit = QTextEdit()
        self.notes_edit.setPlaceholderText("Detailed notes...")
        right_layout.addWidget(self.notes_edit)
        
        self.btn_save = QPushButton("💾 Save Entry")
        self.btn_save.clicked.connect(self.save_entry)
        self.btn_save.setEnabled(False)
        right_layout.addWidget(self.btn_save)
        
        right_layout.addStretch()
        right_panel.setLayout(right_layout)
        
        # Main splitter
        splitter = QSplitter()
        splitter.addWidget(left_panel)
        splitter.addWidget(center_panel)
        splitter.addWidget(right_panel)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)
        splitter.setStretchFactor(2, 1)
        
        # Central widget
        container = QWidget()
        main_layout = QHBoxLayout()
        main_layout.addWidget(splitter)
        container.setLayout(main_layout)
        self.setCentralWidget(container)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.update_status("Ready. Press Ctrl+Alt+S to capture screen region.")
    
    def setup_shortcuts(self):
        """Setup keyboard shortcuts"""
        # Save shortcut
        save_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        save_shortcut.activated.connect(self.save_entry)
        
        # Tool shortcuts
        arrow_shortcut = QShortcut(QKeySequence("A"), self)
        arrow_shortcut.activated.connect(lambda: self.canvas.set_tool(ToolType.ARROW))
        
        box_shortcut = QShortcut(QKeySequence("B"), self)
        box_shortcut.activated.connect(lambda: self.canvas.set_tool(ToolType.BOX))
        
        pen_shortcut = QShortcut(QKeySequence("P"), self)
        pen_shortcut.activated.connect(lambda: self.canvas.set_tool(ToolType.PEN))
        
        # Text shortcut
        text_shortcut = QShortcut(QKeySequence("T"), self)
        text_shortcut.activated.connect(lambda: self.canvas.set_tool(ToolType.TEXT))
        
        # V3.5.3: Blur shortcut removed (tool was causing crashes)
    
    def show_welcome_message(self):
        """Show welcome message"""
        self.update_status("Welcome! Create a session to begin capturing.")
    
    def choose_session_folder(self):
        """Choose or create session folder"""
        default_dir = str(self.project_root / "sessions")
        Path(default_dir).mkdir(exist_ok=True)
        
        path = QFileDialog.getExistingDirectory(
            self,
            "Choose Session Folder",
            default_dir
        )
        
        if not path:
            return
        
        self.session_path = Path(path)
        self.session_path.mkdir(parents=True, exist_ok=True)
        (self.session_path / "images").mkdir(exist_ok=True)
        (self.session_path / "metadata").mkdir(exist_ok=True)
        
        self.store = SessionStore(self.session_path)
        self.load_session_entries()
        
        # V3.5: Load report name
        if hasattr(self, 'report_name_edit'):
            self.report_name_edit.setText(self.store.metadata.report_title)
        
        # Enable buttons
        self.btn_capture.setEnabled(True)
        self.btn_export.setEnabled(True)
        
        self.update_status(f"Session loaded: {self.session_path.name}")
    
    def load_session_entries(self):
        """Load existing entries from session"""
        if not self.store:
            return
        
        self.entry_list.clear()
        entries = self.store.load_entries()
        
        for i, entry in enumerate(entries, 1):
            # V3.5: Show with number and truncated title
            display = f"#{i} - {entry.title[:50]}"
            if len(entry.title) > 50:
                display += "..."
            self.entry_list.addItem(display)
        
        # V3.5: Update stats panel and report name
        self.update_stats_panel()
        if hasattr(self, 'report_name_edit'):
            self.report_name_edit.setText(self.store.metadata.report_title)
    
    def load_entry(self, item):
        """Load selected entry into canvas"""
        if not self.store:
            return
        
        # Parse entry number from display text
        text = item.text()
        try:
            entry_num = int(text.split('#')[1].split(' -')[0])
            entries = self.store.load_entries()
            if 0 < entry_num <= len(entries):
                entry = entries[entry_num - 1]
                
                # Load image
                img_path = self.session_path / entry.image.path
                if img_path.exists():
                    pil = Image.open(img_path)
                    self.canvas.load_pil(pil)
                    
                    # Load metadata
                    self.title_edit.setPlainText(entry.title)
                    
                    # V3.5: Load new fields
                    if hasattr(entry, 'details'):
                        self.details_edit.setPlainText(entry.details)
                    if hasattr(entry, 'location_type'):
                        # Map data values to UI labels
                        type_map = {
                            "web": "Web Page",
                            "app": "Desktop App",
                            "mobile": "Mobile",
                            "other": "Other"
                        }
                        ui_type = type_map.get(entry.location_type, "Other")
                        self.location_type_combo.setCurrentText(ui_type)
                    if hasattr(entry, 'location_url'):
                        self.location_url_edit.setText(entry.location_url)
                    
                    self.notes_edit.setPlainText(entry.notes)
                    self.layout_select.setCurrentText(entry.layout)
                    
                    self.update_status(f"Loaded entry: {entry.title}")
        except (ValueError, IndexError):
            self.update_status("Error loading entry")
    
    def trigger_capture(self):
        """Manually trigger capture (for testing without hotkey)"""
        if self.app_instance:
            if self.logger:
                self.logger.debug("Capture button clicked - triggering overlay")
            self.app_instance.show_capture_overlay()
        else:
            self.update_status("Error: Capture overlay not available")
            if self.logger:
                self.logger.error("App instance not set - cannot trigger capture")
    
    def handle_captured_region(self, pil_img: Image.Image):
        """Handle captured screen region"""
        try:
            if self.logger:
                self.logger.info(f"Handling captured region: {pil_img.width}x{pil_img.height}")
            
            if not self.store:
                if self.logger:
                    self.logger.warning("No session - cannot handle captured region")
                QMessageBox.warning(self, "No Session", "Please create a session first.")
                return
            
            # Load into canvas
            if self.logger:
                self.logger.debug("Loading image into canvas...")
            self.canvas.load_pil(pil_img)
            
            # Enable annotation controls
            self.btn_show_toolbar.setEnabled(True)
            self.btn_undo.setEnabled(True)
            self.btn_clear.setEnabled(True)
            self.btn_save.setEnabled(True)
            
            # Auto-show toolbar
            self.show_annotation_toolbar()
            
            self.update_status("Image captured! Annotate and save.")
            if self.logger:
                self.logger.info("Image loaded successfully, ready for annotation")
                
        except Exception as e:
            if self.logger:
                self.logger.error("Error handling captured region", exc_info=True)
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to load captured image:\n{str(e)}"
            )
    
    def show_annotation_toolbar(self):
        """Show floating annotation toolbar"""
        try:
            if self.logger:
                self.logger.debug("Showing annotation toolbar...")
            
            if self.annotation_toolbar is None:
                if self.logger:
                    self.logger.debug("Creating new annotation toolbar")
                # CRITICAL: Set parent to prevent orphaned widget crashes
                self.annotation_toolbar = AnnotationToolbar(parent=self)
                
                # Connect signals
                self.annotation_toolbar.tool_selected.connect(self.canvas.set_tool)
                self.annotation_toolbar.save_requested.connect(self.save_entry)
                self.annotation_toolbar.cancel_requested.connect(self.cancel_annotation)
                self.annotation_toolbar.text_requested.connect(self.canvas.add_text_annotation)
                self.annotation_toolbar.undo_btn.clicked.connect(self.canvas.undo_last)
                
                if self.logger:
                    self.logger.debug("Toolbar created and signals connected")
            
            # Position toolbar near top center
            toolbar_x = self.x() + (self.width() - self.annotation_toolbar.width()) // 2
            toolbar_y = self.y() + 100
            self.annotation_toolbar.move(toolbar_x, toolbar_y)
            
            if self.logger:
                self.logger.debug(f"Toolbar positioned at {toolbar_x}, {toolbar_y}")
            
            self.annotation_toolbar.show()
            self.annotation_toolbar.raise_()
            
            if self.logger:
                self.logger.info("Annotation toolbar shown successfully")
                
        except Exception as e:
            if self.logger:
                self.logger.error("Error showing annotation toolbar", exc_info=True)
            QMessageBox.warning(
                self,
                "Toolbar Error",
                f"Failed to show annotation toolbar:\n{str(e)}"
            )
    
    def cancel_annotation(self):
        """Cancel current annotation"""
        self.canvas.clear_annotations()
        if self.annotation_toolbar:
            self.annotation_toolbar.hide()
        self.update_status("Annotation cancelled")
    
    def request_text_for_annotation(self):
        """Request text input from toolbar when canvas is clicked with text tool"""
        if self.annotation_toolbar:
            text = self.annotation_toolbar.request_text_input()
            if text:
                self.canvas.add_text_annotation(text)
                # Switch back to arrow tool after placing text
                from app.ui.annotation_canvas import ToolType
                self.canvas.set_tool(ToolType.ARROW)
                self.annotation_toolbar.select_tool(ToolType.ARROW)
    
    def save_entry(self):
        """Save annotated entry (V3.5: Enhanced with split notes)"""
        try:
            if not self.store or self.canvas.pil_image is None:
                self.update_status("Nothing to save")
                QMessageBox.warning(self, "Cannot Save", "No screenshot captured or no session created.")
                return
            
            if self.logger:
                self.logger.info("Starting save_entry...")
            
            # Render annotated image
            if self.logger:
                self.logger.info("Rendering annotated image...")
            pil = self.canvas.render_annotated()
            
            # Save image
            if self.logger:
                self.logger.info("Saving image to disk...")
            img_rel_path = self.store.save_image(pil)
            if self.logger:
                self.logger.info(f"Image saved to: {img_rel_path}")
            
            # Get metadata
            title = self.title_edit.toPlainText().strip()
            details = self.details_edit.toPlainText().strip()
            
            # Map location type
            location_type_map = {
                "Web Page": "web",
                "Desktop App": "app",
                "Mobile": "mobile",
                "Other": "other"
            }
            location_type = location_type_map.get(self.location_type_combo.currentText(), "other")
            location_url = self.location_url_edit.text().strip()
            notes = self.notes_edit.toPlainText().strip()
            layout = self.layout_select.currentText()
            
            # Create entry
            if self.logger:
                self.logger.info(f"Creating entry with title: {title or 'Untitled'}")
            entry = Entry.new(
                title=title or "Untitled",
                details=details,
                location_type=location_type,
                location_url=location_url,
                notes=notes,
                layout=layout,
                image=ImageModel(
                    path=str(img_rel_path),
                    width=pil.width,
                    height=pil.height,
                    quality=95,
                    hires=True
                )
            )
            
            # Save entry
            if self.logger:
                self.logger.info("Saving entry to storage...")
            self.store.save_entry(entry)
            if self.logger:
                self.logger.info("Entry saved successfully")
            
            # V3.5: Update and save session metadata
            self.store.metadata.report_title = self.report_name_edit.text().strip() or "Overlay Annotator Report"
            self.store.metadata.entry_count = len(self.store.load_entries())
            self.store.save_session_metadata()
            
            # Update list
            entries = self.store.load_entries()
            self.entry_list.addItem(f"#{len(entries)} - {entry.title[:50]}")
            if self.logger:
                self.logger.info(f"Entry list updated. Total entries: {len(entries)}")
            
            # V3.5: Update stats panel
            self.update_stats_panel()
            
            # Clear form
            self.title_edit.clear()
            self.details_edit.clear()
            self.location_url_edit.clear()
            self.notes_edit.clear()
            self.canvas.clear_annotations()
            
            # Hide toolbar
            if self.annotation_toolbar:
                self.annotation_toolbar.hide()
            
            self.update_status(f"Entry saved: {entry.title}")
            
            QMessageBox.information(
                self,
                "Saved",
                f"Entry '{entry.title}' saved successfully!"
            )
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to save entry: {e}", exc_info=True)
            QMessageBox.critical(
                self,
                "Save Failed",
                f"Failed to save entry:\n\n{str(e)}\n\nCheck console for details."
            )
    
    def export_report(self):
        """Export session report as both Markdown and HTML"""
        if not self.store:
            return
        
        try:
            # Export both formats
            md_path = self.store.export_markdown()
            html_path = self.store.export_html()
            
            self.update_status(f"Reports exported: {md_path.name} & {html_path.name}")
            
            # Ask user which one to open
            reply = QMessageBox.question(
                self,
                "Export Complete",
                f"Reports exported successfully!\n\n"
                f"📄 Markdown: {md_path}\n"
                f"🌐 HTML: {html_path}\n\n"
                f"Open HTML report in browser?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.Yes
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                import webbrowser
                webbrowser.open(str(html_path.absolute()))
                
        except Exception as e:
            if self.logger:
                self.logger.error("Export failed", exc_info=True)
            QMessageBox.critical(
                self,
                "Export Failed",
                f"Failed to export report:\n{str(e)}"
            )
    
    def update_stats_panel(self):
        """V3.5: Update stats panel with current data"""
        if self.store and hasattr(self, 'stats_panel'):
            entries = self.store.load_entries()
            self.stats_panel.update_stats(entries, self.store.metadata)
    
    def on_search_changed(self, search_text):
        """V3.5: Handle search text change"""
        self.filter_entries(search_text=search_text)
    
    def on_filter_changed(self, filter_type):
        """V3.5: Handle filter type change"""
        self.current_filter = filter_type
        search_text = self.stats_panel.search_box.text() if hasattr(self, 'stats_panel') else ""
        self.filter_entries(search_text=search_text, filter_type=filter_type)
    
    def filter_entries(self, search_text="", filter_type="All"):
        """V3.5: Filter entry list based on search and filter"""
        if not self.store:
            return
        
        all_entries = self.store.load_entries()
        filtered = all_entries
        
        # Apply location filter
        if filter_type != "All":
            type_map = {
                "Web": "web",
                "App": "app",
                "Mobile": "mobile",
                "Other": "other"
            }
            target_type = type_map.get(filter_type, "other")
            filtered = [e for e in filtered if getattr(e, 'location_type', 'other') == target_type]
        
        # Apply search filter
        if search_text:
            search_lower = search_text.lower()
            filtered = [e for e in filtered if (
                search_lower in e.title.lower() or
                search_lower in getattr(e, 'details', '').lower() or
                search_lower in e.notes.lower() or
                search_lower in getattr(e, 'location_url', '').lower()
            )]
        
        # Update entry list display
        self.entry_list.clear()
        for i, entry in enumerate(filtered, 1):
            # Show with number and truncated title
            display = f"#{i} - {entry.title[:50]}"
            if len(entry.title) > 50:
                display += "..."
            self.entry_list.addItem(display)
    
    def update_status(self, message: str):
        """Update status bar"""
        self.status_bar.showMessage(message)
    
    # ========== V3.5.4: Entry Management Methods ==========
    
    def show_entry_context_menu(self, position):
        """Show context menu for entry list items (V3.5.4)"""
        item = self.entry_list.itemAt(position)
        if not item:
            return
        
        menu = QMenu(self)
        
        edit_action = menu.addAction("✏️ Edit Entry")
        edit_action.triggered.connect(self.edit_selected_entry)
        
        menu.addSeparator()
        
        renumber_action = menu.addAction("🔢 Renumber All Entries")
        renumber_action.triggered.connect(self.renumber_all_entries)
        
        menu.addSeparator()
        
        delete_action = menu.addAction("🗑️ Delete Entry")
        delete_action.triggered.connect(self.delete_selected_entry)
        
        menu.exec(self.entry_list.mapToGlobal(position))
    
    def edit_selected_entry(self):
        """Open editor dialog for selected entry (V3.5.4)"""
        current_row = self.entry_list.currentRow()
        if current_row < 0:
            QMessageBox.information(
                self,
                "No Selection",
                "Please select an entry to edit."
            )
            return
        
        if not self.store:
            return
        
        try:
            # Load all entries
            entries = self.store.load_entries()
            
            # Apply current filter to get the correct entry
            if current_row >= len(entries):
                return
            
            entry = entries[current_row]
            entry_number = current_row + 1  # Display as 1-based
            
            # Open editor dialog
            dialog = EntryEditorDialog(entry, entry_number, self)
            
            if dialog.exec() == QDialog.DialogCode.Accepted:
                updated_entry, new_number = dialog.get_updated_entry()
                
                # Check if number changed
                if new_number != entry_number:
                    # Update order field
                    updated_entry.order = new_number
                    
                # Save updated entry
                self.store.save_entry(updated_entry)
                
                # If order changed, renumber all entries
                if new_number != entry_number:
                    self.reorder_entries_by_list()
                
                # Refresh display
                self.load_session_entries()
                self.update_status(f"Entry #{new_number} updated")
                
                if self.logger:
                    self.logger.info(f"Entry #{entry_number} edited (new #: {new_number})")
        
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to edit entry: {e}", exc_info=True)
            QMessageBox.warning(
                self,
                "Edit Failed",
                f"Could not edit entry: {str(e)}"
            )
    
    def renumber_all_entries(self):
        """Renumber all entries sequentially (V3.5.4)"""
        if not self.store:
            QMessageBox.information(
                self,
                "No Session",
                "Please open a session first."
            )
            return
        
        try:
            entries = self.store.load_entries()
            
            if not entries:
                QMessageBox.information(
                    self,
                    "No Entries",
                    "No entries to renumber."
                )
                return
            
            # Show renumber dialog
            dialog = QuickRenumberDialog(len(entries), self)
            
            if dialog.exec() == QDialog.DialogCode.Accepted:
                start_number = dialog.get_start_number()
                
                # Renumber all entries
                for i, entry in enumerate(entries):
                    entry.order = start_number + i
                    self.store.save_entry(entry)
                
                # Refresh display
                self.load_session_entries()
                self.update_status(f"Renumbered {len(entries)} entries starting from #{start_number}")
                
                if self.logger:
                    self.logger.info(f"Renumbered {len(entries)} entries (start: {start_number})")
        
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to renumber entries: {e}", exc_info=True)
            QMessageBox.warning(
                self,
                "Renumber Failed",
                f"Could not renumber entries: {str(e)}"
            )
    
    def delete_selected_entry(self):
        """Delete the selected entry (V3.5.4)"""
        current_row = self.entry_list.currentRow()
        if current_row < 0:
            QMessageBox.information(
                self,
                "No Selection",
                "Please select an entry to delete."
            )
            return
        
        if not self.store:
            return
        
        try:
            entries = self.store.load_entries()
            if current_row >= len(entries):
                return
            
            entry = entries[current_row]
            
            # Confirm deletion
            reply = QMessageBox.question(
                self,
                "Confirm Delete",
                f"Delete entry #{current_row + 1}: {entry.title}?\n\nThis cannot be undone.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                # Delete entry files
                self.store.delete_entry(entry)
                
                # Refresh display
                self.load_session_entries()
                self.update_status(f"Entry deleted")
                
                if self.logger:
                    self.logger.info(f"Deleted entry: {entry.title}")
        
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to delete entry: {e}", exc_info=True)
            QMessageBox.warning(
                self,
                "Delete Failed",
                f"Could not delete entry: {str(e)}"
            )
    
    def on_entry_order_changed(self):
        """Handle entry order change from drag-and-drop (V3.5.4)"""
        if self.logger:
            self.logger.info("Entry order changed via drag-and-drop")
        
        # Reorder entries based on new list order
        self.reorder_entries_by_list()
        self.update_status("Entries reordered")
    
    def reorder_entries_by_list(self):
        """Reorder entries based on current list display order (V3.5.4)"""
        if not self.store:
            return
        
        try:
            entries = self.store.load_entries()
            
            # Get new order from list (1-based display numbers)
            for i in range(self.entry_list.count()):
                item = self.entry_list.item(i)
                text = item.text()
                
                # Extract original entry number from "#X - Title"
                if text.startswith('#'):
                    try:
                        old_num = int(text.split(' - ')[0].replace('#', '').strip())
                        if 1 <= old_num <= len(entries):
                            # Set new order
                            entries[old_num - 1].order = i + 1
                    except:
                        pass
            
            # Save all entries with new order
            for entry in entries:
                self.store.save_entry(entry)
            
            # Refresh display
            self.load_session_entries()
            
            if self.logger:
                self.logger.info("Entries reordered and saved")
        
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to reorder entries: {e}", exc_info=True)
    
    def move_entry_up(self):
        """Move selected entry up in the list (V3.5.4)"""
        current_row = self.entry_list.currentRow()
        if current_row > 0:
            self.entry_list.move_item(current_row, current_row - 1)
    
    def move_entry_down(self):
        """Move selected entry down in the list (V3.5.4)"""
        current_row = self.entry_list.currentRow()
        if current_row < self.entry_list.count() - 1:
            self.entry_list.move_item(current_row, current_row + 1)
    
    # ========== End V3.5.4 Methods ==========
    
    def closeEvent(self, event):
        """Handle window close"""
        if self.annotation_toolbar:
            self.annotation_toolbar.close()
        event.accept()
