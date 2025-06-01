# OSX Automation System
"""
A sophisticated macOS automation system that integrates with yabai and Lima.
"""

from .event_listener import run_event_listener
from .events import EventHandlers, build_app
from .const import S

__version__ = "0.1.0"
__all__ = ["run_event_listener", "EventHandlers", "build_app", "S"]
