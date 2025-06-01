#!/usr/bin/env python3
"""Test the refactored structure with window.py and app.py"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

def test_refactored_structure():
    """Test that the refactored structure works correctly"""
    print("🧪 Testing refactored structure...")
    
    print("\n1. Testing imports:")
    try:
        from src.window import EventHandlers
        print("   ✅ EventHandlers from window.py")
    except ImportError as e:
        print(f"   ❌ EventHandlers import failed: {e}")
        return
    
    try:
        from src.app import build_app, build_spc_menu
        print("   ✅ build_app and build_spc_menu from app.py")
    except ImportError as e:
        print(f"   ❌ App functions import failed: {e}")
        return
    
    try:
        from src.window import build_win_menu, window, arrange_wins
        print("   ✅ Window functions from window.py")
    except ImportError as e:
        print(f"   ❌ Window functions import failed: {e}")
        return
    
    print("\n2. Testing EventHandlers methods:")
    handler = EventHandlers()
    expected_methods = ['none', 'keyboard_event', 'space_changed', 'window_destroyed', 'window_focused', 'window_created']
    
    for method in expected_methods:
        if hasattr(handler, method):
            print(f"   ✅ {method}")
        else:
            print(f"   ❌ {method} - NOT FOUND")
    
    print("\n3. Testing event handlers work:")
    from src.const import S
    
    # Test space_changed
    handler.space_changed(["space_changed", "1", "2"])
    print(f"   Space indicator: {S.menutitle.get('space', 'NOT SET')}")
    
    # Test keyboard_event 
    handler.keyboard_event(["keyboard_event", "0", "logger_started", "system"])
    print(f"   Keyboard indicator: {S.menutitle.get('keyboard', 'NOT SET')}")
    
    print("\n✅ Refactored structure test complete!")

if __name__ == "__main__":
    test_refactored_structure()
