"""Base command class for script commands."""

from abc import ABC, abstractmethod


class ScriptCommand(ABC):
    """Abstract base class for all script commands.
    
    All concrete commands must:
    1. Implement execute() method
    2. Implement from_dict() class method (for deserialization)
    3. Implement to_dict() method (for serialization)
    """
    
    @abstractmethod
    def execute(self, context):
        """Execute this command.
        
        Args:
            context: ExecutionContext with browser, settings, logging
            
        Raises:
            RuntimeError: If command cannot be executed
        """
        pass
    
    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict):
        """Create command instance from dictionary.
        
        Args:
            data: Dictionary with command parameters
            
        Returns:
            ScriptCommand instance
        """
        pass
    
    @abstractmethod
    def to_dict(self) -> dict:
        """Convert command to dictionary for serialization.
        
        Returns:
            Dictionary with 'command' key and all parameters
        """
        pass
    
    def __str__(self):
        """String representation for logging."""
        return f"{self.__class__.__name__}({self.to_dict()})"