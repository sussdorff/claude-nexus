# Claude Nexus

[![Tests](https://github.com/sussdorff/claude-nexus/actions/workflows/test.yml/badge.svg)](https://github.com/sussdorff/claude-nexus/actions/workflows/test.yml)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Claude Nexus is your central connection point for development tool orchestration in the Claude ecosystem. It provides a unified interface to interact with various development tools like GitLab, GitHub, JIRA, and more.

## Features

- 🔧 **Unified Interface**: Single CLI for all your development tools
- 🔄 **Swappable Implementations**: Seamlessly switch between CLI, API, and MCP implementations
- 📋 **Smart Configuration**: Auto-detects repository type and settings
- 🎯 **Capability-Based Selection**: Automatically chooses the best tool for the job
- 🤖 **AI-Agent Friendly**: Designed for both human and AI agent use

## Installation

### For Development

```bash
git clone https://github.com/sussdorff/claude-nexus.git
cd claude-nexus
pip install -e ".[dev]"
```

### For Usage

```bash
pip install git+https://github.com/sussdorff/claude-nexus.git
```

## Quick Start

```bash
# Check system health
claude-nexus doctor
# or use the short alias
cnx doctor

# Show version
cnx version

# Get help
cnx --help
```

## Configuration

Claude Nexus looks for configuration in `~/.claude/toolkit.yaml`:

```yaml
toolkit:
  code_host:
    type: gitlab  # or github
    prefer: api   # or cli, mcp
    
  issue_tracker:
    type: jira
    project: PROJ
    instance: https://company.atlassian.net
    
  release:
    versioning:
      scheme: semver
```

If no configuration is found, Claude Nexus will auto-detect settings from your git repository.

## Architecture

Claude Nexus follows a hexagonal architecture pattern with:

- **Stable Interfaces**: Protocol-based contracts that don't change
- **Swappable Implementations**: CLI, API, and MCP adapters
- **Capability System**: Implementations declare what they can do
- **Smart Selection**: Automatic fallback to best available implementation

## Development

### Project Structure

```
nexus/
├── cli.py              # Main Click entry point
├── core/               # Core components
│   ├── config.py      # Configuration management
│   ├── registry.py    # Implementation registry
│   ├── selector.py    # Tool selection logic
│   └── interfaces.py  # Protocol definitions
└── commands/          # Domain commands (future)
    ├── reviews/       # MR/PR review commands
    ├── tickets/       # Ticket management
    └── releases/      # Release management
```

### Running Tests

```bash
# Run all tests with coverage
pytest --cov=nexus --cov-report=term-missing

# Run specific test file
pytest tests/test_core/test_config.py

# Run with verbose output
pytest -v
```

### Code Quality

```bash
# Format code
black nexus tests

# Check linting
ruff check nexus tests
```

## Roadmap

### Phase 1: Foundation ✅
- Core configuration system
- Implementation registry
- Tool selection logic
- Basic CLI structure

### Phase 2: Review Domain (Coming Soon)
- MR/PR review commands
- Discussion analysis
- Auto-fix suggestions

### Phase 3: Ticket Domain
- Ticket-based worktree management
- Issue tracker integration
- Workflow automation

### Phase 4: Release Domain
- Version management
- Changelog generation
- Deployment orchestration

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Malte Sussdorff

## Acknowledgments

Built for the Claude ecosystem to provide seamless development tool integration.