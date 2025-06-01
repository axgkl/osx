# OSX Automation

A macOS automation system integrating yabai (tiling window manager), Lima VMs, and Hammerspoon for advanced desktop management via a menu bar interface.

## Features

- **Window Management**: Click-to-focus windows, automatic app arrangement to designated spaces
- **Space Navigation**: Visual space indicators with emoji numbers (1️⃣, 2️⃣, etc.)
- **Keyboard Event Display**: Real-time keypress visualization with unicode symbols (🎹⌘⌃k)
- **VM Control**: Lima VM management with Docker container status and controls
- **System Integration**: Dark mode toggle, system sleep, yabai restart

## Prerequisites

- **yabai**: Tiling window manager
- **Hammerspoon**: Automation toolkit (for keyboard events)
- **Lima**: Linux VMs (optional)
- **Python 3.13+** with dependencies in `pyproject.toml`

## Quick Start

1. **Install dependencies:**
   ```bash
   uv sync
   ```

2. **Set up environment variable:**
   ```bash
   # Create LaunchAgent for OSX_EVTS_PORT
   launchctl load ~/Library/LaunchAgents/com.user.environment.plist
   launchctl start com.user.environment
   ```

3. **Configure yabai signals:**
   ```bash
   yabai -m signal --add event=space_changed action='curl -s "http://127.0.0.1:${OSX_EVTS_PORT:-10888}/evt/space_changed?space_id=$YABAI_SPACE_ID&space_index=$YABAI_SPACE_INDEX"'
   yabai -m signal --add event=window_focused action='curl -s "http://127.0.0.1:${OSX_EVTS_PORT:-10888}/evt/window_focused?window_id=$YABAI_WINDOW_ID"'
   yabai -m signal --add event=window_destroyed action='curl -s "http://127.0.0.1:${OSX_EVTS_PORT:-10888}/evt/window_destroyed?window_id=$YABAI_WINDOW_ID"'
   ```

4. **Start the system:**
   ```bash
   just start
   ```

## Configuration

### App Arrangement

Edit `~/.config/yabai/spec.py`:
```python
arrange_spec = [
    [2, "term"],      # Terminal apps to space 2
    [4, "chrome"],    # Chrome to space 4
    [8, "discor"],    # Discord to space 8
    [1, ""],          # Default space
]
```

### Hammerspoon Integration

For keyboard event display, add to `~/.hammerspoon/init.lua`:
```lua
local KeyboardEvents = require('keyboard_events')
KeyboardEvents.setup(hs.hotkey.bind, hs.alert.show)
```

Toggle keyboard logging: `Cmd+Ctrl+K`

## HTTP API

The system provides HTTP endpoints for yabai integration:

- `GET /evt/space_changed?space_id=X&space_index=Y`
- `GET /evt/window_focused?window_id=X`
- `GET /evt/window_destroyed?window_id=X`
- `GET /evt/keyboard_event?key_code=X&key_char=Y&modifiers=Z`

## Environment Setup

Create `~/Library/LaunchAgents/com.user.environment.plist`:
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
        <string>launchctl setenv OSX_EVTS_PORT 10888</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
```

## Testing

```bash
# Run all tests
just test

# Test specific components
just test-keyboard-menu
just test-startup

# Demo keyboard behavior
just demo-keyboard
```

## Architecture

- **Event Listener**: HTTP server receiving yabai events via curl
- **Modular Handlers**: Individual event processors in `src/evt/`
- **Menu App**: Menu bar interface built with rumps
- **Lima Integration**: VM and Docker container management

## Documentation

- [Keyboard Event System](docs/keyboard_event.md) - Complete integration guide
- Run `just docs-keyboard` to view documentation

## Troubleshooting

### Port Issues
```bash
# Check port availability
lsof -i :10888

# Verify environment variable
launchctl getenv OSX_EVTS_PORT
```

### Server Status
```bash
# Test endpoints
curl "http://127.0.0.1:10888/evt/space_changed?space_id=1&space_index=2"

# Check logs
tail -f /tmp/event-listener-*.log
```
