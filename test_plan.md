# Braava M6 — Test Plan

## Overview

Behavioral evaluation of the iRobot Braava Jet M6 (6110) in a real home environment.
Three focused test cases covering the most critical aspects of robot mop behavior —
dock return navigation, coverage consistency, and obstacle handling.

---

## Test Environment

- **Device:** iRobot Braava Jet M6 (6110)
- **Location:** Single bedroom apartment
- **Primary test zone:** Dead-end hallway (~25ft), hardwood/tile surface
- **Secondary test zone:** Kitchen with obstacles (chair legs, trash bin, recycle bin, boxes)
- **Dock location:** Living room at hallway entrance
- **Map state:** No pre-existing map — robot builds from scratch
- **Data collection:** roombapy local MQTT, state polled every 5 seconds
- **Runs per test:** 3-5 runs

---

## Test Cases

### TEST-001: Dock Return Reliability

**Category:** Navigation
**Type:** Automated + Observation
**Priority:** High

**Why this matters:** The hallway is a dead end. The robot must navigate back out
and locate the dock in the living room after cleaning. This is a non-trivial
navigation challenge — getting in is easy, getting back is the real test.

**Preconditions:**
- Robot fully charged
- Dock in living room at hallway entrance
- Hallway clear of obstacles

**Steps:**
1. Start cleaning mission
2. Allow mission to complete naturally
3. Log final phase — did it reach "charge" state?
4. Record time from mission end to successful dock

**Pass criteria:** `cleanMissionStatus.phase == "charge"` within 3 minutes of mission end
**Fail criteria:** phase = "stuck" or "error", or robot cannot locate dock

---

### TEST-002: Coverage Consistency

**Category:** Performance
**Type:** Automated
**Priority:** High

**Why this matters:** A reliable robot should report consistent coverage across
identical runs of the same space. High variance suggests navigation inconsistency.

**Preconditions:**
- Same hallway layout across all runs
- Robot fully charged before each run
- No changes to environment between runs

**Steps:**
1. Run 3 cleaning missions on same hallway
2. Log `sqft` reported at end of each mission
3. Log mission duration per run
4. Calculate variance across runs

**Pass criteria:** sqft variance < 15% across runs
**Fail criteria:** Any run deviates > 25% from mean — indicates inconsistent coverage

---

### TEST-003: Obstacle Handling

**Category:** Navigation
**Type:** Manual Observation
**Priority:** Medium

**Why this matters:** Kitchen environment represents real-world complexity —
chair legs, bins, and boxes test the robot's ability to navigate tight spaces
with irregular obstacles.

**Preconditions:**
- Kitchen in normal state — no obstacles removed or added
- Chair legs, trash bin, recycle bin, boxes present
- Robot fully charged

**Steps:**
1. Start cleaning mission in kitchen
2. Observe and note behavior at each obstacle type
3. Record whether robot gets stuck, avoids, or navigates through

**Observation template per obstacle:**
```
Obstacle type:
Behavior observed:
Time spent:
Result: PASS / PARTIAL / FAIL
Notes:
```

**Pass criteria:** Mission completes without getting stuck
**Fail criteria:** Robot stuck requiring manual intervention

---

## Results Tracking

Results logged per run in `data/runs/` as timestamped JSON files.
Manual observations recorded in `data/runs/observations.md`.
Aggregated in `results/summary.csv`.

---

## Failure Mode Taxonomy

| Category | Description | Test |
|----------|-------------|------|
| Dock failure | Cannot locate or return to dock | 001 |
| Coverage gap | Significant area missed or inconsistent | 002 |
| Obstacle stuck | Robot requires manual rescue | 003 |
| Navigation loop | Robot repeatedly revisits same area | 001, 002 |