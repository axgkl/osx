# Test Scripts

This directory contains test scripts for the OSX automation system.

## Test Scripts

### `test_env.py`
Tests if the `OSX_EVTS_PORT` environment variable is properly set via LaunchAgent.
```bash
cd /Users/gk/uv/osx
python3 test/test_env.py
```

### `test_import.py`
Tests basic imports to verify all modules can be loaded correctly.
```bash
cd /Users/gk/uv/osx
.venv/bin/python3 test/test_import.py
```

### `test_basic.py`
Tests basic event handling functionality without GUI components.
```bash
cd /Users/gk/uv/osx
.venv/bin/python3 test/test_basic.py
```

### `test_http.py`
Tests the HTTP server event handling with automated requests.
```bash
cd /Users/gk/uv/osx
.venv/bin/python3 test/test_http.py
```

### `server_test.py`
Starts a test HTTP server for manual testing with curl commands.
```bash
cd /Users/gk/uv/osx
.venv/bin/python3 test/server_test.py
# Then test with: curl "http://127.0.0.1:10888/evt/space_changed?space_id=1&space_index=3"
```

### `test_listener.py`
Tests the full event listener system without Lima dependencies.
```bash
cd /Users/gk/uv/osx
.venv/bin/python3 test/test_listener.py
```

### `test_pid_port.py`
Tests port detection and PID file management functionality.
```bash
cd /Users/gk/uv/osx
.venv/bin/python3 test/test_pid_port.py
```

### `test_default_port.py`
Tests default port behavior using environment variables.
```bash
cd /Users/gk/uv/osx
OSX_EVTS_PORT=10893 .venv/bin/python3 test/test_default_port.py
```

### `test_pid_kill.py`
Tests the process killing functionality when starting a new event listener.
```bash
cd /Users/gk/uv/osx
.venv/bin/python3 test/test_pid_kill.py
```

## Running All Tests

To run a quick verification of the system:

```bash
cd /Users/gk/uv/osx

# Test environment variable
python3 test/test_env.py

# Test imports
.venv/bin/python3 test/test_import.py

# Test HTTP server
.venv/bin/python3 test/test_http.py
```
