#!/usr/bin/env python3
import sys
import os
import time
import signal
from time import ctime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading
import json
from .const import S


def log(*msg):
    print(*msg)
    if hasattr(S, "fn_fifo") and S.fn_fifo:
        logfile = f"{S.fn_fifo}.log"
        with open(logfile, "a") as f:
            f.write(" ".join(map(str, msg)) + "\n")
        S.lognr += 1
        if S.lognr < 1000:
            return
        with open(logfile, "w") as f:
            f.write("cleared log")
        S.lognr = 0


def pidfile():
    return (
        f"{S.fn_fifo}.pid"
        if hasattr(S, "fn_fifo") and S.fn_fifo
        else "/tmp/event_listener.pid"
    )


class EventHTTPHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Suppress default HTTP server logging
        pass

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        params = parse_qs(parsed.query)

        if path.startswith("/evt/"):
            event_type = path[5:]  # Remove '/evt/' prefix
            
            try:
                success = self.handle_event(event_type, params)
                
                if success:
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"status": "ok", "event": event_type}).encode())
                else:
                    self.send_response(404)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"status": "error", "message": f"Event type '{event_type}' not supported"}).encode())
            
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": "Event handling failed"}).encode())
        else:
            # Invalid path
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            error_response = {
                "status": "error",
                "message": "Invalid endpoint. Use /evt/{event_type}",
                "example": "/evt/space_changed?space_id=1&space_index=2"
            }
            self.wfile.write(json.dumps(error_response).encode())

    def handle_event(self, event_type, params):
        """Convert HTTP event to the format expected by event handlers"""
        try:
            if event_type == "space_changed":
                space_id = params.get("space_id", [""])[0]
                space_index = params.get("space_index", [""])[0]
                evt = ["space_changed", space_id, space_index]
            elif event_type == "window_focused":
                window_id = params.get("window_id", [""])[0]
                evt = ["window_focused", window_id]
            elif event_type == "window_destroyed":
                window_id = params.get("window_id", [""])[0]
                evt = ["window_destroyed", window_id]
            elif event_type == "keyboard_event":
                key_code = params.get("key_code", [""])[0]
                key_char = params.get("key_char", [""])[0]
                modifiers = params.get("modifiers", [""])[0]
                evt = ["keyboard_event", key_code, key_char, modifiers]
            else:
                # For any other event type, just pass the event name
                evt = [event_type]

            # Get the event handler and call it
            if hasattr(self.server, "event_handlers"):
                handler_method = getattr(self.server.event_handlers, event_type, None)
                if handler_method is None:
                    return False  # Event type not supported
                
                handler_method(evt)
                log(f"Handled event: {evt}")
                return True

        except Exception as e:
            log(f"Error handling event {event_type}: {e}")
            raise  # Re-raise exception to be caught by do_GET
        
        return False


def setup_http_listener(event_handlers, port=10888):
    """Setup HTTP server to listen for events"""
    server = HTTPServer(("127.0.0.1", port), EventHTTPHandler)
    server.event_handlers = event_handlers
    log(f"HTTP event server listening on http://127.0.0.1:{port}")

    # Run server in a separate thread so it doesn't block the GUI
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()

    return server


def run_event_listener(port=None, event_handlers_class=None, app_builder=None):
    """Main event listener runner with HTTP server"""
    # Use environment variable or default port
    if port is None:
        port = int(os.environ.get("OSX_EVTS_PORT", 10888))

    S.mode = "s"  # Default to space mode for HTTP
    S.fn_fifo = f"/tmp/event-listener-{port}"  # For logging purposes

    # Kill any existing process using PID file
    pid_file = pidfile()
    if os.path.exists(pid_file):
        try:
            with open(pid_file, "r") as f:
                old_pid = int(f.read().strip())

            # Check if process is still running
            try:
                os.kill(old_pid, 0)  # Signal 0 just checks if process exists
                log(f"Killing existing process {old_pid}")
                os.kill(old_pid, 15)  # SIGTERM
                time.sleep(1)  # Give it time to exit gracefully

                # Force kill if still running
                try:
                    os.kill(old_pid, 0)
                    log(f"Force killing process {old_pid}")
                    os.kill(old_pid, 9)  # SIGKILL
                except OSError:
                    pass  # Process already dead

            except OSError:
                # Process doesn't exist anymore
                pass

        except (ValueError, OSError) as e:
            log(f"Error reading/killing old process: {e}")

    # Write new PID
    with open(pid_file, "w") as f:
        f.write(str(os.getpid()))

    log(f"Starting HTTP event listener on port {port} {ctime()}")
    log(f"PID: {os.getpid()}, PID file: {pid_file}")

    try:
        if event_handlers_class is None:
            from events import EventHandlers

            event_handlers_class = EventHandlers

        if app_builder is None:
            from events import build_app

        event_handlers = event_handlers_class()
        server = setup_http_listener(event_handlers, port)
        app_builder(event_handlers)

    except KeyboardInterrupt:
        log("Interrupted by user")
    except Exception as e:
        log(f"Error: {e}")
        import traceback

        traceback.print_exc()
    finally:
        log("Exiting event listener...")
        if os.path.exists(pid_file):
            os.remove(pid_file)


if __name__ == "__main__":
    # Parse command line arguments
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"Error: Invalid port '{sys.argv[1]}'. Must be a number.")
            sys.exit(1)
    else:
        # Use environment variable or default
        port = int(os.environ.get("OSX_EVTS_PORT", 10888))

    print(f"Starting event listener on port {port}")

    # Import here to avoid circular dependencies
    from .events import EventHandlers, build_app

    run_event_listener(port, EventHandlers, build_app)
