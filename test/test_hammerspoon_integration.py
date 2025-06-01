#!/usr/bin/env python3
import sys
import os
import time
import requests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.const import S
from src.events import EventHandlers
from src.event_listener import setup_http_listener

def test_hammerspoon_events():
    """Test Hammerspoon keyboard event integration"""
    S.mode = "s"
    S.menutitle = {}
    S.windows = {}
    S.cur_win = {}
    S.app = None
    
    print("Testing Hammerspoon keyboard event integration...")
    
    event_handlers = EventHandlers()
    test_port = 10899
    
    try:
        server = setup_http_listener(event_handlers, test_port)
        time.sleep(1)
        
        base_url = f"http://127.0.0.1:{test_port}"
        
        # Test 1: Logger started event
        print("\n1. Testing logger started event...")
        response = requests.get(f"{base_url}/evt/keyboard_event?key_code=0&key_char=logger_started&modifiers=system")
        print(f"   Status: {response.status_code}")
        print(f"   Menu title: {S.menutitle}")
        
        # Test 2: Regular key event
        print("\n2. Testing regular key event...")
        response = requests.get(f"{base_url}/evt/keyboard_event?key_code=42&key_char=k&modifiers=cmd,ctrl")
        print(f"   Status: {response.status_code}")
        print(f"   Menu title: {S.menutitle}")
        
        # Test 3: Hammerspoon reload combo
        print("\n3. Testing Hammerspoon reload combo...")
        response = requests.get(f"{base_url}/evt/keyboard_event?key_code=15&key_char=r&modifiers=cmd,ctrl")
        print(f"   Status: {response.status_code}")
        
        # Test 4: Logger stopped event
        print("\n4. Testing logger stopped event...")
        response = requests.get(f"{base_url}/evt/keyboard_event?key_code=0&key_char=logger_stopped&modifiers=system")
        print(f"   Status: {response.status_code}")
        print(f"   Menu title: {S.menutitle}")
        
        print("\n✅ Hammerspoon integration test complete!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_hammerspoon_events()
