"""Project and widget generator for create-chatgpt-app."""

import os
import re
from pathlib import Path
from typing import Optional

from jinja2 import Environment, PackageLoader, select_autoescape

from create_chatgpt_app.models import ProjectConfig, WidgetConfig


class ProjectGenerator:
    """Generate a new ChatGPT app project from templates."""

    def __init__(self, config: ProjectConfig):
        self.config = config
        self.env = Environment(
            loader=PackageLoader("create_chatgpt_app", "templates"),
            autoescape=select_autoescape(),
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def generate(self) -> Path:
        """Generate the project structure and files."""
        project_path = Path.cwd() / self.config.project_name

        # Create project directory
        if project_path.exists():
            raise ValueError(f"Directory '{self.config.project_name}' already exists")

        project_path.mkdir(parents=True)

        # Generate files
        self._generate_main_py(project_path)
        self._generate_requirements_txt(project_path)
        self._generate_readme(project_path)
        self._generate_gitignore(project_path)

        if self.config.include_docker:
            self._generate_dockerfile(project_path)
            self._generate_dockerignore(project_path)

        if self.config.include_tests:
            self._generate_tests(project_path)

        return project_path

    def _generate_main_py(self, project_path: Path) -> None:
        """Generate main.py file."""
        template = self.env.get_template("main.py.j2")
        content = template.render(
            app_name=self.config.app_name,
            description=self.config.description,
            port=self.config.port,
            host=self.config.host,
            widgets=self.config.widgets,
        )
        (project_path / "main.py").write_text(content)

    def _generate_requirements_txt(self, project_path: Path) -> None:
        """Generate requirements.txt file."""
        template = self.env.get_template("requirements.txt.j2")
        content = template.render()
        (project_path / "requirements.txt").write_text(content)

    def _generate_readme(self, project_path: Path) -> None:
        """Generate README.md file."""
        template = self.env.get_template("README.md.j2")
        content = template.render(
            project_name=self.config.project_name,
            app_name=self.config.app_name,
            description=self.config.description,
            port=self.config.port,
            host=self.config.host,
            widgets=self.config.widgets,
        )
        (project_path / "README.md").write_text(content)

    def _generate_gitignore(self, project_path: Path) -> None:
        """Generate .gitignore file."""
        template = self.env.get_template("gitignore.j2")
        content = template.render()
        (project_path / ".gitignore").write_text(content)

    def _generate_dockerfile(self, project_path: Path) -> None:
        """Generate Dockerfile."""
        template = self.env.get_template("Dockerfile.j2")
        content = template.render(
            python_version=self.config.python_version,
            port=self.config.port,
        )
        (project_path / "Dockerfile").write_text(content)

    def _generate_dockerignore(self, project_path: Path) -> None:
        """Generate .dockerignore file."""
        template = self.env.get_template("dockerignore.j2")
        content = template.render()
        (project_path / ".dockerignore").write_text(content)

    def _generate_tests(self, project_path: Path) -> None:
        """Generate test files."""
        tests_dir = project_path / "tests"
        tests_dir.mkdir()

        template = self.env.get_template("test_main.py.j2")
        content = template.render(
            app_name=self.config.app_name,
            widgets=self.config.widgets,
        )
        (tests_dir / "test_main.py").write_text(content)
        (tests_dir / "__init__.py").write_text("")


class WidgetAdder:
    """Add a widget to an existing project."""

    def add_widget(self, widget: WidgetConfig) -> None:
        """Add a widget to the main.py file."""
        main_py_path = Path("main.py")

        if not main_py_path.exists():
            raise FileNotFoundError("main.py not found in current directory")

        content = main_py_path.read_text()

        # Generate widget code
        widget_code = self._generate_widget_code(widget)

        # Find the widgets list and add the new widget
        # Look for the pattern: widgets: List[...] = [
        pattern = r"(widgets:\s*List\[[^\]]+\]\s*=\s*\[)(.*?)(\n\])"
        match = re.search(pattern, content, re.DOTALL)

        if not match:
            raise ValueError("Could not find widgets list in main.py")

        before = match.group(1)
        existing_widgets = match.group(2)
        after = match.group(3)

        # Add comma if there are existing widgets
        separator = "," if existing_widgets.strip() else ""

        # Construct new content
        new_widgets_section = f"{before}{existing_widgets}{separator}\n{widget_code}{after}"
        new_content = content[: match.start()] + new_widgets_section + content[match.end() :]

        # Write back
        main_py_path.write_text(new_content)

    def _generate_widget_code(self, widget: WidgetConfig) -> str:
        """Generate Python code for a widget."""
        html = self._generate_widget_html(widget)

        code = f"""    {self._get_widget_class_name()}(
        identifier="{widget.identifier}",
        title="{widget.title}",
        template_uri="{widget.template_uri}",
        invoking="{widget.invoking}",
        invoked="{widget.invoked}",
        html=(
{self._indent_multiline(html, 12)}
        ),
        response_text="{widget.response_text}",
    )"""

        return code

    def _generate_widget_html(self, widget: WidgetConfig) -> str:
        """Generate HTML for a widget based on its type."""
        root_id = widget.identifier.replace("-", "_")

        if widget.widget_type == "cdn":
            cdn_css = widget.cdn_css or f"https://example.com/{widget.identifier}.css"
            cdn_js = widget.cdn_js or f"https://example.com/{widget.identifier}.js"
            return (
                f'"<div id=\\"{root_id}_root\\\"></div>\\n"'
                f'"<link rel=\\"stylesheet\\" href=\\"{cdn_css}\\">\\n"'
                f'"<script type=\\"module\\" src=\\"{cdn_js}\\"></script>"'
            )
        elif widget.widget_type == "local":
            return (
                f'"<div id=\\"{root_id}_root\\\"></div>\\n"'
                f'"<link rel=\\"stylesheet\\" href=\\"/static/{widget.identifier}.css\\">\\n"'
                f'"<script type=\\"module\\" src=\\"/static/{widget.identifier}.js\\"></script>"'
            )
        else:  # inline
            html_content = widget.html_content or (
                f"<div style='padding: 20px; border: 1px solid #ccc;'>"
                f"<h2>{widget.title}</h2>"
                f"<p>This is {widget.identifier} widget.</p>"
                f"</div>"
            )
            # Escape the HTML for Python string
            escaped = html_content.replace("\\", "\\\\").replace('"', '\\"')
            return f'"{escaped}"'

    def _get_widget_class_name(self) -> str:
        """Detect the widget class name from main.py."""
        main_py_path = Path("main.py")
        content = main_py_path.read_text()

        # Look for @dataclass class definitions
        match = re.search(r"@dataclass\(frozen=True\)\s*class\s+(\w+Widget):", content)
        if match:
            return match.group(1)

        # Default fallback
        return "Widget"

    def _indent_multiline(self, text: str, spaces: int) -> str:
        """Indent multiline text."""
        indent = " " * spaces
        lines = text.split("\n")
        return "\n".join(indent + line if line else line for line in lines)
