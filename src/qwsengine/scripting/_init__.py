"""QWSEngine scripting module."""

from .executor import ScriptExecutor
from .context import ExecutionContext
from .registry import CommandRegistry

# Import all commands
from .commands.load_url import LoadURLCommand
from .commands.pause import PauseCommand
from .commands.save_html import SaveHTMLCommand
from .commands.save_text import SaveTextCommand

# Register all commands
CommandRegistry.register('load_url', LoadURLCommand)
CommandRegistry.register('pause', PauseCommand)
CommandRegistry.register('save_html', SaveHTMLCommand)
CommandRegistry.register('save_text', SaveTextCommand)

__all__ = [
    'ScriptExecutor',
    'ExecutionContext',
    'CommandRegistry',
    'LoadURLCommand',
    'PauseCommand',
    'SaveHTMLCommand',
    'SaveTextCommand',
]
