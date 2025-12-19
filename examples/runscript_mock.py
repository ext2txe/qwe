"""Example of running a QWSEngine script with mock objects (headless/testing mode)."""

import sys
from pathlib import Path

# Add the src directory to path so we can import qwsengine
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# IMPORTANT: Create QApplication before importing any Qt-dependent modules
# SettingsManager uses QWebEngineProfile, which requires Qt to be initialized
from PySide6.QtWidgets import QApplication

# Create minimal Qt app (doesn't show any windows)
app = QApplication(sys.argv)

from qwsengine.scripting import ScriptExecutor, ExecutionContext
from qwsengine.core.settings import SettingsManager


class MockView:
    """Mock browser view for testing."""
    def __init__(self, html_content, url="about:blank"):
        self.html_content = html_content
        self._url = url
        self._title = "Mock Page"
        # Fake signal for load finished
        self._load_finished_callbacks = []
    
    def page(self):
        """Return a mock page object."""
        return self
    
    def toHtml(self):
        """Return HTML content."""
        return self.html_content
    
    def url(self):
        """Return current URL."""
        from PySide6.QtCore import QUrl
        return QUrl(self._url)
    
    def title(self):
        """Return page title."""
        return self._title
    
    @property
    def loadFinished(self):
        """Return a mock signal object."""
        return MockSignal(self._load_finished_callbacks)


class MockSignal:
    """Mock Qt signal for testing."""
    def __init__(self, callbacks_list):
        self.callbacks = callbacks_list
    
    def connect(self, callback):
        """Connect a callback to the signal."""
        self.callbacks.append(callback)
        # Immediately emit the signal (page is already loaded in mock)
        callback(True)
    
    def disconnect(self, callback):
        """Disconnect a callback from the signal."""
        try:
            self.callbacks.remove(callback)
        except ValueError:
            pass


class MockTab:
    """Mock browser tab for testing."""
    def __init__(self):
        self.html_content = "<html><body>Mock page</body></html>"
        self._url = "about:blank"
        self.view = MockView(self.html_content, self._url)


class MockTabManager:
    """Mock tab manager for testing."""
    def __init__(self):
        self.current_tab = MockTab()
    
    def navigate_current(self, url):
        """Mock navigation."""
        print(f"[MockBrowser] Navigating to: {url}")
        # Update the tab's HTML content to reflect the navigation
        html_content = f"<html><head><title>{url}</title></head><body>Content from {url}</body></html>"
        self.current_tab.html_content = html_content
        self.current_tab._url = url
        # Update the view with the new content and URL
        self.current_tab.view = MockView(html_content, url)
    
    def get_current_tab(self):
        """Get current tab."""
        return self.current_tab


class MockBrowserWindow:
    """Mock browser window for testing/headless mode."""
    def __init__(self, settings_manager=None):
        self.settings_manager = settings_manager
        self.tab_manager = MockTabManager()
    
    def save_html(self, filename, path):
        """Save HTML to file."""
        output_dir = Path(path)
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / filename
        
        tab = self.tab_manager.get_current_tab()
        
        # Get HTML content from the view
        html_content = ""
        if tab.view:
            # Try to get HTML from view's toHtml() method
            try:
                html_content = tab.view.toHtml()
            except Exception:
                # Fallback to html_content attribute
                html_content = tab.html_content
        else:
            html_content = tab.html_content
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"[MockBrowser] Saved HTML to: {output_path}")


def main():
    """Main function to execute a script with mocks."""
    
    # Create settings manager (now Qt is initialized)
    settings_manager = SettingsManager()
    
    # Create mock browser window (no GUI window shown)
    my_browser_window = MockBrowserWindow(settings_manager=settings_manager)
    
    # Create execution context with your browser window
    context = ExecutionContext(
        browser_window=my_browser_window,
        settings_manager=settings_manager
    )
    
    # Create executor
    executor = ScriptExecutor(context)
    
    # Load from JSON
    script_json = {
        "version": "1.0",
        "commands": [
            {"command": "load_url", "url": "https://codaland.com/ip.php"},
            {"command": "save_html", "filename": "m_page1.html", "path": "./output"},
            {"command": "pause", "seconds": 1},  # Reduced for testing
            {"command": "load_url", "url": "https://codaland.com/ipcheck.php"},
            {"command": "save_html", "filename": "m_page2.html", "path": "./output"},
            {"command": "pause", "seconds": 1}  # Reduced for testing
        ]
    }
    
    executor.load_from_json(script_json)
    
    # Execute with progress callback
    def on_progress(current, total, description):
        print(f"[Progress] [{current+1}/{total}] {description}")
    
    print("Starting script execution...\n")
    success = executor.execute(on_progress=on_progress)
    
    # Check results
    print()
    if success:
        print("✓ Script executed successfully!")
    else:
        print("✗ Errors occurred:")
        for idx, cmd, error in executor.get_errors():
            print(f"  [{idx}] {cmd}: {error}")
    
    # View logs
    print("\n--- Execution Logs ---")
    for log in context.get_logs():
        print(log)
    
    # Proper cleanup
    app.quit()


if __name__ == "__main__":
    main()
