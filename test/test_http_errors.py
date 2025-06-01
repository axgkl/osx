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

def test_http_error_handling():
    # Set up basic state
    S.mode = "s"
    S.menutitle = {}
    S.windows = {}
    S.cur_win = {}
    S.app = None  # No GUI for this test
    
    print("Testing HTTP error handling...")
    
    # Create event handlers
    event_handlers = EventHandlers()
    
    # Start HTTP server on a test port
    test_port = 10896
    try:
        server = setup_http_listener(event_handlers, test_port)
        print(f"Server started on port {test_port}")
        time.sleep(1)  # Give server time to start
        
        base_url = f"http://127.0.0.1:{test_port}"
        
        # Test 1: Valid event type (should return 200)
        print("\n1. Testing valid event type...")
        try:
            response = requests.get(f"{base_url}/evt/space_changed?space_id=1&space_index=2")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.json()}")
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            print("   ✅ Valid event type test passed")
        except Exception as e:
            print(f"   ❌ Valid event type test failed: {e}")
        
        # Test 2: Invalid event type (should return 404)
        print("\n2. Testing invalid event type...")
        try:
            response = requests.get(f"{base_url}/evt/invalid_event")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.json()}")
            assert response.status_code == 404, f"Expected 404, got {response.status_code}"
            print("   ✅ Invalid event type test passed")
        except Exception as e:
            print(f"   ❌ Invalid event type test failed: {e}")
        
        # Test 3: Invalid path (should return 404)
        print("\n3. Testing invalid path...")
        try:
            response = requests.get(f"{base_url}/invalid/path")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.json()}")
            assert response.status_code == 404, f"Expected 404, got {response.status_code}"
            print("   ✅ Invalid path test passed")
        except Exception as e:
            print(f"   ❌ Invalid path test failed: {e}")
        
        # Test 4: Check error message format
        print("\n4. Testing error message format...")
        try:
            response = requests.get(f"{base_url}/evt/unsupported_event")
            data = response.json()
            if "status" in data and data["status"] == "error":
                print(f"   Error message: {data.get('message', 'No message')}")
                print("   ✅ Error message format test passed")
            else:
                print("   ❌ Unexpected response format")
        except Exception as e:
            print(f"   ❌ Error message format test failed: {e}")
            
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Port {test_port} is already in use")
        else:
            print(f"❌ Error starting server: {e}")
    
    print("\nHTTP error handling test complete!")

if __name__ == "__main__":
    test_http_error_handling()
