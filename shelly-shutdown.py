#!/usr/bin/env python3

import requests
import sys
EXPECTED_TOKEN = "<YOUR_TOKEN_HERE>"
SHELLY_IP = "<SHELLY_IP_ADDRESS>"
SCRIPT_ID = "<SHELLY_SCRIPT_ID>"

def notify_shelly(event_type="shutdown"):
    """
    Send notification to Home Assistant
    Args:
        event_type: Type of event (shutdown, startup, etc.)
    """
    try:
        # Replace with your Home Assistant details
		shelly_url = f"http://{SHELLY_IP}/script/{SCRIPT_ID}/shutdown"        
        # Send webhook with event data
        payload = {
            "action": event_type,
            "token": EXPECTED_TOKEN
        }
        
        response = requests.post(shelly_url, json=payload, timeout=5)
        
        if response.status_code == 200:
            print(f"Shelly notified successfully: {event_type}")
            return True
        else:
            print(f"Shelly notification failed: {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print("Shelly notification timed out")
        return False
    except Exception as e:
        print(f"Failed to notify Shelly: {e}")
        return False

if __name__ == "__main__":
    # Get event type from command line argument, default to "shutdown"
    event = sys.argv[1] if len(sys.argv) > 1 else "shutdown"
    notify_shelly(event)