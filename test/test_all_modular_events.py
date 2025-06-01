#!/usr/bin/env python3
"""Test all modular event handlers"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from src.events import EventHandlers
from src.const import S, Events

def test_all_modular_events():
    """Test that all event handlers are properly modularized"""
    print("🧪 Testing all modular event handlers...")
    
    # Create handler instance
    handler = EventHandlers()
    
    # Test that all expected methods exist
    expected_methods = [
        'none',
        'keyboard_event', 
        'space_changed',
        'window_destroyed',
        'window_focused',
        'window_created'
    ]
    
    print("\n1. Checking method availability:")
    for method_name in expected_methods:
        if hasattr(handler, method_name):
            print(f"   ✅ {method_name}")
        else:
            print(f"   ❌ {method_name} - NOT FOUND")
    
    print("\n2. Testing Events base class:")
    for method_name in expected_methods:
        if hasattr(Events, method_name):
            print(f"   ✅ Events.{method_name}")
        else:
            print(f"   ❌ Events.{method_name} - NOT FOUND")
    
    print("\n3. Testing event handlers:")
    
    # Test none method (from base class)
    print("   Testing none:")
    handler.none(["test_event", "param1"])
    
    # Test space_changed
    print("   Testing space_changed:")
    handler.space_changed(["space_changed", "1", "3"])
    print(f"     Space indicator: {S.menutitle.get('space', 'NOT SET')}")
    
    # Test window_destroyed
    print("   Testing window_destroyed:")
    S.windows = {"123": {"app": "Test"}}
    handler.window_destroyed(["window_destroyed", "123"])
    print(f"     Windows after destroy: {len(S.windows)} (should be 0)")
    
    # Test keyboard_event system events
    print("   Testing keyboard_event:")
    handler.keyboard_event(["keyboard_event", "0", "logger_started", "system"])
    print(f"     Keyboard indicator: {S.menutitle.get('keyboard', 'NOT SET')}")
    
    # Test window_created 
    print("   Testing window_created:")
    handler.window_created(["window_created", "456"])
    
    # Test window_focused
    print("   Testing window_focused:")
    handler.window_focused(["window_focused", "789"])
    
    print("\n✅ All modular event handlers test complete!")

if __name__ == "__main__":
    test_all_modular_events()
