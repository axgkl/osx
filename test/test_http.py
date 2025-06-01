#!/usr/bin/env python3
import sys
import os
import time
import requests
import threading

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.const import S
from src.events import EventHandlers
from src.event_listener import setup_http_listener

def test_http_server():
    # Set up basic state
    S.mode = "s"
    S.menutitle = {}
    S.windows = {}
    S.cur_win = {}
    S.app = None  # No GUI for this test
    
    print("Setting up HTTP event server...")
    
    # Create event handlers
    event_handlers = EventHandlers()
    
    # Try different ports if 10888 is busy
    test_port = 10889
    server = None
    for port in range(test_port, test_port + 10):
        try:
            server = setup_http_listener(event_handlers, port)
            test_port = port
            break
        except OSError as e:
            if "Address already in use" in str(e):
                continue
            else:
                raise
    
    if not server:
        print("❌ Could not find available port for testing")
        return
    
    print(f"Server started on port {test_port}, testing events...")
    time.sleep(1)  # Give server time to start
    
    base_url = f"http://127.0.0.1:{test_port}"
    
    # Test space_changed event
    try:
        response = requests.get(f"{base_url}/evt/space_changed?space_id=1&space_index=2")
        print(f"Space changed response: {response.json()}")
        print(f"Menu title after space change: {S.menutitle}")
    except Exception as e:
        print(f"Error testing space_changed: {e}")
    
    # Test window_focused event
    try:
        response = requests.get(f"{base_url}/evt/window_focused?window_id=123")
        print(f"Window focused response: {response.json()}")
    except Exception as e:
        print(f"Error testing window_focused: {e}")
    
    # Test unknown event
    try:
        response = requests.get(f"{base_url}/evt/unknown_event")
        print(f"Unknown event response: {response.json()}")
    except Exception as e:
        print(f"Error testing unknown_event: {e}")
    
    print("HTTP server test complete!")

if __name__ == "__main__":
    test_http_server()
