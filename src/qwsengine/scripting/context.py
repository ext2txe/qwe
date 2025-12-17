"""Execution context - passed to commands, provides utilities."""

from datetime import datetime


class ExecutionContext:
    """Context for command execution.
    
    Provides:
    - Access to browser window
    - Access to settings
    - Logging functionality
    - Execution state
    """
    
    def __init__(self, browser_window=None, settings_manager=None):
        """Initialize execution context.
        
        Args:
            browser_window: Reference to BrowserWindow
            settings_manager: Reference to SettingsManager
        """
        self.browser_window = browser_window
        self.settings_manager = settings_manager
        
        # Execution control
        self.stop_on_error = False
        self.pause_on_error = False
        
        # Logging
        self.logs = []
        self.log_to_console = True
    
    def log(self, message: str, level: str = "INFO"):
        """Log a message.
        
        Args:
            message: Message to log
            level: Log level (INFO, WARNING, ERROR)
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        self.logs.append(log_entry)
        
        if self.log_to_console:
            print(log_entry)
    
    def get_logs(self) -> list:
        """Get all logged messages.
        
        Returns:
            List of log entries
        """
        return self.logs.copy()
    
    def clear_logs(self):
        """Clear log history."""
        self.logs.clear()
    
    def __repr__(self):
        return (
            f"ExecutionContext("
            f"browser={self.browser_window is not None}, "
            f"settings={self.settings_manager is not None})"
        )