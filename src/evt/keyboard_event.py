"""Keyboard event handler module"""
from ..const import Events, S


def keyboard_event(self, evt: list):
    """Handle keyboard events from Hammerspoon"""
    if len(evt) >= 4:
        key_code, key_char, modifiers = evt[1], evt[2], evt[3]
        
        # Handle system events (logger start/stop)
        if modifiers == "system":
            if key_char == "logger_started":
                print("🎹 Keyboard logger started in Hammerspoon")
                S.menutitle["keyboard"] = "🎹"
            elif key_char == "logger_stopped":
                print("⏸️ Keyboard logger stopped in Hammerspoon")
                S.menutitle.pop("keyboard", None)
            if S.app:
                S.app.set_title()
            return
        
        # Handle regular keyboard events
        print(f"Keyboard event: {key_char} (code: {key_code}) modifiers: {modifiers}")
        
        # Update menu for special key combinations
        if modifiers and ("cmd" in modifiers or "ctrl" in modifiers):
            S.menutitle["keyboard"] = "⌨️"
            if S.app:
                S.app.set_title()
        
        # You can add custom key combination handlers here
        # Example: specific actions for certain key combinations
        if "cmd" in modifiers and "ctrl" in modifiers:
            if key_char == "r":
                print("🔄 Detected Hammerspoon reload combo")
            elif key_char == "k":
                print("🎹 Detected keyboard logger toggle")
    else:
        print(f"Keyboard event: {evt}")


# Add the handler to the Events class
Events.keyboard_event = keyboard_event
