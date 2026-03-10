#!/usr/bin/env python3
"""
collect_state.py
----------------
Polls Braava M6 state during a live cleaning run.
Each test ID uses different fields and polling frequency.

Usage:
    python scripts/collect_state.py --test TEST-002
    python scripts/collect_state.py --test TEST-003
    python scripts/collect_state.py --test TEST-004
    python scripts/collect_state.py --test TEST-005

Then start your mission from the iRobot app.
Hit Ctrl+C when mission is complete.
"""

import json
import time
import os
import argparse
from datetime import datetime
from roombapy import RoombaFactory
from dotenv import load_dotenv

load_dotenv()

ROBOT_IP = os.getenv("ROBOT_IP")
BLID     = os.getenv("BLID")
PASSWORD = os.getenv("PASSWORD")

OUTPUT_DIR = "data/runs"

# ---------------------------------------------------------------
# Per-test configuration
# fields: what to extract from the state blob
# interval: seconds between snapshots
# notes: what this test is looking for
# ---------------------------------------------------------------
TEST_CONFIGS = {
    "TEST-002": {
        "interval": 10,
        "notes": "Coverage consistency — sqft and mission time across runs",
        "fields": [
            "phase", "cycle", "mssnM", "batPct", "sqft", "tankLvl"
        ]
    },
    "TEST-003": {
        "interval": 2,
        "notes": "Obstacle handling — catch stuck/panic events quickly",
        "fields": [
            "phase", "cycle", "error", "mssnM", "batPct",
            "nStuck", "nPanics"
        ]
    },
    "TEST-004": {
        "interval": 1,
        "notes": "Cliff sensor — capture exact moment of cliff detection",
        "fields": [
            "phase", "error", "nCliffsF", "nCliffsR", "nPanics"
        ]
    },
    "TEST-005": {
        "interval": 1,
        "notes": "Bumper collision — does nCBump increment on physical contact",
        "fields": [
            "phase", "error", "nCBump", "nPanics", "nStuck"
        ]
    },
}

def extract_snapshot(state, fields):
    """Extract only the fields specified by the test config."""
    reported = state.get("state", {}).get("reported", {})
    mission  = reported.get("cleanMissionStatus", {})
    bbrun    = reported.get("bbrun", {})
    runtime  = reported.get("runtimeStats", {})

    # Map field names to their locations in the blob
    field_map = {
        "phase":    mission.get("phase"),
        "cycle":    mission.get("cycle"),
        "error":    mission.get("error"),
        "mssnM":    mission.get("mssnM"),
        "batPct":   reported.get("batPct"),
        "sqft":     runtime.get("sqft"),
        "tankLvl":  reported.get("tankLvl"),
        "nStuck":   bbrun.get("nStuck"),
        "nPanics":  bbrun.get("nPanics"),
        "nCliffsF": bbrun.get("nCliffsF"),
        "nCliffsR": bbrun.get("nCliffsR"),
        "nCBump":   bbrun.get("nCBump"),
    }

    snapshot = {"timestamp": datetime.now().isoformat()}
    for field in fields:
        snapshot[field] = field_map.get(field)

    return snapshot

def main():
    parser = argparse.ArgumentParser(description="Braava M6 state collector")
    parser.add_argument(
        "--test",
        required=True,
        choices=TEST_CONFIGS.keys(),
        help="Test ID to run (e.g. TEST-002)"
    )
    args = parser.parse_args()

    config   = TEST_CONFIGS[args.test]
    interval = config["interval"]
    fields   = config["fields"]

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    run_id   = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(OUTPUT_DIR, f"run_{run_id}_{args.test}.json")

    print("================================")
    print(f"   Braava M6 — {args.test}")
    print(f"   {config['notes']}")
    print(f"   Polling every {interval}s")
    print("================================")
    print(f"Connecting to {ROBOT_IP}...")

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
    print("Start your mission from the iRobot app.")
    print("Press Ctrl+C when complete.\n")

    snapshots = []

    try:
        while True:
            state    = roomba.master_state
            snapshot = extract_snapshot(state, fields)

            if snapshot.get("phase") is not None:
                snapshots.append(snapshot)

                # Build a compact live status line from available fields
                status = " | ".join(
                    f"{k}={v}"
                    for k, v in snapshot.items()
                    if k != "timestamp" and v is not None
                )
                print(f"[{snapshot['timestamp']}] {status}")
            else:
                print(f"[{snapshot['timestamp']}] disconnected — waiting...")

            time.sleep(interval)

    except KeyboardInterrupt:
        print("\nStopping collection...")

    finally:
        with open(filepath, "w") as f:
            json.dump(snapshots, f, indent=2)

        roomba.disconnect()
        print(f"Saved {len(snapshots)} snapshots to {filepath}")
        print("Disconnected cleanly.")

if __name__ == "__main__":
    main()