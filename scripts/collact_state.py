#!/usr/bin/env python3
"""
collect_state.py
----------------
Polls Braava M6 state every 5 seconds during a live cleaning run.
Saves timestamped snapshots to data/runs/ as a JSON log file.

Usage:
    python collect_state.py
    Then start cleaning mission from iRobot app.
    Hit Ctrl+C when mission is complete.
"""

import json
import time
import os
from datetime import datetime
from roombapy import RoombaFactory
from dotenv import load_dotenv

load_dotenv()

ROBOT_IP = os.getenv("ROBOT_IP")
BLID     = os.getenv("BLID")
PASSWORD = os.getenv("PASSWORD")

POLL_INTERVAL = 5  # seconds between snapshots
OUTPUT_DIR    = "data/runs"

def extract_snapshot(state):
    """Pull only the fields we care about from the full state blob."""
    reported = state.get("state", {}).get("reported", {})
    mission  = reported.get("cleanMissionStatus", {})

    return {
        "timestamp":  datetime.now().isoformat(),
        "phase":      mission.get("phase"),
        "cycle":      mission.get("cycle"),
        "error":      mission.get("error"),
        "notReady":   mission.get("notReady"),
        "mssnM":      mission.get("mssnM"),
        "batPct":     reported.get("batPct"),
        "sqft":       reported.get("runtimeStats", {}).get("sqft"),
        "tankLvl":    reported.get("tankLvl"),
        "detectedPad": reported.get("detectedPad"),
    }

def main():
    # Create output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Generate timestamped filename for this run
    run_id   = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(OUTPUT_DIR, f"run_{run_id}.json")

    print("================================")
    print("   Braava M6 — State Collector")
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

    print(f"Logging to: {filepath}")
    print("Start your cleaning mission in the iRobot app.")
    print("Press Ctrl+C when the mission is complete.\n")

    snapshots = []

    try:
        while True:
            state    = roomba.master_state
            snapshot = extract_snapshot(state)
            snapshots.append(snapshot)

            # Print live status to terminal
            print(f"[{snapshot['timestamp']}] phase={snapshot['phase']} | "
                  f"bat={snapshot['batPct']}% | sqft={snapshot['sqft']} | "
                  f"error={snapshot['error']}")

            time.sleep(POLL_INTERVAL)

    except KeyboardInterrupt:
        print("\nStopping collection...")

    finally:
        # Always save and disconnect even if something goes wrong
        with open(filepath, "w") as f:
            json.dump(snapshots, f, indent=2)

        roomba.disconnect()
        print(f"Saved {len(snapshots)} snapshots to {filepath}")
        print("Disconnected cleanly.")

if __name__ == "__main__":
    main()