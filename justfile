# OSX Automation System - Commands

# Default Python executable
python := ".venv/bin/python3"

# Default recipe - show available commands
default:
    @just --list

# Start the event listener
start:
    @echo "🚀 Starting OSX automation event listener..."
    @echo "Using OSX_EVTS_PORT environment variable (default: 10888)"
    @echo "Press Ctrl+C to stop"
    {{python}} -m src.event_listener

# Run all tests
test: test-env test-import test-simplified test-keyboard-menu test-startup test-http

# Test environment variable setup
test-env:
    @echo "🧪 Testing environment variable..."
    python3 test/test_env.py

# Test imports and basic functionality
test-import:
    @echo "🧪 Testing imports..."
    {{python}} test/test_import.py

# Test basic event handling
test-basic:
    @echo "🧪 Testing basic event handling..."
    {{python}} test/test_basic.py

# Test HTTP server functionality
test-http:
    @echo "🧪 Testing HTTP server..."
    {{python}} test/test_http.py

# Test HTTP error handling
test-http-errors:
    @echo "🧪 Testing HTTP error handling..."
    {{python}} test/test_http_errors.py

# Test simplified structure  
test-simplified:
    @echo "🧪 Testing simplified structure..."
    {{python}} test/test_simplified_structure.py

# Test keyboard menu behavior
test-keyboard-menu:
    @echo "🧪 Testing keyboard menu behavior..."
    {{python}} test/test_keyboard_menu_behavior.py

# Demo keyboard menu behavior
demo-keyboard:
    @echo "🎹 Demonstrating keyboard menu behavior..."
    {{python}} test/demo_keyboard_menu.py

# Show keyboard event documentation
docs-keyboard:
    @echo "📖 Opening keyboard event documentation..."
    @if command -v bat >/dev/null 2>&1; then \
        bat docs/keyboard_event.md; \
    elif command -v less >/dev/null 2>&1; then \
        less docs/keyboard_event.md; \
    else \
        cat docs/keyboard_event.md; \
    fi

# Test event listener startup
test-startup:
    @echo "🧪 Testing event listener startup..."
    {{python}} test/test_event_listener_startup.py

# Test Hammerspoon integration
test-hammerspoon:
    @echo "🧪 Testing Hammerspoon integration..."
    {{python}} test/test_hammerspoon_integration.py

# Verify Hammerspoon module structure
verify-hammerspoon:
    @echo "🔍 Verifying Hammerspoon structure..."
    {{python}} test/verify_hammerspoon_structure.py

# Verify project structure
verify-structure:
    @echo "🔍 Verifying project structure..."
    {{python}} test/verify_new_structure.py

# Start test HTTP server for manual testing
test-server:
    @echo "🚀 Starting test HTTP server..."
    @echo "Test with: curl 'http://127.0.0.1:10888/evt/space_changed?space_id=1&space_index=3'"
    {{python}} test/server_test.py

# Test full listener (GUI components)
test-listener:
    @echo "🧪 Testing full listener..."
    {{python}} test/test_listener.py

# Run quick verification tests
verify: test-env test-import
    @echo "✅ Quick verification complete!"

# Clean up test artifacts
clean:
    @echo "🧹 Cleaning up test artifacts..."
    rm -f /tmp/event-listener-*.pid
    rm -f /tmp/event-listener-*.log
    rm -f /tmp/yabai-*.fifo

# Show available tasks
help:
    @just --list
