#!/usr/bin/env python3
import requests
import json

def test_manual_curl():
    """Test the HTTP error responses manually"""
    base_url = "http://127.0.0.1:10888"  # Use default port
    
    tests = [
        ("Valid event", f"{base_url}/evt/space_changed?space_id=1&space_index=2"),
        ("Invalid event", f"{base_url}/evt/nonexistent_event"),
        ("Invalid path", f"{base_url}/wrong/path"),
    ]
    
    for test_name, url in tests:
        try:
            print(f"\n{test_name}: {url}")
            response = requests.get(url)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
        except requests.exceptions.ConnectionError:
            print(f"❌ Server not running on {base_url}")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_manual_curl()
