"""Script executor - orchestrates command execution."""

import time
from typing import Callable

from .registry import CommandRegistry


class ScriptExecutor:
    """Executes a sequence of commands from a script.
    
    Features:
    - Load scripts from JSON
    - Execute commands sequentially
    - Handle errors (stop or continue)
    - Pause/resume execution
    - Progress tracking
    """
    
    def __init__(self, context=None):
        """Initialize executor.
        
        Args:
            context: ExecutionContext (will create default if None)
        """
        from .context import ExecutionContext
        self.context = context or ExecutionContext()
        self.commands = []
        self.current_index = 0
        self.is_running = False
        self.is_paused = False
        self.errors = []
    
    def load_from_json(self, json_data: dict):
        """Load script from JSON data.
        
        Args:
            json_data: Dictionary with 'commands' list
            
        Raises:
            ValueError: If JSON format is invalid
        """
        self.commands = []
        self.errors = []
        
        if 'commands' not in json_data:
            raise ValueError("JSON must contain 'commands' key")
        
        for i, cmd_data in enumerate(json_data['commands']):
            try:
                if 'command' not in cmd_data:
                    raise ValueError(f"Command {i} missing 'command' key")
                
                command_name = cmd_data['command']
                cmd = CommandRegistry.create_command(command_name, cmd_data)
                self.commands.append(cmd)
                
            except Exception as e:
                error = f"Error loading command {i}: {e}"
                self.errors.append(error)
                self.context.log(error, level="ERROR")
    
    def load_from_file(self, filepath: str):
        """Load script from file (auto-detects format).
        
        Supports:
        - .json files (JSON format)
        - .script files (simple text format)
        
        Args:
            filepath: Path to script file
            
        Raises:
            FileNotFoundError: If file not found
            ValueError: If format is invalid
        """
        import json
        from pathlib import Path
        
        try:
            file_path = Path(filepath)
            extension = file_path.suffix.lower()
            
            if extension == '.json':
                # JSON format
                with open(filepath, 'r', encoding='utf-8') as f:
                    json_data = json.load(f)
                self.load_from_json(json_data)
            else:
                # Simple format (.script, .txt, or other)
                try:
                    from .simple_parser import parse_simple_script
                except ImportError:
                    try:
                        from qwsengine.scripting.simple_parser import parse_simple_script
                    except ImportError:
                        raise ImportError("simple_parser module not found")
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    text = f.read()
                
                json_data = parse_simple_script(text)
                self.load_from_json(json_data)
            
            self.context.log(f"Loaded script from: {filepath}")
            
        except FileNotFoundError:
            raise FileNotFoundError(f"Script file not found: {filepath}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {filepath}: {e}")
        except ValueError as e:
            raise ValueError(f"Invalid script format in {filepath}: {e}")
    
    def save_to_file(self, filepath: str):
        """Save current script to JSON file.
        
        Args:
            filepath: Path where to save file
        """
        import json
        script_data = {
            'version': '1.0',
            'commands': [cmd.to_dict() for cmd in self.commands]
        }
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(script_data, f, indent=2)
        self.context.log(f"Saved script to: {filepath}")
    
    def execute(self, on_progress: Callable = None) -> bool:
        """Execute all commands sequentially.
        
        Args:
            on_progress: Callback(current_index, total, command_description)
            
        Returns:
            True if all commands succeeded, False if errors occurred
        """
        self.is_running = True
        self.errors = []
        
        self.context.log(f"Starting script execution ({len(self.commands)} commands)")
        
        success_count = 0
        error_count = 0
        
        for i, cmd in enumerate(self.commands):
            self.current_index = i
            
            # Handle pause/resume
            while self.is_paused and self.is_running:
                time.sleep(0.1)
            
            # Check for stop request
            if not self.is_running:
                self.context.log("Script execution stopped by user")
                break
            
            try:
                # Update progress
                if on_progress:
                    on_progress(i, len(self.commands), str(cmd))
                
                # Execute command
                self.context.log(f"Executing [{i+1}/{len(self.commands)}]: {cmd}")
                cmd.execute(self.context)
                success_count += 1
                
            except Exception as e:
                error_msg = f"Command failed: {e}"
                error_count += 1
                self.errors.append((i, cmd, str(e)))
                self.context.log(error_msg, level="ERROR")
                
                # Check error handling mode
                if self.context.stop_on_error:
                    self.context.log("Stopping on error")
                    break
        
        self.is_running = False
        
        # Summary
        self.context.log(
            f"Script execution complete: {success_count} succeeded, "
            f"{error_count} failed"
        )
        
        return error_count == 0
    
    def pause(self):
        """Pause script execution."""
        self.is_paused = True
        self.context.log("Script paused")
    
    def resume(self):
        """Resume script execution."""
        self.is_paused = False
        self.context.log("Script resumed")
    
    def stop(self):
        """Stop script execution."""
        self.is_running = False
        self.context.log("Script stopped")
    
    def get_progress(self) -> tuple:
        """Get current execution progress.
        
        Returns:
            (current_index, total_commands, is_running)
        """
        return (self.current_index, len(self.commands), self.is_running)
    
    def get_errors(self) -> list:
        """Get all errors from last execution.
        
        Returns:
            List of (index, command, error_message) tuples
        """
        return self.errors.copy()