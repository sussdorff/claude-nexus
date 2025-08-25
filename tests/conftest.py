"""Pytest configuration and fixtures."""

import pytest
from pathlib import Path
import tempfile
import shutil
from typing import Generator
from nexus.core.registry import ImplementationRegistry
from nexus.core.capabilities import Capability


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for testing.
    
    Yields:
        Path to temporary directory.
    """
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path)


@pytest.fixture
def sample_config_file(temp_dir: Path) -> Path:
    """Create a sample configuration file.
    
    Args:
        temp_dir: Temporary directory fixture.
        
    Returns:
        Path to configuration file.
    """
    config_dir = temp_dir / ".claude"
    config_dir.mkdir()
    config_file = config_dir / "toolkit.yaml"
    
    config_file.write_text("""
toolkit:
  code_host:
    type: gitlab
    prefer: api
  issue_tracker:
    type: jira
    project: TEST
    instance: https://example.atlassian.net
  release:
    versioning:
      scheme: semver
""")
    
    return config_file


@pytest.fixture
def empty_registry() -> ImplementationRegistry:
    """Create an empty implementation registry.
    
    Returns:
        Empty ImplementationRegistry.
    """
    return ImplementationRegistry()


@pytest.fixture
def populated_registry() -> ImplementationRegistry:
    """Create a registry with sample implementations.
    
    Returns:
        ImplementationRegistry with test implementations.
    """
    from tests.fixtures.mock_implementations import (
        MockGitLabCLI,
        MockGitLabAPI,
        MockJiraCLI,
        MockCodeHost,
        MockIssueTracker
    )
    from nexus.core.interfaces import CodeHost, IssueTracker
    
    registry = ImplementationRegistry()
    
    # Register CodeHost implementations
    registry.register(
        CodeHost,
        MockGitLabCLI,
        [Capability.BASIC_READ, Capability.CLI_AVAILABLE],
        priority=1,
        name="gitlab-cli"
    )
    
    registry.register(
        CodeHost,
        MockGitLabAPI,
        [
            Capability.BASIC_READ,
            Capability.BASIC_WRITE,
            Capability.ADVANCED_SEARCH,
            Capability.API_ACCESS
        ],
        priority=2,
        name="gitlab-api"
    )
    
    # Register IssueTracker implementations
    registry.register(
        IssueTracker,
        MockJiraCLI,
        [Capability.BASIC_READ, Capability.BASIC_WRITE, Capability.CLI_AVAILABLE],
        priority=1,
        name="jira-cli"
    )
    
    return registry