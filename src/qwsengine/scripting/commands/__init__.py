"""Script commands package."""

from .load_url import LoadURLCommand
from .save_html import SaveHTMLCommand
from .pause import PauseCommand
from ..registry import CommandRegistry

# Auto-register commands when package is imported
def register_all_commands():
    """Register all built-in commands."""
    CommandRegistry.register('load_url', LoadURLCommand)
    CommandRegistry.register('save_html', SaveHTMLCommand)
    CommandRegistry.register('pause', PauseCommand)

# Register on import
register_all_commands()

__all__ = [
    'LoadURLCommand',
    'SaveHTMLCommand',
    'PauseCommand',
    'CommandRegistry'
]