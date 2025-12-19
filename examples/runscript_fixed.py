"""Example of running a QWSEngine script with proper initialization."""

import sys
from pathlib import Path

# Add the src directory to path so we can import qwsengine
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from PySide6.QtWidgets import QApplication
from qwsengine.scripting import ScriptExecutor, ExecutionContext
from qwsengine.core import AppContext
from qwsengine.core.settings import SettingsManager
from qwsengine.ui.browser_window import BrowserWindow


def main():
    """Main function to execute a script."""
    
    # Create Qt application (required for BrowserWindow to work)
    app = QApplication(sys.argv)
    
    # Initialize context
    ctx = AppContext.create(qt_app=app)
    settings_manager = ctx.settings_manager
    
    # Create browser window (this is required by the commands)
    # Note: For headless/testing, you might want to create a mock instead
    my_browser_window = BrowserWindow(
        ctx=ctx,
        settings_manager=settings_manager,
    )
    # Show the window (required for it to be fully initialized)
    my_browser_window.show()
    
    # Create execution context with your browser window
    context = ExecutionContext(
        browser_window=my_browser_window,
        settings_manager=settings_manager
    )
    
    # Create executor
    executor = ScriptExecutor(context)
    
    # Load from JSON
    # script_json = {
    #     "version": "1.0",
    #     "commands": [
    #         {"command": "load_url", "url": "https://codaland.com/ip.php"},
    #         {"command": "save_html", "filename": "f_page1.html", "path": "./output"},
    #         {"command": "pause", "seconds": 10},
    #         {"command": "load_url", "url": "https://codaland.com/ipcheck.php"},
    #         {"command": "save_html", "filename": "f_page2.html", "path": "./output"},
    #         {"command": "pause", "seconds": 10}
    #     ]
    # }
    
    script_json = {
        "version": "1.0",
        "commands": [
            {"command": "load_url", "url": "https://codaland.com/ip.php"},
            {"command": "pause", "seconds": 5},
            {"command": "load_url", "url": "https://codaland.com/ipcheck.php"},
            {"command": "pause", "seconds": 5}
        ]
    }
    
    executor.load_from_json(script_json)
    
    # Execute with progress callback
    def on_progress(current, total, description):
        print(f"[{current+1}/{total}] {description}")
    
    success = executor.execute(on_progress=on_progress)
    
    # Check results
    if success:
        print("Script executed successfully!")
    else:
        print("Errors occurred:")
        for idx, cmd, error in executor.get_errors():
            print(f"  [{idx}] {cmd}: {error}")
    
    # View logs
    for log in context.get_logs():
        print(log)
    
    # Cleanup
    my_browser_window.close()
    sys.exit(0)


if __name__ == "__main__":
    main()
