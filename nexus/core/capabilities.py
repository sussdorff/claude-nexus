"""Capability definitions for Claude Nexus."""

from enum import Enum, auto


class Capability(Enum):
    """Capabilities that implementations can provide."""
    
    # Basic operations
    BASIC_READ = auto()
    BASIC_WRITE = auto()
    
    # Advanced operations
    BULK_OPERATIONS = auto()
    ADVANCED_SEARCH = auto()
    CUSTOM_FIELDS = auto()
    
    # Integration features
    WEBHOOKS = auto()
    WORKFLOW_AUTOMATION = auto()
    REAL_TIME_UPDATES = auto()
    
    # API-specific
    API_ACCESS = auto()
    RATE_LIMITING = auto()
    
    # CLI-specific
    CLI_AVAILABLE = auto()
    INTERACTIVE_MODE = auto()