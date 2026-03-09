# Robot Profile — Current State

Last updated: 2026-03-08
Run `python snapshot_profile.py` to refresh.

---

## Device Info
| Field | Value |
|-------|-------|
| Name | RoboMop |
| SKU | m611220 |
| Firmware | sanmarino+22.29.6+2022-12-01-82f3372a65c+Firmware-Build+2321 |
| IMU | BMI055 |

---

## Mission History
| Field | Value | Meaning |
|-------|-------|---------|
| nMssn | 10 | Total missions lifetime |
| nMssnOk | 4 | Successful completions |
| nMssnF | 1 | Failed missions |
| aMssnM | 41 min | Average mission duration |
| aCycleM | 18 min | Average cycle time |

---

## Error & Stuck History
| Field | Value | Meaning |
|-------|-------|---------|
| nStuck | 7 | Total stuck events |
| nPanics | 33 | Navigation panics |
| nCliffsF | 531 | Cliff sensor triggers (front) |
| nCliffsR | 0 | Cliff sensor triggers (rear) |
| nCBump | 0 | Bumper collisions |
| nWStll | 1 | Wheel stalls |
| nOvertemps | 0 | Overheating events |

---

## Battery Health
| Field | Value | Meaning |
|-------|-------|---------|
| batPct | 99% | Current charge |
| estCap | 1859 mAh | Estimated capacity |
| nAvail | 117 | Charge cycles remaining |
| nChgOk | 88 | Successful charges lifetime |
| cCount | 9 | Battery charge count |
| Manufacturer | Panasonic | Battery brand |
| Manufacture date | 2022-6-22 | Battery age |

---

## Runtime Stats
| Field | Value | Meaning |
|-------|-------|---------|
| sqft | 3 | Total sqft cleaned lifetime |
| hr | 4 | Total hours runtime |
| min | 37 | Total minutes runtime |

---

## Hardware
| Field | Value |
|-------|-------|
| Tank level | 100% |
| Tank present | True |
| Pad detected | invalid |
| Lid open | False |