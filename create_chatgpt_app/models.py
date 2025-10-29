"""Data models for ChatGPT App Scaffold."""

from dataclasses import dataclass, field
from typing import List, Literal


@dataclass
class WidgetConfig:
    """Configuration for a widget."""

    identifier: str
    title: str
    widget_type: Literal["cdn", "inline", "local"]
    template_uri: str
    invoking: str
    invoked: str
    response_text: str
    cdn_css: str = ""
    cdn_js: str = ""
    html_content: str = ""


@dataclass
class ProjectConfig:
    """Configuration for a project."""

    project_name: str
    app_name: str
    description: str
    port: int = 8000
    host: str = "0.0.0.0"
    widgets: List[WidgetConfig] = field(default_factory=list)
    include_docker: bool = True
    include_tests: bool = True
    python_version: str = "3.11"
