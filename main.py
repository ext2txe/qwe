"""QWSEngine - Main entry point

This is the corrected version that properly integrates the controller and browser windows.
"""

import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from qwsengine.app_info import APP_ID
from qwsengine.ui import resources_rc  # noqa: F401 - ensure Qt resources are registered

from qwsengine.core import AppContext
from qwsengine.core.settings import SettingsManager
from qwsengine.ui.browser_window import BrowserWindow
from qwsengine.ui.browser_controller_window import BrowserControllerWindow


def main() -> None:
    """Application entry point."""
    app = QApplication(sys.argv)

    # Windows taskbar grouping + app identity
    try:
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_ID)
    except Exception:
        # Non-Windows or failure – just ignore
        pass

    # Set main application icon from Qt resources
    try:
        app.setWindowIcon(QIcon(":/qws/icons/logo.ico"))
    except Exception:
        # Icon is nice to have but not critical
        pass

    # Initialize context with the Qt application
    ctx = AppContext.create(qt_app=app)
    settings_manager = ctx.settings_manager

    # Create controller window first
    controller_window = BrowserControllerWindow(
        parent=None,
        settings_manager=settings_manager,
    )
    controller_window.show()
    controller_window.update_status("Controller ready")

    # Check if browser should auto-launch
    should_auto_launch_browser = settings_manager.get("auto_launch_browser", True)

    browser_window = None
    if should_auto_launch_browser:
        # Create browser window
        browser_window = BrowserWindow(
            ctx=ctx,
            settings_manager=settings_manager,
        )
        browser_window.show()
        
        # Wire controller to browser - THIS IS THE KEY INTEGRATION
        controller_window.browser_window = browser_window
        controller_window.update_status("Connected to browser - Ready")

    # Run event loop with error handling
    try:
        sys.exit(app.exec())
    except Exception as e:
        # Best-effort logging
        try:
            if browser_window is not None and hasattr(browser_window, "settings_manager"):
                browser_window.settings_manager.log_error("App", f"Application crashed: {e}")
        except Exception:
            pass
        raise


if __name__ == "__main__":
    main()