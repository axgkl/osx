"""Window destroyed event handler module"""
from ..const import Events, S


def window_destroyed(self, evt: list):
    """Handle window destroyed events from yabai"""
    S.windows.pop(evt[1], 0)


# Add the handler to the Events class
Events.window_destroyed = window_destroyed
