"""Save HTML command."""

from pathlib import Path
from ..command import ScriptCommand


class SaveHTMLCommand(ScriptCommand):
    """Save current page HTML to file.
    
    Parameters:
        filename (str): Output filename (default: 'page.html')
        path (str): Output directory path (default: current directory)
    """
    
    def __init__(self, filename: str = None, path: str = None):
        """Initialize SaveHTML command.
        
        Args:
            filename: Output filename
            path: Output directory
        """
        self.filename = filename or "page.html"
        self.path = path or "."
    
    def execute(self, context):
        """Execute the command.
        
        Args:
            context: ExecutionContext
            
        Raises:
            RuntimeError: If save fails
        """
        if not context.browser_window:
            raise RuntimeError("No browser window available")
        
        try:
            # Get current tab
            tab = None
            if hasattr(context.browser_window, 'tab_manager'):
                tab = context.browser_window.tab_manager.get_current_tab()
            
            if not tab:
                raise RuntimeError("No active tab available")
            
            # Create output directory if needed
            output_dir = Path(self.path)
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Save HTML
            output_path = output_dir / self.filename
            context.log(f"Saving HTML to: {output_path}")
            
            # Get HTML content from browser view
            if hasattr(tab, 'view') and tab.view:
                # Use toHtml if available, otherwise use the browser's save function
                if hasattr(context.browser_window, 'save_html'):
                    context.browser_window.save_html(self.filename, self.path)
                else:
                    # Fallback: extract HTML manually
                    html = self._extract_html(tab.view)
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(html)
            else:
                raise RuntimeError("No browser view available")
            
            context.log(f"HTML saved successfully: {output_path}")
            
        except Exception as e:
            raise RuntimeError(f"Failed to save HTML: {e}")
    
    def _extract_html(self, browser_view):
        """Extract HTML from browser view.
        
        Args:
            browser_view: QWebEngineView instance
            
        Returns:
            HTML content as string
        """
        # This would need to be implemented based on your browser_view structure
        # For now, this is a placeholder
        page = browser_view.page()
        if page:
            # Use toHtml (async in WebEngine, might need callback)
            return page.toHtml()
        return ""
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create from dictionary.
        
        Args:
            data: Dictionary with optional 'filename' and 'path' keys
            
        Returns:
            SaveHTMLCommand instance
        """
        filename = data.get('filename', 'page.html')
        path = data.get('path', '.')
        return cls(filename, path)
    
    def to_dict(self) -> dict:
        """Convert to dictionary.
        
        Returns:
            Dictionary representation
        """
        return {
            'command': 'save_html',
            'filename': self.filename,
            'path': self.path
        }