#!/usr/bin/env python3
from functools import partial
from .lima import Lima
from .const import FSPC, S, YabaiMenuApp, quit_app

import os
import json
import subprocess
from AppKit import NSWorkspace, NSRunningApplication, NSImage, NSBitmapImageRep

import sys
sys.path.insert(0, os.environ["HOME"] + "/.config/yabai")
from spec import arrange_spec

Y = "/opt/homebrew/bin/yabai"


def switchwin(_, wid):
    os.system(f"yabai -m window --focus {wid}")


def switchspace(_, sid):
    os.system(f"yabai -m space --focus {sid}")


def focus_win(win):
    if win["app"] == "Dock":
        return
    cmd = f"yabai -m window --focus {win['id']}"
    os.system(cmd)


def makeico(win):
    win["callback"] = partial(switchwin, wid=win["id"])
    win["menu"] = win.get("title", "")[:30]
    win["ico"] = get_app_icon(win)
    # focus_win(win)
    return win


d_icos = os.path.abspath(os.path.dirname(__file__)) + "/icos"


def get_app_icon(win):
    fn = f"{d_icos}/{win['app']}.png"
    if os.path.exists(fn):
        return fn
    id = NSRunningApplication.runningApplicationWithProcessIdentifier_
    app = id(win["pid"])
    if not app:
        return
    icon = app.icon()
    if not icon:
        return
    bitmap_rep = NSBitmapImageRep.imageRepWithData_(icon.TIFFRepresentation())
    png = bitmap_rep.representationUsingType_properties_
    with open(fn, "wb") as f:
        f.write(png(4, None))
    return fn


def rebuild_wins():
    old = {wid: w for wid, w in S.windows.items()}
    S.windows.clear()
    try:
        print("wins")
        output = os.popen(Y + " -m query --windows").read().strip()
        data = json.loads(output)
        S.windows = {w["id"]: old.get(w["id"]) or makeico(w) for w in data}
    except Exception:
        return


def toggle_darkmode(*_):
    cmd = "osascript -e 'tell application \"System Events\" to tell appearance preferences to set dark mode to not dark mode'"
    os.system(cmd)


def add_window(wid, add):
    w = S.windows.get(wid)
    if w is None:
        rebuild_wins()
        w = S.windows.get(wid)
        if not w:
            return
    add(w["menu"], w["callback"], ico=w["ico"])


def system_sleep(_):
    os.system("pmset sleepnow")


def yabai_restart(_):
    os.system("yabai --restart-service")


sep = "─"


def querywin(win):
    win = {}
    try:
        output = os.popen(Y + " -m query --windows --window").read().strip()
        win = json.loads(output)
        win["ico"] = get_app_icon(win)
    except Exception:
        pass
    S.cur_win = win
    return win


def window(wid):
    S.windows[wid] = win = S.windows.get(wid) or querywin(wid)
    return win


def mv_win(win):
    a = win["app"].lower()
    for nr, app in arrange_spec:
        if app in a:
            cmd = Y + f" -m window {win['id']} --space {nr}"
            return os.system(cmd)


def spaces():
    output = os.popen(Y + " -m query --spaces").read().strip()
    return json.loads(output)


def arrange_wins(*_):
    output = os.popen(Y + " -m query --windows").read().strip()
    wins = json.loads(output)
    [mv_win(win) for win in wins]
    s = len(spaces())
    [os.system(Y + f" -m space {nr} --balance") for nr in range(s)]


def build_spc_menu(_=None):
    S.app.menu.clear()
    S.app.add("🔁 Refresh Menu", build_spc_menu)
    S.app.add("🧹 Arrange", arrange_wins)
    S.app.add("☯ Dark/White", toggle_darkmode)
    S.app.add("🌙 System Sleep", system_sleep)
    S.app.add("🔁 Restart Yabai", yabai_restart)
    S.app.add("🚪Quit Menu", quit_app)
    Lima.build_menu()


# def start_docker_default(_):
#     cmd = "docker context use lima-docker-default"
#     os.system(cmd)
#     cmd = "docker start gk-docker"
#     os.system(cmd)
#     cmd = "docker ps -a"
#     output = os.popen(cmd).read().strip()
#     log(output)


noop = lambda *_: None
wins = [
    ["title", noop, ""],
    "id",
    "pid",
    "app",
    "scratchpad",
    "frame",
    "role",
    "subrole",
    "root-window",
    "display",
    "space",
    "level",
    "sub-level",
    "layer",
    "sub-layer",
    "opacity",
    "split-type",
    "split-child",
    "stack-index",
    "can-move",
    "can-resize",
    "has-focus",
    "has-shadow",
    "has-parent-zoom",
    "has-fullscreen-zoom",
    "has-ax-reference",
    "is-native-fullscreen",
    "is-visible",
    "is-minimized",
    "is-hidden",
    "is-floating",
    "is-sticky",
    "is-grabbed",
]
wins = [w if isinstance(w, list) else [w] for w in wins]


def win_menu_add(key, cb=None, title=None):
    if not S.app:
        return
    if title is None:
        title = f"{key}:"
    v = S.cur_win.get(key, "")
    cb = noop
    S.app.add(f"{title}{v}", cb)


def build_win_menu():
    if not S.app:
        return
    S.app.menu.clear()
    for l in wins:
        win_menu_add(*l)


class EventHandlers:
    def none(self, evt):
        print(evt)

    def space_changed(self, evt: list):
        spaceidx = int(evt[2])
        S.menutitle["space"] = FSPC.get(spaceidx, 1)
        if S.app:
            S.app.set_title()

    def window_destroyed(self, evt: list):
        S.windows.pop(evt[1], 0)

    def window_focused(self, evt: list):
        print(len(S.windows))
        wid = evt[1]
        fnico = window(wid)["ico"]
        if fnico and S.app:
            S.app.icon = fnico
        build_win_menu()

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

    # def ghostty_created(self, evt: list):
    #     os.system('yabai -m query --spaces --space |jq ".index" ')


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



