"""Load URL command."""

from ..command import ScriptCommand


class LoadURLCommand(ScriptCommand):
    """Load a URL in the browser.
    
    Parameters:
        url (str): URL to load
        wait_for_load (bool): Wait for page to load (default: True)
    """
    
    def __init__(self, url: str, wait_for_load: bool = True):
        """Initialize LoadURL command.
        
        Args:
            url: URL to load
            wait_for_load: Wait for page load to complete
        """
        if not url:
            raise ValueError("URL cannot be empty")
        self.url = url
        self.wait_for_load = wait_for_load
    
    def execute(self, context):
        """Execute the command.
        
        Args:
            context: ExecutionContext
            
        Raises:
            RuntimeError: If no browser window available
        """
        if not context.browser_window:
            raise RuntimeError("No browser window available")
        
        try:
            context.log(f"Loading URL: {self.url}")
            
            # Navigate to URL
            if hasattr(context.browser_window, 'tab_manager'):
                # Use tab manager if available
                context.browser_window.tab_manager.navigate_current(self.url)
            else:
                # Fallback
                raise RuntimeError("Tab manager not available")
            
            context.log(f"URL loaded successfully: {self.url}")
            
        except Exception as e:
            raise RuntimeError(f"Failed to load URL {self.url}: {e}")
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create from dictionary.
        
        Args:
            data: Dictionary with 'url' key
            
        Returns:
            LoadURLCommand instance
        """
        url = data.get('url')
        if not url:
            raise ValueError("'url' parameter is required")
        
        wait = data.get('wait_for_load', True)
        return cls(url, wait)
    
    def to_dict(self) -> dict:
        """Convert to dictionary.
        
        Returns:
            Dictionary representation
        """
        return {
            'command': 'load_url',
            'url': self.url,
            'wait_for_load': self.wait_for_load
        }