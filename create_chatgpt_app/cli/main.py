"""Main CLI entry point for create-chatgpt-app."""

import click
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.table import Table

from create_chatgpt_app.generator import ProjectGenerator
from create_chatgpt_app.models import ProjectConfig, WidgetConfig

console = Console()


@click.group()
@click.version_option()
def cli():
    """create-chatgpt-app - Scaffold ChatGPT apps with ease."""
    pass


@cli.command()
@click.argument("project_name", required=False)
@click.option("--name", "-n", help="Project name")
@click.option("--description", "-d", help="Project description")
@click.option("--port", "-p", type=int, default=8000, help="Server port (default: 8000)")
@click.option("--host", "-h", default="0.0.0.0", help="Server host (default: 0.0.0.0)")
@click.option("--no-docker", is_flag=True, help="Skip Dockerfile generation")
@click.option("--no-tests", is_flag=True, help="Skip test file generation")
def init(project_name, name, description, port, host, no_docker, no_tests):
    """Initialize a new ChatGPT app project.

    Examples:
        create-chatgpt-app init my-app
        create-chatgpt-app init --name "My App" --description "My awesome app"
    """
    console.print(Panel.fit(
        "[bold cyan]create-chatgpt-app[/bold cyan]\n"
        "Let's create your ChatGPT app!",
        border_style="cyan"
    ))

    # Interactive prompts if options not provided
    if not project_name and not name:
        project_name = Prompt.ask(
            "[yellow]Project directory name[/yellow]",
            default="my-chatgpt-app"
        )

    if not name:
        name = Prompt.ask(
            "[yellow]App name (for MCP server)[/yellow]",
            default=project_name or "my-chatgpt-app"
        )

    if not description:
        description = Prompt.ask(
            "[yellow]App description[/yellow]",
            default=f"{name} - A ChatGPT app"
        )

    # Confirm widget creation
    create_widget = Confirm.ask(
        "[yellow]Create an initial widget?[/yellow]",
        default=True
    )

    widgets = []
    if create_widget:
        widget_id = Prompt.ask(
            "[yellow]Widget identifier (e.g., 'my-widget')[/yellow]",
            default="example-widget"
        )
        widget_title = Prompt.ask(
            "[yellow]Widget title[/yellow]",
            default="Example Widget"
        )
        widget_type = Prompt.ask(
            "[yellow]Widget type[/yellow]",
            choices=["cdn", "inline", "local"],
            default="inline"
        )

        widgets.append(WidgetConfig(
            identifier=widget_id,
            title=widget_title,
            widget_type=widget_type,
            template_uri=f"ui://widget/{widget_id}.html",
            invoking=f"Loading {widget_title}",
            invoked=f"{widget_title} loaded",
            response_text=f"{widget_title} rendered successfully!"
        ))

    # Create project configuration
    config = ProjectConfig(
        project_name=project_name or name,
        app_name=name,
        description=description,
        port=port,
        host=host,
        widgets=widgets,
        include_docker=not no_docker,
        include_tests=not no_tests
    )

    # Generate project
    try:
        generator = ProjectGenerator(config)
        project_path = generator.generate()

        console.print(f"\n[green]✓[/green] Project created successfully at: [cyan]{project_path}[/cyan]")

        # Display next steps
        console.print("\n[bold yellow]Next steps:[/bold yellow]")
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_row("1.", f"cd {config.project_name}")
        table.add_row("2.", "python -m venv .venv")
        table.add_row("3.", "source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate")
        table.add_row("4.", "pip install -r requirements.txt")
        table.add_row("5.", "python main.py")
        console.print(table)

        console.print(f"\n[dim]Your server will be running at http://{host}:{port}[/dim]")

    except Exception as e:
        console.print(f"[red]✗[/red] Error creating project: {e}")
        raise click.Abort()


@cli.command()
@click.option("--identifier", "-i", help="Widget identifier")
@click.option("--title", "-t", help="Widget title")
@click.option("--type", "widget_type", type=click.Choice(["cdn", "inline", "local"]), help="Widget type")
def add_widget(identifier, title, widget_type):
    """Add a new widget to the current project.

    Examples:
        create-chatgpt-app add-widget --identifier my-widget --title "My Widget"
        create-chatgpt-app add-widget  # Interactive mode
    """
    # Check if we're in a project directory
    if not Path("main.py").exists():
        console.print("[red]✗[/red] Error: Not in a ChatGPT app project directory.")
        console.print("[dim]Run 'create-chatgpt-app init' first or navigate to your project directory.[/dim]")
        raise click.Abort()

    console.print(Panel.fit(
        "[bold cyan]Add New Widget[/bold cyan]",
        border_style="cyan"
    ))

    # Interactive prompts
    if not identifier:
        identifier = Prompt.ask(
            "[yellow]Widget identifier (e.g., 'my-widget')[/yellow]"
        )

    if not title:
        title = Prompt.ask(
            "[yellow]Widget title[/yellow]",
            default=identifier.replace("-", " ").title()
        )

    if not widget_type:
        widget_type = Prompt.ask(
            "[yellow]Widget type[/yellow]",
            choices=["cdn", "inline", "local"],
            default="inline"
        )

    widget = WidgetConfig(
        identifier=identifier,
        title=title,
        widget_type=widget_type,
        template_uri=f"ui://widget/{identifier}.html",
        invoking=f"Loading {title}",
        invoked=f"{title} loaded",
        response_text=f"{title} rendered successfully!"
    )

    try:
        from chatgpt_scaffold.generator import WidgetAdder
        adder = WidgetAdder()
        adder.add_widget(widget)

        console.print(f"\n[green]✓[/green] Widget '{identifier}' added successfully!")
        console.print(f"[dim]Don't forget to restart your server to see the changes.[/dim]")

    except Exception as e:
        console.print(f"[red]✗[/red] Error adding widget: {e}")
        raise click.Abort()


@cli.command()
@click.option("--identifier", "-i", help="Tool identifier")
@click.option("--title", "-t", help="Tool title")
@click.option("--description", "-d", help="Tool description")
@click.option("--no-widget", is_flag=True, help="Create tool without a widget")
def add_tool(identifier, title, description, no_widget):
    """Add a new tool to the current project.

    Examples:
        create-chatgpt-app add-tool --identifier my-tool --title "My Tool"
        create-chatgpt-app add-tool  # Interactive mode
    """
    # Check if we're in a project directory
    if not Path("main.py").exists():
        console.print("[red]✗[/red] Error: Not in a ChatGPT app project directory.")
        console.print("[dim]Run 'create-chatgpt-app init' first or navigate to your project directory.[/dim]")
        raise click.Abort()

    console.print(Panel.fit(
        "[bold cyan]Add New Tool[/bold cyan]",
        border_style="cyan"
    ))

    # Interactive prompts
    if not identifier:
        identifier = Prompt.ask(
            "[yellow]Tool identifier (e.g., 'my-tool')[/yellow]"
        )

    if not title:
        title = Prompt.ask(
            "[yellow]Tool title[/yellow]",
            default=identifier.replace("-", " ").title()
        )

    if not description:
        description = Prompt.ask(
            "[yellow]Tool description[/yellow]",
            default=title
        )

    has_widget = not no_widget
    if no_widget is False:  # Not explicitly set
        has_widget = Confirm.ask(
            "[yellow]Does this tool render a widget?[/yellow]",
            default=True
        )

    widget = None
    if has_widget:
        widget_type = Prompt.ask(
            "[yellow]Widget type[/yellow]",
            choices=["cdn", "inline", "local"],
            default="inline"
        )

        widget = WidgetConfig(
            identifier=identifier,
            title=title,
            widget_type=widget_type,
            template_uri=f"ui://widget/{identifier}.html",
            invoking=f"Executing {title}",
            invoked=f"{title} completed",
            response_text=f"{title} executed successfully!"
        )

    console.print(f"\n[yellow]Note:[/yellow] Adding custom tools requires manual implementation.")
    console.print(f"[dim]This command will add the boilerplate for '{identifier}'.[/dim]")

    console.print(f"\n[green]✓[/green] Tool '{identifier}' structure created!")
    console.print(f"[dim]Edit main.py to implement your tool's business logic.[/dim]")


@cli.command()
def list_templates():
    """List available project templates."""
    console.print(Panel.fit(
        "[bold cyan]Available Templates[/bold cyan]",
        border_style="cyan"
    ))

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Template", style="cyan")
    table.add_column("Description")

    templates = [
        ("basic", "Basic MCP server with one widget"),
        ("multi-widget", "Server with multiple widget examples"),
        ("database", "Server with database integration example"),
        ("api", "Server with external API integration"),
    ]

    for name, desc in templates:
        table.add_row(name, desc)

    console.print(table)
    console.print("\n[dim]Use --template flag with 'init' command to select a template.[/dim]")


if __name__ == "__main__":
    cli()
