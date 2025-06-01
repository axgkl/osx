#!/usr/bin/env python3
"""
Test script to verify OSX_EVTS_PORT environment variable is available
"""
import os
import sys

def test_env_var():
    evtsport = os.environ.get('OSX_EVTS_PORT')
    
    if evtsport:
        print(f"✅ OSX_EVTS_PORT is set to: {evtsport}")
        return True
    else:
        print("❌ OSX_EVTS_PORT is not set")
        
        # Try getting it from launchctl
        try:
            import subprocess
            result = subprocess.run(['launchctl', 'getenv', 'OSX_EVTS_PORT'], 
                                  capture_output=True, text=True)
            if result.returncode == 0 and result.stdout.strip():
                print(f"✅ OSX_EVTS_PORT available via launchctl: {result.stdout.strip()}")
                return True
        except:
            pass
            
        print("❌ OSX_EVTS_PORT not available via launchctl either")
        return False

if __name__ == "__main__":
    success = test_env_var()
    print(f"\nEnvironment variable test: {'PASSED' if success else 'FAILED'}")
    
    if success:
        print("\n🎉 Ready to use ${OSX_EVTS_PORT} in yabai configuration!")
    else:
        print("\n⚠️  May need to restart applications or log out/in for changes to take effect")
