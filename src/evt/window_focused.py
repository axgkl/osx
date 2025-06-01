"""Window focused event handler module"""
from ..const import Events, S


def window_focused(self, evt: list):
    """Handle window focused events from yabai"""
    # Import here to avoid circular imports
    from ..window import window, build_win_menu
    
    print(len(S.windows))
    wid = evt[1]
    fnico = window(wid)["ico"]
    if fnico and S.app:
        S.app.icon = fnico
    build_win_menu()


# Add the handler to the Events class
Events.window_focused = window_focused
