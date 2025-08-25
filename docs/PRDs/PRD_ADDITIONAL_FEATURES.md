# Product Requirements Document: Additional Toolkit Features

## Overview
Additional features and utilities to complete the Claude Toolkit migration, based on existing commands and scripts that provide value to the development workflow.

## Features Summary

Based on the review of existing commands, the toolkit already covers the main features:
1. **MR Review** (/mr-review) - Already covered in PRD_MR_REVIEWER.md
2. **Ticket Management** (/ticket, /tickets) - Already covered in PRD_TICKET_MANAGER.md
3. **Release Management** (/vorabversion) - Already covered in PRD_RELEASE_AGENT.md

## Additional Utilities to Consider

### 1. Worktree Cleanup Utility
**Command**: `toolkit worktree cleanup`

**Purpose**: Clean up abandoned or merged worktrees

**Features**:
- Detect merged branches
- Find abandoned worktrees (no commits in X days)
- Safe removal with confirmation
- Batch operations

### 2. Project Setup Command
**Command**: `toolkit project init`

**Purpose**: Initialize a new project with toolkit configuration

**Features**:
- Create `.claude/toolkit.yaml`
- Detect and configure code host
- Set up issue tracker
- Generate initial CLAUDE.md

### 3. Configuration Management
**Command**: `toolkit config`

**Purpose**: Manage toolkit configuration

**Subcommands**:
- `toolkit config show` - Display current configuration
- `toolkit config set <key> <value>` - Set configuration value
- `toolkit config validate` - Validate configuration
- `toolkit config migrate` - Migrate from old format

### 4. Diagnostics Command
**Command**: `toolkit doctor`

**Purpose**: Check toolkit health and dependencies

**Features**:
- Check installed CLI tools (glab, gh, acli, etc.)
- Verify API credentials
- Test connections to services
- Suggest fixes for common issues

### 5. Alias Management
**Command**: `toolkit alias`

**Purpose**: Manage command aliases for backward compatibility

**Features**:
- Register aliases (/ticket → toolkit ticket create)
- List active aliases
- Export shell functions
- Generate shell completion

### 6. PRD Generator Integration
**Command**: `toolkit prd generate <ticket-id>`

**Purpose**: Generate Product Requirements Documents from tickets

**Features**:
- Fetch ticket details
- Analyze linked issues
- Generate structured PRD
- Save to `.claude/prd.md`

### 7. Test Runner Integration
**Command**: `toolkit test`

**Purpose**: Unified test running across projects

**Features**:
- Auto-detect test framework
- Run specific test suites
- Watch mode for TDD
- Coverage reporting

### 8. Git Hooks Management
**Command**: `toolkit hooks`

**Purpose**: Manage git hooks for the project

**Subcommands**:
- `toolkit hooks install` - Install project hooks
- `toolkit hooks run <hook>` - Run specific hook
- `toolkit hooks list` - Show installed hooks

## Implementation Priority

### High Priority (Include in Initial Release)
1. **Worktree Cleanup** - Essential for workspace management
2. **Configuration Management** - Core functionality
3. **Diagnostics** - Critical for troubleshooting

### Medium Priority (Phase 2)
4. **Project Setup** - Useful for onboarding
5. **Alias Management** - Backward compatibility
6. **PRD Generator** - Enhances ticket workflow

### Low Priority (Future Enhancements)
7. **Test Runner** - Nice to have
8. **Git Hooks** - Advanced feature

## Integration Points

### With Existing Features
- Worktree cleanup integrates with ticket management
- Configuration affects all commands
- Diagnostics helps troubleshoot all features
- PRD generator enhances ticket workflow

### With External Tools
- Git hooks integrate with CI/CD
- Test runner works with project test frameworks
- Alias management integrates with shell

## Success Criteria

- [ ] All high-priority utilities implemented
- [ ] Seamless integration with core features
- [ ] Comprehensive help documentation
- [ ] Agent-friendly interfaces
- [ ] Backward compatibility maintained

## Notes

The core functionality (tickets, reviews, releases) covers the main developer workflow. These additional utilities enhance the toolkit but are not critical for the initial release. Focus should be on making the core features robust before adding these utilities.