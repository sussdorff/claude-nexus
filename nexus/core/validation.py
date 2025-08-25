"""Input validation utilities for Claude Nexus."""

import re
from typing import Optional


class InputValidator:
    """Validates user input."""
    
    @staticmethod
    def validate_ticket_id(ticket_id: str) -> bool:
        """Validate ticket ID format.
        
        Args:
            ticket_id: Ticket ID to validate.
            
        Returns:
            True if valid, False otherwise.
        """
        # Common patterns: PROJ-123, CH-456, etc.
        pattern = r'^[A-Z]+-\d+$'
        return bool(re.match(pattern, ticket_id))
    
    @staticmethod
    def validate_branch_name(branch_name: str) -> bool:
        """Validate git branch name.
        
        Args:
            branch_name: Branch name to validate.
            
        Returns:
            True if valid, False otherwise.
        """
        # Git branch name rules
        invalid_patterns = [
            r'^\.', r'\.$',  # Starting or ending with dot
            r'\.\.', r'\.lock$',  # Double dots or .lock ending
            r'^/', r'/$',  # Starting or ending with slash
            r'//', r'\s',  # Double slashes or spaces
            r'[\x00-\x1f\x7f~^:?*\[]',  # Control chars and special chars
        ]
        
        for pattern in invalid_patterns:
            if re.search(pattern, branch_name):
                return False
        
        return len(branch_name) > 0 and len(branch_name) <= 255
    
    @staticmethod
    def validate_version(version: str) -> bool:
        """Validate semantic version string.
        
        Args:
            version: Version string to validate.
            
        Returns:
            True if valid, False otherwise.
        """
        # Semantic versioning pattern
        pattern = r'^v?\d+\.\d+\.\d+(-[a-zA-Z0-9\-\.]+)?(\+[a-zA-Z0-9\-\.]+)?$'
        return bool(re.match(pattern, version))
    
    @staticmethod
    def sanitize_path(path: str) -> str:
        """Sanitize file path.
        
        Args:
            path: Path to sanitize.
            
        Returns:
            Sanitized path.
        """
        # Remove potentially dangerous characters
        sanitized = re.sub(r'[^\w\s\-\./]', '', path)
        # Remove multiple slashes
        sanitized = re.sub(r'/+', '/', sanitized)
        # Remove leading/trailing whitespace
        return sanitized.strip()
    
    @staticmethod
    def validate_url(url: str) -> bool:
        """Validate URL format.
        
        Args:
            url: URL to validate.
            
        Returns:
            True if valid, False otherwise.
        """
        pattern = r'^https?://[^\s/$.?#].[^\s]*$'
        return bool(re.match(pattern, url, re.IGNORECASE))