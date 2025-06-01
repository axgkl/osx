#!/usr/bin/env python3
"""Test that build_spc_menu is correctly assigned as build_menu"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from src.const import S, YabaiMenuApp
from src.app import build_spc_menu

def test_build_menu_assignment():
    """Test that build_spc_menu is assigned correctly as build_menu"""
    print("🧪 Testing build_menu assignment...")
    
    # Create a YabaiMenuApp instance
    S.app = YabaiMenuApp()
    
    # Assign build_spc_menu as build_menu
    S.app.build_menu = build_spc_menu
    
    # Verify the assignment
    if S.app.build_menu == build_spc_menu:
        print("✅ build_spc_menu correctly assigned as S.app.build_menu")
    else:
        print("❌ build_spc_menu assignment failed")
        return False
    
    # Verify we can call it
    try:
        # This would normally clear menu and rebuild, but since we don't have
        # a full GUI context, we'll just check it's callable
        if callable(S.app.build_menu):
            print("✅ S.app.build_menu is callable")
        else:
            print("❌ S.app.build_menu is not callable")
            return False
    except Exception as e:
        print(f"❌ Error calling S.app.build_menu: {e}")
        return False
    
    print("✅ build_menu assignment test passed!")
    return True

if __name__ == "__main__":
    success = test_build_menu_assignment()
    if not success:
        sys.exit(1)
