#!/usr/bin/env python3
import sys
import os
import time
import requests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.const import S
from src.events import EventHandlers
from src.event_listener import setup_http_listener

def test_keyboard_event():
    """Test the new keyboard event handling"""
    S.menutitle = {}
    S.windows = {}
    S.cur_win = {}
    S.app = None
    
    print("Testing keyboard event handling...")
    
    event_handlers = EventHandlers()
    test_port = 10898
    
    try:
        server = setup_http_listener(event_handlers, test_port)
        time.sleep(1)
        
        base_url = f"http://127.0.0.1:{test_port}"
        
        # Test keyboard event
        print("\n1. Testing keyboard event...")
        response = requests.get(f"{base_url}/evt/keyboard_event?key_code=42&key_char=k&modifiers=cmd,ctrl")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        if response.status_code == 200:
            print("   ✅ Keyboard event test passed")
        else:
            print(f"   ❌ Expected 200, got {response.status_code}")
        
        # Test with minimal parameters
        print("\n2. Testing keyboard event with minimal params...")
        response = requests.get(f"{base_url}/evt/keyboard_event?key_char=a")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        # Check menu title was updated
        print("\n3. Checking menu title update...")
        print(f"   Menu title: {S.menutitle}")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_keyboard_event()
