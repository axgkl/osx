#!/usr/bin/env python3
"""Test the enhanced keyboard event handler with dynamic menu display"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from src.const import Events, S

def test_keyboard_menu_behavior():
    """Test the dynamic keyboard menu behavior"""
    print("🧪 Testing enhanced keyboard menu behavior...")
    
    # Create handler instance
    handler = Events()
    
    print("\n1. Testing logger startup:")
    handler.keyboard_event(["keyboard_event", "0", "logger_started", "system"])
    print(f"   Keyboard indicator: '{S.menutitle.get('keyboard', 'NOT SET')}'")
    print(f"   Keypress display: '{S.menutitle.get('keypress', 'NOT SET')}'")
    
    print("\n2. Testing various key combinations:")
    
    # Test simple key
    handler.keyboard_event(["keyboard_event", "1", "a", ""])
    print(f"   Key 'a': '{S.menutitle.get('keypress', 'NOT SET')}'")
    
    # Test key with single modifier
    handler.keyboard_event(["keyboard_event", "15", "r", "cmd"])
    print(f"   Key '⌘r': '{S.menutitle.get('keypress', 'NOT SET')}'")
    
    # Test key with multiple modifiers
    handler.keyboard_event(["keyboard_event", "42", "k", "cmd,ctrl"])
    print(f"   Key '⌘⌃k': '{S.menutitle.get('keypress', 'NOT SET')}'")
    
    # Test special keys
    handler.keyboard_event(["keyboard_event", "49", "space", ""])
    print(f"   Space key: '{S.menutitle.get('keypress', 'NOT SET')}'")
    
    handler.keyboard_event(["keyboard_event", "36", "return", ""])
    print(f"   Return key: '{S.menutitle.get('keypress', 'NOT SET')}'")
    
    handler.keyboard_event(["keyboard_event", "53", "escape", ""])
    print(f"   Escape key: '{S.menutitle.get('keypress', 'NOT SET')}'")
    
    # Test arrow keys with shift
    handler.keyboard_event(["keyboard_event", "126", "up", "shift"])
    print(f"   Shift+Up: '{S.menutitle.get('keypress', 'NOT SET')}'")
    
    # Test complex combination
    handler.keyboard_event(["keyboard_event", "2", "d", "cmd,alt,shift"])
    print(f"   ⌘⌥⇧d: '{S.menutitle.get('keypress', 'NOT SET')}'")
    
    print("\n3. Testing logger stop:")
    handler.keyboard_event(["keyboard_event", "0", "logger_stopped", "system"])
    print(f"   Keyboard indicator: '{S.menutitle.get('keyboard', 'REMOVED')}'")
    print(f"   Keypress display: '{S.menutitle.get('keypress', 'REMOVED')}'")
    
    print("\n4. Testing keypress when logger is off:")
    handler.keyboard_event(["keyboard_event", "1", "x", ""])
    print(f"   Key when off: '{S.menutitle.get('keypress', 'SHOULD BE REMOVED')}'")
    
    print("\n✅ Enhanced keyboard menu behavior test complete!")

if __name__ == "__main__":
    test_keyboard_menu_behavior()
