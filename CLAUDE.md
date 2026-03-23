# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`relative-position` is a Python library for positioning UI elements relative to window coordinates on Linux (X11/Wayland) and Windows platforms. The library provides programmatic element definition using Python classes rather than configuration files.

## Quick Commands

```bash
# Install dependencies
pip install -e .

# Run example scripts
python example_simple_api.py
python example_ele.py

# Build package (uses hatchling)
pip install build
python -m build
```

## Architecture

### Platform Detection
- `relative_position/config.py` automatically detects platform (Windows/X11/Wayland)
- Global constants: `IS_WINDOWS`, `IS_X11`, `IS_WAYLAND`
- Detection based on `sys.platform` and `XDG_SESSION_TYPE` environment variable

### Core Classes (Simplified API)

**Public API**: Only exports `Direction`, `Ele`, `App`, and `Mouse`. Other utilities are available internally but not exported.

- **Direction** (`relative_position/elements.py`): Enum for element reference point directions
  - `LEFT_TOP`, `RIGHT_TOP`, `LEFT_BOTTOM`, `RIGHT_BOTTOM`
  - `TOP_CENTER`, `BOTTOM_CENTER`, `LEFT_CENTER`, `RIGHT_CENTER`
  - `WINDOW_SIZE`

- **App** (`relative_position/app.py`): Main interface for UI operations
  - `Ele(direction, location, name=None)`: Create and register elements
  - `get_center(element)`: Get element center coordinates
  - `focus_window()`, `window_size()`, `window_center()`, etc.

- **Ele** (`relative_position/elements.py`): Element definition with mouse operations
  - `center()`, `click()`, `right_click()`, `double_click()`, `hover()`
  - Must be associated with an App instance (via constructor or `set_app()`)

- **Mouse** (`relative_position/app.py`): Cross-platform mouse operations using pyautogui
  - `move_to(x, y)`, `click(button='left', clicks=1)`, `double_click()`

- **Elements** (`relative_position/elements.py`): Collection of Ele objects
  - Dictionary-like interface for managing multiple elements

### Platform Implementation Pattern

#### Linux Platform
- **Base Class**: `RelativePositionBase` (`relative_position/linux/base.py`) - Abstract interface
  - Defines abstract methods for window operations and element positioning
  - Implements common logic for positioning calculations

- **Implementation**: `RelativePosition` (`relative_position/linux/main.py`) - Concrete class
  - Handles both X11 and Wayland display servers
  - Dynamically selects window provider based on platform detection

- **Window Providers** (implement `WindowInfoProvider` ABC):
  - `X11WindowInfo`: Uses `xdotool` and `xwininfo` commands
  - `WaylandWindowInfo`: Uses D-Bus APIs (Deepin-specific)

#### Windows Platform
- **Implementation**: `RelativePosition` (`relative_position/windows/main.py`)
- **Window Provider**: `WindowsWindowInfo` uses Windows API via `ctypes`
- **Dependencies**: `psutil` for process management

### Element Positioning System

Elements are positioned relative to window reference points using 9 directions defined in `Direction` enum:

**Corner References**: `LEFT_TOP`, `RIGHT_TOP`, `LEFT_BOTTOM`, `RIGHT_BOTTOM`
**Center References**: `TOP_CENTER`, `BOTTOM_CENTER`, `LEFT_CENTER`, `RIGHT_CENTER`
**Full Window**: `WINDOW_SIZE`

Each element definition:
```python
Ele(
    direction=Direction.LEFT_TOP,      # Reference point
    location=[20, 20, 50, 35]  # [x, y, width, height]
)

# Or using string (backward compatible)
Ele(
    direction="left_top",
    location=[20, 20, 50, 35]
)
```

Positioning logic calculates absolute screen coordinates based on:
1. Get window position/size from window provider
2. Apply element offset based on reference direction
3. Return center coordinates or bounding box

### Configuration System

The library uses programmatic configuration (no INI file support):

**Supported Config Types**:
- `Ele` object: Single element
- `Elements` object: Collection of elements
- `dict`: Dictionary of `{name: {direction, location}}`

**Config Parsing**: Both `RelativePosition` classes (`_parse_config()`) convert these to internal dictionary format.

### Design Patterns

- **Factory Pattern**: Window provider selected at runtime based on platform
- **Inheritance**: Platform implementations share common base class (`RelativePositionBase`)
- **Dependency Injection**: Elements accept App instance for coordinate calculations
- **Late Binding**: Window provider selected at runtime based on platform
- **Enum Pattern**: `Direction` enum provides type safety and IDE auto-completion

## Platform-Specific Notes

### Windows
- Uses Windows API (`user32.dll`) via `ctypes`
- Mouse operations via `pyautogui` (cross-platform)
- Shortcut key support (`ESC`, etc.) via `ShortCut` class
- `focus_windows()` works; Wayland focus_windows() is no-op

### Linux - X11
- Requires: `xdotool`, `xwininfo` system packages
- Stable implementation, widely tested

### Linux - Wayland
- Requires: D-Bus, `dbus-python` library
- Deepin-specific D-Bus APIs for window management
- May require platform-specific adjustments for other Wayland compositors

## Module Structure

```
relative_position/
├── __init__.py              # Exports Direction, Ele, App, Mouse (simplified API)
├── config.py               # Platform detection
├── app.py                 # App, Mouse classes
├── elements.py            # Ele, Elements, Direction classes
├── exceptions.py          # Custom exceptions
├── utils.py              # Logger, CmdCtl, ShortCut utilities
├── linux/
│   ├── base.py           # RelativePositionBase, WindowInfoProvider ABCs
│   ├── main.py           # Linux RelativePosition implementation
│   ├── x11_wininfo.py   # X11 window provider
│   └── wayland_wininfo.py # Wayland window provider
└── windows/
    ├── main.py           # Windows RelativePosition implementation
    └── windows_wininfo.py # Windows window provider
```

## Testing

- `example_simple_api.py`: Demonstrates the simplified API with `App` and `Direction` enum
- `example_ele.py`: Demonstrates `Ele` and `Elements` classes
- For manual testing, use: `python -c "from relative_position import Ele, App, Direction; print('Works!')"`

## Important Design Decisions

1. **Programmatic over Configuration**: Elements defined as Python objects, not INI files
2. **Platform Abstraction**: Common interface with platform-specific implementations
3. **Auto-Detection**: Platform detected automatically at runtime
4. **Simple API Top**: User-facing API (App, Ele, Direction) hides complexity
5. **Enum-based Directions**: `Direction` enum provides type safety and IDE support
6. **Cross-platform Mouse**: `pyautogui` used for consistent mouse operations across platforms
7. **Class Renaming**: `ButtonCenter` renamed to `RelativePosition` for clarity
8. **No config_path**: Removed deprecated config_path parameter, only supports Elements and dict configs
