"""Main CLI entry point for Claude Nexus."""

import click
from pathlib import Path
from nexus.core.config import Configuration
from nexus.core.registry import ImplementationRegistry
from nexus.core.selector import ToolSelector
from nexus import __version__


@click.group()
@click.pass_context
def cli(ctx):
    """Claude Nexus - Your central connection point for development tools."""
    ctx.ensure_object(dict)
    ctx.obj['config'] = Configuration()
    ctx.obj['registry'] = ImplementationRegistry()
    ctx.obj['selector'] = ToolSelector(ctx.obj['registry'])


@cli.command()
def version():
    """Show Claude Nexus version."""
    click.echo(f"Claude Nexus v{__version__.__version__}")


@cli.command()
@click.pass_context
def doctor(ctx):
    """Check Claude Nexus health and configuration."""
    from rich.console import Console
    from rich.table import Table
    import subprocess
    
    console = Console()
    config = ctx.obj['config']
    
    console.print("\n🔍 [bold cyan]Claude Nexus Doctor[/bold cyan]")
    console.print("=" * 50)
    
    # Configuration check
    console.print("\n📋 [bold]Configuration:[/bold]")
    config_path = config.config_path
    if config_path and config_path.exists():
        console.print(f"  ✅ Config file: {config_path}")
    else:
        console.print(f"  ⚠️  No config file found (will use auto-detection)")
        console.print(f"     Expected locations:")
        console.print(f"     - {Path.cwd() / '.claude' / 'toolkit.yaml'}")
        console.print(f"     - {Path.home() / '.claude' / 'toolkit.yaml'}")
    
    # Environment detection
    console.print("\n🔧 [bold]Environment:[/bold]")
    repo_type = config.get("toolkit.code_host.type", "unknown")
    if repo_type != "unknown":
        console.print(f"  ✅ Repository type: {repo_type}")
    else:
        console.print(f"  ⚠️  Repository type: not detected")
    
    # Tool availability
    console.print("\n🛠️  [bold]Available Tools:[/bold]")
    
    tools = {
        "git": "Version control",
        "gh": "GitHub CLI",
        "glab": "GitLab CLI",
        "jq": "JSON processor",
        "acli": "Atlassian CLI (JIRA)",
    }
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Tool", style="cyan")
    table.add_column("Purpose", style="white")
    table.add_column("Status", style="green")
    
    for tool, purpose in tools.items():
        try:
            result = subprocess.run(
                ["which", tool],
                capture_output=True,
                text=True,
                check=False
            )
            if result.returncode == 0:
                status = "✅ Available"
            else:
                status = "❌ Not found"
        except Exception:
            status = "❌ Error"
        
        table.add_row(tool, purpose, status)
    
    console.print(table)
    
    # Summary
    console.print("\n📊 [bold]Summary:[/bold]")
    console.print("  Claude Nexus is ready for use!")
    console.print("  Run 'claude-nexus --help' or 'cnx --help' for available commands.")


def main():
    """Entry point for the Claude Nexus CLI."""
    cli(obj={})


if __name__ == "__main__":
    main()