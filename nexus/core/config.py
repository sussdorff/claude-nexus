"""Configuration management for Claude Nexus."""

from pathlib import Path
from typing import Any, Optional, Dict
import yaml
import subprocess
import os


class Configuration:
    """Manages Claude Nexus configuration from multiple sources."""
    
    def __init__(self, search_path: Optional[Path] = None):
        """Initialize configuration.
        
        Args:
            search_path: Starting path to search for config files.
                        Defaults to current working directory.
        """
        self.search_path = search_path or Path.cwd()
        self.config_path = None
        self._config = self._load_configuration()
    
    def _find_config_file(self) -> Optional[Path]:
        """Find toolkit.yaml in standard locations.
        
        Returns:
            Path to config file if found, None otherwise.
        """
        search_paths = [
            self.search_path / ".claude" / "toolkit.yaml",
            Path.home() / ".claude" / "toolkit.yaml",
        ]
        
        for path in search_paths:
            if path.exists():
                return path
        return None
    
    def _auto_detect_repo(self) -> Dict[str, Any]:
        """Auto-detect repository type from git remote.
        
        Returns:
            Dictionary with auto-detected configuration.
        """
        try:
            # Try to get git remote URL
            result = subprocess.run(
                ["git", "remote", "get-url", "origin"],
                capture_output=True,
                text=True,
                check=False,
                cwd=self.search_path
            )
            
            if result.returncode == 0:
                remote_url = result.stdout.strip().lower()
                
                if "gitlab" in remote_url:
                    return {"toolkit": {"code_host": {"type": "gitlab"}}}
                elif "github" in remote_url:
                    return {"toolkit": {"code_host": {"type": "github"}}}
        except (subprocess.SubprocessError, FileNotFoundError):
            pass
        
        return {"toolkit": {"code_host": {"type": "unknown"}}}
    
    def _load_configuration(self) -> Dict[str, Any]:
        """Load configuration from file or auto-detect.
        
        Returns:
            Merged configuration dictionary.
        """
        config = {}
        
        # First, get auto-detected configuration
        auto_config = self._auto_detect_repo()
        
        # Then try to load from file
        self.config_path = self._find_config_file()
        if self.config_path:
            try:
                with open(self.config_path, 'r') as f:
                    file_config = yaml.safe_load(f) or {}
                # File config overrides auto-detection
                config = self._deep_merge(auto_config, file_config)
            except (yaml.YAMLError, IOError) as e:
                # If there's an error reading the file, fall back to auto-detection
                print(f"Warning: Error reading config file: {e}")
                config = auto_config
        else:
            config = auto_config
        
        return config
    
    def _deep_merge(self, base: dict, override: dict) -> dict:
        """Deep merge two dictionaries.
        
        Args:
            base: Base dictionary.
            override: Dictionary with values to override.
            
        Returns:
            Merged dictionary.
        """
        result = base.copy()
        
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        
        return result
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value using dot notation.
        
        Args:
            key: Configuration key using dot notation (e.g., 'toolkit.code_host.type')
            default: Default value if key not found.
            
        Returns:
            Configuration value or default.
        """
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        
        return value
    
    def get_all(self) -> Dict[str, Any]:
        """Get all configuration.
        
        Returns:
            Complete configuration dictionary.
        """
        return self._config.copy()