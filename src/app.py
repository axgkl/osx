#!/usr/bin/env python3
"""App building and menu management module"""

import os
from .lima import Lima
from .const import S, YabaiMenuApp
from .window import arrange_wins, toggle_darkmode, system_sleep, yabai_restart, build_win_menu, d_icos
from .const import quit_app

# Import event handler modules to register them
from . import evt  # This imports all event handlers

def build_spc_menu(_=None):
    """Build the space menu with system controls"""
    S.app.menu.clear()
    S.app.add("🔁 Refresh Menu", build_spc_menu)
    S.app.add("🧹 Arrange", arrange_wins)
    S.app.add("☯ Dark/White", toggle_darkmode)
    S.app.add("🌙 System Sleep", system_sleep)
    S.app.add("🔁 Restart Yabai", yabai_restart)
    S.app.add("🚪Quit Menu", quit_app)
    Lima.build_menu()


def build_app(event_handlers):
    """Build and run the menu app"""
    print("Building app...")
    try:
        print("Preparing Lima docker socket...")
        Lima.prepare_docker_socket()
        print("✓ Lima preparation complete")
    except Exception as e:
        print(f"Warning: Lima preparation failed: {e}")
    
    print("Creating icons directory...")
    os.makedirs(d_icos, exist_ok=True)
    
    print("Creating YabaiMenuApp...")
    S.app = YabaiMenuApp()
    S.app.build_menu = build_win_menu
    
    if S.mode == "s":
        print("Setting up space mode...")
        event_handlers.space_changed([0, 0, "1"])
        S.app.build_menu = build_spc_menu
        S.app.build_menu()
    
    print("Starting app.run()...")
    S.app.run()
