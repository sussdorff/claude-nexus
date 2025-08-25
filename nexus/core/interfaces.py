"""Protocol definitions for Claude Nexus interfaces."""

from typing import Protocol, List, Dict, Any, Optional
from nexus.core.capabilities import Capability


class Tool(Protocol):
    """Base protocol for all tool implementations."""
    
    @property
    def capabilities(self) -> List[Capability]:
        """Return list of capabilities this tool supports.
        
        Returns:
            List of Capability enums.
        """
        ...


class CodeHost(Protocol):
    """Interface for code hosting platforms (GitLab, GitHub)."""
    
    @property
    def capabilities(self) -> List[Capability]:
        """Return capabilities of this implementation."""
        ...
    
    def get_merge_request(self, mr_id: int) -> Dict[str, Any]:
        """Get merge request details.
        
        Args:
            mr_id: Merge request ID.
            
        Returns:
            Dictionary with MR details.
        """
        ...
    
    def list_merge_requests(self, state: str = "opened") -> List[Dict[str, Any]]:
        """List merge requests.
        
        Args:
            state: State filter (opened, closed, merged, all).
            
        Returns:
            List of MR dictionaries.
        """
        ...
    
    def get_discussions(self, mr_id: int) -> List[Dict[str, Any]]:
        """Get discussions for a merge request.
        
        Args:
            mr_id: Merge request ID.
            
        Returns:
            List of discussion dictionaries.
        """
        ...


class IssueTracker(Protocol):
    """Interface for issue tracking systems (JIRA, Linear, GitHub Issues)."""
    
    @property
    def capabilities(self) -> List[Capability]:
        """Return capabilities of this implementation."""
        ...
    
    def get_issue(self, issue_id: str) -> Dict[str, Any]:
        """Get issue details.
        
        Args:
            issue_id: Issue identifier.
            
        Returns:
            Dictionary with issue details.
        """
        ...
    
    def create_issue(self, title: str, description: str, **kwargs) -> str:
        """Create new issue.
        
        Args:
            title: Issue title.
            description: Issue description.
            **kwargs: Additional fields.
            
        Returns:
            Created issue ID.
        """
        ...
    
    def update_issue(self, issue_id: str, **fields) -> None:
        """Update issue fields.
        
        Args:
            issue_id: Issue identifier.
            **fields: Fields to update.
        """
        ...
    
    def search_issues(self, query: str) -> List[Dict[str, Any]]:
        """Search for issues.
        
        Args:
            query: Search query.
            
        Returns:
            List of issue dictionaries.
        """
        ...


class VCS(Protocol):
    """Interface for version control operations."""
    
    @property
    def capabilities(self) -> List[Capability]:
        """Return capabilities of this implementation."""
        ...
    
    def get_current_branch(self) -> str:
        """Get current branch name.
        
        Returns:
            Branch name.
        """
        ...
    
    def create_branch(self, name: str, base: Optional[str] = None) -> None:
        """Create new branch.
        
        Args:
            name: Branch name.
            base: Base branch (defaults to current).
        """
        ...
    
    def create_worktree(self, path: str, branch: str) -> None:
        """Create git worktree.
        
        Args:
            path: Worktree path.
            branch: Branch name.
        """
        ...
    
    def list_worktrees(self) -> List[Dict[str, Any]]:
        """List all worktrees.
        
        Returns:
            List of worktree dictionaries.
        """
        ...