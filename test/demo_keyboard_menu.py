#!/usr/bin/env python3
"""Visual demonstration of keyboard menu behavior"""

import sys
import os
import time
sys.path.insert(0, os.path.abspath('.'))

from src.const import Events, S

def simulate_menu_title():
    """Simulate how the menu title would look"""
    title = ""
    for key, value in S.menutitle.items():
        title += value
    return title

def demonstrate_keyboard_menu():
    """Demonstrate the keyboard menu behavior visually"""
    print("🎹 Keyboard Menu Behavior Demonstration")
    print("=" * 50)
    
    handler = Events()
    
    print("\n📍 Initial state:")
    print(f"   Menu title: '{simulate_menu_title()}'")
    
    print("\n🎯 Starting keyboard logger...")
    handler.keyboard_event(["keyboard_event", "0", "logger_started", "system"])
    print(f"   Menu title: '{simulate_menu_title()}'")
    
    print("\n⌨️  Keyboard activity simulation:")
    
    keypresses = [
        ("a", "", "Simple letter"),
        ("r", "cmd", "Command+R (Hammerspoon reload)"),
        ("space", "", "Space bar"),
        ("return", "shift", "Shift+Return"),
        ("k", "cmd,ctrl", "Command+Control+K (toggle logger)"),
        ("d", "cmd,alt,shift", "Complex modifier combo"),
        ("escape", "", "Escape key"),
        ("up", "alt", "Alt+Up arrow"),
        ("tab", "cmd", "Command+Tab"),
        ("backspace", "ctrl", "Control+Backspace")
    ]
    
    for key_char, modifiers, description in keypresses:
        handler.keyboard_event(["keyboard_event", "42", key_char, modifiers])
        title = simulate_menu_title()
        print(f"   {description:<35} → '{title}'")
        time.sleep(0.1)  # Small delay for visual effect
    
    print("\n🛑 Stopping keyboard logger...")
    handler.keyboard_event(["keyboard_event", "0", "logger_stopped", "system"])
    print(f"   Menu title: '{simulate_menu_title()}'")
    
    print("\n📝 After logger stops, keypresses don't show:")
    handler.keyboard_event(["keyboard_event", "42", "x", "cmd"])
    print(f"   Command+X (ignored) → '{simulate_menu_title()}'")
    
    print("\n✅ Demonstration complete!")
    print("\nMenu behavior summary:")
    print("• 🎹 appears when logger starts")  
    print("• Each keypress overwrites the previous one")
    print("• Unicode symbols for modifiers (⌘⌃⌥⇧)")
    print("• Special symbols for common keys (␣↩⎋⇥←↑→↓)")
    print("• All indicators removed when logger stops")

if __name__ == "__main__":
    demonstrate_keyboard_menu()
