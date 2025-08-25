"""Custom exceptions for Claude Nexus."""


class NexusError(Exception):
    """Base exception for Claude Nexus."""
    pass


class ConfigurationError(NexusError):
    """Configuration-related errors."""
    pass


class NoImplementationError(NexusError):
    """No implementation registered for interface."""
    pass


class NoCapableImplementationError(NexusError):
    """No implementation has required capabilities."""
    pass


class ToolExecutionError(NexusError):
    """Error executing tool command."""
    pass