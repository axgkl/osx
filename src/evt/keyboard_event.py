"""Keyboard event handler module"""
from ..const import Events, S


# Unicode symbols for modifier keys
MODIFIER_SYMBOLS = {
    'cmd': '⌘',
    'ctrl': '⌃', 
    'alt': '⌥',
    'shift': '⇧',
    'fn': '🌐'
}


def format_modifiers(modifiers_str):
    """Convert modifier string to unicode symbols"""
    if not modifiers_str or modifiers_str == "system":
        return ""
    
    modifiers = modifiers_str.split(',')
    symbols = []
    
    for mod in modifiers:
        mod = mod.strip().lower()
        if mod in MODIFIER_SYMBOLS:
            symbols.append(MODIFIER_SYMBOLS[mod])
        else:
            symbols.append(mod)  # fallback to text
    
    return ''.join(symbols)


def format_key_display(key_char, modifiers_str):
    """Format the key and modifiers for display"""
    mod_symbols = format_modifiers(modifiers_str)
    
    # Handle special keys
    key_display = key_char
    if key_char == "space":
        key_display = "␣"
    elif key_char == "return" or key_char == "enter":
        key_display = "↩"
    elif key_char == "tab":
        key_display = "⇥"
    elif key_char == "escape":
        key_display = "⎋"
    elif key_char == "delete":
        key_display = "⌫"
    elif key_char == "backspace":
        key_display = "⌫"
    elif key_char == "up":
        key_display = "↑"
    elif key_char == "down":
        key_display = "↓"
    elif key_char == "left":
        key_display = "←"
    elif key_char == "right":
        key_display = "→"
    elif key_char == "unknown":
        key_display = "?"
    
    return f"{mod_symbols}{key_display}"


def keyboard_event(self, evt: list):
    """Handle keyboard events from Hammerspoon"""
    if len(evt) >= 4:
        key_code, key_char, modifiers = evt[1], evt[2], evt[3]
        
        # Handle system events (logger start/stop)
        if modifiers == "system":
            if key_char == "logger_started":
                print("🎹 Keyboard logger started in Hammerspoon")
                S.menutitle["keyboard"] = "🎹"
                S.menutitle["keypress"] = ""  # Initialize keypress display
            elif key_char == "logger_stopped":
                print("⏸️ Keyboard logger stopped in Hammerspoon")
                S.menutitle.pop("keyboard", None)
                S.menutitle.pop("keypress", None)  # Remove keypress display
            if S.app:
                S.app.set_title()
            return
        
        # Handle regular keyboard events - show current keypress
        print(f"Keyboard event: {key_char} (code: {key_code}) modifiers: {modifiers}")
        
        # Only update display if keyboard logger is active
        if "keyboard" in S.menutitle:
            key_display = format_key_display(key_char, modifiers)
            S.menutitle["keypress"] = key_display
            
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
