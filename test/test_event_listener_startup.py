#!/usr/bin/env python3
"""Test that the event listener starts without import errors"""

import sys
import os
import subprocess
import time
import signal

def test_event_listener_startup():
    """Test that the event listener can start without import errors"""
    print("🧪 Testing event listener startup...")
    
    # Change to project directory
    os.chdir("/Users/gk/uv/osx")
    
    try:
        # Start the event listener
        process = subprocess.Popen(
            [".venv/bin/python3", "-m", "src.event_listener"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait a moment for it to start up
        time.sleep(2)
        
        # Check if process is still running (no import errors)
        if process.poll() is None:
            print("✅ Event listener started successfully")
            
            # Kill the process
            process.terminate()
            try:
                process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
            
            print("✅ Event listener stopped cleanly")
            return True
        else:
            # Process exited, check for errors
            stdout, stderr = process.communicate()
            print(f"❌ Event listener failed to start:")
            print(f"   stdout: {stdout}")
            print(f"   stderr: {stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing event listener: {e}")
        return False

if __name__ == "__main__":
    success = test_event_listener_startup()
    if success:
        print("\n✅ Event listener startup test PASSED")
    else:
        print("\n❌ Event listener startup test FAILED")
        sys.exit(1)
