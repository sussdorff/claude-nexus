"""Mock implementations for testing."""

from typing import List, Dict, Any
from nexus.core.capabilities import Capability


class MockCodeHost:
    """Mock CodeHost implementation."""
    
    @property
    def capabilities(self) -> List[Capability]:
        return [Capability.BASIC_READ]
    
    def get_merge_request(self, mr_id: int) -> Dict[str, Any]:
        return {
            "id": mr_id,
            "title": f"Mock MR #{mr_id}",
            "state": "opened"
        }
    
    def list_merge_requests(self, state: str = "opened") -> List[Dict[str, Any]]:
        return [
            {"id": 1, "title": "Mock MR #1", "state": state},
            {"id": 2, "title": "Mock MR #2", "state": state}
        ]
    
    def get_discussions(self, mr_id: int) -> List[Dict[str, Any]]:
        return [
            {"id": "disc1", "body": "Test discussion", "resolved": False}
        ]


class MockGitLabCLI(MockCodeHost):
    """Mock GitLab CLI implementation."""
    
    @property
    def capabilities(self) -> List[Capability]:
        return [Capability.BASIC_READ, Capability.CLI_AVAILABLE]


class MockGitLabAPI(MockCodeHost):
    """Mock GitLab API implementation."""
    
    @property
    def capabilities(self) -> List[Capability]:
        return [
            Capability.BASIC_READ,
            Capability.BASIC_WRITE,
            Capability.ADVANCED_SEARCH,
            Capability.API_ACCESS
        ]


class MockIssueTracker:
    """Mock IssueTracker implementation."""
    
    @property
    def capabilities(self) -> List[Capability]:
        return [Capability.BASIC_READ, Capability.BASIC_WRITE]
    
    def get_issue(self, issue_id: str) -> Dict[str, Any]:
        return {
            "id": issue_id,
            "title": f"Mock Issue {issue_id}",
            "status": "Open"
        }
    
    def create_issue(self, title: str, description: str, **kwargs) -> str:
        return "TEST-123"
    
    def update_issue(self, issue_id: str, **fields) -> None:
        pass
    
    def search_issues(self, query: str) -> List[Dict[str, Any]]:
        return [
            {"id": "TEST-1", "title": "Found Issue 1"},
            {"id": "TEST-2", "title": "Found Issue 2"}
        ]


class MockJiraCLI(MockIssueTracker):
    """Mock JIRA CLI implementation."""
    
    @property
    def capabilities(self) -> List[Capability]:
        return [
            Capability.BASIC_READ,
            Capability.BASIC_WRITE,
            Capability.CLI_AVAILABLE
        ]