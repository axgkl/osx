#!/usr/bin/env python3
"""Test that S.mode removal doesn't break functionality"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from src.const import S, Events
from src.app import build_app

def test_mode_removal():
    """Test that removing S.mode doesn't break the system"""
    print("🧪 Testing S.mode removal...")
    
    # Verify S.mode doesn't exist
    if hasattr(S, 'mode'):
        print("❌ S.mode still exists!")
        return False
    else:
        print("✅ S.mode successfully removed")
    
    # Test Events class still works
    events = Events()
    
    # Test space_changed (should always work now)
    events.space_changed(["space_changed", "1", "3"])
    expected_space = "3️⃣"
    if S.menutitle.get("space") == expected_space:
        print(f"✅ Space changed works: {expected_space}")
    else:
        print(f"❌ Space changed failed: {S.menutitle.get('space')}")
        return False
    
    # Test keyboard events
    events.keyboard_event(["keyboard_event", "0", "logger_started", "system"])
    if S.menutitle.get("keyboard") == "🎹":
        print("✅ Keyboard events work: 🎹")
    else:
        print(f"❌ Keyboard events failed: {S.menutitle.get('keyboard')}")
        return False
    
    events.keyboard_event(["keyboard_event", "42", "a", "cmd"])
    if S.menutitle.get("keypress") == "⌘a":
        print("✅ Keypress display works: ⌘a")
    else:
        print(f"❌ Keypress display failed: {S.menutitle.get('keypress')}")
        return False
    
    print("\n✅ All tests passed - S.mode removal successful!")
    return True

if __name__ == "__main__":
    success = test_mode_removal()
    if not success:
        sys.exit(1)
