#!/usr/bin/env python3
"""Test the simplified structure using Events class directly"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

def test_simplified_structure():
    """Test that the simplified structure works correctly"""
    print("🧪 Testing simplified structure...")
    
    print("\n1. Testing imports:")
    try:
        from src.const import Events
        print("   ✅ Events class from const.py")
    except ImportError as e:
        print(f"   ❌ Events import failed: {e}")
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
    
    print("\n2. Testing Events class methods:")
    events = Events()
    expected_methods = ['none', 'keyboard_event', 'space_changed', 'window_destroyed', 'window_focused', 'window_created']
    
    for method in expected_methods:
        if hasattr(events, method):
            print(f"   ✅ {method}")
        else:
            print(f"   ❌ {method} - NOT FOUND")
    
    print("\n3. Testing event handlers work:")
    from src.const import S
    
    # Test space_changed
    events.space_changed(["space_changed", "1", "4"])
    print(f"   Space indicator: {S.menutitle.get('space', 'NOT SET')}")
    
    # Test keyboard_event 
    events.keyboard_event(["keyboard_event", "0", "logger_started", "system"])
    print(f"   Keyboard indicator: {S.menutitle.get('keyboard', 'NOT SET')}")
    
    # Test none method
    print("   Testing none method:")
    events.none(["test", "data"])
    
    print("\n✅ Simplified structure test complete!")

if __name__ == "__main__":
    test_simplified_structure()
