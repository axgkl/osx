#!/usr/bin/env python3
"""Test the modular keyboard event handler"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from src.events import EventHandlers
from src.const import S

def test_keyboard_event_module():
    """Test that the keyboard event handler works from the module"""
    print("🧪 Testing modular keyboard event handler...")
    
    # Create handler instance
    handler = EventHandlers()
    
    # Test system events
    print("\n1. Testing system events:")
    handler.keyboard_event(["keyboard_event", "0", "logger_started", "system"])
    print(f"   Menu title after start: {S.menutitle.get('keyboard', 'NOT SET')}")
    
    handler.keyboard_event(["keyboard_event", "0", "logger_stopped", "system"])
    print(f"   Menu title after stop: {S.menutitle.get('keyboard', 'NOT SET')}")
    
    # Test regular keyboard events
    print("\n2. Testing regular keyboard events:")
    handler.keyboard_event(["keyboard_event", "42", "k", "cmd,ctrl"])
    print(f"   Menu title after cmd+ctrl+k: {S.menutitle.get('keyboard', 'NOT SET')}")
    
    handler.keyboard_event(["keyboard_event", "15", "r", "cmd,ctrl"])
    print(f"   Menu title after cmd+ctrl+r: {S.menutitle.get('keyboard', 'NOT SET')}")
    
    # Test simple key
    print("\n3. Testing simple key:")
    handler.keyboard_event(["keyboard_event", "1", "a", ""])
    
    print("\n✅ Modular keyboard event handler test complete!")

if __name__ == "__main__":
    test_keyboard_event_module()
