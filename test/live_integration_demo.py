#!/usr/bin/env python3
"""
Live demonstration of Hammerspoon keyboard event integration
"""
import sys
import os

def show_integration_instructions():
    """Show instructions for testing the live integration"""
    
    print("🎹 HAMMERSPOON ↔ OSX AUTOMATION INTEGRATION")
    print("=" * 50)
    
    print("\n1. START THE EVENT LISTENER:")
    print("   cd /Users/gk/uv/osx")
    print("   .venv/bin/python3 event_listener.py")
    
    print("\n2. RELOAD HAMMERSPOON CONFIG:")
    print("   Press Cmd+Ctrl+R in Hammerspoon")
    print("   (This loads the updated configuration with HTTP events)")
    
    print("\n3. ACTIVATE KEYBOARD LOGGER:")
    print("   Press Cmd+Ctrl+K to start logging")
    print("   You should see: 🎹 indicator in menu bar")
    
    print("\n4. TEST KEYBOARD EVENTS:")
    print("   Type some keys and watch both:")
    print("   • Hammerspoon Console (for local logs)")
    print("   • Event listener terminal (for HTTP events)")
    
    print("\n5. WATCH MENU BAR INDICATORS:")
    print("   🎹 = Logger active")
    print("   ⌨️ = Recent keystroke with modifiers")
    print("   (no indicator) = Logger stopped")
    
    print("\n6. STOP LOGGING:")
    print("   Press Cmd+Ctrl+K again")
    print("   Menu indicator should disappear")
    
    print("\n📝 WHAT YOU'LL SEE:")
    print("   • Every keystroke → HTTP request to event listener")
    print("   • Real-time menu bar updates")
    print("   • Logs in both Hammerspoon and Python")
    print("   • Special detection for Cmd+Ctrl combinations")
    
    print("\n🔧 CONFIGURATION UPDATED:")
    print("   ~/.hammerspoon/init.lua now includes HTTP event sending")
    
    print("\n" + "=" * 50)
    print("Ready for live integration testing! 🚀")

if __name__ == "__main__":
    show_integration_instructions()
