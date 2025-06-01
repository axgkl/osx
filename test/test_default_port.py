#!/usr/bin/env python3
import sys
import os
import time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from event_listener import run_event_listener
from events import EventHandlers

def simple_app_builder(event_handlers):
    """Simple app builder that doesn't use GUI components"""
    print("App builder called - would normally start menu bar app")
    print("Simulating app running for 3 seconds...")
    time.sleep(3)
    print("App simulation complete")

def test_default_port():
    print("Testing default port behavior...")
    print(f"OSX_EVTS_PORT environment: {os.environ.get('OSX_EVTS_PORT', 'Not set')}")
    
    try:
        # Test default port (should use environment variable)
        run_event_listener(event_handlers_class=EventHandlers, 
                          app_builder=simple_app_builder)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_default_port()
