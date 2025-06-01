"""Window created event handler module"""
from ..const import Events, S


def window_created(self, evt: list):
    """Handle window created events from yabai"""
    # Import here to avoid circular imports
    from ..window import rebuild_wins
    
    print(f"Window created: {evt}")
    # Rebuild windows list to include the new window
    rebuild_wins()


# Add the handler to the Events class
Events.window_created = window_created
