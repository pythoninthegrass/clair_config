# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Architecture Overview

This is a Clair Obscur: Expedition 33 configuration manager with a modern GUI architecture:
- **Backend**: `core/backend.py` contains `ClairObscurConfig` class handling all game configuration logic
- **Frontend**: `core/frontend.py` contains Flet GUI implementation with cross-platform UI components
- **Entry Point**: `main.py` provides both GUI and CLI modes with argument parsing

### Core Components

- **ClairObscurConfig** (backend): Manages Engine.ini files, presets, backups, and custom settings
- **ClairConfigFlet** (frontend): Main Flet app with sections for game version, graphics presets, and advanced options
- **ThemeConfig** (frontend): Attrs-based theme configuration with decouple integration for environment-based settings
- **Configuration**: `config.toml` defines performance presets and engine tweaks for the Unreal Engine game

### Game Support

Supports both Steam and GamePass versions with different file paths defined in `config.toml`. The tool creates and manages Engine.ini configuration files in the appropriate game directories.

## Development Commands

### Environment Setup
```bash
# Use uv for all Python operations
uv run <command>
```

### Screenshots

Use `screencap` (`sc`) on macOS (darwin) to take screenshots of the gui window

```bash
λ screencap --auto Flet ~/Desktop/flet_$(date +%Y%m%d_%H%M%S).png
=== Checking windows for "Flet" ===
Trying application name: "Flet"
Found windows:
"Clair Obscur: Expedition 33 - Unreal Config v2.0" size=1185x1127 id=88196
Found windows for "Flet"

Window title: Clair Obscur: Expedition 33 - Unreal Config v2.0
Capturing screenshot of window 88196 from Flet...
Screenshot saved to: /Users/lance/Desktop/flet_20250831_225022.png
```

### Running the Application
```bash
# GUI Mode (default) - Flet cross-platform interface
uv run main.py

# CLI Mode examples
./main.py create --preset ultra --read-only
./main.py show
./main.py backup
./main.py custom --section SystemSettings --setting "r.ViewDistance" "1.5"
```

### Code Quality
```bash
# Format and lint
uv run ruff format .
uv run ruff check --fix .

# Pre-commit hooks (runs ruff automatically)
uv run pre-commit run --all-files
```

### Flet GUI Development and Features

- **Cross-Platform**: Runs on Windows, macOS, Linux as desktop app or web app
- **Game-Inspired Design**: Dark theme matching Clair Obscur's aesthetic with amber accent colors
- **Responsive Layout**: Two-column layout with game version/graphics on left, presets/advanced on right
- **Interactive Controls**: Dropdowns, sliders, switches, and color-coded preset buttons
- **Real-time Feedback**: Snackbar notifications for user actions and status updates

Key UI Features:
- Performance preset buttons with color coding (Low=Red, Balanced=Orange, Ultra=Green, etc.)
- Advanced options with sliders for precise control (View Distance, Sharpening, etc.)
- Game version radio buttons for Steam/GamePass selection
- Bottom action bar with Save, Reload, Launch, and Theme toggle buttons

## Configuration Structure

The `config.toml` file defines:
- **Paths**: Steam and GamePass directory locations
- **Presets**: Performance configurations (low, balanced, ultra, sharp_clear, soft_ambient)
- **Engine Tweaks**: Unreal Engine settings for frame rate, networking, and rendering

## Separation of Concerns

The codebase maintains strict separation:
- Backend handles all file operations, configuration parsing, and game logic
- Frontend only manages UI state and user interactions
- CLI and GUI modes share the same backend implementation

## Project Status

Completed migration to Flet framework ✅
- **Frontend**: Successfully migrated from Textual TUI to Flet GUI for cross-platform compatibility
- **UI Design**: Implemented game-inspired interface matching Clair Obscur's visual aesthetic
- **Functionality**: Maintained 100% feature parity with original TUI implementation

Active development focuses on:
- Backend refactoring to reduce complexity (currently 782 LOC target < 500 LOC)
- Enhanced preset management and configuration validation
- Progressive Web App (PWA) capabilities for web deployment

## Context

- Context7 mcp libraries
  - astral-sh/uv
  - astral-sh/ruff
  - flet-dev/flet
  - taskfile_dev
