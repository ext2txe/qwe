"""Pause/Sleep command."""

import time
from ..command import ScriptCommand


class PauseCommand(ScriptCommand):
    """Pause execution for specified number of seconds.
    
    Parameters:
        seconds (float): Number of seconds to pause (must be positive)
    """
    
    def __init__(self, seconds: float):
        """Initialize Pause command.
        
        Args:
            seconds: Seconds to sleep
            
        Raises:
            ValueError: If seconds is negative
        """
        if seconds < 0:
            raise ValueError("Seconds must be non-negative")
        self.seconds = float(seconds)
    
    def execute(self, context):
        """Execute the command.
        
        Args:
            context: ExecutionContext
        """
        if self.seconds > 0:
            context.log(f"Pausing for {self.seconds} seconds...")
            time.sleep(self.seconds)
            context.log(f"Pause complete")
        else:
            context.log("Pause duration is 0 seconds")
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create from dictionary.
        
        Args:
            data: Dictionary with 'seconds' key
            
        Returns:
            PauseCommand instance
            
        Raises:
            ValueError: If seconds not provided or invalid
        """
        if 'seconds' not in data:
            raise ValueError("'seconds' parameter is required")
        
        try:
            seconds = float(data['seconds'])
        except (ValueError, TypeError):
            raise ValueError(f"'seconds' must be a number, got: {data['seconds']}")
        
        return cls(seconds)
    
    def to_dict(self) -> dict:
        """Convert to dictionary.
        
        Returns:
            Dictionary representation
        """
        return {
            'command': 'pause',
            'seconds': self.seconds
        }