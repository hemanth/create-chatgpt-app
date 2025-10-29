# ChatGPT App Scaffold

A powerful CLI tool to quickly scaffold ChatGPT apps using the OpenAI Apps SDK and Model Context Protocol (MCP).

## Features

- 🚀 **Quick Start**: Generate a complete ChatGPT app in seconds
- 🎨 **Widget Templates**: Support for CDN, inline, and local widget types
- 🔧 **Extensible**: Easy to add new widgets and tools
- 🐳 **Docker Ready**: Includes Dockerfile and Docker configuration
- ✅ **Testing**: Pre-configured test structure with pytest
- 📚 **Well Documented**: Comprehensive README and inline documentation
- 🎯 **Interactive CLI**: Friendly prompts guide you through setup

## Installation

### From Source

```bash
git clone https://github.com/openai/openai-apps-sdk-examples.git
cd openai-apps-sdk-examples/create-chatgpt-app
pip install -e .
```

### From PyPI (Coming Soon)

```bash
pip install create-chatgpt-app
```

## Quick Start

### Create a New Project

```bash
create-chatgpt-app init my-awesome-app
```

This will:
1. Create a new directory with your project
2. Generate all necessary files (main.py, requirements.txt, Dockerfile, etc.)
3. Set up a basic widget
4. Provide next steps to get started

### Interactive Mode

Run without arguments for an interactive experience:

```bash
create-chatgpt-app init
```

You'll be prompted for:
- Project name
- App description
- Initial widget configuration
- Port and host settings

## Usage

### Initialize a New Project

```bash
# Basic usage
create-chatgpt-app init my-app

# With options
create-chatgpt-app init my-app --name "My App" --description "My awesome ChatGPT app"

# Custom port and host
create-chatgpt-app init my-app --port 3000 --host localhost

# Skip Docker files
create-chatgpt-app init my-app --no-docker

# Skip test files
create-chatgpt-app init my-app --no-tests
```

### Add a Widget

Navigate to your project directory and add widgets:

```bash
cd my-app

# Interactive mode
create-chatgpt-app add-widget

# With options
create-chatgpt-app add-widget --identifier my-widget --title "My Widget" --type inline
```

#### Widget Types

1. **CDN**: Load widget from external CDN
   ```bash
   create-chatgpt-app add-widget --type cdn
   ```

2. **Inline**: Simple HTML inline widget
   ```bash
   create-chatgpt-app add-widget --type inline
   ```

3. **Local**: Load from local static files
   ```bash
   create-chatgpt-app add-widget --type local
   ```

### Add a Tool

```bash
# Interactive mode
create-chatgpt-app add-tool

# With options
create-chatgpt-app add-tool --identifier my-tool --title "My Tool"

# Tool without widget
create-chatgpt-app add-tool --identifier data-processor --no-widget
```

### List Available Templates

```bash
create-chatgpt-app list-templates
```

## Project Structure

After running `create-chatgpt-app init my-app`, you'll get:

```
my-app/
├── main.py              # Main MCP server implementation
├── requirements.txt     # Python dependencies
├── README.md           # Project documentation
├── .gitignore          # Git ignore patterns
├── Dockerfile          # Docker configuration
├── .dockerignore       # Docker ignore patterns
└── tests/              # Test directory
    ├── __init__.py
    └── test_main.py    # Unit tests
```

## Example: Complete Workflow

```bash
# 1. Create a new project
create-chatgpt-app init pizza-finder

# 2. Navigate to the project
cd pizza-finder

# 3. Set up virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Add more widgets
create-chatgpt-app add-widget --identifier pizza-map --title "Pizza Map" --type cdn

# 6. Run the server
python main.py

# 7. Test with MCP Inspector
npm install -g @modelcontextprotocol/inspector
mcp-inspector
# Connect to http://localhost:8000/mcp
```

## Generated Code Structure

### Main Components

The generated `main.py` includes:

1. **Widget Definitions**: Data structures for your widgets
2. **MCP Protocol Handlers**:
   - `list_tools()`: Register available tools
   - `list_resources()`: Expose widgets as resources
   - `list_resource_templates()`: Define resource templates
   - `_handle_read_resource()`: Serve widget HTML
   - `_call_tool_request()`: Execute tool logic
3. **Input Validation**: Pydantic models for type-safe inputs
4. **FastAPI App**: HTTP/SSE transport layer
5. **CORS Configuration**: For local development

### Customization Points

Edit the generated `main.py` to:

1. **Add Business Logic**: Implement your tool's functionality in `_call_tool_request()`
2. **Modify Input Schema**: Update `ToolInput` class and `TOOL_INPUT_SCHEMA`
3. **Customize Widgets**: Edit widget HTML, CSS, and JavaScript
4. **Add Middleware**: Include authentication, rate limiting, etc.
5. **Connect to Services**: Add database, API calls, file processing

## Widget Development

### CDN Widget Example

```python
AppWidget(
    identifier="my-dashboard",
    title="Analytics Dashboard",
    template_uri="ui://widget/dashboard.html",
    invoking="Loading dashboard",
    invoked="Dashboard loaded",
    html=(
        "<div id=\"dashboard-root\"></div>\n"
        "<link rel=\"stylesheet\" href=\"https://cdn.example.com/dashboard.css\">\n"
        "<script type=\"module\" src=\"https://cdn.example.com/dashboard.js\"></script>"
    ),
    response_text="Dashboard rendered successfully!",
)
```

### Inline Widget Example

```python
AppWidget(
    identifier="simple-card",
    title="Info Card",
    template_uri="ui://widget/card.html",
    invoking="Creating card",
    invoked="Card created",
    html=(
        "<div style='padding: 20px; border: 1px solid #ccc; border-radius: 8px;'>"
        "  <h2>Hello from MCP!</h2>"
        "  <p>This is a simple inline widget.</p>"
        "</div>"
    ),
    response_text="Info card displayed",
)
```

### Local Widget Example

```python
AppWidget(
    identifier="custom-widget",
    title="Custom Widget",
    template_uri="ui://widget/custom.html",
    invoking="Loading widget",
    invoked="Widget loaded",
    html=(
        "<div id=\"custom-root\"></div>\n"
        "<link rel=\"stylesheet\" href=\"/static/custom.css\">\n"
        "<script type=\"module\" src=\"/static/custom.js\"></script>"
    ),
    response_text="Custom widget rendered!",
)
```

## Testing

The generated project includes a test structure:

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest

# Run with coverage
pip install pytest-cov
pytest --cov=. --cov-report=html
```

## Docker Support

### Build and Run

```bash
# Build the image
docker build -t my-app .

# Run the container
docker run -p 8000:8000 my-app

# Run with environment variables
docker run -p 8000:8000 -e PORT=3000 my-app
```

### Docker Compose

Create a `docker-compose.yml`:

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - PORT=8000
      - HOST=0.0.0.0
    restart: unless-stopped
```

Run with:

```bash
docker-compose up
```

## Advanced Usage

### Custom Input Schema

Edit your `ToolInput` class to add custom fields:

```python
class ToolInput(BaseModel):
    """Schema for tool inputs."""

    user_query: str = Field(
        ...,
        alias="userQuery",
        description="The user's input query",
    )

    # Add custom fields
    max_results: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Maximum number of results"
    )

    category: str = Field(
        default="all",
        description="Filter by category"
    )

    model_config = ConfigDict(populate_by_name=True, extra="forbid")
```

### Adding Database Support

```python
import asyncpg

# Initialize DB pool
DB_POOL = None

async def get_db_pool():
    global DB_POOL
    if DB_POOL is None:
        DB_POOL = await asyncpg.create_pool(
            "postgresql://user:pass@localhost/dbname"
        )
    return DB_POOL

# Use in tool handler
async def _call_tool_request(req: types.CallToolRequest) -> types.ServerResult:
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        results = await conn.fetch("SELECT * FROM items WHERE ...")
    # Process results...
```

### External API Integration

```python
import httpx

async def _call_tool_request(req: types.CallToolRequest) -> types.ServerResult:
    payload = ToolInput.model_validate(req.params.arguments or {})

    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.example.com/search",
            params={"q": payload.user_query}
        )
        api_data = response.json()

    # Return with widget...
```

## Troubleshooting

### Widget Not Rendering

Check:
1. `template_uri` matches between widget and metadata
2. HTML is valid and includes root element
3. External CSS/JS URLs are accessible (for CDN widgets)
4. MIME type is `text/html+skybridge`
5. Metadata includes `openai/widgetAccessible: true`

### Input Validation Errors

Verify:
1. Field names match between schema and Pydantic model
2. Required fields are marked correctly
3. Test validation independently:

```python
from main import ToolInput

test_input = {"userQuery": "test"}
result = ToolInput.model_validate(test_input)
print(result)
```

### Server Won't Start

Check:
1. Port is not already in use: `lsof -i :8000` (macOS/Linux)
2. All dependencies are installed: `pip list`
3. Virtual environment is activated
4. Python version is 3.10+: `python --version`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Resources

- [OpenAI Apps SDK Examples](https://github.com/openai/openai-apps-sdk-examples)
- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [MCP Inspector](https://github.com/modelcontextprotocol/inspector)

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- Open an issue on [GitHub](https://github.com/openai/openai-apps-sdk-examples/issues)
- Check the [HOWTO guide](./pizzaz_server_python/HOWTO.md)
- Review [example projects](https://github.com/openai/openai-apps-sdk-examples)

---

Made with ❤️ for the ChatGPT developer community
