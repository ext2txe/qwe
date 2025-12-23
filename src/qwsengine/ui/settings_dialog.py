"""
Enhanced Settings Dialog for QWE
Provides comprehensive settings UI with tabs and helper dialogs
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QCheckBox,
    QPushButton, QMessageBox, QTabWidget, QWidget, QSpinBox, QComboBox,
    QGroupBox, QFileDialog, QTextEdit, QFormLayout, QGridLayout, QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIntValidator
import json


class SettingsDialog(QDialog):
    """
    Enhanced settings dialog with tabbed interface.
    
    Tabs:
    - General: Basic browser settings
    - Privacy: User-Agent, headers, tracking
    - Proxy: Proxy configuration
    - Logging: Log settings and file access
    - Scripting: Script execution settings
    - Advanced: Custom headers, browser data
    """
    
    def __init__(self, parent=None, settings_manager=None):
        super().__init__(parent)
        self.settings_manager = settings_manager
        self.setWindowTitle("QWE Settings")
        self.setModal(True)
        self.resize(700, 600)
        
        self._setup_ui()
        self._load_current_settings()
    
    def _setup_ui(self):
        """Create the main UI layout with tabs."""
        main_layout = QVBoxLayout(self)
        
        # Create tab widget
        self.tabs = QTabWidget()
        
        # Add tabs
        self.tabs.addTab(self._create_general_tab(), "General")
        self.tabs.addTab(self._create_privacy_tab(), "Privacy && Security")
        self.tabs.addTab(self._create_proxy_tab(), "Proxy")
        self.tabs.addTab(self._create_logging_tab(), "Logging")
        self.tabs.addTab(self._create_scripting_tab(), "Scripting")
        self.tabs.addTab(self._create_advanced_tab(), "Advanced")
        
        main_layout.addWidget(self.tabs)
        
        # Info label
        info_label = QLabel("Settings are saved immediately. Some changes require browser restart.")
        info_label.setStyleSheet("color: gray; font-size: 10px;")
        info_label.setWordWrap(True)
        main_layout.addWidget(info_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        reset_button = QPushButton("Reset to Defaults")
        reset_button.setToolTip("Reset all settings to default values")
        reset_button.clicked.connect(self._reset_to_defaults)
        
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        
        save_button = QPushButton("Save")
        save_button.setDefault(True)
        save_button.clicked.connect(self._save_settings)
        
        button_layout.addWidget(reset_button)
        button_layout.addStretch()
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(save_button)
        
        main_layout.addLayout(button_layout)
    
    # =========================================================================
    # TAB 1: GENERAL
    # =========================================================================
    
    def _create_general_tab(self):
        """General browser settings."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # --- Startup ---
        startup_group = QGroupBox("Startup")
        startup_layout = QVBoxLayout()
        
        # Auto-launch browser
        self.auto_launch = QCheckBox("Automatically launch browser on startup")
        self.auto_launch.setToolTip("Open browser window automatically when application starts")
        startup_layout.addWidget(self.auto_launch)
        
        # Start URL
        url_layout = QHBoxLayout()
        url_layout.addWidget(QLabel("Start URL:"))
        self.start_url = QLineEdit()
        self.start_url.setPlaceholderText("https://example.com")
        self.start_url.setToolTip("Default URL for new tabs and browser launch")
        url_layout.addWidget(self.start_url)
        startup_layout.addLayout(url_layout)
        
        startup_group.setLayout(startup_layout)
        layout.addWidget(startup_group)
        
        # --- Window Size ---
        window_group = QGroupBox("Default Window Size")
        window_layout = QFormLayout()
        
        # Width
        self.window_width = QSpinBox()
        self.window_width.setRange(400, 7680)
        self.window_width.setSingleStep(100)
        self.window_width.setSuffix(" px")
        self.window_width.setToolTip("Initial window width (400-7680 pixels)")
        window_layout.addRow("Width:", self.window_width)
        
        # Height
        self.window_height = QSpinBox()
        self.window_height.setRange(300, 4320)
        self.window_height.setSingleStep(100)
        self.window_height.setSuffix(" px")
        self.window_height.setToolTip("Initial window height (300-4320 pixels)")
        window_layout.addRow("Height:", self.window_height)
        
        # Note
        note = QLabel("Note: Current window size is saved automatically")
        note.setStyleSheet("color: gray; font-size: 9px;")
        window_layout.addRow("", note)
        
        window_group.setLayout(window_layout)
        layout.addWidget(window_group)
        
        layout.addStretch()
        return widget
    
    # =========================================================================
    # TAB 2: PRIVACY & SECURITY
    # =========================================================================
    
    def _create_privacy_tab(self):
        """Privacy and security settings."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # --- Identity ---
        identity_group = QGroupBox("Browser Identity")
        identity_layout = QVBoxLayout()
        
        # User-Agent
        ua_layout = QHBoxLayout()
        ua_layout.addWidget(QLabel("User-Agent:"))
        self.user_agent = QLineEdit()
        self.user_agent.setPlaceholderText("Leave blank for default")
        self.user_agent.setToolTip("Custom User-Agent string (blank = use default)")
        ua_layout.addWidget(self.user_agent)
        
        ua_reset_btn = QPushButton("Reset")
        ua_reset_btn.setToolTip("Clear to use default User-Agent")
        ua_reset_btn.clicked.connect(lambda: self.user_agent.clear())
        ua_layout.addWidget(ua_reset_btn)
        
        identity_layout.addLayout(ua_layout)
        
        # Accept-Language
        lang_layout = QHBoxLayout()
        lang_layout.addWidget(QLabel("Accept-Language:"))
        self.accept_language = QLineEdit()
        self.accept_language.setPlaceholderText("en-US,en;q=0.9")
        self.accept_language.setToolTip("Language preferences header (e.g., en-US,en;q=0.9)")
        lang_layout.addWidget(self.accept_language)
        
        lang_reset_btn = QPushButton("Reset")
        lang_reset_btn.setToolTip("Reset to default")
        lang_reset_btn.clicked.connect(lambda: self.accept_language.setText("en-US,en;q=0.9"))
        lang_layout.addWidget(lang_reset_btn)
        
        identity_layout.addLayout(lang_layout)
        
        identity_group.setLayout(identity_layout)
        layout.addWidget(identity_group)
        
        # --- Privacy ---
        privacy_group = QGroupBox("Privacy Options")
        privacy_layout = QVBoxLayout()
        
        # DNT
        self.send_dnt = QCheckBox("Send Do Not Track (DNT) header")
        self.send_dnt.setToolTip("Request that websites not track your browsing")
        privacy_layout.addWidget(self.send_dnt)
        
        # Chrome hints
        self.spoof_chrome_hints = QCheckBox("Spoof Chrome client hints")
        self.spoof_chrome_hints.setToolTip("Send Chrome-compatible client hint headers")
        privacy_layout.addWidget(self.spoof_chrome_hints)
        
        privacy_group.setLayout(privacy_layout)
        layout.addWidget(privacy_group)
        
        # --- Data Persistence ---
        data_group = QGroupBox("Data Persistence")
        data_layout = QVBoxLayout()
        
        self.persist_cookies = QCheckBox("Persist cookies (remember logins)")
        self.persist_cookies.setToolTip("Save cookies between sessions")
        data_layout.addWidget(self.persist_cookies)
        
        self.persist_cache = QCheckBox("Persist cache (faster page loading)")
        self.persist_cache.setToolTip("Cache web resources to disk")
        data_layout.addWidget(self.persist_cache)
        
        # Clear data button
        clear_btn = QPushButton("Clear All Browser Data")
        clear_btn.setToolTip("Delete all cookies, cache, and stored data")
        clear_btn.clicked.connect(self._clear_browser_data)
        data_layout.addWidget(clear_btn)
        
        data_group.setLayout(data_layout)
        layout.addWidget(data_group)
        
        layout.addStretch()
        return widget
    
    # =========================================================================
    # TAB 3: PROXY
    # =========================================================================
    
    def _create_proxy_tab(self):
        """Proxy configuration."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        proxy_group = QGroupBox("Proxy Configuration")
        proxy_layout = QVBoxLayout()
        
        # Mode
        mode_layout = QHBoxLayout()
        mode_layout.addWidget(QLabel("Proxy Mode:"))
        self.proxy_mode = QComboBox()
        self.proxy_mode.addItems(["system", "manual", "none"])
        self.proxy_mode.setToolTip(
            "system: Use system proxy settings\n"
            "manual: Configure proxy manually\n"
            "none: Direct connection (no proxy)"
        )
        mode_layout.addWidget(self.proxy_mode)
        mode_layout.addStretch()
        proxy_layout.addLayout(mode_layout)
        
        # Manual settings (enabled only when mode == manual)
        manual_group = QGroupBox("Manual Proxy Settings")
        manual_layout = QFormLayout()
        
        # Type
        self.proxy_type = QComboBox()
        self.proxy_type.addItems(["http", "socks5"])
        self.proxy_type.setToolTip("Proxy protocol type")
        manual_layout.addRow("Type:", self.proxy_type)
        
        # Host
        self.proxy_host = QLineEdit()
        self.proxy_host.setPlaceholderText("proxy.example.com")
        self.proxy_host.setToolTip("Proxy server hostname or IP address")
        manual_layout.addRow("Host:", self.proxy_host)
        
        # Port
        self.proxy_port = QSpinBox()
        self.proxy_port.setRange(0, 65535)
        self.proxy_port.setToolTip("Proxy server port (1-65535)")
        manual_layout.addRow("Port:", self.proxy_port)
        
        # Username
        self.proxy_user = QLineEdit()
        self.proxy_user.setPlaceholderText("Optional")
        self.proxy_user.setToolTip("Proxy authentication username (if required)")
        manual_layout.addRow("Username:", self.proxy_user)
        
        # Password
        self.proxy_password = QLineEdit()
        self.proxy_password.setPlaceholderText("Optional")
        self.proxy_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.proxy_password.setToolTip("Proxy authentication password (if required)")
        manual_layout.addRow("Password:", self.proxy_password)
        
        manual_group.setLayout(manual_layout)
        proxy_layout.addWidget(manual_group)
        
        # Store reference to manual group for enable/disable
        self.proxy_manual_group = manual_group
        
        # Enable/disable manual settings based on mode
        def update_proxy_fields():
            manual = (self.proxy_mode.currentText() == "manual")
            self.proxy_manual_group.setEnabled(manual)
        
        self.proxy_mode.currentTextChanged.connect(lambda: update_proxy_fields())
        
        proxy_group.setLayout(proxy_layout)
        layout.addWidget(proxy_group)
        
        # Test connection button (future feature)
        test_btn = QPushButton("Test Proxy Connection")
        test_btn.setToolTip("Test if proxy is reachable (not yet implemented)")
        test_btn.setEnabled(False)
        layout.addWidget(test_btn)
        
        layout.addStretch()
        return widget
    
    # =========================================================================
    # TAB 4: LOGGING
    # =========================================================================
    
    def _create_logging_tab(self):
        """Logging settings."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # --- Enable/Disable ---
        logging_group = QGroupBox("Logging Options")
        logging_layout = QVBoxLayout()
        
        self.logging_enabled = QCheckBox("Enable logging")
        self.logging_enabled.setToolTip("Master switch for all logging")
        logging_layout.addWidget(self.logging_enabled)
        
        # What to log
        log_options_layout = QVBoxLayout()
        log_options_layout.setContentsMargins(20, 0, 0, 0)  # Indent
        
        self.log_navigation = QCheckBox("Log page navigation")
        self.log_navigation.setToolTip("Log when pages are loaded")
        log_options_layout.addWidget(self.log_navigation)
        
        self.log_tab_actions = QCheckBox("Log tab actions")
        self.log_tab_actions.setToolTip("Log tab creation, closure, switching")
        log_options_layout.addWidget(self.log_tab_actions)
        
        self.log_errors = QCheckBox("Log errors")
        self.log_errors.setToolTip("Log error messages")
        log_options_layout.addWidget(self.log_errors)
        
        logging_layout.addLayout(log_options_layout)
        
        # Enable/disable log options based on master switch
        def update_log_options():
            enabled = self.logging_enabled.isChecked()
            self.log_navigation.setEnabled(enabled)
            self.log_tab_actions.setEnabled(enabled)
            self.log_errors.setEnabled(enabled)
        
        self.logging_enabled.toggled.connect(update_log_options)
        
        logging_group.setLayout(logging_layout)
        layout.addWidget(logging_group)
        
        # --- Log File Info ---
        log_file_group = QGroupBox("Log Files")
        log_file_layout = QVBoxLayout()
        
        # Log directory - safely handle missing attribute
        log_dir = None
        try:
            if self.settings_manager and hasattr(self.settings_manager, 'get_log_dir'):
                log_dir = self.settings_manager.get_log_dir()
        except (AttributeError, Exception):
            pass
            
        if log_dir:
            dir_layout = QHBoxLayout()
            dir_layout.addWidget(QLabel("Log Directory:"))
            dir_label = QLabel(str(log_dir))
            dir_label.setStyleSheet("color: blue; text-decoration: underline;")
            dir_label.setCursor(Qt.CursorShape.PointingHandCursor)
            dir_label.setToolTip("Click to open log directory")
            dir_label.mousePressEvent = lambda e: self._open_log_directory()
            dir_layout.addWidget(dir_label)
            dir_layout.addStretch()
            log_file_layout.addLayout(dir_layout)
        
        # Current log file - safely handle missing attribute
        log_file = None
        try:
            if self.settings_manager and hasattr(self.settings_manager, 'get_log_file_path'):
                log_file = self.settings_manager.get_log_file_path()
        except (AttributeError, Exception):
            pass
            
        if log_file:
            file_layout = QHBoxLayout()
            file_layout.addWidget(QLabel("Current Log File:"))
            file_name = str(log_file.name) if hasattr(log_file, 'name') else str(log_file)
            file_label = QLabel(file_name)
            file_label.setStyleSheet("color: gray; font-size: 9px;")
            file_label.setWordWrap(True)
            file_layout.addWidget(file_label)
            file_layout.addStretch()
            log_file_layout.addLayout(file_layout)
        
        # Open log button
        open_log_btn = QPushButton("Open Log Directory")
        open_log_btn.setToolTip("Open folder containing log files")
        open_log_btn.clicked.connect(self._open_log_directory)
        if not log_dir:
            open_log_btn.setEnabled(False)
            open_log_btn.setToolTip("Log directory not available")
        log_file_layout.addWidget(open_log_btn)
        
        log_file_group.setLayout(log_file_layout)
        layout.addWidget(log_file_group)
        
        layout.addStretch()
        return widget
    
    # =========================================================================
    # TAB 5: SCRIPTING
    # =========================================================================
    
    def _create_scripting_tab(self):
        """Script execution settings."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # --- Output Location ---
        output_group = QGroupBox("Script Output")
        output_layout = QVBoxLayout()
        
        # Save folder
        folder_layout = QHBoxLayout()
        folder_layout.addWidget(QLabel("Save Folder:"))
        
        self.save_folder = QLineEdit()
        self.save_folder.setPlaceholderText("./output/captures")
        self.save_folder.setToolTip("Default folder for SAVE HTML, SAVE TEXT commands")
        folder_layout.addWidget(self.save_folder)
        
        browse_btn = QPushButton("Browse...")
        browse_btn.setToolTip("Select folder")
        browse_btn.clicked.connect(self._browse_save_folder)
        folder_layout.addWidget(browse_btn)
        
        output_layout.addLayout(folder_layout)
        
        # Note
        note = QLabel(
            "Script output files (screenshots, HTML captures, text extracts) "
            "will be saved to this folder with automatic timestamps."
        )
        note.setStyleSheet("color: gray; font-size: 9px;")
        note.setWordWrap(True)
        output_layout.addWidget(note)
        
        output_group.setLayout(output_layout)
        layout.addWidget(output_group)
        
        # --- Future Settings (Placeholders) ---
        execution_group = QGroupBox("Execution Settings (Future)")
        execution_layout = QFormLayout()
        
        # Timeout
        timeout_spin = QSpinBox()
        timeout_spin.setRange(10, 3600)
        timeout_spin.setSuffix(" seconds")
        timeout_spin.setToolTip("Maximum time for script execution")
        timeout_spin.setEnabled(False)
        execution_layout.addRow("Command Timeout:", timeout_spin)
        
        # Max concurrent
        concurrent_spin = QSpinBox()
        concurrent_spin.setRange(1, 10)
        concurrent_spin.setToolTip("Maximum concurrent script executions")
        concurrent_spin.setEnabled(False)
        execution_layout.addRow("Max Concurrent Scripts:", concurrent_spin)
        
        execution_group.setLayout(execution_layout)
        layout.addWidget(execution_group)
        
        layout.addStretch()
        return widget
    
    # =========================================================================
    # TAB 6: ADVANCED
    # =========================================================================
    
    def _create_advanced_tab(self):
        """Advanced settings."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # --- Custom Headers ---
        headers_group = QGroupBox("Custom HTTP Headers")
        headers_layout = QVBoxLayout()
        
        # Global headers
        global_layout = QVBoxLayout()
        global_layout.addWidget(QLabel("Global Headers (sent with all requests):"))
        
        self.headers_global = QTextEdit()
        self.headers_global.setPlaceholderText('{\n  "X-Custom-Header": "value",\n  "X-API-Key": "abc123"\n}')
        self.headers_global.setToolTip("JSON object of headers to send with every request")
        self.headers_global.setMaximumHeight(100)
        global_layout.addWidget(self.headers_global)
        
        headers_layout.addLayout(global_layout)
        
        # Per-host headers
        host_layout = QVBoxLayout()
        host_layout.addWidget(QLabel("Per-Host Headers (sent only to specific hosts):"))
        
        self.headers_per_host = QTextEdit()
        self.headers_per_host.setPlaceholderText(
            '{\n'
            '  "api.example.com": {\n'
            '    "X-API-Key": "key123"\n'
            '  },\n'
            '  "cdn.example.com": {\n'
            '    "X-CDN-Auth": "token456"\n'
            '  }\n'
            '}'
        )
        self.headers_per_host.setToolTip("JSON object mapping hostnames to headers")
        self.headers_per_host.setMaximumHeight(120)
        host_layout.addWidget(self.headers_per_host)
        
        headers_layout.addLayout(host_layout)
        
        # Validate button
        validate_btn = QPushButton("Validate JSON")
        validate_btn.setToolTip("Check if headers are valid JSON")
        validate_btn.clicked.connect(self._validate_headers)
        headers_layout.addWidget(validate_btn)
        
        headers_group.setLayout(headers_layout)
        layout.addWidget(headers_group)
        
        # --- Data Management ---
        data_group = QGroupBox("Browser Data")
        data_layout = QVBoxLayout()
        
        clear_btn = QPushButton("Clear All Browser Data")
        clear_btn.setToolTip("Delete cookies, cache, and all stored data")
        clear_btn.clicked.connect(self._clear_browser_data)
        data_layout.addWidget(clear_btn)
        
        data_note = QLabel("Clearing data requires restart to take effect")
        data_note.setStyleSheet("color: gray; font-size: 9px;")
        data_layout.addWidget(data_note)
        
        data_group.setLayout(data_layout)
        layout.addWidget(data_group)
        
        layout.addStretch()
        return widget
    
    # =========================================================================
    # LOAD CURRENT SETTINGS
    # =========================================================================
    
    def _load_current_settings(self):
        """Load current settings from SettingsManager into UI controls."""
        if not self.settings_manager:
            return
        
        # General
        self.auto_launch.setChecked(
            self.settings_manager.get("auto_launch_browser", True)
        )
        self.start_url.setText(
            self.settings_manager.get("start_url", "https://codaland.com/ipdefault")
        )
        self.window_width.setValue(
            self.settings_manager.get("window_width", 1024)
        )
        self.window_height.setValue(
            self.settings_manager.get("window_height", 768)
        )
        
        # Privacy
        self.user_agent.setText(
            self.settings_manager.get("user_agent", "")
        )
        self.accept_language.setText(
            self.settings_manager.get("accept_language", "en-US,en;q=0.9")
        )
        self.send_dnt.setChecked(
            self.settings_manager.get("send_dnt", False)
        )
        self.spoof_chrome_hints.setChecked(
            self.settings_manager.get("spoof_chrome_client_hints", False)
        )
        self.persist_cookies.setChecked(
            self.settings_manager.get("persist_cookies", True)
        )
        self.persist_cache.setChecked(
            self.settings_manager.get("persist_cache", True)
        )
        
        # Proxy
        self.proxy_mode.setCurrentText(
            self.settings_manager.get("proxy_mode", "system")
        )
        self.proxy_type.setCurrentText(
            self.settings_manager.get("proxy_type", "http")
        )
        self.proxy_host.setText(
            self.settings_manager.get("proxy_host", "")
        )
        self.proxy_port.setValue(
            self.settings_manager.get("proxy_port", 0)
        )
        self.proxy_user.setText(
            self.settings_manager.get("proxy_user", "")
        )
        self.proxy_password.setText(
            self.settings_manager.get("proxy_password", "")
        )
        
        # Trigger proxy fields update
        self.proxy_mode.currentTextChanged.emit(self.proxy_mode.currentText())
        
        # Logging
        self.logging_enabled.setChecked(
            self.settings_manager.get("logging_enabled", True)
        )
        self.log_navigation.setChecked(
            self.settings_manager.get("log_navigation", True)
        )
        self.log_tab_actions.setChecked(
            self.settings_manager.get("log_tab_actions", True)
        )
        self.log_errors.setChecked(
            self.settings_manager.get("log_errors", True)
        )
        
        # Trigger log options update
        self.logging_enabled.toggled.emit(self.logging_enabled.isChecked())
        
        # Scripting
        self.save_folder.setText(
            self.settings_manager.get("save_folder", "./output/captures")
        )
        
        # Advanced - Headers
        headers_global = self.settings_manager.get("headers_global", {})
        if headers_global:
            self.headers_global.setPlainText(
                json.dumps(headers_global, indent=2)
            )
        
        headers_per_host = self.settings_manager.get("headers_per_host", {})
        if headers_per_host:
            self.headers_per_host.setPlainText(
                json.dumps(headers_per_host, indent=2)
            )
    
    # =========================================================================
    # HELPER METHODS
    # =========================================================================
    
    def _browse_save_folder(self):
        """Open folder browser for save folder."""
        current_folder = self.save_folder.text() or "./output/captures"
        
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Save Folder",
            current_folder,
            QFileDialog.Option.ShowDirsOnly
        )
        
        if folder:
            self.save_folder.setText(folder)
    
    def _validate_headers(self):
        """Validate that header JSON is valid."""
        errors = []
        
        # Validate global headers
        global_text = self.headers_global.toPlainText().strip()
        if global_text:
            try:
                json.loads(global_text)
            except json.JSONDecodeError as e:
                errors.append(f"Global headers: {e}")
        
        # Validate per-host headers
        host_text = self.headers_per_host.toPlainText().strip()
        if host_text:
            try:
                json.loads(host_text)
            except json.JSONDecodeError as e:
                errors.append(f"Per-host headers: {e}")
        
        if errors:
            QMessageBox.warning(
                self,
                "Invalid JSON",
                "Header JSON is invalid:\n\n" + "\n".join(errors)
            )
        else:
            QMessageBox.information(
                self,
                "Valid JSON",
                "All header JSON is valid!"
            )
    
    def _clear_browser_data(self):
        """Clear all browser data."""
        reply = QMessageBox.question(
            self,
            "Clear Browser Data",
            "This will delete all cookies, cache, and stored data. Continue?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            if self.settings_manager and self.settings_manager.clear_browser_data():
                QMessageBox.information(
                    self,
                    "Data Cleared",
                    "Browser data cleared successfully! Restart to see changes."
                )
            else:
                QMessageBox.warning(
                    self,
                    "Clear Failed",
                    "Failed to clear browser data."
                )
    
    def _open_log_directory(self):
        """Open the log directory in file manager."""
        if not self.settings_manager:
            return
        
        # Safely get log directory
        log_dir = None
        try:
            if hasattr(self.settings_manager, 'get_log_dir'):
                log_dir = self.settings_manager.get_log_dir()
        except (AttributeError, Exception):
            QMessageBox.warning(
                self,
                "Not Available",
                "Log directory information is not available."
            )
            return
            
        if log_dir and hasattr(log_dir, 'exists') and log_dir.exists():
            import subprocess
            import sys
            
            try:
                if sys.platform == "win32":
                    subprocess.run(["explorer", str(log_dir)])
                elif sys.platform == "darwin":
                    subprocess.run(["open", str(log_dir)])
                else:  # Linux
                    subprocess.run(["xdg-open", str(log_dir)])
            except Exception as e:
                QMessageBox.warning(
                    self,
                    "Error",
                    f"Could not open log directory: {e}"
                )
        else:
            QMessageBox.information(
                self,
                "Not Available",
                "Log directory not found or not configured."
            )
    
    def _reset_to_defaults(self):
        """Reset all settings to defaults."""
        reply = QMessageBox.question(
            self,
            "Reset to Defaults",
            "Reset all settings to default values?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # General
            self.auto_launch.setChecked(True)
            self.start_url.setText("https://codaland.com/ipdefault")
            self.window_width.setValue(1024)
            self.window_height.setValue(768)
            
            # Privacy
            self.user_agent.clear()
            self.accept_language.setText("en-US,en;q=0.9")
            self.send_dnt.setChecked(False)
            self.spoof_chrome_hints.setChecked(False)
            self.persist_cookies.setChecked(True)
            self.persist_cache.setChecked(True)
            
            # Proxy
            self.proxy_mode.setCurrentText("manual")
            self.proxy_type.setCurrentText("http")
            self.proxy_host.clear()
            self.proxy_port.setValue(0)
            self.proxy_user.clear()
            self.proxy_password.clear()
            
            # Logging
            self.logging_enabled.setChecked(True)
            self.log_navigation.setChecked(True)
            self.log_tab_actions.setChecked(True)
            self.log_errors.setChecked(True)
            
            # Scripting
            self.save_folder.setText("./output/captures")
            
            # Advanced
            self.headers_global.clear()
            self.headers_per_host.clear()
    
    # =========================================================================
    # SAVE SETTINGS
    # =========================================================================
    
    def _save_settings(self):
        """Save all settings."""
        try:
            # Validate inputs
            if not self._validate_inputs():
                return
            
            # Parse headers JSON
            headers_global = {}
            headers_per_host = {}
            
            global_text = self.headers_global.toPlainText().strip()
            if global_text:
                try:
                    headers_global = json.loads(global_text)
                except json.JSONDecodeError as e:
                    QMessageBox.warning(
                        self,
                        "Invalid JSON",
                        f"Global headers JSON is invalid: {e}"
                    )
                    return
            
            host_text = self.headers_per_host.toPlainText().strip()
            if host_text:
                try:
                    headers_per_host = json.loads(host_text)
                except json.JSONDecodeError as e:
                    QMessageBox.warning(
                        self,
                        "Invalid JSON",
                        f"Per-host headers JSON is invalid: {e}"
                    )
                    return
            
            # Save all settings
            settings = {
                # General
                "auto_launch_browser": self.auto_launch.isChecked(),
                "start_url": self.start_url.text().strip(),
                "window_width": self.window_width.value(),
                "window_height": self.window_height.value(),
                
                # Privacy
                "user_agent": self.user_agent.text().strip(),
                "accept_language": self.accept_language.text().strip(),
                "send_dnt": self.send_dnt.isChecked(),
                "spoof_chrome_client_hints": self.spoof_chrome_hints.isChecked(),
                "persist_cookies": self.persist_cookies.isChecked(),
                "persist_cache": self.persist_cache.isChecked(),
                
                # Proxy
                "proxy_mode": self.proxy_mode.currentText(),
                "proxy_type": self.proxy_type.currentText(),
                "proxy_host": self.proxy_host.text().strip(),
                "proxy_port": self.proxy_port.value(),
                "proxy_user": self.proxy_user.text().strip(),
                "proxy_password": self.proxy_password.text(),
                
                # Logging
                "logging_enabled": self.logging_enabled.isChecked(),
                "log_navigation": self.log_navigation.isChecked(),
                "log_tab_actions": self.log_tab_actions.isChecked(),
                "log_errors": self.log_errors.isChecked(),
                
                # Scripting
                "save_folder": self.save_folder.text().strip(),
                
                # Advanced
                "headers_global": headers_global,
                "headers_per_host": headers_per_host,
            }
            
            # Apply settings
            for key, value in settings.items():
                self.settings_manager.set(key, value, persist=False)
            
            # Save to file
            if self.settings_manager.save_settings():
                # Apply immediate changes (UA, proxy, etc.)
                self.settings_manager.apply_proxy_settings()
                self.settings_manager.apply_network_overrides()
                
                QMessageBox.information(
                    self,
                    "Settings Saved",
                    "Settings saved successfully!"
                )
                self.accept()
            else:
                QMessageBox.critical(
                    self,
                    "Save Error",
                    "Failed to save settings to file."
                )
                
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"An error occurred while saving: {str(e)}"
            )
    
    def _validate_inputs(self):
        """Validate all inputs before saving."""
        # Validate URL
        url = self.start_url.text().strip()
        if not url:
            QMessageBox.warning(self, "Invalid URL", "Start URL cannot be empty.")
            self.tabs.setCurrentIndex(0)
            return False
        
        if not url.startswith(("http://", "https://")):
            self.start_url.setText("https://" + url)
        
        # Validate window size (already constrained by spinbox, but double-check)
        if self.window_width.value() < 400 or self.window_height.value() < 300:
            QMessageBox.warning(
                self,
                "Invalid Size",
                "Window size must be at least 400x300."
            )
            self.tabs.setCurrentIndex(0)
            return False
        
        # Validate proxy port if manual mode
        if self.proxy_mode.currentText() == "manual":
            if not self.proxy_host.text().strip():
                QMessageBox.warning(
                    self,
                    "Invalid Proxy",
                    "Proxy host is required for manual mode."
                )
                self.tabs.setCurrentIndex(2)
                return False
            
            if self.proxy_port.value() == 0:
                QMessageBox.warning(
                    self,
                    "Invalid Proxy",
                    "Proxy port is required for manual mode."
                )
                self.tabs.setCurrentIndex(2)
                return False
        
        return True
