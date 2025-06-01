#!/usr/bin/env python3
import sys
import os
import time
from time import ctime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from const import S
from events import EventHandlers, build_spc_menu, d_icos
from const import YabaiMenuApp

def simple_build_app(event_handlers):
    """Simplified app builder without Lima"""
    print("Building app (no Lima)...")
    
    print("Creating icons directory...")
    os.makedirs(d_icos, exist_ok=True)
    
    print("Creating YabaiMenuApp...")
    S.app = YabaiMenuApp()
    
    if S.mode == "s":
        print("Setting up space mode...")
        event_handlers.space_changed([0, 0, "1"])
        S.app.build_menu = build_spc_menu
        S.app.build_menu()
    
    print("Starting app.run()...")
    S.app.run()

def test_listener():
    S.fn_fifo = "/tmp/yabai-spc.fifo"
    S.mode = "s"
    S.menutitle = {}
    S.windows = {}
    S.cur_win = {}
    
    print(f"Starting test listener {ctime()}")
    
    # Ensure FIFO exists
    if not os.path.exists(S.fn_fifo):
        os.mkfifo(S.fn_fifo)
        print(f"Created FIFO: {S.fn_fifo}")
    
    try:
        event_handlers = EventHandlers()
        simple_build_app(event_handlers)
    except KeyboardInterrupt:
        print("Interrupted by user")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_listener()
