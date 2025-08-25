# Claude Nexus Development Guide

## Project Overview
Claude Nexus is a unified CLI toolkit that provides a central connection point for development tool orchestration in the Claude ecosystem. It follows hexagonal architecture with stable interfaces and swappable implementations.

## Current Status
- ✅ Phase 1: Foundation (Complete)
  - Core configuration system
  - Implementation registry
  - Tool selector with capabilities
  - Basic CLI with doctor command
  - Comprehensive test framework

- 🚧 Phase 2: Review Domain (Next)
  - MR/PR review commands
  - GitLab/GitHub adapters
  - Discussion analysis

- 📋 Phase 3: Ticket Domain (Planned)
  - Ticket-based worktree management
  - JIRA/Linear integration

- 📋 Phase 4: Release Domain (Planned)
  - Version management
  - Changelog generation

## Development Guidelines

### Architecture Principles
1. **Hexagonal Architecture**: Stable interfaces with swappable implementations
2. **Capability-Based Selection**: Implementations declare capabilities, selector chooses best fit
3. **Progressive Enhancement**: CLI → API → MCP fallback chain
4. **Test-Driven Development**: Write tests first, then implementation

### Code Style
- Use Python 3.8+ features
- Type hints for all public methods
- Docstrings for all classes and methods
- Black for formatting (88 line length)
- Ruff for linting

### Testing Requirements
- Minimum 80% test coverage
- Unit tests for all components
- Integration tests for workflows
- Mock implementations for testing

### Command Structure
Commands follow domain organization:
```
nexus/
└── commands/
    ├── reviews/   # MR/PR review commands
    ├── tickets/   # Ticket management
    └── releases/  # Release management
```

### Adding New Features
1. Create interface in `nexus/core/interfaces.py`
2. Define capabilities in `nexus/core/capabilities.py`
3. Implement adapters in `nexus/adapters/`
4. Register in `nexus/core/registry.py`
5. Add commands in `nexus/commands/<domain>/`
6. Write comprehensive tests

## Key Files
- `docs/PRDs/` - Product Requirements Documents for each domain
- `docs/architecture/` - Architecture and migration plans
- `nexus/core/` - Core framework components
- `tests/` - Test suite

## Testing
```bash
# Run all tests with coverage
pytest --cov=nexus --cov-report=term-missing

# Run specific domain tests
pytest tests/test_core/

# Format code
black nexus tests

# Lint code
ruff check nexus tests
```

## Important Notes
- This is the development repository for Claude Nexus
- User configuration stays in `~/.claude/toolkit.yaml`
- Framework code lives here in `~/code/claude-nexus`
- Always maintain backward compatibility