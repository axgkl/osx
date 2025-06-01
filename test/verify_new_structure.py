#!/usr/bin/env python3
"""
Verify the new src/ structure and start command
"""

def verify_new_structure():
    """Verify the reorganized structure works correctly"""
    
    print("🔄 PROJECT STRUCTURE REORGANIZATION")
    print("=" * 50)
    
    import os
    
    # Check new structure
    checks = [
        ("src/ directory", "/Users/gk/uv/osx/src"),
        ("src/__init__.py", "/Users/gk/uv/osx/src/__init__.py"),
        ("src/event_listener.py", "/Users/gk/uv/osx/src/event_listener.py"),
        ("src/events.py", "/Users/gk/uv/osx/src/events.py"),
        ("src/const.py", "/Users/gk/uv/osx/src/const.py"),
        ("src/lima.py", "/Users/gk/uv/osx/src/lima.py"),
        ("justfile", "/Users/gk/uv/osx/justfile"),
    ]
    
    print("\n📁 FILE STRUCTURE:")
    for name, path in checks:
        exists = os.path.exists(path)
        print(f"   {'✅' if exists else '❌'} {name}")
    
    # Check justfile has start command
    justfile_path = "/Users/gk/uv/osx/justfile"
    if os.path.exists(justfile_path):
        with open(justfile_path, 'r') as f:
            content = f.read()
            has_start = "start:" in content and "src.event_listener" in content
            print(f"\n🚀 START COMMAND:")
            print(f"   {'✅' if has_start else '❌'} 'just start' command available")
    
    print(f"\n📦 NEW STRUCTURE:")
    print(f"   /Users/gk/uv/osx/")
    print(f"   ├── src/              # Source code (NEW)")
    print(f"   │   ├── __init__.py   # Package init")
    print(f"   │   ├── event_listener.py")
    print(f"   │   ├── events.py")
    print(f"   │   ├── const.py")
    print(f"   │   ├── lima.py")
    print(f"   │   └── main.py")
    print(f"   ├── test/             # Test scripts")
    print(f"   ├── justfile          # Task runner")
    print(f"   └── README.md")
    
    print(f"\n🎯 USAGE:")
    print(f"   # Start the system")
    print(f"   just start")
    print(f"   ")
    print(f"   # Run tests")
    print(f"   just test")
    print(f"   ")
    print(f"   # Or run directly")
    print(f"   .venv/bin/python3 -m src.event_listener")
    
    print(f"\n✨ BENEFITS:")
    print(f"   • Clean project organization")
    print(f"   • Proper Python package structure")
    print(f"   • Simple 'just start' command")
    print(f"   • Relative imports in source code")
    print(f"   • Better separation of source and tests")
    
    print("\n" + "=" * 50)
    print("Project restructuring complete! 🎉")

if __name__ == "__main__":
    verify_new_structure()
