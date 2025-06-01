# OSX Automation System Documentation

This directory contains documentation for the OSX automation system components.

## Available Documentation

### [Keyboard Event System](keyboard_event.md)
Complete guide to the keyboard event integration with Hammerspoon:
- Visual menu behavior and unicode symbols
- Hammerspoon module requirements and setup
- HTTP API specification  
- Troubleshooting and configuration

## Quick Commands

```bash
# View keyboard documentation
just docs-keyboard

# Test keyboard menu behavior
just test-keyboard-menu

# Demo keyboard menu  
just demo-keyboard

# Start the system
just start
```

## Overview

The OSX automation system provides:
- **Window Management**: Click-to-focus windows, auto-arrange apps
- **Space Navigation**: Visual space indicators with emoji numbers  
- **Keyboard Logging**: Real-time keypress display in menu bar
- **VM Control**: Start/stop Lima VMs with Docker management
- **System Controls**: Dark mode, sleep, yabai restart

For more information, see the main [README.md](../README.md).
