"""Command registry - central place to register and retrieve commands."""


class CommandRegistry:
    """Registry for available script commands.
    
    Allows:
    - Registering new commands
    - Creating commands by name
    - Listing available commands
    """
    
    _registry = {}
    
    @classmethod
    def register(cls, command_name: str, command_class):
        """Register a command class.
        
        Args:
            command_name: Name of command (e.g., 'load_url')
            command_class: Class implementing ScriptCommand
        """
        if command_name in cls._registry:
            raise ValueError(f"Command already registered: {command_name}")
        
        if not hasattr(command_class, 'from_dict'):
            raise ValueError(f"Command must implement from_dict: {command_name}")
        
        cls._registry[command_name] = command_class
        print(f"[Registry] Registered command: {command_name}")
    
    @classmethod
    def unregister(cls, command_name: str):
        """Unregister a command.
        
        Args:
            command_name: Name of command to remove
        """
        if command_name in cls._registry:
            del cls._registry[command_name]
            print(f"[Registry] Unregistered command: {command_name}")
    
    @classmethod
    def get(cls, command_name: str):
        """Get command class by name.
        
        Args:
            command_name: Name of command
            
        Returns:
            Command class or None if not found
        """
        return cls._registry.get(command_name)
    
    @classmethod
    def list_commands(cls) -> list:
        """List all available command names.
        
        Returns:
            List of command names
        """
        return sorted(list(cls._registry.keys()))
    
    @classmethod
    def create_command(cls, command_name: str, data: dict):
        """Factory method: create command instance from name and data.
        
        Args:
            command_name: Name of command
            data: Dictionary with command parameters
            
        Returns:
            ScriptCommand instance
            
        Raises:
            ValueError: If command not found
        """
        command_class = cls.get(command_name)
        if not command_class:
            available = cls.list_commands()
            raise ValueError(
                f"Unknown command: {command_name}\n"
                f"Available commands: {', '.join(available)}"
            )
        return command_class.from_dict(data)
    
    @classmethod
    def is_registered(cls, command_name: str) -> bool:
        """Check if command is registered.
        
        Args:
            command_name: Name of command
            
        Returns:
            True if registered, False otherwise
        """
        return command_name in cls._registry