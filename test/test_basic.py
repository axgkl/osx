#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.const import S, Events

def simple_test():
    # Set up basic state
    S.fn_fifo = "/tmp/yabai-spc.fifo"
    S.menutitle = {}
    S.windows = {}
    
    print(f"FIFO: {S.fn_fifo}")
    
    # Test event handlers
    eh = Events()
    print("Testing space_changed event...")
    eh.space_changed(['space_changed', '1', '2'])
    print(f"Menu title: {S.menutitle}")
    
    print("✓ Basic functionality works")

if __name__ == "__main__":
    simple_test()
