# CLAUDE.md

This file gives Claude Code practical guidance for working in this repository. It is intended for maintainers and coding agents, not as end-user documentation.

## Project Overview

This project is a Python-based NetEase Cloud Music MCP controller. It exposes music automation features to MCP clients through FastMCP.

The project combines three main control paths:

- NetEase Cloud Music URL schemes such as `orpheus://` for launching the desktop client and playing songs or playlists.
- Global hotkeys through `pyautogui` for playback, track navigation, volume, lyrics, liking songs, and mini mode.
- Selenium automation against the NetEase Cloud Music desktop client running with a remote debugging port, used for daily recommendations and private roaming.

Windows is the primary target platform. macOS supports the basic hotkey and URL-scheme features, while daily recommendations and private roaming are Windows-oriented and may not work on macOS.

## Technology Stack

- Python: `>=3.10`
- Package manager: `uv`
- MCP framework: `fastmcp>=2.0.0`
- Desktop automation: `pyautogui`
- Windows integration: `pywin32`
- Process management: `psutil`
- Browser automation: `selenium`
- HTTP requests: `requests`

Dependency declarations live in [pyproject.toml](pyproject.toml). The resolved dependency lockfile is [uv.lock](uv.lock).

## Common Commands

### Set Up The Environment

```powershell
uv sync
```

Install development dependencies when needed:

```powershell
uv sync --extra dev
```

### Run The MCP Server

```powershell
uv run src/server.py
```

Or run the installed project script:

```powershell
uv run cloudmusic-auto-player
```

The script registered in [pyproject.toml](pyproject.toml) is `cloudmusic-auto-player`. Do not use the older name `cloudmusic-mcp`.

### Code Quality

```powershell
uv run black src/
uv run isort src/
uv run flake8 src/
uv run mypy src/
```

### Tests

```powershell
uv run pytest
```

At the time of writing, this repository may not contain a `tests/` directory. If no tests exist, `pytest` can fail because the configured test path is missing or because there are no collected tests. Add focused tests when changing core logic.

### Dependency Maintenance

```powershell
uv add <package-name>
uv add --dev <package-name>
uv lock --upgrade
```

## Repository Layout

```text
CloudMusic_Auto_Player/
├── src/
│   ├── server.py                     # FastMCP server entry point and MCP tool definitions
│   ├── controllers/
│   │   ├── netease_controller.py      # URL schemes, hotkeys, and window minimization
│   │   └── daily_controller.py        # Selenium automation for daily recommendations and roaming
│   ├── utils/
│   │   ├── config_manager.py          # Configuration loading, saving, and platform detection
│   │   └── music_search.py            # NetEase search API integration and play URL generation
│   ├── config/
│   │   ├── hotkeys.json               # Windows and macOS hotkey configuration
│   │   └── README.md                  # Hotkey configuration notes
│   └── chromedriver/
│       └── win64/chromedriver.exe     # Bundled Windows ChromeDriver
├── config.json                        # MCP client example or compatibility config
├── netease_config.json                # NetEase client path, debug port, and ChromeDriver path
├── playlists.json                     # System and user playlist configuration
├── pyproject.toml                     # Project metadata, dependencies, and tool config
├── PROJECT_STRUCTURE.md               # Architecture and structure notes
└── README.md                          # End-user documentation
```

## Core Modules

### [src/server.py](src/server.py)

`server.py` is the MCP-facing boundary. It is responsible for:

- Creating the `FastMCP("网易云音乐控制器")` server instance.
- Initializing `NeteaseMusicController`.
- Registering all MCP tools.
- Returning consistent dictionaries such as `{"success": ..., "data": ..., "message": ...}`.

Development guidance:

- Put business logic in `controllers/` or `utils/` first, then expose it through a thin MCP tool in `server.py`.
- Avoid adding complex Selenium, search, or configuration logic directly to `server.py`.
- Keep MCP tool responses structured. Failure paths should include a clear `error` or `message`.

### [src/controllers/netease_controller.py](src/controllers/netease_controller.py)

This module handles basic desktop-client control:

- `launch_by_url_scheme()` tries `os.startfile`, `subprocess`, and `webbrowser` to open NetEase URL schemes.
- `send_global_hotkey()` sends configured hotkeys through `pyautogui.hotkey()`.
- `_minimize_netease_window()` uses `win32gui` on Windows to find and minimize NetEase Cloud Music windows.

Important notes:

- This code affects the real desktop session. Be careful when testing changes that send hotkeys.
- `pyautogui.FAILSAFE = False` is set, so shortcut changes should be reviewed carefully.
- `win32gui` is Windows-only. Do not assume window control is available on all platforms.

### [src/controllers/daily_controller.py](src/controllers/daily_controller.py)

This module handles advanced Selenium-based features:

- Starts NetEase Cloud Music with `--remote-debugging-port=<port>`.
- Connects ChromeDriver to that debugging port.
- Uses fixed XPath selectors and fallback selectors for daily recommendations and private roaming.

Risk areas:

- Selectors depend on the internal UI structure of the NetEase desktop client and can break after client updates.
- `kill_netease_processes()` terminates NetEase Cloud Music processes. Check call paths carefully before changing it.
- `subprocess.CREATE_NO_WINDOW` is Windows-specific. Cross-platform support needs explicit platform branching.
- Private roaming may depend on account login state, VIP status, and feature availability. Code alone cannot guarantee success.

### [src/utils/config_manager.py](src/utils/config_manager.py)

This module owns configuration file behavior:

- `src/config/hotkeys.json`: hotkey configuration.
- `playlists.json`: system and user playlist configuration.
- `netease_config.json`: NetEase client path, debug port, and ChromeDriver path.

Configuration precedence:

- `NETEASE_MUSIC_PATH` overrides `netease_config.json` field `netease_music_path`.
- `CHROMEDRIVER_PATH` overrides `netease_config.json` field `chromedriver_path`.
- Playlists are loaded from `playlists.json` first. `config.json` is only a backward-compatibility fallback.

Important notes:

- Read and write JSON files with `encoding="utf-8"`.
- Preserve `ensure_ascii=False` and indentation when saving JSON.
- `load_hotkeys_config()` merges `custom_hotkeys` over the platform defaults. Do not break this override behavior.

### [src/utils/music_search.py](src/utils/music_search.py)

This module handles NetEase search and play URL generation:

- `search_netease_music()` searches for a song.
- `search_netease_playlist()` searches for a playlist.
- `generate_play_url()` creates a song play URL.
- `generate_playlist_play_url()` creates a playlist play URL.

Important notes:

- The search code uses the older endpoint `http://music.163.com/api/search/get/web`, which may be affected by network issues, rate limiting, or upstream changes.
- Request timeout is currently 10 seconds. Do not introduce unbounded waits.
- Play commands are compact JSON encoded with Base64 and wrapped in `orpheus://`. Validate client compatibility before changing the format.

## MCP Tools

The main tools exposed by `server.py` are:

- `launch_netease_music(minimize_window=True)`: launch NetEase Cloud Music.
- `control_playback(action="play_pause")`: play/pause, previous track, or next track.
- `control_volume(action="volume_up")`: volume up or down.
- `toggle_mini_mode()`: toggle mini mode.
- `toggle_lyrics()`: toggle lyrics display.
- `like_current_song()`: like the current song.
- `search_and_play(query, minimize_window=True)`: search for and play a song.
- `search_and_play_playlist(query="", playlist_name="", minimize_window=True)`: search for a playlist or play a configured playlist.
- `manage_custom_playlists(action, playlist_name, playlist_id, description)`: list, add, or remove custom playlists.
- `get_controller_info()`: inspect controller capabilities and configuration.
- `get_netease_config()`: check NetEase client path, ChromeDriver path, Selenium availability, and readiness.
- `play_daily_recommend()`: play daily recommendations.
- `play_roaming()`: start private roaming.

When adding an MCP tool:

- Use type annotations and a clear docstring.
- Validate enum-like parameters explicitly.
- Return `success: True` on success and `success: False` on failure.
- Include `platform` in returned data when platform differences matter.

## Configuration Files

### Hotkeys

File: [src/config/hotkeys.json](src/config/hotkeys.json)

Maintenance rules:

- Platform defaults live under `hotkeys.windows` and `hotkeys.mac`.
- User overrides live under `custom_hotkeys`.
- Hotkey strings must use the `+`-separated format accepted by `pyautogui.hotkey()`, for example `ctrl+alt+p`.

### NetEase Client Configuration

File: [netease_config.json](netease_config.json)

Key fields:

- `netease_music_path`: full path to the NetEase Cloud Music executable.
- `debug_port`: remote debugging port, default `9222`.
- `chromedriver_path`: ChromeDriver path, either absolute or relative to the project root.

Debugging guidance:

- For advanced feature failures, call `get_netease_config()` first to check paths and Selenium readiness.
- If the debug port is occupied, change `debug_port`, then restart both the MCP server and NetEase Cloud Music.

### Playlists

File: [playlists.json](playlists.json)

Structure:

- `systemPlaylists`: built-in playlists and charts. Normal remove operations should not delete these.
- `userPlaylists`: user-defined playlists, managed by `manage_custom_playlists()`.

Only store playlist IDs and metadata. Do not store full playlist contents in the repository.

## Development Conventions

- Keep this guidance file and developer-facing docs in English.
- Preserve existing module boundaries: MCP API in `server.py`, desktop control in `controllers/`, shared utilities in `utils/`.
- Avoid large new dependencies. If a dependency is necessary, add it with `uv add` and document why.
- Use the existing `logging.getLogger(__name__)` pattern.
- Always account for platform differences in desktop, process, and window-control code.
- Do not hardcode user-specific local paths. Prefer environment variables or JSON configuration.
- When changing configuration defaults, update both `README.md` and this file when relevant.
- Preserve existing user-facing Chinese strings unless the requested change is specifically about copy or localization.

## Testing And Verification

Choose verification based on the change:

- Configuration load/save logic: add unit tests for missing files, missing fields, malformed values, and environment-variable overrides.
- URL generation logic: test that Base64-decoded payloads match the expected JSON command shape.
- MCP tool validation: test invalid `action`, empty playlist names, empty search terms, and other failure branches.
- Selenium features: prefer manual verification with detailed logs; use mocked WebDriver objects for automated tests where possible.
- Desktop hotkeys: verify manually on a real Windows environment and avoid disrupting the user's current active window.

Recommended pre-submit checks:

```powershell
uv run black src/
uv run isort src/
uv run flake8 src/
uv run mypy src/
uv run pytest
```

If a command cannot run because of local environment limits or missing tests, state that clearly in the final handoff.

## Troubleshooting

### Hotkeys Do Not Work

Check in this order:

1. Confirm `pyautogui` is installed.
2. Confirm the matching global hotkeys are enabled inside NetEase Cloud Music.
3. Confirm the current platform section in `src/config/hotkeys.json` is correct.
4. Check whether another application has captured the same shortcuts.

### Search Or Playback Fails

Check in this order:

1. Confirm the network can reach `music.163.com`.
2. Use a more specific search query.
3. Confirm generated `orpheus://` URLs are handled by the desktop client.
4. Confirm the installed NetEase Cloud Music client is the desktop version and supports the URL scheme.

### Daily Recommendations Or Private Roaming Fails

Check in this order:

1. Call `get_netease_config()` and inspect path, driver, Selenium, and readiness status.
2. Confirm NetEase Cloud Music is logged in.
3. Confirm the ChromeDriver path exists and is compatible with the embedded browser/client environment.
4. Check whether fixed XPath selectors broke after a NetEase client update.
5. For private roaming, confirm account permissions and VIP status.

## Architecture Improvement Ideas

If the project continues to grow, prioritize these improvements:

- Add focused tests around MCP tool behavior in `server.py`.
- Introduce a lightweight response helper to reduce duplicated success and failure dictionaries.
- Centralize Selenium selector configuration or add a client-version adapter layer.
- Improve error classification in `music_search.py`, separating network errors, rate limiting, no results, and parse failures.
- Separate Windows-only behavior from cross-platform logic more clearly before expanding macOS support.
