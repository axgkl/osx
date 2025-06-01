"""Space changed event handler module"""
from ..const import Events, S, FSPC


def space_changed(self, evt: list):
    """Handle space changed events from yabai"""
    spaceidx = int(evt[2])
    S.menutitle["space"] = FSPC.get(spaceidx, 1)
    if S.app:
        S.app.set_title()


# Add the handler to the Events class
Events.space_changed = space_changed
