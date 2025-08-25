"""Output formatting utilities for Claude Nexus."""

import json
from typing import Any, Dict, List
from rich.console import Console
from rich.table import Table
from rich.json import JSON


class OutputFormatter:
    """Formats output for different display modes."""
    
    def __init__(self):
        """Initialize formatter."""
        self.console = Console()
    
    def format_json(self, data: Any) -> str:
        """Format data as JSON.
        
        Args:
            data: Data to format.
            
        Returns:
            JSON string.
        """
        return json.dumps(data, indent=2, default=str)
    
    def format_table(
        self,
        data: List[Dict[str, Any]],
        columns: Optional[List[str]] = None,
        title: Optional[str] = None
    ) -> None:
        """Format data as a table and print it.
        
        Args:
            data: List of dictionaries to display.
            columns: Column names to display (defaults to all keys).
            title: Table title.
        """
        if not data:
            self.console.print("No data to display")
            return
        
        # Determine columns
        if not columns:
            columns = list(data[0].keys())
        
        # Create table
        table = Table(title=title, show_header=True, header_style="bold magenta")
        
        # Add columns
        for col in columns:
            table.add_column(col, style="cyan")
        
        # Add rows
        for item in data:
            row = []
            for col in columns:
                value = item.get(col, "")
                if value is None:
                    value = ""
                row.append(str(value))
            table.add_row(*row)
        
        self.console.print(table)
    
    def format_summary(self, data: Dict[str, Any], title: Optional[str] = None) -> None:
        """Format data as a summary.
        
        Args:
            data: Dictionary to display.
            title: Summary title.
        """
        if title:
            self.console.print(f"\n[bold cyan]{title}[/bold cyan]")
            self.console.print("=" * 50)
        
        for key, value in data.items():
            # Convert key from snake_case to Title Case
            display_key = key.replace('_', ' ').title()
            self.console.print(f"[bold]{display_key}:[/bold] {value}")
    
    def print_json(self, data: Any) -> None:
        """Print data as formatted JSON.
        
        Args:
            data: Data to print.
        """
        json_str = self.format_json(data)
        self.console.print(JSON(json_str))
    
    def print_error(self, message: str) -> None:
        """Print error message.
        
        Args:
            message: Error message.
        """
        self.console.print(f"[bold red]Error:[/bold red] {message}")
    
    def print_warning(self, message: str) -> None:
        """Print warning message.
        
        Args:
            message: Warning message.
        """
        self.console.print(f"[bold yellow]Warning:[/bold yellow] {message}")
    
    def print_success(self, message: str) -> None:
        """Print success message.
        
        Args:
            message: Success message.
        """
        self.console.print(f"[bold green]Success:[/bold green] {message}")