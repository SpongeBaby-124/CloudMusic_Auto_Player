# AGENTS.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.

## Project Overview

This is a NetEase Cloud Music MCP (Model Context Protocol) controller that provides global hotkey control, music search/playback, playlist management, daily recommendations, and roaming features. It's designed as an MCP server to integrate with MCP clients for music control automation.

## Development Commands

### Project Setup
```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies and create virtual environment
uv sync
```

### Run MCP Server
```bash
# Using uv
uv run src/server.py

# Or activate venv and run directly
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
python src/server.py

# Or use the installed script
uv run cloudmusic-mcp
```

### Development Tools
```bash
# Run code formatting
uv run black src/
uv run isort src/

# Run linting
uv run flake8 src/

# Run type checking
uv run mypy src/

# Run tests (when available)
uv run pytest
```

### Add New Dependencies
```bash
# Add runtime dependency
uv add package-name

# Add development dependency  
uv add --dev package-name

# Update dependencies
uv lock --upgrade
```

## Architecture

### Core Components
- **src/server.py**: Main MCP server entry point with FastMCP framework
- **src/controllers/**: Controller modules for different functionalities
  - `netease_controller.py`: Basic music control via global hotkeys and URL schemes
  - `daily_controller.py`: Daily recommendations and roaming via Selenium automation
- **src/utils/**: Utility modules
  - `config_manager.py`: Configuration file management
  - `music_search.py`: NetEase Music API integration for search functionality

### Configuration Files
- **src/config/hotkeys.json**: Platform-specific global hotkey configurations
- **netease_config.json**: NetEase Music client paths and browser automation settings
- **playlists.json**: System and user playlist configurations
- **config.json**: Example MCP client configuration

### Key Architecture Patterns
- **MCP Tool-based API**: All functionality exposed as MCP tools using FastMCP framework
- **Platform Detection**: Automatic Windows/Mac platform detection for hotkey mappings
- **URL Scheme Integration**: Uses `orpheus://` protocol for NetEase Music client control
- **Selenium Automation**: Browser automation for advanced features (daily recommendations, roaming)
- **Configuration Management**: JSON-based configuration with runtime modification support

### Dependencies
Project dependencies are managed via `pyproject.toml` and `uv`:

**Runtime Dependencies:**
- `fastmcp>=2.0.0`: MCP server framework
- `pyautogui>=0.9.54`: Global hotkey support (cross-platform)
- `pywin32>=306`: Windows system integration (Windows only)
- `psutil>=5.9.0`: Process management
- `selenium>=4.0.0`: Web automation for advanced features
- `requests>=2.28.0`: HTTP requests for NetEase API

**Development Dependencies:**
- `pytest>=7.0.0`: Testing framework
- `black>=23.0.0`: Code formatting
- `isort>=5.12.0`: Import sorting
- `flake8>=6.0.0`: Code linting
- `mypy>=1.0.0`: Type checking

### Platform Support
- Primary: Windows (full feature support)
- Secondary: Mac (basic hotkey support, limited Selenium features)
- ChromeDriver included for Windows in `src/chromedriver/win64/`

### Key Configuration Requirements
- NetEase Cloud Music client must be installed for URL scheme support
- For daily recommendations/roaming: NetEase Music client path must be configured via `set_netease_music_path()` tool
- ChromeDriver is pre-included for Windows automation features

### MCP Integration
- Designed to run as MCP server with client configuration in `config.json`
- All functionality exposed as MCP tools (launch, control_playback, search_and_play, etc.)
- Supports real-time configuration updates through MCP tools