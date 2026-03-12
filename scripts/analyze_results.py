#!/usr/bin/env python3
"""
analyze_results.py
------------------
Reads all JSON run logs from data/runs/ and generates a summary CSV.
Calculates mission duration, dock return time, battery drain, and pass/fail.

Usage:
    python scripts/analyze_results.py
"""

import json
import csv
import os
from datetime import datetime

INPUT_DIR  = "data/runs"
OUTPUT_DIR = "results"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "summary.csv")

def parse_timestamp(ts):
    return datetime.fromisoformat(ts)

def analyze_run(filepath, test_id="UNKNOWN"):
    with open(filepath, "r") as f:
        snapshots = json.load(f)

    if not snapshots:
        return None

    filename = f"{test_id} | {os.path.basename(filepath).replace('.json', '')}"

    # --- Basic info ---
    date = snapshots[0]["timestamp"][:10]
    battery_start = None
    battery_end   = None

    # --- Phase tracking ---
    run_start     = None
    run_end       = None
    homing_start  = None
    charge_time   = None
    errors        = []

    for snap in snapshots:
        phase = snap.get("phase")
        ts    = parse_timestamp(snap["timestamp"])
        bat   = snap.get("batPct")
        error = snap.get("error")

        # Battery
        if bat is not None:
            if battery_start is None:
                battery_start = bat
            battery_end = bat

        # Error codes
        if error and error != 0:
            errors.append(f"{snap['timestamp']}: error={error}")

        # Phase transitions
        if phase == "run" and run_start is None:
            run_start = ts

        if phase == "hmPostMsn" and run_end is None:
            run_end = ts

        if phase == "hmPostMsn" and homing_start is None:
            homing_start = ts

        if phase == "charge" and homing_start is not None and charge_time is None:
            charge_time = ts

    # --- Calculations ---
    duration_min = None
    if run_start and run_end:
        duration_min = round((run_end - run_start).total_seconds() / 60, 1)

    dock_time_sec = None
    if homing_start and charge_time:
        dock_time_sec = round((charge_time - homing_start).total_seconds())

    battery_drain = None
    if battery_start is not None and battery_end is not None:
        battery_drain = battery_start - battery_end

    # --- Pass/fail ---
    docked = charge_time is not None
    has_errors = len(errors) > 0

    if "invalid" in filename:
        result = "INVALID"
    elif docked and not has_errors:
        result = "PASS"
    elif not docked:
        result = "FAIL - no dock"
    else:
        result = "FAIL - errors"

    return {
        "run_id":         filename,
        "date":           date,
        "duration_min":   duration_min,
        "dock_return":    "YES" if docked else "NO",
        "dock_time_sec":  dock_time_sec,
        "battery_start":  battery_start,
        "battery_end":    battery_end,
        "battery_drain":  battery_drain,
        "errors":         "; ".join(errors) if errors else "none",
        "result":         result,
    }

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Analyze Braava M6 test run logs")
    parser.add_argument("--test", help="Filter by test ID (e.g. TEST-002). Omit to analyze all.")
    args = parser.parse_args()

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Get all JSON files in data/runs/
    files = []
    for test_id in sorted(os.listdir(INPUT_DIR)):
        if args.test and test_id != args.test:
            continue
        test_path = os.path.join(INPUT_DIR, test_id)
        if os.path.isdir(test_path):
            for f in sorted(os.listdir(test_path)):
                if f.endswith(".json"):
                    files.append((test_id, os.path.join(test_path, f)))

    if not files:
        print("No JSON files found in data/runs/")
        return

    results = []
    for test_id, filepath in files:
            print(f"Analyzing: {os.path.basename(filepath)}")
            result = analyze_run(filepath, test_id)
            if result:
                results.append(result)

    # Write CSV
    fieldnames = [
        "run_id", "date", "duration_min", "dock_return",
        "dock_time_sec", "battery_start", "battery_end",
        "battery_drain", "errors", "result"
    ]

    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"\nSummary written to {OUTPUT_FILE}")
    print(f"Total runs analyzed: {len(results)}")

    # Print table to terminal
    print("\n--- Results ---")
    for r in results:
        print(f"{r['run_id'][:40]:<40} | {r['result']:<20} | "
              f"duration={r['duration_min']}min | "
              f"dock_time={r['dock_time_sec']}s | "
              f"battery_drain={r['battery_drain']}%")

if __name__ == "__main__":
    main()