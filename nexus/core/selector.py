"""Tool selection logic for Claude Nexus."""

from typing import Type, List, Any, Optional, TypeVar
from nexus.core.registry import ImplementationRegistry
from nexus.core.capabilities import Capability
from nexus.core.exceptions import NoImplementationError, NoCapableImplementationError


T = TypeVar('T')


class ToolSelector:
    """Selects the best tool implementation based on requirements."""
    
    def __init__(self, registry: ImplementationRegistry):
        """Initialize the selector.
        
        Args:
            registry: Implementation registry to use.
        """
        self.registry = registry
    
    def get_tool(
        self,
        interface: Type[T],
        required_capabilities: Optional[List[Capability]] = None,
        preferred_name: Optional[str] = None
    ) -> T:
        """Select the best available implementation for an interface.
        
        Args:
            interface: Interface protocol class.
            required_capabilities: List of required capabilities.
            preferred_name: Preferred implementation name.
            
        Returns:
            Instance of the selected implementation.
            
        Raises:
            NoImplementationError: No implementations registered.
            NoCapableImplementationError: No implementation has required capabilities.
        """
        # If a specific implementation is requested
        if preferred_name:
            impl = self.registry.get_implementation_by_name(interface, preferred_name)
            if impl:
                # Check if it has required capabilities
                if required_capabilities:
                    if not all(cap in impl.capabilities for cap in required_capabilities):
                        raise NoCapableImplementationError(
                            f"Implementation '{preferred_name}' does not have required capabilities: "
                            f"{required_capabilities}"
                        )
                return impl.implementation()
            else:
                # Fall through to normal selection if preferred not found
                pass
        
        # Get all implementations
        implementations = self.registry.get_implementations(interface)
        
        if not implementations:
            raise NoImplementationError(
                f"No implementations registered for {interface.__name__}"
            )
        
        # Filter by required capabilities
        if required_capabilities:
            capable_impls = self.registry.get_implementations_with_capabilities(
                interface,
                required_capabilities
            )
            
            if not capable_impls:
                raise NoCapableImplementationError(
                    f"No implementation has required capabilities: {required_capabilities}"
                )
            
            # Return the highest priority capable implementation
            return capable_impls[0].implementation()
        
        # Return the highest priority implementation
        return implementations[0].implementation()
    
    def list_available_tools(self, interface: Type) -> List[str]:
        """List available tool implementations for an interface.
        
        Args:
            interface: Interface protocol class.
            
        Returns:
            List of implementation names.
        """
        implementations = self.registry.get_implementations(interface)
        return [impl.name for impl in implementations]
    
    def get_tool_capabilities(
        self,
        interface: Type,
        tool_name: str
    ) -> List[Capability]:
        """Get capabilities of a specific tool.
        
        Args:
            interface: Interface protocol class.
            tool_name: Tool implementation name.
            
        Returns:
            List of capabilities.
        """
        impl = self.registry.get_implementation_by_name(interface, tool_name)
        if impl:
            return impl.capabilities
        return []