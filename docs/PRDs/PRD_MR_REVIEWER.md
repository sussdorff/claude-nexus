# Product Requirements Document: MR Reviewer Migration

## Overview
Migrate the MR Review functionality from ZSH scripts to the Click toolkit, solving JSON parsing issues and providing a robust interface for reviewing merge/pull requests.

## Current State
- **Script**: `mr-review-handler.zsh` and `lib/mr-review.zsh`
- **Pain Points**:
  - JSON parsing with control characters fails
  - Using grep/sed to extract JSON fields
  - Complex error handling in shell scripts
  - Limited testing capabilities

## Target State
A Click-based command that provides merge request review functionality with:
- Robust JSON handling
- Support for both GitLab MRs and GitHub PRs
- Progressive implementation (CLI → API → MCP)
- Agent-friendly interface

## User Stories

### As a Developer
- I want to review merge requests from the command line
- I want to see all unresolved discussions
- I want to automatically apply suggested fixes
- I want the tool to work with both GitLab and GitHub

### As an AI Agent
- I want to programmatically review MRs
- I want structured data about discussions
- I want to apply fixes without subprocess calls
- I want rich error information

## Functional Requirements

### Core Commands

#### `toolkit review mr <mr-id>`
Review a merge/pull request

**Options**:
- `--auto-fix`: Automatically apply suggested fixes
- `--format [json|table|summary]`: Output format
- `--fetch-changes`: Include file changes in review
- `--verbose`: Detailed output

**Output**:
- MR/PR details (title, author, status)
- Unresolved discussions count
- List of feedback items
- Suggested fixes (if any)

#### `toolkit review list`
List all open MRs/PRs for current repository

**Options**:
- `--assigned-to-me`: Only show assigned reviews
- `--needs-attention`: Show MRs with unresolved discussions
- `--format [json|table]`: Output format

#### `toolkit review approve <mr-id>`
Approve a merge/pull request

**Options**:
- `--message`: Approval message

## Technical Requirements

### Interfaces

```python
class CodeReview(Protocol):
    """Interface for code review operations"""
    
    def get_review(self, review_id: int) -> Review
    def get_discussions(self, review_id: int) -> List[Discussion]
    def post_comment(self, review_id: int, comment: str) -> None
    def approve(self, review_id: int, message: str = None) -> None
    def apply_suggestion(self, suggestion_id: str) -> None
    
    @property
    def capabilities(self) -> List[Capability]:
        ...
```

### Data Models

```python
@dataclass
class Review:
    id: int
    title: str
    author: str
    status: str
    source_branch: str
    target_branch: str
    discussions_count: int
    unresolved_count: int
    
@dataclass
class Discussion:
    id: str
    author: str
    body: str
    resolved: bool
    resolvable: bool
    suggestions: List[Suggestion]
    
@dataclass
class Suggestion:
    id: str
    diff: str
    applicable: bool
```

### Implementation Priority

1. **GitLabCLI** (using glab) - Immediate need
2. **GitLabAPI** - When API token available
3. **GitHubCLI** (using gh) - Personal projects
4. **GitHubAPI** - Enhanced features

### Capability Requirements

| Capability | CLI | API | MCP |
|------------|-----|-----|-----|
| Get MR details | ✓ | ✓ | ✓ |
| Get discussions | ✓ | ✓ | ✓ |
| Post comments | ✓ | ✓ | ✓ |
| Apply suggestions | ✗ | ✓ | ✓ |
| Bulk operations | ✗ | ✗ | ✓ |

## Migration Plan

### Phase 1: Core Review Command
1. Create `toolkit/commands/reviews/` directory
2. Implement `review.py` with basic MR fetching
3. Create GitLabCLI adapter using glab
4. Handle JSON parsing properly with Python

### Phase 2: Discussion Analysis
1. Add discussion fetching and parsing
2. Implement feedback analysis logic
3. Add suggestion detection

### Phase 3: Auto-Fix Feature
1. Implement suggestion application (API only)
2. Add git operations for applying changes
3. Create fix verification logic

### Phase 4: Extended Features
1. Add GitHub support
2. Implement approval command
3. Add list command for multiple MRs

## Success Metrics

- [ ] No JSON parsing errors
- [ ] 100% compatibility with existing workflow
- [ ] Support for both GitLab and GitHub
- [ ] Agent can use without subprocess
- [ ] Comprehensive test coverage
- [ ] Performance: < 2s for basic review

## Configuration

```yaml
# .claude/toolkit.yaml
toolkit:
  code_host:
    type: gitlab  # or github
    prefer: api   # cli, api, or mcp
    
  review:
    auto_fetch_changes: true
    default_format: table
    show_suggestions: true
```

## Testing Requirements

### Unit Tests
- Mock GitLab/GitHub responses
- Test discussion parsing
- Test suggestion extraction

### Integration Tests
- Test with real MR (in test project)
- Test auto-fix application
- Test error handling

### Agent Tests
- Test programmatic invocation
- Test structured data return
- Test error propagation

## Documentation Requirements

- Command-line help text
- README with examples
- Agent usage guide
- Migration guide from ZSH script

## Dependencies

- Click framework
- httpx (for API implementations)
- Rich (for table formatting)
- GitPython (for git operations)

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| API changes | High | Use versioned APIs, implement adapters |
| Large MRs | Medium | Implement pagination |
| Network issues | Medium | Add retry logic with backoff |
| Auth failures | Low | Clear error messages, auth check command |

## Future Enhancements

- Real-time discussion monitoring
- Integration with IDE
- Batch review operations
- AI-powered review suggestions
- Webhook support for notifications