"""Save Text command with timestamp."""

from pathlib import Path
from datetime import datetime
from ..command import ScriptCommand


class SaveTextCommand(ScriptCommand):
    """Save current page text content to file with timestamp.
    
    Extracts rendered text content (no HTML markup).
    
    Filename format: YYYYMMDDHHMMSS.milliseconds[_TAG].txt
    
    Examples:
        20251222185623.456.txt                  # No tag
        20251222185623.456_results.txt          # With tag
        20251222185623.456_article_content.txt  # Tag with underscores
    
    Parameters:
        tag (str): Optional descriptive tag for filename
        folder (str): Output folder (from settings if not provided)
    """
    
    def __init__(self, tag: str = None, folder: str = None):
        """Initialize SaveText command.
        
        Args:
            tag: Optional tag to append to filename
            folder: Output folder path (uses settings default if None)
        """
        self.tag = self._sanitize_tag(tag) if tag else None
        self.folder = folder
    
    @staticmethod
    def _sanitize_tag(tag: str) -> str:
        """Sanitize tag for safe filename.
        
        Args:
            tag: Raw tag from user
            
        Returns:
            Sanitized tag safe for filenames
        """
        if not tag:
            return None
        
        # Replace spaces with underscores
        tag = tag.strip().replace(' ', '_')
        
        # Remove any characters that aren't alphanumeric or underscore
        tag = ''.join(c for c in tag if c.isalnum() or c == '_')
        
        # Remove leading/trailing underscores
        tag = tag.strip('_')
        
        return tag if tag else None
    
    @staticmethod
    def _generate_filename(tag: str = None) -> str:
        """Generate unique filename with timestamp.
        
        Args:
            tag: Optional tag to include in filename
            
        Returns:
            Filename like: 20251222185623.456.txt or 20251222185623.456_results.txt
        """
        now = datetime.now()
        timestamp = now.strftime('%Y%m%d%H%M%S')
        milliseconds = now.microsecond // 1000
        
        if tag:
            return f"{timestamp}.{milliseconds:03d}_{tag}.txt"
        else:
            return f"{timestamp}.{milliseconds:03d}.txt"
    
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
            # Determine output folder
            folder = self.folder
            if not folder and context.settings_manager:
                folder = context.settings_manager.get("save_folder", "./output/captures")
            else:
                folder = folder or "./output/captures"
            
            # Generate filename
            filename = self._generate_filename(self.tag)
            
            # Create output directory if needed
            output_dir = Path(folder)
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Get text and save
            text = self._extract_text(context)
            filepath = output_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(text)
            
            context.log(f"Saved TEXT to: {filepath}")
            
        except Exception as e:
            raise RuntimeError(f"Failed to save text: {e}")
    
    def _extract_text(self, context):
        """Extract text content from page.
        
        Uses page's rendered text content (innerText).
        
        Args:
            context: ExecutionContext
            
        Returns:
            Text content as string
        """
        from PySide6.QtCore import QEventLoop
        
        # Get current tab
        tab = None
        if hasattr(context.browser_window, 'tab_manager'):
            tab = context.browser_window.tab_manager.get_current_tab()
        
        if not tab or not hasattr(tab, 'view') or not tab.view:
            raise RuntimeError("No active tab or browser view available")
        
        page = tab.view.page()
        if not page:
            raise RuntimeError("No page available")
        
        text_content = []
        
        def handle_text(text):
            """Callback to receive text content."""
            text_content.append(text)
            loop.quit()
        
        try:
            # JavaScript to extract page text
            script = "return document.documentElement.innerText;"
            
            # Create loop first so callback can reference it
            loop = QEventLoop()
            
            # Run JavaScript
            page.runJavaScript(script, handle_text)
            
            # Run event loop until callback receives the text
            loop.exec()
            
            # Return the collected text
            return text_content[0] if text_content else ""
        
        except Exception as e:
            context.log(f"Error extracting text: {e}", level="WARNING")
            return ""
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create from dictionary.
        
        Args:
            data: Dictionary with optional 'tag' and 'folder' keys
            
        Returns:
            SaveTextCommand instance
        """
        tag = data.get('tag')
        folder = data.get('folder')
        return cls(tag=tag, folder=folder)
    
    def to_dict(self) -> dict:
        """Convert to dictionary.
        
        Returns:
            Dictionary representation
        """
        return {
            'command': 'save_text',
            'tag': self.tag
        }
    
    def __str__(self):
        """String representation for logging."""
        if self.tag:
            return f"SaveText(tag={self.tag})"
        else:
            return "SaveText()"
