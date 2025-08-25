"""Tests for implementation registry."""

import pytest
from nexus.core.registry import ImplementationRegistry, Implementation
from nexus.core.capabilities import Capability
from nexus.core.interfaces import CodeHost, IssueTracker


class MockImplementation:
    """Mock implementation for testing."""
    pass


class TestImplementationRegistry:
    """Test ImplementationRegistry class."""
    
    def test_register_implementation(self, empty_registry: ImplementationRegistry):
        """Test registering an implementation."""
        empty_registry.register(
            CodeHost,
            MockImplementation,
            [Capability.BASIC_READ],
            priority=1,
            name="mock"
        )
        
        implementations = empty_registry.get_implementations(CodeHost)
        assert len(implementations) == 1
        assert implementations[0].name == "mock"
        assert implementations[0].priority == 1
        assert Capability.BASIC_READ in implementations[0].capabilities
    
    def test_get_implementations_sorted_by_priority(self, empty_registry: ImplementationRegistry):
        """Test implementations are sorted by priority."""
        empty_registry.register(
            CodeHost,
            MockImplementation,
            [Capability.BASIC_READ],
            priority=1,
            name="low"
        )
        
        empty_registry.register(
            CodeHost,
            MockImplementation,
            [Capability.BASIC_READ],
            priority=3,
            name="high"
        )
        
        empty_registry.register(
            CodeHost,
            MockImplementation,
            [Capability.BASIC_READ],
            priority=2,
            name="medium"
        )
        
        implementations = empty_registry.get_implementations(CodeHost)
        
        assert len(implementations) == 3
        assert implementations[0].name == "high"
        assert implementations[1].name == "medium"
        assert implementations[2].name == "low"
    
    def test_get_implementation_by_name(self, populated_registry: ImplementationRegistry):
        """Test getting specific implementation by name."""
        impl = populated_registry.get_implementation_by_name(CodeHost, "gitlab-api")
        
        assert impl is not None
        assert impl.name == "gitlab-api"
        assert Capability.API_ACCESS in impl.capabilities
    
    def test_get_implementation_by_name_not_found(self, populated_registry: ImplementationRegistry):
        """Test getting non-existent implementation."""
        impl = populated_registry.get_implementation_by_name(CodeHost, "nonexistent")
        assert impl is None
    
    def test_get_implementations_with_capabilities(self, populated_registry: ImplementationRegistry):
        """Test filtering implementations by capabilities."""
        # Request advanced search capability
        impls = populated_registry.get_implementations_with_capabilities(
            CodeHost,
            [Capability.ADVANCED_SEARCH]
        )
        
        assert len(impls) == 1
        assert impls[0].name == "gitlab-api"
    
    def test_get_implementations_with_multiple_capabilities(self, populated_registry: ImplementationRegistry):
        """Test filtering with multiple required capabilities."""
        impls = populated_registry.get_implementations_with_capabilities(
            CodeHost,
            [Capability.BASIC_READ, Capability.API_ACCESS]
        )
        
        assert len(impls) == 1
        assert impls[0].name == "gitlab-api"
    
    def test_no_implementations_with_capabilities(self, populated_registry: ImplementationRegistry):
        """Test when no implementation has required capabilities."""
        impls = populated_registry.get_implementations_with_capabilities(
            CodeHost,
            [Capability.WEBHOOKS]  # No implementation has this
        )
        
        assert len(impls) == 0
    
    def test_list_interfaces(self, populated_registry: ImplementationRegistry):
        """Test listing all registered interfaces."""
        interfaces = populated_registry.list_interfaces()
        
        assert CodeHost in interfaces
        assert IssueTracker in interfaces
    
    def test_clear_registry(self, populated_registry: ImplementationRegistry):
        """Test clearing all registrations."""
        populated_registry.clear()
        
        assert len(populated_registry.list_interfaces()) == 0
        assert len(populated_registry.get_implementations(CodeHost)) == 0