#!/usr/bin/env python3
import sys
import os
import time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from const import S
from events import EventHandlers
from event_listener import setup_http_listener

def run_test_server():
    # Set up basic state
    S.mode = "s"
    S.menutitle = {}
    S.windows = {}
    S.cur_win = {}
    S.app = None  # No GUI for this test
    
    print("Starting HTTP event server on port 10888...")
    print("Test with: curl 'http://127.0.0.1:10888/evt/space_changed?space_id=1&space_index=3'")
    print("Press Ctrl+C to stop")
    
    # Create event handlers
    event_handlers = EventHandlers()
    
    # Start HTTP server (this will run forever)
    server = setup_http_listener(event_handlers, 10888)
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down server...")

if __name__ == "__main__":
    run_test_server()
