"""Simple script format parser.

Converts simple text format to JSON for script execution.

Simple Format Examples:
    load https://example.com
    wait 5
    SAVE HTML panda
    SAVE TEXT results
    SAVE HTML "google search"
"""

import re
from typing import List, Dict, Tuple


class SimpleScriptParser:
    """Parse simple script format and convert to JSON."""
    
    def __init__(self):
        """Initialize parser."""
        self.errors = []
        self.warnings = []
    
    def parse(self, script_text: str) -> Dict:
        """Parse simple script text and return JSON representation.
        
        Args:
            script_text: Simple format script text
            
        Returns:
            Dict with 'version' and 'commands' keys
            
        Raises:
            ValueError: If script contains syntax errors
        """
        self.errors = []
        self.warnings = []
        
        # Split into lines
        lines = script_text.strip().split('\n')
        
        commands = []
        
        for line_num, line in enumerate(lines, 1):
            # Remove comments
            if '#' in line:
                line = line.split('#')[0]
            
            # Strip whitespace
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
            
            try:
                cmd = self._parse_line(line)
                if cmd:
                    commands.append(cmd)
            except ValueError as e:
                self.errors.append(f"Line {line_num}: {e}")
        
        # If there are errors, raise
        if self.errors:
            raise ValueError('\n'.join(self.errors))
        
        return {
            'version': '1.0',
            'commands': commands
        }
    
    def _parse_line(self, line: str) -> Dict:
        """Parse a single command line.
        
        Args:
            line: Single command line (comments already removed)
            
        Returns:
            Command dict or None if empty
        """
        parts = self._split_command(line)
        
        if not parts:
            return None
        
        cmd = parts[0].lower()
        
        if cmd == 'load':
            return self._parse_load(parts)
        elif cmd == 'wait':
            return self._parse_wait(parts)
        elif cmd == 'save':
            return self._parse_save(parts)
        else:
            raise ValueError(f"Unknown command: {cmd}")
    
    def _split_command(self, line: str) -> List[str]:
        """Split command line, respecting quoted strings.
        
        Args:
            line: Command line
            
        Returns:
            List of parts
        """
        parts = []
        current = ""
        in_quotes = False
        
        for char in line:
            if char == '"':
                in_quotes = not in_quotes
            elif char.isspace() and not in_quotes:
                if current:
                    parts.append(current)
                    current = ""
            else:
                current += char
        
        if current:
            parts.append(current)
        
        return parts
    
    def _parse_load(self, parts: List[str]) -> Dict:
        """Parse LOAD command.
        
        Syntax: LOAD <URL> [nowait]
        """
        if len(parts) < 2:
            raise ValueError("LOAD requires a URL")
        
        url = parts[1]
        wait = 'nowait' not in [p.lower() for p in parts[2:]]
        
        return {
            'command': 'load_url',
            'url': url,
            'wait_for_load': wait
        }
    
    def _parse_wait(self, parts: List[str]) -> Dict:
        """Parse WAIT command.
        
        Syntax: WAIT <SECONDS>
        """
        if len(parts) < 2:
            raise ValueError("WAIT requires seconds")
        
        try:
            seconds = float(parts[1])
        except ValueError:
            raise ValueError(f"WAIT seconds must be a number, got: {parts[1]}")
        
        if seconds < 0:
            raise ValueError("WAIT seconds must be positive")
        
        return {
            'command': 'pause',
            'seconds': seconds
        }
    
    def _parse_save(self, parts: List[str]) -> Dict:
        """Parse SAVE command.
        
        Syntax: SAVE HTML|TEXT [TAG]
        
        Examples:
            SAVE HTML
            SAVE HTML panda
            SAVE HTML "my data"
            SAVE TEXT results
        """
        if len(parts) < 2:
            raise ValueError("SAVE requires HTML or TEXT type")
        
        save_type = parts[1].lower()
        if save_type not in ('html', 'text'):
            raise ValueError(f"SAVE type must be HTML or TEXT, got: {save_type}")
        
        # Get optional tag (everything after the type)
        tag = None
        if len(parts) > 2:
            # Join remaining parts as tag (handles quoted strings)
            tag = ' '.join(parts[2:])
            # Remove quotes if present
            if tag.startswith('"') and tag.endswith('"'):
                tag = tag[1:-1]
        
        command = 'save_html' if save_type == 'html' else 'save_text'
        
        result = {
            'command': command
        }
        
        if tag:
            result['tag'] = tag
        
        return result
    
    def validate(self, script_dict: Dict) -> Tuple[bool, List[str]]:
        """Validate parsed script.
        
        Args:
            script_dict: Parsed script dictionary
            
        Returns:
            Tuple of (is_valid, error_list)
        """
        errors = []
        
        if 'version' not in script_dict:
            errors.append("Missing 'version' key")
        
        if 'commands' not in script_dict:
            errors.append("Missing 'commands' key")
        elif not isinstance(script_dict['commands'], list):
            errors.append("'commands' must be a list")
        
        return len(errors) == 0, errors


def parse_simple_script(text: str) -> Dict:
    """Convenience function to parse simple script.
    
    Args:
        text: Simple format script text
        
    Returns:
        JSON-compatible dict
        
    Raises:
        ValueError: If script is invalid
    """
    parser = SimpleScriptParser()
    return parser.parse(text)


# Example usage:
if __name__ == '__main__':
    example_script = """
    # Example script
    load https://example.com
    wait 2
    SAVE HTML example_page
    
    load https://google.com
    wait 3
    SAVE HTML google
    SAVE TEXT google_text
    """
    
    try:
        result = parse_simple_script(example_script)
        import json
        print(json.dumps(result, indent=2))
    except ValueError as e:
        print(f"Error: {e}")
