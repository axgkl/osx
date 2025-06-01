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
    print("Simulating app running for 5 seconds...")
    time.sleep(5)
    print("App simulation complete")

def test_port_and_pid():
    print("Testing port detection and PID management...")
    
    # Test 1: Default port from environment
    print(f"OSX_EVTS_PORT environment: {os.environ.get('OSX_EVTS_PORT', 'Not set')}")
    
    # Test 2: PID file creation
    print("Testing run_event_listener with simple app builder...")
    
    try:
        run_event_listener(port=10891, 
                          event_handlers_class=EventHandlers, 
                          app_builder=simple_app_builder)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_port_and_pid()
