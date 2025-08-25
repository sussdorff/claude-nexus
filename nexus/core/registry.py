"""Implementation registry for Claude Nexus."""

from typing import Type, List, Dict, Any, Optional
from dataclasses import dataclass
from nexus.core.capabilities import Capability


@dataclass
class Implementation:
    """Represents a registered implementation."""
    
    interface: Type
    implementation: Type
    capabilities: List[Capability]
    priority: int = 0
    name: str = ""
    
    def __post_init__(self):
        if not self.name:
            self.name = self.implementation.__name__


class ImplementationRegistry:
    """Registry for tool implementations."""
    
    def __init__(self):
        """Initialize the registry."""
        self._implementations: Dict[Type, List[Implementation]] = {}
    
    def register(
        self,
        interface: Type,
        implementation: Type,
        capabilities: List[Capability],
        priority: int = 0,
        name: Optional[str] = None
    ) -> None:
        """Register an implementation for an interface.
        
        Args:
            interface: Interface protocol class.
            implementation: Implementation class.
            capabilities: List of capabilities this implementation provides.
            priority: Priority for selection (higher = preferred).
            name: Optional name for the implementation.
        """
        impl = Implementation(
            interface=interface,
            implementation=implementation,
            capabilities=capabilities,
            priority=priority,
            name=name or implementation.__name__
        )
        
        if interface not in self._implementations:
            self._implementations[interface] = []
        
        self._implementations[interface].append(impl)
        
        # Sort by priority (highest first)
        self._implementations[interface].sort(
            key=lambda x: x.priority,
            reverse=True
        )
    
    def get_implementations(self, interface: Type) -> List[Implementation]:
        """Get all implementations for an interface.
        
        Args:
            interface: Interface protocol class.
            
        Returns:
            List of Implementation objects.
        """
        return self._implementations.get(interface, [])
    
    def get_implementation_by_name(
        self,
        interface: Type,
        name: str
    ) -> Optional[Implementation]:
        """Get a specific implementation by name.
        
        Args:
            interface: Interface protocol class.
            name: Implementation name.
            
        Returns:
            Implementation object if found, None otherwise.
        """
        implementations = self.get_implementations(interface)
        
        for impl in implementations:
            if impl.name == name:
                return impl
        
        return None
    
    def get_implementations_with_capabilities(
        self,
        interface: Type,
        required_capabilities: List[Capability]
    ) -> List[Implementation]:
        """Get implementations that have all required capabilities.
        
        Args:
            interface: Interface protocol class.
            required_capabilities: List of required capabilities.
            
        Returns:
            List of Implementation objects that satisfy requirements.
        """
        implementations = self.get_implementations(interface)
        matching = []
        
        for impl in implementations:
            # Check if implementation has all required capabilities
            if all(cap in impl.capabilities for cap in required_capabilities):
                matching.append(impl)
        
        return matching
    
    def list_interfaces(self) -> List[Type]:
        """List all registered interfaces.
        
        Returns:
            List of interface types.
        """
        return list(self._implementations.keys())
    
    def clear(self) -> None:
        """Clear all registrations."""
        self._implementations.clear()