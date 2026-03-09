#!/usr/bin/env python3
"""
snapshot_profile.py
-------------------
One-time script to capture baseline robot profile before testing begins.
Prints all relevant lifetime stats cleanly to terminal.

Usage:
    python snapshot_profile.py
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

def main():
    roomba = RoombaFactory.create_roomba(
        address=ROBOT_IP,
        blid=BLID,
        password=PASSWORD,
        continuous=False
    )

    roomba.connect()
    print("Connected. Waiting for state...")
    time.sleep(5)

    state    = roomba.master_state
    reported = state.get("state", {}).get("reported", {})
    mission  = reported.get("cleanMissionStatus", {})
    bbrun    = reported.get("bbrun", {})
    bbmssn   = reported.get("bbmssn", {})
    bbchg    = reported.get("bbchg", {})
    bbchg3   = reported.get("bbchg3", {})
    batinfo  = reported.get("batInfo", {})
    runtime  = reported.get("runtimeStats", {})
    hw       = reported.get("hwPartsRev", {})

    print("\n========================================")
    print("   Braava M6 — Initial Robot Profile")
    print(f"   Captured: {datetime.now().isoformat()}")
    print("========================================")

    print("\n--- Device Info ---")
    print(f"Name:        {reported.get('name')}")
    print(f"SKU:         {reported.get('sku')}")
    print(f"Firmware:    {reported.get('softwareVer')}")
    print(f"IMU:         {hw.get('imuPartNo')}")

    print("\n--- Mission History ---")
    print(f"Total missions:       {bbmssn.get('nMssn')}")
    print(f"Successful:           {bbmssn.get('nMssnOk')}")
    print(f"Failed:               {bbmssn.get('nMssnF')}")
    print(f"Avg duration (min):   {bbmssn.get('aMssnM')}")
    print(f"Avg cycle (min):      {bbmssn.get('aCycleM')}")

    print("\n--- Error & Stuck History ---")
    print(f"Times stuck:          {bbrun.get('nStuck')}")
    print(f"Navigation panics:    {bbrun.get('nPanics')}")
    print(f"Cliff triggers (F):   {bbrun.get('nCliffsF')}")
    print(f"Cliff triggers (R):   {bbrun.get('nCliffsR')}")
    print(f"Bumper collisions:    {bbrun.get('nCBump')}")
    print(f"Wheel stalls:         {bbrun.get('nWStll')}")
    print(f"Overtemps:            {bbrun.get('nOvertemps')}")

    print("\n--- Battery Health ---")
    print(f"Current charge:       {reported.get('batPct')}%")
    print(f"Estimated capacity:   {bbchg3.get('estCap')} mAh")
    print(f"Cycles available:     {bbchg3.get('nAvail')}")
    print(f"Successful charges:   {bbchg.get('nChgOk')}")
    print(f"Charge count:         {batinfo.get('cCount')}")
    print(f"Manufacturer:         {batinfo.get('mName')}")
    print(f"Manufacture date:     {batinfo.get('mDate')}")

    print("\n--- Runtime Stats ---")
    print(f"Total sqft cleaned:   {runtime.get('sqft')}")
    print(f"Total hours:          {runtime.get('hr')}")
    print(f"Total minutes:        {runtime.get('min')}")

    print("\n--- Hardware ---")
    print(f"Tank level:           {reported.get('tankLvl')}%")
    print(f"Tank present:         {reported.get('tankPresent')}")
    print(f"Pad detected:         {reported.get('detectedPad')}")
    print(f"Lid open:             {reported.get('lidOpen')}")

    roomba.disconnect()
    print("\nDone. Copy output above into initial_robot_profile.md")

if __name__ == "__main__":
    main()