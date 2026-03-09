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
    # print(f"Connecting to {ROBOT_IP}...")
    print(f"Connecting to Robot IP Address...")

    roomba = RoombaFactory.create_roomba(
        address=ROBOT_IP,
        blid=BLID,
        password=PASSWORD,
        continuous=False
    )

    roomba.connect()
    print("Connected. Waiting for state...")
    time.sleep(5)

    state = roomba.master_state
    reported = state.get("state", {}).get("reported", {})

    print("\n--- Robot Status ---")
    print(f"Name:       {reported.get('name')}")
    print(f"Battery:    {reported.get('batPct')}%")
    print(f"Tank level: {reported.get('tankLvl')}%")
    print(f"Phase:      {reported.get('cleanMissionStatus', {}).get('phase')}")
    print(f"Firmware:   {reported.get('softwareVer')}")
    print(f"Pad detected: {reported.get('detectedPad')}")
    print("--------------------\n")

    roomba.disconnect()
    print("Disconnected cleanly.")

if __name__ == "__main__":
    main()