# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Architecture Overview

This is a Clair Obscur: Expedition 33 configuration manager with a dual-interface architecture:
- **Backend**: `core/backend.py` contains `ClairObscurConfig` class handling all game configuration logic
- **Frontend**: `core/frontend.py` contains Textual TUI implementation with UI components
- **Entry Point**: `main.py` provides both TUI and CLI modes with argument parsing

### Core Components

- **ClairObscurConfig** (backend): Manages Engine.ini files, presets, backups, and custom settings
- **ClairConfigTUI** (frontend): Main Textual app with sections for game version, graphics presets, and advanced options
- **Configuration**: `config.toml` defines performance presets and engine tweaks for the Unreal Engine game

### Game Support

Supports both Steam and GamePass versions with different file paths defined in `config.toml`. The tool creates and manages Engine.ini configuration files in the appropriate game directories.

## Development Commands

### Environment Setup
```bash
# Use uv for all Python operations
uv run <command>
```

### Running the Application
```bash
# TUI Mode (default) - ALWAYS use textual for development
uv run textual run --dev --no-mouse main.py

# Watch logs in separate terminal
uv run textual console

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

### TUI Development and Debugging

- **Screenshots**: Press Ctrl+S in running app or use `app.save_screenshot()` method (saves SVG format)
- **Layout Requirements**: 3-unit button height necessary for performance preset button text visibility
- **Target Resolution**: Optimized for 1080p screens - advanced options should be visible without scrolling

Key UI constraints:
- ConfigOption height: 1 (reduced from 2)
- Section padding: `0 1 0 1` (removed bottom padding)  
- Grid gutters: 0 (use margins instead)
- Button bar: Individual button margins for optimal spacing

## Configuration Structure

The `config.toml` file defines:
- **Paths**: Steam and GamePass directory locations
- **Presets**: Performance configurations (low, balanced, ultra, sharp_clear, soft_ambient)
- **Engine Tweaks**: Unreal Engine settings for frame rate, networking, and rendering

## Separation of Concerns

The codebase maintains strict separation:
- Backend handles all file operations, configuration parsing, and game logic
- Frontend only manages UI state and user interactions
- CLI and TUI modes share the same backend implementation

## Project Status

Active development focuses on:
- TUI layout optimization for better space utilization
- Potential migration to Flet framework for cross-platform GUI
- Backend refactoring to reduce complexity (currently 782 LOC target < 500 LOC)