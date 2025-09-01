
- ALWAYS use `uv run` to activate python environment and call scripts
- NEVER run main.py without using `textual`

```bash
# run with live reload
textual run --dev main.py

# watch logs in second terminal
textual console

# take screenshot for debugging UI layout (saves as SVG)
# In the running app, press Ctrl+S to trigger action_screenshot()
# Or programmatically: app.save_screenshot(filename="debug.svg")
```

## Usage Examples:

```bash
# TUI Mode (default)
./main.py
./main.py --game-version gamepass

# CLI Mode (identical to original main.py)
./main.py create --preset ultra --read-only
./main.py show
./main.py backup
./main.py custom --section SystemSettings --setting "r.ViewDistance" "1.5"
./main.py readonly on

# CLI Mode with TUI enhancements
./main.py create --preset soft_ambient --game-version gamepass
./main.py --game-version gamepass show
```

- 3 unit height is necessary for performance preset button text to be visible

## Debugging TUI Layout

For layout optimization and debugging:

1. **Running in background**: Use `uv run textual run --dev main.py &` to run in background
2. **Screenshots**: Press Ctrl+S in running app or use `app.save_screenshot()` method (saves SVG format)
3. **Terminal output inspection**: Use BashOutput tool to capture terminal ANSI output for layout analysis
3. **Layout optimization**: Focus on reducing padding/margins while maintaining 3-unit button heights
4. **Screen space utilization**: Target 1080p screens - ensure advanced options visible without scrolling

Key layout elements:
- ConfigOption height: 1 (reduced from 2)
- Section padding: `0 1 0 1` (removed bottom padding)  
- Grid gutters: 0 (use margins instead)
- Button bar: Optimized spacing with individual button margins
