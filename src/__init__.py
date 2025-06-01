# OSX Automation System
"""
A sophisticated macOS automation system that integrates with yabai and Lima.
"""

# Only import what's needed for the package API
# Don't import event_listener to avoid module loading conflicts when using -m
from .const import Events
from .app import build_app
from .const import S

__version__ = "0.1.0"
__all__ = ["Events", "build_app", "S"]
