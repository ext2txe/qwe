# At the top with other imports
from .save_html import SaveHTMLCommand
from .save_text import SaveTextCommand

# In the section where commands are registered (look for CommandRegistry.register calls)
# This might be in __init__.py or in a separate registration function

from ..registry import CommandRegistry

# Register save_html command
CommandRegistry.register('save_html', SaveHTMLCommand)

# Register save_text command
CommandRegistry.register('save_text', SaveTextCommand)


# ============================================================================
# EXAMPLE: If the file currently looks like this:
# ============================================================================

"""
from .load_url import LoadURLCommand
from .pause import PauseCommand
from .save_html import SaveHTMLCommand

from ..registry import CommandRegistry

CommandRegistry.register('load_url', LoadURLCommand)
CommandRegistry.register('pause', PauseCommand)
CommandRegistry.register('save_html', SaveHTMLCommand)
"""

# UPDATE IT TO:

"""
from .load_url import LoadURLCommand
from .pause import PauseCommand
from .save_html import SaveHTMLCommand
from .save_text import SaveTextCommand

from ..registry import CommandRegistry

CommandRegistry.register('load_url', LoadURLCommand)
CommandRegistry.register('pause', PauseCommand)
CommandRegistry.register('save_html', SaveHTMLCommand)
CommandRegistry.register('save_text', SaveTextCommand)
"""
