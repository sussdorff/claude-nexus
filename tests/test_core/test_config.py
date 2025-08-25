"""Tests for configuration management."""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from nexus.core.config import Configuration


class TestConfiguration:
    """Test Configuration class."""
    
    def test_loads_from_yaml(self, temp_dir: Path):
        """Test configuration loads from toolkit.yaml."""
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
""")
        
        config = Configuration(search_path=temp_dir)
        
        assert config.config_path == config_file
        assert config.get("toolkit.code_host.type") == "gitlab"
        assert config.get("toolkit.code_host.prefer") == "api"
        assert config.get("toolkit.issue_tracker.project") == "TEST"
    
    def test_auto_detects_github(self, temp_dir: Path):
        """Test auto-detection of GitHub from git remote."""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout="https://github.com/user/repo.git"
            )
            
            config = Configuration(search_path=temp_dir)
            assert config.get("toolkit.code_host.type") == "github"
    
    def test_auto_detects_gitlab(self, temp_dir: Path):
        """Test auto-detection of GitLab from git remote."""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout="https://gitlab.com/user/repo.git"
            )
            
            config = Configuration(search_path=temp_dir)
            assert config.get("toolkit.code_host.type") == "gitlab"
    
    def test_file_overrides_auto_detection(self, temp_dir: Path):
        """Test that file configuration overrides auto-detection."""
        config_dir = temp_dir / ".claude"
        config_dir.mkdir()
        config_file = config_dir / "toolkit.yaml"
        config_file.write_text("""
toolkit:
  code_host:
    type: github
""")
        
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout="https://gitlab.com/user/repo.git"
            )
            
            config = Configuration(search_path=temp_dir)
            # File config should override auto-detection
            assert config.get("toolkit.code_host.type") == "github"
    
    def test_get_with_default(self, temp_dir: Path):
        """Test getting config value with default."""
        config = Configuration(search_path=temp_dir)
        
        assert config.get("nonexistent.key", "default") == "default"
        assert config.get("toolkit.missing.value", 42) == 42
    
    def test_deep_merge(self, temp_dir: Path):
        """Test deep merging of configuration."""
        config_dir = temp_dir / ".claude"
        config_dir.mkdir()
        config_file = config_dir / "toolkit.yaml"
        config_file.write_text("""
toolkit:
  code_host:
    prefer: api
  custom:
    value: 123
""")
        
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout="https://gitlab.com/user/repo.git"
            )
            
            config = Configuration(search_path=temp_dir)
            
            # Auto-detected type should be present
            assert config.get("toolkit.code_host.type") == "gitlab"
            # File config should also be present
            assert config.get("toolkit.code_host.prefer") == "api"
            assert config.get("toolkit.custom.value") == 123
    
    def test_handles_missing_git(self, temp_dir: Path):
        """Test handling when git is not available."""
        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = FileNotFoundError()
            
            config = Configuration(search_path=temp_dir)
            assert config.get("toolkit.code_host.type") == "unknown"
    
    def test_handles_invalid_yaml(self, temp_dir: Path):
        """Test handling of invalid YAML file."""
        config_dir = temp_dir / ".claude"
        config_dir.mkdir()
        config_file = config_dir / "toolkit.yaml"
        config_file.write_text("invalid: yaml: content: :")
        
        config = Configuration(search_path=temp_dir)
        # Should fall back to auto-detection
        assert config.get("toolkit.code_host.type") in ["github", "gitlab", "unknown"]
    
    def test_get_all(self, temp_dir: Path):
        """Test getting all configuration."""
        config_dir = temp_dir / ".claude"
        config_dir.mkdir()
        config_file = config_dir / "toolkit.yaml"
        config_file.write_text("""
toolkit:
  test: value
""")
        
        config = Configuration(search_path=temp_dir)
        all_config = config.get_all()
        
        assert isinstance(all_config, dict)
        assert "toolkit" in all_config
        assert all_config["toolkit"]["test"] == "value"