# Robot Profile — Device Under Test

## Device Info
- **Name:** RoboMop
- **SKU:** m611220
- **Firmware:** sanmarino+22.29.6+2022-12-01-82f3372a65c+Firmware-Build+2321
- **Captured:** 2026-03-08

---

## Baseline Lifetime Stats (pre-testing)

These values were captured before any test runs in this evaluation.
They provide context for the robot's history and wear state going in.

### Mission History
| Field | Value | Meaning |
|-------|-------|---------|
| nMssn | 10 | Total missions run lifetime |
| nMssnOk | 4 | Successful completions |
| nMssnF | 1 | Failed missions |
| aMssnM | 41 | Average mission duration (min) |

### Error & Stuck History
| Field | Value | Meaning |
|-------|-------|---------|
| nStuck | 7 | Total stuck events lifetime |
| nPanics | 33 | Total navigation panics |
| nCliffsF | 531 | Cliff sensor triggers (front) |
| nCBump | 0 | Bumper collisions |

### Battery Health
| Field | Value | Meaning |
|-------|-------|---------|
| batPct | 36% | Charge at capture time |
| estCap | 1859 | Estimated capacity (mAh) |
| nAvail | 117 | Charge cycles remaining |
| nChgOk | 88 | Successful charges lifetime |
| cCount | 9 | Battery charge count |

### Hardware
| Field | Value | Meaning |
|-------|-------|---------|
| tankLvl | 100% | Water tank at capture |
| detectedPad | invalid | No pad attached at capture |
| imuPartNo | BMI055 | IMU sensor model |

---

## Notable Pre-existing Conditions

- **531 cliff sensor triggers** — high count suggesting frequent edge detection
or prior use near stairs/drops. Worth monitoring during dock return tests.
- **33 navigation panics** — indicates this robot has encountered significant
navigation difficulty in its lifetime. Baseline for comparison against our runs.
- **7 stuck events** — robot has a history of getting stuck. Relevant context
for obstacle handling tests.
- **4/10 mission success rate** — only 4 of 10 lifetime missions completed
successfully before our testing began.