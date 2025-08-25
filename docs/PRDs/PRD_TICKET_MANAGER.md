# Product Requirements Document: Ticket Manager Migration

## Overview
Migrate ticket management functionality to the Click toolkit, providing unified commands for creating, managing, and listing ticket-based development workflows with git worktrees.

## Current State
- **Scripts**: 
  - `ticket-manager.zsh` - Complex ticket workflow automation
  - `tickets-lister.zsh` - List all ticket worktrees
  - Various lib files for JIRA/Git integration
- **Pain Points**:
  - Complex orchestration in shell scripts
  - Multiple tool dependencies (acli, git, jq)
  - Limited error handling
  - No agent-friendly interface

## Target State
A comprehensive Click-based ticket management system that:
- Creates and manages ticket-based git worktrees
- Integrates with multiple issue trackers (JIRA, Linear, GitHub Issues)
- Provides both creation and listing capabilities
- Supports agent automation

## User Stories

### As a Developer
- I want to create a new development environment for a ticket with one command
- I want to list all my active ticket worktrees
- I want to see ticket summaries without accessing JIRA
- I want to sync ticket status with git branches
- I want to clean up completed ticket worktrees

### As an AI Agent
- I want to programmatically create ticket environments
- I want to query active tickets and their status
- I want structured data about worktrees and tickets
- I want to orchestrate complete ticket workflows

## Functional Requirements

### Core Commands

#### `toolkit ticket create <ticket-id>`
Create a new ticket-based development environment

**Aliases**: `/ticket` (for backward compatibility)

**Options**:
- `--base-branch [branch]`: Base branch (default: main)
- `--no-fetch`: Skip fetching ticket details
- `--template [name]`: Use a ticket template
- `--auto-setup`: Run setup commands after creation

**Actions**:
1. Fetch ticket details from issue tracker
2. Generate appropriate branch name
3. Create git worktree
4. Set up development environment
5. Create context files
6. Generate initial specs

**Output**:
- Worktree location
- Branch name
- Ticket summary
- Next steps

#### `toolkit ticket list [repository]`
List all ticket worktrees

**Aliases**: `/tickets` (for backward compatibility)

**Options**:
- `--format [json|table|summary]`: Output format
- `--show-merged`: Include merged branches
- `--filter [status]`: Filter by ticket status
- `--verbose`: Show detailed information

**Output**:
- Ticket ID
- Summary
- Branch name
- Commit count
- Last activity
- Worktree path
- Merge status

#### `toolkit ticket sync <ticket-id>`
Synchronize ticket with issue tracker

**Options**:
- `--update-status`: Update ticket status based on branch
- `--fetch-comments`: Fetch latest comments
- `--push-branch`: Push branch to remote

#### `toolkit ticket cleanup`
Clean up completed ticket worktrees

**Options**:
- `--dry-run`: Show what would be removed
- `--keep-merged`: Don't remove merged branches
- `--older-than [days]`: Remove inactive worktrees

## Technical Requirements

### Interfaces

```python
class TicketManager(Protocol):
    """Interface for ticket management operations"""
    
    def create_ticket_environment(self, ticket_id: str, base: str = "main") -> Worktree
    def list_ticket_worktrees(self, repo_path: Path) -> List[TicketWorktree]
    def sync_ticket(self, ticket_id: str) -> SyncResult
    def cleanup_worktrees(self, older_than: int = 30) -> CleanupResult
    
    @property
    def capabilities(self) -> List[Capability]:
        ...
```

### Data Models

```python
@dataclass
class TicketWorktree:
    ticket_id: str
    summary: str
    branch_name: str
    worktree_path: Path
    commit_count: int
    last_activity: datetime
    is_merged: bool
    ticket_status: str
    
@dataclass
class TicketContext:
    ticket: Issue
    worktree: Worktree
    branch: Branch
    specs: Dict[str, Any]
    context_path: Path
    
@dataclass
class SyncResult:
    ticket_updated: bool
    branch_pushed: bool
    status_changed: bool
    new_comments: int
```

### Workflow Integration

```python
class TicketWorkflow:
    """Orchestrates complete ticket workflow"""
    
    def __init__(self, issue_tracker: IssueTracker, vcs: VCS):
        self.tracker = issue_tracker
        self.vcs = vcs
    
    def create_environment(self, ticket_id: str) -> TicketContext:
        # 1. Fetch ticket
        ticket = self.tracker.get_issue(ticket_id)
        
        # 2. Create branch name
        branch_name = self.generate_branch_name(ticket)
        
        # 3. Create worktree
        worktree = self.vcs.create_worktree(branch_name)
        
        # 4. Setup context
        context = self.create_context(ticket, worktree)
        
        # 5. Generate specs
        specs = self.generate_specs(ticket)
        
        return TicketContext(ticket, worktree, branch, specs, context_path)
```

### Repository Detection

```python
class RepositoryDetector:
    """Detects repository structure and worktree patterns"""
    
    def find_worktrees_dir(self, repo: Path) -> Path:
        """Find or create worktrees directory"""
        return repo.parent / f"{repo.name}.worktrees"
    
    def is_ticket_worktree(self, path: Path) -> bool:
        """Check if path is a ticket worktree"""
        return bool(re.match(r'^[A-Z]+-\d+', path.name))
```

## Migration Plan

### Phase 1: Create Command
1. Implement basic ticket fetching
2. Add branch name generation
3. Implement worktree creation
4. Create context file generation

### Phase 2: List Command
1. Implement worktree discovery
2. Add ticket summary fetching
3. Implement merge status detection
4. Add formatting options

### Phase 3: Sync Command
1. Implement ticket status sync
2. Add branch pushing
3. Implement comment fetching

### Phase 4: Cleanup Command
1. Implement merged branch detection
2. Add age-based filtering
3. Implement safe removal

## Configuration

```yaml
# .claude/toolkit.yaml
toolkit:
  tickets:
    worktree_pattern: "{repo}.worktrees"
    branch_format: "{type}/{ticket}/{summary}"
    auto_fetch: true
    context_dir: ".claude"
    
  issue_tracker:
    type: jira
    project: PROJ
    default_assignee: me
```

## Success Metrics

- [ ] Single command ticket environment creation
- [ ] Support for multiple issue trackers
- [ ] Faster than current ZSH implementation
- [ ] Agent-friendly programmatic interface
- [ ] Comprehensive test coverage
- [ ] Backward compatibility with aliases

## Testing Requirements

### Unit Tests
- Branch name generation
- Worktree path calculation
- Context file creation

### Integration Tests
- Full ticket creation workflow
- List with multiple worktrees
- Sync with real issue tracker

### Agent Tests
- Programmatic ticket creation
- Bulk operations
- Error handling

## Documentation Requirements

- Migration guide from `/ticket` command
- Workflow examples
- Agent automation guide
- Configuration reference

## Dependencies

- Click framework
- GitPython (for git operations)
- Rich (for table formatting)
- Issue tracker adapters (JIRA, Linear, etc.)

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Breaking existing workflows | High | Maintain aliases, backward compatibility |
| Issue tracker API limits | Medium | Implement caching, rate limiting |
| Large number of worktrees | Medium | Implement pagination, filtering |
| Corrupted worktrees | Low | Add validation, recovery commands |

## Future Enhancements

- Template system for common ticket types
- Automated PR/MR creation from tickets
- Time tracking integration
- Team collaboration features
- IDE integration
- Webhook support for real-time updates