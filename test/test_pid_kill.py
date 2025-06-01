#!/usr/bin/env python3
import sys
import os
import time
import subprocess
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_pid_kill():
    print("Testing PID file kill functionality...")
    
    # Create a fake PID file
    pid_file = "/tmp/event-listener-10894.pid"
    
    # Start a dummy process to test killing
    dummy_process = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(30)"])
    dummy_pid = dummy_process.pid
    
    print(f"Created dummy process with PID: {dummy_pid}")
    
    # Write the dummy PID to the file
    with open(pid_file, "w") as f:
        f.write(str(dummy_pid))
    print(f"Wrote PID {dummy_pid} to {pid_file}")
    
    # Now start event listener - it should kill the dummy process
    from event_listener import run_event_listener
    from events import EventHandlers
    
    def quick_app_builder(event_handlers):
        print("App builder called - exiting quickly")
        time.sleep(1)
    
    print("Starting event listener - should kill dummy process...")
    
    try:
        run_event_listener(port=10894, 
                          event_handlers_class=EventHandlers, 
                          app_builder=quick_app_builder)
    except Exception as e:
        print(f"Error: {e}")
    
    # Check if dummy process was killed
    try:
        os.kill(dummy_pid, 0)  # Check if process still exists
        print(f"❌ Dummy process {dummy_pid} is still running")
        dummy_process.terminate()  # Clean up
    except OSError:
        print(f"✅ Dummy process {dummy_pid} was successfully killed")

if __name__ == "__main__":
    test_pid_kill()
