#!/usr/bin/env python3
"""
connect.py
----------
Connects to Braava M6 and prints current robot state.
Run this first to verify credentials and connection are working.

Usage:
    python connect.py
"""

import json
import time
from roombapy import RoombaFactory
from dotenv import load_dotenv
import os

load_dotenv()

ROBOT_IP = os.getenv("ROBOT_IP")
BLID     = os.getenv("BLID")
PASSWORD = os.getenv("PASSWORD")

def main():
    print("================================")
    print("   Braava M6 — Connection Test")
    print("================================")
    print(f"Connecting to {ROBOT_IP}...")

    try:
        # Connect to robot
        roomba = RoombaFactory.create_roomba(
            address=ROBOT_IP,
            blid=BLID,
            password=PASSWORD,
            continuous=False
        )

        roomba.connect()
        print("Connected successfully!")
        print("")

        # Give it a moment to receive state data
        print("Reading robot state...")
        time.sleep(3)

        # Print full state
        state = roomba.master_state
        print("--------------------------------")
        print("Current Robot State:")
        print("--------------------------------")
        print(json.dumps(state, indent=2))
        print("--------------------------------")

        # Pull out key fields
        status = state.get("state", {}).get("reported", {})
        print(f"\nBattery:  {status.get('batPct', 'N/A')}%")
        print(f"Phase:    {status.get('cleanMissionStatus', {}).get('phase', 'N/A')}")
        print(f"Name:     {status.get('name', 'N/A')}")

        roomba.disconnect()
        print("\nDisconnected cleanly.")
        print("================================")

    except Exception as e:
        print(f"Connection failed: {e}")
        print("Check your IP, BLID, and password.")

if __name__ == "__main__":
    main()