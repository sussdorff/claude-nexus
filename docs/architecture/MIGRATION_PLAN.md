# Claude Toolkit Migration Plan

## Overview
Migration from ZSH scripts to a Python/Click-based toolkit with stable interfaces and swappable implementations.

## Core Principles
1. **One Tool to Rule Them All**: Single `toolkit` CLI with domain-organized commands
2. **Stable Interfaces**: Commands use interfaces that don't change when switching implementations
3. **Swappable Implementations**: CLI → API → MCP progression based on capabilities
4. **Repository Configuration**: Each repo declares its tools in `.claude/toolkit.yaml`
5. **Agent-First Design**: Optimized for Claude Code agents while remaining human-friendly

## Architecture Summary

### Directory Structure
```
toolkit/
├── cli.py                      # Main Click entry point
├── core/                       # Cross-cutting concerns
│   ├── config.py              # Repository configuration loader
│   ├── context.py             # Environment detection
│   └── registry.py            # Implementation selection
│
├── interfaces/                 # Stable protocol definitions
│   ├── code_host.py          # MR/PR operations
│   ├── issue_tracker.py      # Issue management
│   ├── vcs.py                # Version control
│   └── quality.py            # Code quality tools
│
├── tools/                      # Implementation adapters
│   ├── base.py               # Base classes
│   ├── code_hosts/           # GitLab, GitHub implementations
│   ├── issue_trackers/       # JIRA, Linear implementations
│   └── quality/              # Linters, formatters
│
└── commands/                   # Domain commands
    ├── tickets/               # Ticket management
    ├── reviews/               # Code reviews
    ├── quality/               # Code quality
    └── releases/              # Release management
```

### Configuration Strategy

Each repository can configure its tools via:

1. `.claude/toolkit.yaml` - Primary configuration
2. `.claude/CLAUDE.md` - Embedded configuration
3. `.env` - Environment overrides
4. Auto-detection - Git remote, file presence

Example configuration:
```yaml
toolkit:
  code_host:
    type: auto  # Auto-detect from git remote
    prefer: api  # mcp > api > cli
    
  issue_tracker:
    type: jira
    instance: https://company.atlassian.net
    project: PROJ
    prefer: cli  # Start with acli
```

### Implementation Selection

The toolkit automatically selects the best available implementation based on:

1. **Required Capabilities**: What the command needs
2. **Available Implementations**: What's installed/configured
3. **User Preference**: Configured preference
4. **Fallback Chain**: MCP → API → CLI

### Capability System

Each implementation declares its capabilities:
- `BASIC_READ` - Get/list operations
- `BASIC_WRITE` - Create/update operations
- `BULK_OPERATIONS` - Batch updates
- `ADVANCED_SEARCH` - Complex queries
- `CUSTOM_FIELDS` - Extended fields
- `WORKFLOW` - State transitions

## Migration Timeline

### Phase 1: Foundation (Days 1-4)
- Project setup and structure
- Core configuration system
- Interface definitions
- Implementation registry

### Phase 2: Priority Migrations (Week 1)
1. **MR Reviewer** - Solves JSON parsing issues
2. **Ticket Manager** - Core workflow automation
3. **Ticket Lister** - View all worktrees

### Phase 3: Extended Features (Week 2)
- Quality commands (linting, formatting)
- Release management
- Hook management

### Phase 4: Advanced Features (Week 3+)
- MCP server integration
- N8N workflow automation
- Custom client configurations

## Command Examples

### Human Usage
```bash
toolkit tickets create "New feature"
toolkit tickets list
toolkit mr review --mr-id 177
toolkit quality lint src/
toolkit release prepare v1.2.3
```

### Agent Usage
```python
from toolkit import ToolSelector

selector = ToolSelector()
tracker = selector.get_issue_tracker()
issue = tracker.get_issue("PROJ-123")
```

## Benefits

1. **Stable Interfaces**: No code changes when switching tools
2. **Progressive Enhancement**: Upgrade implementations as needed
3. **Per-Repository Config**: Each project has its own setup
4. **Testability**: Mock at interface level
5. **Extensibility**: Easy to add new tools/implementations
6. **Agent-Optimized**: Direct Python invocation for agents
7. **Human-Friendly**: Clean CLI for manual use

## Success Criteria

- [ ] All ZSH scripts migrated to Click commands
- [ ] JSON parsing issues resolved
- [ ] Support for GitLab and GitHub
- [ ] Support for JIRA and Linear
- [ ] Per-repository configuration working
- [ ] Agent integration complete
- [ ] Comprehensive test coverage
- [ ] Documentation complete