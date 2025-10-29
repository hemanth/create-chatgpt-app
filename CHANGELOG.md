# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-10-29

### Added
- Initial release of create-chatgpt-app
- CLI tool to scaffold ChatGPT apps using OpenAI Apps SDK
- `init` command to create new projects
- `add-widget` command to add widgets to existing projects
- `add-tool` command to add tools to existing projects
- `list-templates` command to show available templates
- Support for three widget types: CDN, inline, and local
- Interactive prompts for project configuration
- Automatic generation of:
  - main.py with MCP server implementation
  - requirements.txt with dependencies
  - README.md with documentation
  - Dockerfile for containerization
  - .gitignore and .dockerignore
  - Test structure with pytest
- Jinja2 templates for all generated files
- Rich CLI interface with colored output
- Input validation using Pydantic

### Changed
- Package renamed from `chatgpt-app-scaffold` to `create-chatgpt-app`
- CLI command renamed from `chatgpt-scaffold` to `create-chatgpt-app`
- Copyright updated to Hemanth HM <hemanth.hm@gmail.com>

[0.1.0]: https://github.com/openai/openai-apps-sdk-examples/releases/tag/v0.1.0
