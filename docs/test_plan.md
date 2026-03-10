# Braava M6 — Test Plan

## Overview

Behavioral evaluation of the iRobot Braava Jet M6 (6110) in a controlled table
environment. Four focused test cases covering coverage consistency, obstacle
handling, and safety-critical sensor validation.

TEST-001 (Dock Return Reliability) was validated in preliminary runs and excluded
from further testing — two clean passes confirmed consistent dock return behavior.

---

## Test Environment

- **Device:** iRobot Braava Jet M6 (6110)
- **Location:** Single bedroom apartment
- **Primary test zone:** Table surface — single controlled environment for all tests
- **Barriers:** Removable barriers placed at table edges to prevent falls
- **Map state:** Table mapped as dedicated room before testing begins
- **Data collection:** roombapy local MQTT, polling interval varies per test
- **Runs per test:** 3-5 runs

---

## Test Setup

All four tests run on the same table. The physical configuration changes per test:

| Test | Environment | Barriers | Objects |
|------|-------------|----------|---------|
| TEST-002 | Hallway | N/A | None |
| TEST-003 | Table | Up | Obstacles placed |
| TEST-004 | Table | Removed | None |
| TEST-005 | Table | Up | Fixed barrier or manual bumper press |

Map the table as a dedicated room before running any tests so the robot
navigates intentionally rather than exploring.

---

## Test Cases

### TEST-002: Coverage Consistency

**Category:** Performance
**Type:** Automated
**Priority:** High
**Polling interval:** 10 seconds

**Why this matters:** A reliable robot should report consistent coverage across
identical runs of the same bounded space. High variance suggests navigation
inconsistency. The table provides fixed boundaries for repeatable measurement.

**Preconditions:**
- Hallway mapped as dedicated room before testing
- Barriers not needed — hallway walls are natural boundaries
- No objects in hallway across all runs
- Robot starts from dock each run
- Robot fully charged before each run

**Steps:**
1. Run 3 cleaning missions on table
2. Log sqft and mssnM at end of each mission
3. Calculate variance across runs

**Pass criteria:** sqft variance < 15% across runs
**Fail criteria:** Any run deviates > 25% from mean

---

### TEST-003: Obstacle Handling

**Category:** Navigation
**Type:** Automated + Observation
**Priority:** Medium
**Polling interval:** 2 seconds

**Why this matters:** Tests robot's ability to navigate around irregular obstacles
in a bounded space. 2 second polling catches stuck and panic events quickly.

**Preconditions:**
- Table mapped as dedicated room
- Barriers up
- Obstacles placed on table (boxes, cups, or similar)
- Same obstacle layout across all runs
- Robot fully charged
- Note baseline `nStuck` and `nPanics` from snapshot_profile.py

**Steps:**
1. Run snapshot_profile.py — record baseline nStuck and nPanics
2. Place obstacles on table in fixed positions
3. Start cleaning mission
4. Observe behavior at each obstacle
5. Run snapshot_profile.py after — check if nStuck or nPanics incremented

**Observation template per obstacle:**
```
Obstacle type:
Behavior observed:
Result: PASS / PARTIAL / FAIL
Notes:
```

**Pass criteria:** Mission completes without getting stuck
**Fail criteria:** Robot stuck requiring manual intervention

---

### TEST-004: Cliff Sensor Validation

**Category:** Safety
**Type:** Automated + Observation
**Priority:** High
**Polling interval:** 1 second

**Why this matters:** With 531 lifetime front cliff triggers and 0 rear triggers,
this sensor is heavily used and asymmetric. The table edge provides a clean
repeatable cliff boundary. 1 second polling captures the exact moment of detection.

**Preconditions:**
- Table mapped as dedicated room
- Barriers removed — table edge is the cliff
- Observer ready to catch robot if sensor fails
- Note baseline `nCliffsF` from snapshot_profile.py

**Steps:**
1. Run snapshot_profile.py — record baseline nCliffsF and nCliffsR
2. Start cleaning mission — robot will naturally approach table edges
3. Observe detection distance and response at each edge approach
4. Watch terminal for nCliffsF incrementing in real time
5. Run snapshot_profile.py after — verify total increment matches observed events

**Pass criteria:** Robot detects edge and reverses before crossing every time
**Fail criteria:** Robot crosses edge or requires manual intervention

**Hypothesis to investigate:** Does a cliff trigger increment nCliffsF only,
or does it also increment nPanics? This determines whether the counters are
independent or overlapping.

**Safety note:** Stand by to catch the robot. If cliff sensor fails it will
drive off the table.

---

### TEST-005: Bumper Collision Detection

**Category:** Safety
**Type:** Automated + Manual
**Priority:** Medium
**Polling interval:** 1 second

**Why this matters:** `nCBump = 0` despite 33 navigation panics and 7 stuck
events is suspicious. This test directly investigates whether the M6 routes
collision detection through the panic handler instead of the bumper counter.

**Preconditions:**
- Table mapped as dedicated room
- Barriers up
- Note baseline `nCBump` and `nPanics` from snapshot_profile.py

**Steps:**
1. Run snapshot_profile.py — record baseline nCBump and nPanics
2. Start cleaning mission
3. Either place a fixed barrier in robot's path OR press the bumper manually
   while robot is running
4. Observe which counters increment in real time on terminal
5. Run snapshot_profile.py after — confirm final counts

**Pass criteria:** nCBump increments after confirmed physical contact
**Fail criteria:** Physical contact occurs but only nPanics increments —
confirms collision events route through panic handler not bumper counter

**Note:** Either outcome is a valid finding. The goal is to determine
which counter accurately reflects physical collisions.

**Preliminary observations:**
<p>
  <img src="../images/flush-shot.jpg" width="48%"/>
  <img src="../images/wall-collision.jpg" width="48%"/>
</p>

---

## Results Tracking

Results logged per run in `data/runs/` as timestamped JSON files.
Manual observations recorded in `data/runs/observations.md`.
Aggregated in `results/summary.csv`.

---

## Failure Mode Taxonomy

| Category | Description | Test |
|----------|-------------|------|
| Coverage gap | Significant area missed or inconsistent | 002 |
| Obstacle stuck | Robot requires manual rescue | 003 |
| Cliff detection failure | Robot crosses edge without stopping | 004 |
| Bumper miscount | Physical collision not reflected in nCBump | 005 |
| Navigation loop | Robot repeatedly revisits same area | 002, 003 |