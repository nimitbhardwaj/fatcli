# Agent Guidelines for fatsecret-hand

## Project Overview

This is a Python CLI application using `uv` as the package manager. Python 3.12+ is required. Uses `src/` layout.

## Commands

### Setup & Installation
```bash
# Install dependencies
uv sync

# Add a dependency
uv add <package>

# Add a dev dependency
uv add --dev <package>

# Remove a dependency
uv remove <package>

# Update lock file
uv lock
```

### Running the Application
```bash
# Run the CLI
uv run fatcli

# Or install and run
uv pip install -e .
fatcli
```

### Code Quality

```bash
# Format code (ruff)
uv run ruff format .

# Lint code (ruff)
uv run ruff check .

# Fix linting issues automatically
uv run ruff check --fix .

# Type check (mypy)
uv run mypy .

# Run all checks
uv run ruff format . && uv run ruff check . && uv run mypy .
```

### Testing

```bash
# Run all tests
uv run pytest

# Run a single test file
uv run pytest tests/test_main.py

# Run a single test function
uv run pytest tests/test_main.py::test_function_name

# Run tests matching a pattern
uv run pytest -k "test_pattern"

# Run with verbose output
uv run pytest -v

# Run with coverage
uv run pytest --cov=fatsecret_hand --cov-report=term-missing
```

## Code Style Guidelines

### General
- 4-space indentation (no tabs)
- Maximum line length: 88 characters (ruff default)
- Use `uv` for ALL package management - never use `pip` directly
- All code must be type-annotated

### Imports
- Use absolute imports when possible (`from fatcli import module`)
- Group imports in order: stdlib, third-party, first-party, local-folder
- Within each group, sort alphabetically

```python
import sys
from pathlib import Path
from typing import Any

from rich.console import Console

from fatcli import MyClass
```

### Naming Conventions
- **Modules**: lowercase_with_underscores (`my_module.py`)
- **Classes**: PascalCase (`MyClass`)
- **Functions/Variables**: snake_case (`my_function`, `my_variable`)
- **Constants**: UPPER_SNAKE_CASE (`MY_CONSTANT`)
- **Type aliases**: PascalCase (e.g., `MyType = dict[str, Any]`)
- **Private members**: prefix with `_` (`_private_method`)
- **File-private**: prefix with `_` (`_private_module.py`)

### Type Annotations
- Always use type hints for function parameters and return values
- Use `Any` sparingly - prefer Union types when possible
- Use `Optional[X]` over `X | None`
- Use `Sequence[T]` over `List[T]` for read-only parameters

```python
def process_items(items: list[str], options: dict[str, Any] | None = None) -> dict[str, int]:
    ...
```

### Error Handling
- Use specific exception types - never catch bare `Exception`
- Let exceptions propagate when appropriate; only catch what you can handle
- Always include context in exception messages
- Use `raise ... from ...` when chaining exceptions

```python
try:
    result = risky_operation()
except ValueError as e:
    raise ConfigurationError(f"Invalid config: {e}") from e
```

### CLI Application Structure
- Use `typer` for CLI argument parsing
- Always include a callback (`@app.callback()`) to ensure subcommands work correctly
- Define a `main()` function that calls `typer_main.get_command(app)` then `app()`
- Keep business logic separate from CLI layer

```python
import typer
from typer import main as typer_main

app = typer.Typer()

@app.callback()
def callback() -> None:
    """CLI help text."""
    pass

@app.command()
def mycommand() -> None:
    """My command help."""
    ...

def main() -> None:
    typer_main.get_command(app)
    app()
```

### Async Code
- Use `async def` for async functions
- Use `uv.run()` for running async code from sync context
- Always handle `asyncio.CancelledError` gracefully in long-running tasks

## Project Structure

```
fatsecret-hand/
├── src/
│   └── fatcli/
│       ├── __init__.py           # Shared utilities (get_fatsecret, console, SESSION_FILE)
│       ├── main.py               # CLI entry point, command registration
│       └── commands/
│           ├── __init__.py       # Empty, for package discovery
│           ├── init.py           # init command
│           └── meals.py          # meals command
├── tests/                    # Test files
├── pyproject.toml            # Project configuration
├── .python-version           # Python version specification
├── .env                      # Environment variables (not committed)
└── AGENTS.md                 # This file
```

## Configuration

This project uses:
- **ruff** for formatting and linting
- **mypy** for type checking
- **pytest** for testing

Environment variables are loaded from `.env` file using `python-dotenv`. Required variables:
- `FATSECRET_CONSUMER_KEY` - Fatsecret API consumer key
- `FATSECRET_CONSUMER_SECRET` - Fatsecret API consumer secret

Ensure all code passes before committing.

## Dependencies

When adding dependencies:
1. Use `uv add <package>` for runtime dependencies
2. Use `uv add --dev <package>` for development dependencies (testing, linting)
3. Never commit `uv.lock` if it exists
