#!/usr/bin/env python3
"""
Test to verify the Hammerspoon module structure works correctly
"""

def verify_hammerspoon_structure():
    """Verify the Hammerspoon configuration structure"""
    
    print("🔍 HAMMERSPOON MODULE STRUCTURE VERIFICATION")
    print("=" * 50)
    
    import os
    
    hammerspoon_dir = "/Users/gk/.hammerspoon"
    init_file = os.path.join(hammerspoon_dir, "init.lua")
    keyboard_module = os.path.join(hammerspoon_dir, "keyboard_events.lua")
    
    # Check files exist
    print(f"\n📁 Hammerspoon directory: {hammerspoon_dir}")
    print(f"   {'✅' if os.path.exists(hammerspoon_dir) else '❌'} Directory exists")
    
    print(f"\n📄 Main config: {init_file}")
    print(f"   {'✅' if os.path.exists(init_file) else '❌'} init.lua exists")
    
    print(f"\n📄 Keyboard module: {keyboard_module}")
    print(f"   {'✅' if os.path.exists(keyboard_module) else '❌'} keyboard_events.lua exists")
    
    # Check main config imports the module
    if os.path.exists(init_file):
        with open(init_file, 'r') as f:
            content = f.read()
            has_import = "require('keyboard_events')" in content
            has_setup = "KeyboardEvents.setup" in content
            print(f"\n🔗 Module integration:")
            print(f"   {'✅' if has_import else '❌'} Contains require('keyboard_events')")
            print(f"   {'✅' if has_setup else '❌'} Contains KeyboardEvents.setup() call")
    
    # Check module structure
    if os.path.exists(keyboard_module):
        with open(keyboard_module, 'r') as f:
            content = f.read()
            has_setup_func = "function M.setup" in content
            has_return = "return M" in content
            has_http_func = "sendHTTPEvent" in content
            print(f"\n⚙️ Module structure:")
            print(f"   {'✅' if has_setup_func else '❌'} Contains setup function")
            print(f"   {'✅' if has_return else '❌'} Returns module table")
            print(f"   {'✅' if has_http_func else '❌'} Contains HTTP event function")
    
    print(f"\n📋 NEXT STEPS:")
    print(f"   1. Reload Hammerspoon: Cmd+Ctrl+R")
    print(f"   2. Start event listener: .venv/bin/python3 event_listener.py")
    print(f"   3. Test keyboard logging: Cmd+Ctrl+K")
    
    print(f"\n✨ BENEFITS OF MODULE STRUCTURE:")
    print(f"   • Clean main config file")
    print(f"   • Reusable keyboard event handling")
    print(f"   • Easy to extend with new features")
    print(f"   • Better organization and maintenance")
    
    print("\n" + "=" * 50)
    print("Module structure verification complete! 🚀")

if __name__ == "__main__":
    verify_hammerspoon_structure()
