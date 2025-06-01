#!/usr/bin/env python3
"""
Example showing keyboard event integration between Hammerspoon and OSX automation system
"""

def show_hammerspoon_integration():
    """Show how to integrate with Hammerspoon"""
    
    print("=== Keyboard Event Integration Example ===\n")
    
    print("1. Your Hammerspoon already has a key logger with Cmd+Ctrl+K toggle")
    print("2. To send events to the OSX automation system, modify ~/.hammerspoon/init.lua\n")
    
    print("Add this function to send HTTP events:")
    print("""
-- Function to send HTTP event to OSX automation system
local function sendHTTPEvent(event_type, params)
    local port = os.getenv("OSX_EVTS_PORT") or "10888"
    local url = string.format("http://127.0.0.1:%s/evt/%s", port, event_type)
    local paramStr = ""
    for key, value in pairs(params) do
        if paramStr ~= "" then paramStr = paramStr .. "&" end
        paramStr = paramStr .. key .. "=" .. tostring(value)
    end
    if paramStr ~= "" then url = url .. "?" .. paramStr end
    
    hs.http.get(url, nil, function(status, body, headers)
        -- Optional: handle response
        if status ~= 200 then
            print("Failed to send event: " .. tostring(status))
        end
    end)
end
""")
    
    print("\n3. Modify your existing keyLogger to send events:")
    print("""
-- Modified key logger to send events via HTTP
local keyLogger = HS.eventtap.new({ HS.eventtap.event.types.keyDown }, function(evt)
    local keyCode = evt:getKeyCode()
    local flags = evt:getFlags()
    local char = HS.keycodes.map[keyCode]
    
    -- Print to console (existing behavior)
    print(string.format("%s key - keyCode: %d, modifiers: %s", char or "nil", keyCode, HS.inspect(flags)))
    
    -- Send to OSX automation system
    sendHTTPEvent("keyboard_event", {
        key_code = keyCode,
        key_char = char or "unknown",
        modifiers = table.concat(hs.fnutils.keys(flags), ",")
    })
    
    return false
end)
""")
    
    print("\n4. Test the integration:")
    print("   - Start the event listener: .venv/bin/python3 event_listener.py")
    print("   - Toggle key logger in Hammerspoon: Cmd+Ctrl+K")
    print("   - Press some keys and see them appear in both:")
    print("     * Hammerspoon Console")
    print("     * OSX automation system logs")
    
    print("\n5. The keyboard events will:")
    print("   - Show up in the menu bar with ⌨️ indicator")
    print("   - Be logged in the event listener")
    print("   - Can trigger custom actions based on key combinations")

if __name__ == "__main__":
    show_hammerspoon_integration()
