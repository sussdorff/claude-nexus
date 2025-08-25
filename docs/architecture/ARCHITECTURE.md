# Claude Toolkit Architecture Design

## System Overview

The Claude Toolkit is a unified command-line interface designed with a hexagonal architecture pattern, emphasizing stable interfaces with swappable implementations. The system follows Domain-Driven Design (DDD) principles and is optimized for both human users and AI agents.

## Architectural Patterns

### 1. Hexagonal Architecture (Ports and Adapters)

```
┌─────────────────────────────────────────────┐
│            Primary Ports (Input)            │
│  ┌──────────────────────────────────────┐  │
│  │    CLI Interface (Click Commands)    │  │
│  └──────────────────────────────────────┘  │
│  ┌──────────────────────────────────────┐  │
│  │    API Interface (Python Methods)    │  │
│  └──────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────┐
│           Core Business Logic               │
│  ┌──────────────────────────────────────┐  │
│  │    Domain Commands & Services        │  │
│  │    (Pure business logic)             │  │
│  └──────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────┐
│         Secondary Ports (Output)            │
│  ┌──────────────────────────────────────┐  │
│  │        Tool Interfaces               │  │
│  │  (CodeHost, IssueTracker, VCS, etc.) │  │
│  └──────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────┐
│            Adapters (Implementations)       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │   CLI    │  │   API    │  │   MCP    │  │
│  │ Adapters │  │ Adapters │  │ Adapters │  │
│  └──────────┘  └──────────┘  └──────────┘  │
└─────────────────────────────────────────────┘
```

### 2. Domain-Driven Design

The system is organized around business domains rather than technical layers:

- **Tickets Domain**: Issue management and worktree operations
- **Reviews Domain**: Code review and merge request management
- **Quality Domain**: Code quality, linting, and formatting
- **Releases Domain**: Version management and deployment

### 3. Interface Segregation Principle

Each interface defines only the methods that clients actually need:

```python
class IssueTracker(Protocol):
    """Minimal interface for issue tracking"""
    def get_issue(self, issue_id: str) -> Issue
    def create_issue(self, title: str, description: str) -> str
    def update_issue(self, issue_id: str, **fields) -> None
```

## Core Components

### 1. Configuration System

**Purpose**: Load and merge configuration from multiple sources

**Sources** (in priority order):
1. `.claude/toolkit.yaml` - Repository-specific configuration
2. `.claude/CLAUDE.md` - Embedded configuration in documentation
3. `.env` - Environment variable overrides
4. Auto-detection - Inferred from repository context

**Interface**:
```python
class Configuration:
    def get(self, key: str, default: Any = None) -> Any
    def get_tool_config(self, tool_type: str) -> Dict[str, Any]
```

### 2. Registry System

**Purpose**: Manage available implementations and their capabilities

**Components**:
- `ImplementationRegistry`: Catalog of all available implementations
- `CapabilityRegistry`: Mapping of capabilities to implementations
- `ToolSelector`: Selects best implementation based on requirements

**Interface**:
```python
class ToolSelector:
    def get_tool(self, 
                 interface_type: Type[T], 
                 required_capabilities: List[Capability] = None) -> T
```

### 3. Interface Definitions

**Purpose**: Define stable contracts between components

**Key Interfaces**:

```python
class CodeHost(Protocol):
    """Operations on code hosting platforms"""
    def get_merge_request(self, mr_id: int) -> MergeRequest
    def create_merge_request(self, title: str, source: str, target: str) -> int
    def get_discussions(self, mr_id: int) -> List[Discussion]

class IssueTracker(Protocol):
    """Issue tracking operations"""
    def get_issue(self, issue_id: str) -> Issue
    def create_issue(self, title: str, description: str) -> str
    def search_issues(self, query: str) -> List[Issue]

class VCS(Protocol):
    """Version control operations"""
    def get_current_branch(self) -> Branch
    def create_branch(self, name: str, base: str = "main") -> None
    def list_worktrees(self) -> List[Worktree]

class QualityTool(Protocol):
    """Code quality operations"""
    def lint(self, path: Path, profile: str = "default") -> LintResult
    def format(self, path: Path, fix: bool = False) -> FormatResult
```

### 4. Capability System

**Purpose**: Declare what each implementation can do

**Capabilities**:
```python
class Capability(Enum):
    # Basic operations
    BASIC_READ = "basic_read"
    BASIC_WRITE = "basic_write"
    
    # Advanced operations
    BULK_OPERATIONS = "bulk_operations"
    ADVANCED_SEARCH = "advanced_search"
    CUSTOM_FIELDS = "custom_fields"
    
    # Integration features
    WEBHOOKS = "webhooks"
    WORKFLOW_AUTOMATION = "workflow_automation"
```

### 5. Implementation Adapters

**Purpose**: Wrap external tools to conform to interfaces

**Base Classes**:
```python
class CLIAdapter:
    """Base for CLI tool wrappers"""
    def run_command(self, cmd: List[str]) -> CommandResult
    def run_json_command(self, cmd: List[str]) -> Dict[str, Any]

class APIAdapter:
    """Base for REST API wrappers"""
    def request(self, method: str, endpoint: str, **kwargs) -> Response

class MCPAdapter:
    """Base for MCP server connections"""
    def call(self, method: str, **params) -> Any
```

## Implementation Strategy

### 1. Progressive Enhancement

Implementations are ordered by capability level:
1. **CLI**: Basic operations, no setup required
2. **API**: Advanced features, requires credentials
3. **MCP**: Full capabilities, requires server setup

### 2. Graceful Degradation

The system automatically falls back to simpler implementations:
```
MCP (unavailable) → API (unavailable) → CLI (available) ✓
```

### 3. Capability-Based Selection

Commands declare required capabilities:
```python
def advanced_search_command():
    tracker = selector.get_tool(
        IssueTracker, 
        required_capabilities=[Capability.ADVANCED_SEARCH]
    )
```

## Command Structure

### 1. Command Organization

Commands are organized by domain:
```
commands/
├── tickets/
│   ├── create.py
│   ├── list.py
│   └── sync.py
├── reviews/
│   ├── review.py
│   └── approve.py
└── quality/
    ├── lint.py
    └── format.py
```

### 2. Command Pattern

Each command follows this pattern:
```python
@click.command()
@click.option('--format', type=click.Choice(['json', 'table']))
def command_name(format):
    """Command description"""
    # 1. Get required tools from selector
    selector = ToolSelector()
    tool = selector.get_tool(InterfaceType)
    
    # 2. Execute business logic
    result = perform_operation(tool)
    
    # 3. Format output
    output = format_result(result, format)
    click.echo(output)
```

## Extension Points

### 1. Adding New Implementations

1. Create adapter class implementing interface
2. Declare capabilities
3. Register in `ImplementationRegistry`

### 2. Adding New Domains

1. Create domain directory under `commands/`
2. Define domain-specific interfaces if needed
3. Implement commands using existing interfaces

### 3. Adding New Tool Types

1. Define interface in `interfaces/`
2. Create base adapter in `tools/base.py`
3. Implement concrete adapters

## Testing Strategy

### 1. Interface Testing

Test that implementations satisfy interface contracts:
```python
def test_interface_compliance(implementation: IssueTracker):
    assert hasattr(implementation, 'get_issue')
    assert hasattr(implementation, 'create_issue')
```

### 2. Mock Implementations

Provide mock implementations for testing:
```python
class MockIssueTracker:
    def get_issue(self, issue_id: str) -> Issue:
        return Issue(id=issue_id, title="Mock Issue")
```

### 3. Integration Testing

Test complete workflows with real implementations:
```python
def test_ticket_workflow():
    selector = ToolSelector(test_config)
    tracker = selector.get_tool(IssueTracker)
    issue_id = tracker.create_issue("Test", "Description")
    issue = tracker.get_issue(issue_id)
    assert issue.title == "Test"
```

## Design Principles

1. **Dependency Inversion**: Depend on interfaces, not implementations
2. **Single Responsibility**: Each component has one reason to change
3. **Open/Closed**: Open for extension, closed for modification
4. **Interface Segregation**: Many specific interfaces over few general ones
5. **Liskov Substitution**: Implementations are interchangeable

## Configuration Examples

### Work Repository
```yaml
toolkit:
  code_host:
    type: gitlab
    prefer: api
  issue_tracker:
    type: jira
    instance: https://company.atlassian.net
    prefer: mcp  # Use MCP for advanced features
```

### Personal Repository
```yaml
toolkit:
  code_host:
    type: github
    prefer: api
  issue_tracker:
    type: linear
    prefer: api
```

## Future Extensibility

The architecture supports future enhancements:

1. **Workflow Automation**: N8N integration for complex workflows
2. **Plugin System**: External plugins can provide new implementations
3. **Remote Execution**: Commands can execute on remote servers
4. **Event System**: Webhooks and real-time updates
5. **Caching Layer**: Performance optimization with caching

## Summary

This architecture provides:
- Stable interfaces that don't change
- Swappable implementations based on capabilities
- Progressive enhancement from CLI to API to MCP
- Per-repository configuration
- Testability through interface mocking
- Clear extension points for new features