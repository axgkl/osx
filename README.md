# OSX Automation

A sophisticated macOS automation system that integrates with **yabai** (tiling window manager) and **Lima** (Linux VMs) to create an advanced desktop management solution with a menu bar interface.

## Overview

This system provides:
- **Window Management**: Click-to-focus windows, auto-arrange apps to specific spaces
- **Space Navigation**: Visual space indicators with emoji numbers
- **VM Control**: Start/stop Lima VMs with Docker container management
- **System Controls**: Dark mode toggle, system sleep, yabai restart
- **App Icons**: Extracts and caches application icons for the menu

## Key Components

### 1. Event System
- **Event Listener** (`event_listener.py`): HTTP server that receives yabai events via curl
- **Event Handlers** (`events.py`): Processes yabai window manager events and manages app behavior
- Provides window switching, space management, and app arrangement
- Auto-arranges windows based on app specifications in `~/.config/yabai/spec.py`

### 2. Lima VM Management (`lima.py`)
- Manages Lima virtual machines from the menu bar
- Integrates Docker container management with real-time status
- Shows VM status, memory usage, and provides start/stop controls
- Handles Docker context switching between VMs

### 3. Architecture
- Uses **HTTP server** for real-time yabai event handling
- **RESTful API** endpoints for different event types
- **Menu bar app** for easy access to all controls
- **Automatic app arrangement** based on predefined rules

## File Structure

- `src/` - Source code directory
  - `event_listener.py` - HTTP server for yabai event handling
  - `events.py` - Event handlers and menu app building logic  
  - `lima.py` - Lima VM and Docker container management
  - `const.py` - Constants, menu app class, and shared state
  - `main.py` - Simple entry point (currently minimal)
- `test/` - Test scripts (see test/README.md for details)
- `~/.config/yabai/spec.py` - App arrangement configuration

## Setup

### Prerequisites

- **yabai**: Tiling window manager for macOS
- **Lima**: Linux virtual machines on macOS (optional)
- **Python 3.13+** with dependencies (see pyproject.toml)

### Environment Variable Setup (One-time)

The system uses `OSX_EVTS_PORT` environment variable set globally via macOS LaunchAgent:

#### LaunchAgent Configuration

The LaunchAgent is located at `~/Library/LaunchAgents/com.user.environment.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.user.environment</string>
    <key>ProgramArguments</key>
    <array>
        <string>sh</string>
        <string>-c</string>
        <string>
        launchctl setenv OSX_EVTS_PORT 10888
        </string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
```

#### Load and Start LaunchAgent

```bash
# Load the LaunchAgent (one-time setup)
launchctl load ~/Library/LaunchAgents/com.user.environment.plist

# Start it immediately
launchctl start com.user.environment

# Verify it's working
launchctl getenv OSX_EVTS_PORT  # Should show: 10888

# Check if it's running
launchctl list | grep com.user.environment
```

#### Managing the LaunchAgent

```bash
# Stop the LaunchAgent
launchctl stop com.user.environment

# Unload it (removes from startup)
launchctl unload ~/Library/LaunchAgents/com.user.environment.plist

# Reload after changes
launchctl unload ~/Library/LaunchAgents/com.user.environment.plist
launchctl load ~/Library/LaunchAgents/com.user.environment.plist
launchctl start com.user.environment
```

### Running the System

```bash
# Start the HTTP event listener (uses OSX_EVTS_PORT environment variable)
just start

# Or run directly with Python module
.venv/bin/python3 -m src.event_listener

# Or specify port explicitly  
.venv/bin/python3 -m src.event_listener 10888

# Configure yabai to send HTTP events
yabai -m signal --add event=space_changed action='curl -s "http://127.0.0.1:${OSX_EVTS_PORT:-10888}/evt/space_changed?space_id=$YABAI_SPACE_ID&space_index=$YABAI_SPACE_INDEX"'
yabai -m signal --add event=window_focused action='curl -s "http://127.0.0.1:${OSX_EVTS_PORT:-10888}/evt/window_focused?window_id=$YABAI_WINDOW_ID"'
yabai -m signal --add event=window_destroyed action='curl -s "http://127.0.0.1:${OSX_EVTS_PORT:-10888}/evt/window_destroyed?window_id=$YABAI_WINDOW_ID"'
```

The event listener will automatically:
- Use the `OSX_EVTS_PORT` environment variable if no port is specified
- Kill any existing event listener process before starting
- Create a PID file for process management

### Yabai Integration Details

#### Event Endpoints

The HTTP server provides these endpoints for yabai events:

- `GET /evt/space_changed?space_id=X&space_index=Y` - Space switching events
- `GET /evt/window_focused?window_id=X` - Window focus events  
- `GET /evt/window_destroyed?window_id=X` - Window destruction events
- `GET /evt/keyboard_event?key_code=X&key_char=Y&modifiers=Z` - Keyboard events from Hammerspoon

**Response Codes:**
- `200 OK` - Event handled successfully: `{"status": "ok", "event": "event_type"}`
- `404 Not Found` - Unsupported event type: `{"status": "error", "message": "Event type 'xyz' not supported"}`
- `404 Not Found` - Invalid endpoint: `{"status": "error", "message": "Invalid endpoint. Use /evt/{event_type}"}`
- `500 Internal Server Error` - Event handling failed: `{"status": "error", "message": "Event handling failed"}`

#### Manual Testing

You can test the system manually:

```bash
# Start the event listener
just test-server

# In another terminal, simulate events:
curl "http://127.0.0.1:10888/evt/space_changed?space_id=1&space_index=3"
curl "http://127.0.0.1:10888/evt/window_focused?window_id=123"
curl "http://127.0.0.1:10888/evt/keyboard_event?key_code=42&key_char=k&modifiers=cmd,ctrl"
```

#### Hammerspoon Integration

The keyboard event integration is implemented through a modular Hammerspoon configuration:

**File Structure:**
- `~/.hammerspoon/init.lua` - Main Hammerspoon configuration (cleaned up)
- `~/.hammerspoon/keyboard_events.lua` - Dedicated keyboard event module

**Features:**
- **Modular design** - Keyboard logic separated from main config
- **Automatic HTTP events** sent for every keystroke when logger is active
- **System events** for logger start/stop with menu bar indicators
- **Special combo detection** for Hammerspoon shortcuts (Cmd+Ctrl+R, Cmd+Ctrl+K)
- **Extensible API** - Easy to add custom keyboard event handling

**Usage:**
1. **Reload Hammerspoon**: `Cmd+Ctrl+R` (loads updated modular config)
2. **Start the event listener**: `.venv/bin/python3 event_listener.py`
3. **Toggle key logger**: `Cmd+Ctrl+K`
4. **Watch events** flow from Hammerspoon → HTTP → OSX automation system

**Menu Bar Indicators:**
- `🎹` - Keyboard logger is active in Hammerspoon
- `⌨️` - Recent keystroke with modifier keys detected
- No indicator - Logger stopped or no recent activity

**Module API:**
The keyboard_events module provides:
- `KeyboardEvents.setup(Bind, Notify)` - Initialize with main config functions
- `KeyboardEvents.isEnabled()` - Check logger status
- `KeyboardEvents.start()` / `KeyboardEvents.stop()` - Manual control
- `KeyboardEvents.sendEvent(code, char, mods)` - Send custom events

### Application Arrangement

Edit `~/.config/yabai/spec.py` to define which apps go to which spaces:

```python
arrange_spec = [
    [2, "term"],      # Terminal apps to space 2
    [4, "chrome"],    # Chrome to space 4
    [5, "zen"],       # Zen browser to space 5
    [8, "discor"],    # Discord to space 8
    [9, "mail"],      # Mail apps to space 9
    [7, "calend"],    # Calendar to space 7
    [1, ""],          # Default space 1
]
```

### Lima VM Integration (Optional)

The system integrates with Lima VMs for Docker container management:

- Shows VM status in menu bar
- Docker container controls
- Memory usage monitoring
- VM start/stop capabilities

Lima integration is optional and will be skipped if not available.

## Dependencies

This project requires:
- **yabai**: Tiling window manager for macOS
- **Lima**: Linux virtual machines on macOS (optional)
- **Python 3.13+** with dependencies:
  - `rumps` - Menu bar app framework
  - `docker` - Docker API client
  - `psutil` - System and process utilities
  - `humanize` - Human-readable data formatting
  - `requests` - HTTP client for testing

Install dependencies:
```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -r requirements.txt
```

## Troubleshooting

### Environment Variable Issues

If `OSX_EVTS_PORT` is not available:

```bash
# Check if LaunchAgent is loaded
launchctl list | grep com.user.environment

# Check if environment variable is set
launchctl getenv OSX_EVTS_PORT

# Reload LaunchAgent if needed
launchctl unload ~/Library/LaunchAgents/com.user.environment.plist
launchctl load ~/Library/LaunchAgents/com.user.environment.plist
launchctl start com.user.environment
```

### Port Conflicts

If port 10888 is in use:

```bash
# Check what's using the port
lsof -i :10888

# Change the port in LaunchAgent configuration
# Edit ~/Library/LaunchAgents/com.user.environment.plist
# Change OSX_EVTS_PORT value, then reload LaunchAgent
```

### HTTP Server Not Responding

```bash
# Test if server is running
curl -s "http://127.0.0.1:10888/evt/space_changed?space_id=1&space_index=2"

# Check for unsupported events (should return 404 with supported events list)
curl -s "http://127.0.0.1:10888/evt/invalid_event"

# Check server logs
tail -f /tmp/event-listener-*.log
```

### Menu Bar App Issues

If the menu bar app doesn't appear:

1. Ensure you're running in a GUI environment (not SSH/terminal-only)
2. Check macOS permissions for the app
3. Try running without Lima integration first
4. Check Console.app for error messages

## Development

### Adding New Features

1. **New Event Types**: Add handlers to `EventHandlers` class in `events.py`
2. **New HTTP Endpoints**: Extend `EventHTTPHandler` in `event_listener.py`
3. **New Menu Items**: Add to `build_spc_menu()` or `build_win_menu()`
4. **New Tests**: Add test scripts to `test/` directory

### Git Aliases

Custom git commands available via `gitcmd.sh`:

```bash
# Repository URL
git url

# URLs of files in last commit  
git files
```

## Dependencies

This project requires:
- **yabai**: Tiling window manager for macOS
- **Lima**: Linux virtual machines on macOS  
- **Python 3.13+** with dependencies:
  - `rumps` - Menu bar app framework
  - `reactivex` - Reactive programming for event streams
  - `docker` - Docker API client
  - `psutil` - System and process utilities
  - `humanize` - Human-readable data formatting

## Configuration

### App Arrangement Rules
Edit `~/.config/yabai/spec.py` to define which apps go to which spaces:
```python
arrange_spec = [
    [2, "term"],      # Terminal apps to space 2
    [4, "chrome"],    # Chrome to space 4
    [5, "zen"],       # Zen browser to space 5
    [8, "discor"],    # Discord to space 8
    [9, "mail"],      # Mail apps to space 9
    [7, "calend"],    # Calendar to space 7
    [1, ""],          # Default space 1
]
```

### Menu Features
- **Space Management**: Visual indicators show current space with emoji numbers (1️⃣, 2️⃣, etc.)
- **Window List**: All windows with app icons and click-to-focus functionality
- **VM Status**: Lima VMs with memory usage and Docker container status
- **System Tools**: Dark mode toggle, system sleep, yabai restart, window arrangement
- **Docker Integration**: Container management, start/stop VMs, resource monitoring

This is a power-user setup for managing complex macOS desktop environments with multiple virtual machines and precise workspace organization.

