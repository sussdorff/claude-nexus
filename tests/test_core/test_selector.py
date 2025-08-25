"""Tests for tool selector."""

import pytest
from nexus.core.selector import ToolSelector
from nexus.core.registry import ImplementationRegistry
from nexus.core.capabilities import Capability
from nexus.core.interfaces import CodeHost, IssueTracker
from nexus.core.exceptions import NoImplementationError, NoCapableImplementationError


class TestToolSelector:
    """Test ToolSelector class."""
    
    def test_get_tool_with_highest_priority(self, populated_registry: ImplementationRegistry):
        """Test selector chooses highest priority implementation."""
        selector = ToolSelector(populated_registry)
        
        # Should get gitlab-api (priority 2) over gitlab-cli (priority 1)
        tool = selector.get_tool(CodeHost)
        
        assert tool is not None
        assert Capability.API_ACCESS in tool.capabilities
    
    def test_get_tool_by_capability(self, populated_registry: ImplementationRegistry):
        """Test selector chooses implementation by capability."""
        selector = ToolSelector(populated_registry)
        
        # Request advanced search capability
        tool = selector.get_tool(
            CodeHost,
            required_capabilities=[Capability.ADVANCED_SEARCH]
        )
        
        assert tool is not None
        assert Capability.ADVANCED_SEARCH in tool.capabilities
    
    def test_get_tool_by_name(self, populated_registry: ImplementationRegistry):
        """Test selector gets specific implementation by name."""
        selector = ToolSelector(populated_registry)
        
        tool = selector.get_tool(
            CodeHost,
            preferred_name="gitlab-cli"
        )
        
        assert tool is not None
        assert Capability.CLI_AVAILABLE in tool.capabilities
        assert Capability.API_ACCESS not in tool.capabilities
    
    def test_fallback_when_preferred_not_found(self, populated_registry: ImplementationRegistry):
        """Test selector falls back when preferred implementation not found."""
        selector = ToolSelector(populated_registry)
        
        tool = selector.get_tool(
            CodeHost,
            preferred_name="nonexistent"
        )
        
        # Should fall back to highest priority
        assert tool is not None
        assert Capability.API_ACCESS in tool.capabilities
    
    def test_no_implementation_error(self, empty_registry: ImplementationRegistry):
        """Test error when no implementations registered."""
        selector = ToolSelector(empty_registry)
        
        with pytest.raises(NoImplementationError) as exc_info:
            selector.get_tool(CodeHost)
        
        assert "No implementations registered" in str(exc_info.value)
    
    def test_no_capable_implementation_error(self, populated_registry: ImplementationRegistry):
        """Test error when no implementation has required capabilities."""
        selector = ToolSelector(populated_registry)
        
        with pytest.raises(NoCapableImplementationError) as exc_info:
            selector.get_tool(
                CodeHost,
                required_capabilities=[Capability.WEBHOOKS]
            )
        
        assert "No implementation has required capabilities" in str(exc_info.value)
    
    def test_preferred_without_capabilities_error(self, populated_registry: ImplementationRegistry):
        """Test error when preferred implementation lacks capabilities."""
        selector = ToolSelector(populated_registry)
        
        with pytest.raises(NoCapableImplementationError) as exc_info:
            selector.get_tool(
                CodeHost,
                required_capabilities=[Capability.ADVANCED_SEARCH],
                preferred_name="gitlab-cli"
            )
        
        assert "gitlab-cli" in str(exc_info.value)
        assert "does not have required capabilities" in str(exc_info.value)
    
    def test_list_available_tools(self, populated_registry: ImplementationRegistry):
        """Test listing available tool implementations."""
        selector = ToolSelector(populated_registry)
        
        tools = selector.list_available_tools(CodeHost)
        
        assert "gitlab-cli" in tools
        assert "gitlab-api" in tools
        assert len(tools) == 2
    
    def test_get_tool_capabilities(self, populated_registry: ImplementationRegistry):
        """Test getting capabilities of specific tool."""
        selector = ToolSelector(populated_registry)
        
        capabilities = selector.get_tool_capabilities(CodeHost, "gitlab-api")
        
        assert Capability.BASIC_READ in capabilities
        assert Capability.ADVANCED_SEARCH in capabilities
        assert Capability.API_ACCESS in capabilities
    
    def test_get_tool_capabilities_not_found(self, populated_registry: ImplementationRegistry):
        """Test getting capabilities of non-existent tool."""
        selector = ToolSelector(populated_registry)
        
        capabilities = selector.get_tool_capabilities(CodeHost, "nonexistent")
        
        assert capabilities == []