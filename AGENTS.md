# Project Overview

This project is a Sublime Text plugin named "Sublime Defold" that enhances the development workflow for the Defold game engine. The core feature of this plugin is "hot-reloading," which automatically updates the game running in the Defold editor whenever a file is saved in Sublime Text. This provides a real-time feedback loop for developers, allowing them to see their changes instantly without manual intervention.

The plugin is written in Python and integrates with Sublime Text's plugin API. It works by listening for file save events. When a file is saved, the plugin runs a shell command to discover the active Defold editor's port and then sends an HTTP POST request to the editor's hot-reload endpoint.

The project uses `ruff` for linting and code formatting, and `pyright` for static type checking to maintain code quality and consistency.

## Key Files

-   `defold-reload-on-save.py`: The main entry point of the plugin, containing the core hot-reload logic.
-   `pyproject.toml`: Defines the project's metadata, dependencies, and development tool configurations for `ruff` and `pyright`.
-   `README.md`: Provides a user-facing overview of the plugin, including installation and usage instructions.
-   `AGENTS.md`: Contains instructions for AI agents on how to interact with the codebase, including build, lint, and test commands.

# Build/Lint/Test Commands

-   **Lint**: `ruff check .`
-   **Type Check**: `pyright`
-   **Test**: No explicit test command found. New tests should use `pytest`. To run a single test, specify the file and test function: `pytest path/to/test_file.py::test_function_name`

# Code Style Guidelines

-   **Formatting**: Adhere to `ruff` formatting rules (line-length: 120, `target-version = 'py38'`).
-   **Imports**: Organize imports according to `ruff` conventions.
-   **Naming**: Follow Python's `PEP8` naming conventions.
-   **Error Handling**: Use explicit `try-except` blocks for error handling.
-   **Typing**: Utilize Python type hints where appropriate, enforced by `pyright` (configured with `pythonVersion = '3.8'` and `include = ["." , "./plugin"]`).