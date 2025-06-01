#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, '/Users/gk/uv/osx')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from src.const import S
    print("✓ Imported src.const.S")
    
    from src.events import EventHandlers, build_app
    print("✓ Imported EventHandlers and build_app from src.events")
    
    print("✓ Testing EventHandlers instantiation")
    eh = EventHandlers()
    print("✓ EventHandlers created successfully")
    
    print("Available methods:")
    for attr in dir(eh):
        if not attr.startswith('_'):
            print(f"  - {attr}")
            
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
