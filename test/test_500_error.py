#!/usr/bin/env python3
import sys
import os
import time
import requests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.const import S
from src.events import EventHandlers
from src.event_listener import setup_http_listener

class FailingEventHandlers(EventHandlers):
    """Event handlers that throw exceptions for testing"""
    def space_changed(self, evt):
        raise Exception("Intentional test failure")

def test_500_error():
    """Test that exceptions in event handlers return 500"""
    S.menutitle = {}
    S.windows = {}
    S.cur_win = {}
    S.app = None
    
    print("Testing 500 error handling...")
    
    # Use failing event handlers
    event_handlers = FailingEventHandlers()
    
    test_port = 10897
    try:
        server = setup_http_listener(event_handlers, test_port)
        time.sleep(1)
        
        # Test that exceptions result in 500 status
        response = requests.get(f"http://127.0.0.1:{test_port}/evt/space_changed?space_id=1&space_index=2")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 500:
            print("✅ Exception handling test passed")
        else:
            print(f"❌ Expected 500, got {response.status_code}")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_500_error()
