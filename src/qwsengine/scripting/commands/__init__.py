"""Command module - imports and registers all available commands."""

# Import all command classes
from .load_url import LoadURLCommand
from .pause import PauseCommand
from .save_html import SaveHTMLCommand
from .save_text import SaveTextCommand

# Import the registry
from ..registry import CommandRegistry

# Register all commands
CommandRegistry.register('load_url', LoadURLCommand)
CommandRegistry.register('pause', PauseCommand)
CommandRegistry.register('save_html', SaveHTMLCommand)
CommandRegistry.register('save_text', SaveTextCommand)

# Export command classes
__all__ = [
    'LoadURLCommand',
    'PauseCommand',
    'SaveHTMLCommand',
    'SaveTextCommand',
]
