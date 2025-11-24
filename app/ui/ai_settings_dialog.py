"""
Simple dialog for AI settings (API key configuration)
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QTextEdit, QMessageBox
)
from PyQt6.QtCore import Qt


class AISettingsDialog(QDialog):
    """Simple dialog for configuring Gemini API key"""
    
    def __init__(self, current_key: str = "", parent=None):
        super().__init__(parent)
        self.setWindowTitle("AI Auto-Fill Settings")
        self.setMinimumWidth(500)
        self.api_key = current_key
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup dialog UI"""
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("🤖 Google Gemini AI Configuration")
        title.setStyleSheet("font-size: 14pt; font-weight: bold; color: #0078d4;")
        layout.addWidget(title)
        
        # Info text
        info = QTextEdit()
        info.setReadOnly(True)
        info.setMaximumHeight(120)
        info.setHtml("""
        <p><b>Free AI-powered auto-fill for screenshots!</b></p>
        <p>Get your free API key:</p>
        <ol>
            <li>Visit: <a href="https://makersuite.google.com/app/apikey">https://makersuite.google.com/app/apikey</a></li>
            <li>Sign in with Google account</li>
            <li>Click "Create API Key"</li>
            <li>Copy and paste below</li>
        </ol>
        <p><i>✨ Free tier: 60 requests/minute (plenty for students!)</i></p>
        """)
        info.setOpenExternalLinks(True)
        layout.addWidget(info)
        
        # API Key input
        key_layout = QHBoxLayout()
        key_layout.addWidget(QLabel("API Key:"))
        
        self.txt_api_key = QLineEdit()
        self.txt_api_key.setPlaceholderText("Paste your Gemini API key here...")
        self.txt_api_key.setText(self.api_key)
        self.txt_api_key.setEchoMode(QLineEdit.EchoMode.Password)
        key_layout.addWidget(self.txt_api_key)
        
        self.btn_show = QPushButton("👁️")
        self.btn_show.setMaximumWidth(40)
        self.btn_show.setToolTip("Show/Hide API key")
        self.btn_show.clicked.connect(self.toggle_visibility)
        key_layout.addWidget(self.btn_show)
        
        layout.addLayout(key_layout)
        
        # Test button
        self.btn_test = QPushButton("🧪 Test Connection")
        self.btn_test.clicked.connect(self.test_connection)
        layout.addWidget(self.btn_test)
        
        # Status label
        self.lbl_status = QLabel("")
        self.lbl_status.setWordWrap(True)
        layout.addWidget(self.lbl_status)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.btn_save = QPushButton("💾 Save")
        self.btn_save.clicked.connect(self.accept)
        
        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.clicked.connect(self.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(self.btn_save)
        button_layout.addWidget(self.btn_cancel)
        
        layout.addLayout(button_layout)
        
        # Privacy note
        privacy = QLabel(
            "🔒 <i>Your API key is stored locally and never shared. "
            "Images are sent to Google Gemini for analysis.</i>"
        )
        privacy.setStyleSheet("color: #666; font-size: 9pt;")
        privacy.setWordWrap(True)
        layout.addWidget(privacy)
    
    def toggle_visibility(self):
        """Toggle API key visibility"""
        if self.txt_api_key.echoMode() == QLineEdit.EchoMode.Password:
            self.txt_api_key.setEchoMode(QLineEdit.EchoMode.Normal)
            self.btn_show.setText("🙈")
        else:
            self.txt_api_key.setEchoMode(QLineEdit.EchoMode.Password)
            self.btn_show.setText("👁️")
    
    def test_connection(self):
        """Test API connection"""
        api_key = self.txt_api_key.text().strip()
        
        if not api_key:
            self.lbl_status.setText("⚠️ Please enter an API key first")
            self.lbl_status.setStyleSheet("color: orange;")
            return
        
        self.lbl_status.setText("🔄 Testing connection...")
        self.lbl_status.setStyleSheet("color: blue;")
        self.btn_test.setEnabled(False)
        
        # Import here to avoid circular imports
        from app.core.ai_analyzer import AIAnalyzer
        
        try:
            analyzer = AIAnalyzer(api_key=api_key)
            success = analyzer.test_connection()
            
            if success:
                self.lbl_status.setText("✅ Connection successful! AI is ready to use.")
                self.lbl_status.setStyleSheet("color: green;")
            else:
                self.lbl_status.setText("❌ Connection failed. Check your API key.")
                self.lbl_status.setStyleSheet("color: red;")
        
        except Exception as e:
            self.lbl_status.setText(f"❌ Error: {str(e)}")
            self.lbl_status.setStyleSheet("color: red;")
        
        finally:
            self.btn_test.setEnabled(True)
    
    def get_api_key(self) -> str:
        """Get the entered API key"""
        return self.txt_api_key.text().strip()


class QuickAISetupDialog(QDialog):
    """Quick first-time setup for AI"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Enable AI Auto-Fill")
        self.setMinimumWidth(450)
        self.api_key = ""
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup dialog UI"""
        layout = QVBoxLayout(self)
        
        # Icon and title
        title = QLabel("🤖 Enable AI-Powered Auto-Fill")
        title.setStyleSheet("font-size: 14pt; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Description
        desc = QLabel(
            "Let AI automatically fill in Title, Details, and Location "
            "by analyzing your screenshots!\n\n"
            "✨ Free • Fast • Accurate"
        )
        desc.setWordWrap(True)
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc.setStyleSheet("color: #666; margin: 10px;")
        layout.addWidget(desc)
        
        # API Key input
        key_label = QLabel("Gemini API Key:")
        layout.addWidget(key_label)
        
        self.txt_api_key = QLineEdit()
        self.txt_api_key.setPlaceholderText("Paste your API key here...")
        layout.addWidget(self.txt_api_key)
        
        # Get key link
        link = QLabel(
            '<a href="https://makersuite.google.com/app/apikey">'
            '→ Get free API key (opens in browser)</a>'
        )
        link.setOpenExternalLinks(True)
        link.setStyleSheet("margin-bottom: 10px;")
        layout.addWidget(link)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.btn_enable = QPushButton("✅ Enable AI")
        self.btn_enable.clicked.connect(self.accept)
        
        self.btn_skip = QPushButton("Skip for now")
        self.btn_skip.clicked.connect(self.reject)
        
        button_layout.addWidget(self.btn_skip)
        button_layout.addWidget(self.btn_enable)
        
        layout.addLayout(button_layout)
        
        # Note
        note = QLabel("<i>You can enable this later in Settings</i>")
        note.setStyleSheet("color: #999; font-size: 9pt;")
        note.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(note)
    
    def get_api_key(self) -> str:
        """Get the entered API key"""
        return self.txt_api_key.text().strip()
