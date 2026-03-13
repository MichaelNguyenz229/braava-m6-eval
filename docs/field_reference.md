# Braava M6 — Field Reference

Raw state blob documented from iRobot Braava Jet M6 (6110), firmware `sanmarino+22.29.6`.
Fields are broadcast over local MQTT via roombapy. iRobot does not publish official documentation
for this data — this reference is based on observed behavior during testing.

**Columns:**
- **Locally updated** — whether the field updates in real time over local MQTT during a mission
- **Useful for testing** — whether it's worth logging in collect_state.py

---

## Battery

| Field | Description | Locally updated | Useful for testing |
|-------|-------------|-----------------|-------------------|
| `batPct` | Battery percentage 0-100 | ✅ Yes | ✅ Yes — track drain per run |
| `batteryType` | Internal battery part number | ❌ Static | ❌ No |
| `batAuthEnable` | Battery authentication flag | ❌ Null on M6 | ❌ No |

### batInfo
Battery hardware metadata. Static — does not change during testing.

| Field | Description |
|-------|-------------|
| `mDate` | Battery manufacture date |
| `mName` | Battery manufacturer (Panasonic) |
| `mDaySerial` | Manufacturing day serial |
| `mData` | Raw hex manufacturing data |
| `mLife` | Raw hex battery life data |
| `cCount` | Charge cycle count |
| `afCount` | Abnormal failure count |

### bbchg — Charging behavior counters
Lifetime charging stats. Do not update during missions.

| Field | Description |
|-------|-------------|
| `nChatters` | Number of charging contact chatters |
| `nKnockoffs` | Number of times knocked off dock |
| `nLithF` | Lithium battery failures |
| `nChgOk` | Successful charge sessions |
| `aborts` | Charge abort event counts |
| `chgErr` | Charge error counts by type |
| `smberr` | SMB protocol errors |
| `nChgErr` | Total charge errors |

### bbchg3 — Battery capacity stats
| Field | Description | Locally updated |
|-------|-------------|-----------------|
| `estCap` | Estimated battery capacity in mAh | ❌ Static |
| `nAvail` | Number of availability checks | ❌ Static |
| `hOnDock` | Lifetime hours spent on dock | ❌ Static |
| `avgMin` | Average mission duration in minutes | ❌ Static |

---

## Mission Stats

### bbmssn — Lifetime mission counters
| Field | Description |
|-------|-------------|
| `nMssn` | Total missions attempted |
| `nMssnOk` | Successful missions |
| `nMssnF` | Failed missions |
| `nMssnC` | Cancelled missions |
| `aMssnM` | Average mission duration (minutes) |
| `aCycleM` | Average cycle duration (minutes) |

### cleanMissionStatus — Current mission state
**Most useful object for real-time monitoring.**

| Field | Description | Locally updated | Useful for testing |
|-------|-------------|-----------------|-------------------|
| `phase` | Current phase: `charge`, `run`, `hmPostMsn`, `stop` | ✅ Yes | ✅ Yes — primary state tracker |
| `cycle` | Mission type: `none`, `clean`, `spot` | ✅ Yes | ✅ Yes |
| `error` | Error code, 0 = no error | ✅ Yes | ✅ Yes |
| `notReady` | Not-ready code, 0 = ready | ✅ Yes | ✅ Yes — 39 = docking transient |
| `mssnM` | Mission elapsed minutes | ⚠️ Infrequent | ⚠️ Unreliable |
| `expireM` | Minutes until mission expires | ❌ Static | ❌ No |
| `rechrgM` | Minutes until recharge needed | ❌ Static | ❌ No |
| `mssnStrtTm` | Mission start Unix timestamp | ✅ Yes | ⚠️ Use phase transitions instead |
| `operatingMode` | Current operating mode | ✅ Yes | ❌ No |
| `initiator` | What started the mission (`localApp`, `schedule`) | ✅ Yes | ❌ No |
| `nMssn` | Total mission count (increments each run) | ✅ Yes | ❌ No |
| `missionId` | Unique ID per mission | ✅ Yes | ❌ No |
| `condNotReady` | Conditions causing not-ready state | ✅ Yes | ❌ No |

### runtimeStats — Cumulative runtime
| Field | Description | Locally updated | Useful for testing |
|-------|-------------|-----------------|-------------------|
| `sqft` | Lifetime square feet cleaned | ❌ Cloud-synced only | ❌ No — never updates locally |
| `min` | Lifetime minutes of cleaning | ❌ Cloud-synced only | ❌ No |
| `hr` | Lifetime hours of cleaning | ❌ Cloud-synced only | ❌ No |

---

## Navigation & Safety Counters

### bbrun — Lifetime run event counters
**Most useful for safety and behavioral testing.**

| Field | Description | Locally updated | Useful for testing |
|-------|-------------|-----------------|-------------------|
| `nCliffsF` | Front cliff sensor triggers | ✅ Yes | ✅ Yes — TEST-004 |
| `nCliffsR` | Rear cliff sensor triggers | ✅ Yes | ✅ Yes — TEST-004 |
| `nPanics` | Navigation panic events | ✅ Yes | ✅ Yes — TEST-003, 005 |
| `nStuck` | Times robot got stuck | ✅ Yes | ✅ Yes — TEST-003 |
| `nCBump` | Bumper contact events | ✅ Yes | ✅ Yes — TEST-005 |
| `nPicks` | Times robot was picked up | ✅ Yes | ⚠️ Informational |
| `nWStll` | Wheel stall events | ✅ Yes | ⚠️ Informational |
| `nOvertemps` | Overtemperature events | ✅ Yes | ❌ No |

**Note:** `nCBump = 0` despite 47 nPanics and 9 nStuck events. Hypothesis: M6 routes
physical collisions through panic handler rather than bumper counter. Under investigation in TEST-005.

### bbswitch — Physical button press counters
Lifetime counts of physical button activations. Not useful for testing.

| Field | Description |
|-------|-------------|
| `nBumper` | Total bumper activations (physical switch, not counter) |
| `nDrops` | Wheel drop events |
| `nDock` | Dock button presses |
| `nSpot` | Spot clean button presses |
| `nClean` | Clean button presses |

**Note:** `nBumper` at 1,406,546 is extremely high — this is a raw hardware switch
activation count, not the same as `nCBump`. Every time the bumper physically flexes
and returns it counts. This is normal for a mopping robot navigating walls.

### bbnav — Navigation system stats
| Field | Description |
|-------|-------------|
| `nGoodLmrks` | Number of good visual landmarks in current map |
| `aMtrack` | Average map tracking quality |
| `aGain` | Average camera gain |
| `aExpo` | Average camera exposure |

### bbrstinfo — System reset counters
| Field | Description |
|-------|-------------|
| `nNavRst` | Navigation system resets |
| `nMapLoadRst` | Map load resets |
| `nMobRst` | Mobile system resets |
| `nSafRst` | Safety system resets |
| `safCauses` | Safety reset cause codes |

### mssnNavStats — Current mission navigation stats
Updates during active mission.

| Field | Description | Locally updated |
|-------|-------------|-----------------|
| `gLmk` | Global landmarks detected | ✅ Yes |
| `lmk` | Local landmarks detected | ✅ Yes |
| `reLc` | Relocalization events | ✅ Yes |
| `plnErr` | Path planning error status | ✅ Yes |
| `mpSt` | Map processing state (`idle`, `active`) | ✅ Yes |
| `mTrk` | Map tracking status | ✅ Yes |

---

## Hardware & Sensors

### detectedPad — Mop pad state
| Value | Meaning |
|-------|---------|
| `invalid` | No mop pad attached |
| `reusableWet` | Reusable pad attached and wet |
| `reusableDry` | Reusable pad attached and dry |
| `disposable` | Disposable pad attached |

### padWetness — Pad wetness settings
| Field | Description |
|-------|-------------|
| `disposable` | Wetness level setting for disposable pads (1-3) |
| `reusable` | Wetness level setting for reusable pads (1-3) |

| Field | Description | Locally updated | Useful for testing |
|-------|-------------|-----------------|-------------------|
| `tankLvl` | Water tank level 0-100 | ❌ Never updates locally | ❌ No |
| `tankPresent` | Whether tank is installed | ✅ Yes | ❌ No |
| `lidOpen` | Whether lid is open | ✅ Yes | ❌ No |

### reflexSettings
| Field | Description |
|-------|-------------|
| `rlWheelDrop.enabled` | Whether wheel drop reflex is enabled (0 = disabled on M6) |

---

## Network & Connectivity

### signal — WiFi signal quality
| Field | Description | Locally updated | Useful for testing |
|-------|-------------|-----------------|-------------------|
| `rssi` | Signal strength in dBm (higher = stronger, e.g. -50 is good) | ✅ Yes | ✅ Yes — diagnose connection drops |
| `snr` | Signal to noise ratio in dB | ✅ Yes | ⚠️ Informational |
| `noise` | Noise floor in dBm | ✅ Yes | ⚠️ Informational |

### netinfo — Network configuration
Static network info. Not useful for testing.

| Field | Description |
|-------|-------------|
| `addr` | Robot IP address |
| `mask` | Subnet mask |
| `gw` | Gateway IP |
| `dns1/dns2` | DNS servers |
| `bssid` | Router MAC address |
| `dhcp` | Whether DHCP is enabled |
| `sec` | WiFi security type |

### wifistat — Cloud connection status
| Field | Description |
|-------|-------------|
| `cloud` | Cloud connection state |
| `wifi` | WiFi connection state |
| `uap` | Whether in AP mode |

### wlcfg — WiFi config
| Field | Description |
|-------|-------------|
| `sec` | Security type |
| `ssid` | Network SSID (hex encoded) |

---

## Maps & Spatial Data

| Field | Description | Locally updated |
|-------|-------------|-----------------|
| `pmaps` | List of saved persistent maps with IDs | ❌ Static |
| `pmapCL` | Persistent map cloud learning enabled | ❌ Static |
| `pmapSGen` | Persistent map generation number | ❌ Static |
| `pmapLearningAllowed` | Whether map learning is enabled | ❌ Static |
| `mapUploadAllowed` | Whether map upload to cloud is allowed | ❌ Static |
| `rankOverlap` | Map overlap ranking percentage | ❌ Static |

**Note:** Position data (x/y coordinates, robot pose) is NOT available over local MQTT on the M6.
The robot builds its map using vSLAM internally and sends spatial data directly to iRobot's cloud.
This data never appears in the local MQTT stream. `pose` fields return null throughout all missions.

### missionTelemetry — Cloud telemetry flags
Flags indicating which telemetry streams are being sent to iRobot's cloud during missions.
All fields set to 1 = enabled. Includes vslam_report, coverage_report, map_save, sensor_stats, etc.
Not useful for local testing but confirms what data iRobot collects.

---

## Device Identity & Firmware

| Field | Description |
|-------|-------------|
| `name` | Robot name ("RoboMop") |
| `sku` | Product SKU (m611220 = Braava Jet M6) |
| `softwareVer` | Full firmware version string |
| `cloudEnv` | Cloud environment (`prod`) |
| `country` | Registered country |
| `timezone` | Configured timezone |
| `connected` | Whether robot is connected to cloud |

### subModSwVer — Subsystem firmware versions
| Field | Description |
|-------|-------------|
| `nav` | Navigation subsystem version |
| `mob` | Mobile platform version |
| `pwr` | Power management version |
| `sft` | Safety subsystem version |
| `mobBtl` | Mobile bootloader version |
| `linux` | Linux kernel version |
| `con` | Connectivity module version |

### hwPartsRev — Hardware revision info
| Field | Description |
|-------|-------------|
| `mobBrd` | Motherboard revision |
| `imuPartNo` | IMU chip part number (BMI055) |
| `lrDrv` | Left/right drive chip |
| `navSerialNo` | Navigation board serial |
| `wlan0HwAddr` | WiFi MAC address |

### cap — Device capability flags
Bitmask of features supported by this firmware/hardware combination.
| Field | Description |
|-------|-------------|
| `maps` | Number of maps supported |
| `pmaps` | Number of persistent maps supported |
| `pose` | Pose capability level (2 = supported in cloud, not local) |
| `multiPass` | Multi-pass cleaning support |
| `eco` | Eco mode support |
| `5ghz` | 5GHz WiFi support |
| `area` | Area targeting support |

---

## Miscellaneous

| Field | Description | Useful for testing |
|-------|-------------|-------------------|
| `bbpause.pauses` | Pause event counts by type | ❌ No |
| `bbsys` | Total system uptime in hours/minutes | ❌ No |
| `cleanSchedule2` | Scheduled cleaning times | ❌ No |
| `schedHold` | Whether schedule is on hold | ❌ No |
| `twoPass` | Whether two-pass cleaning is enabled | ❌ No |
| `noAutoPasses` | Whether auto-passes are disabled | ❌ No |
| `ecoCharge` | Whether eco charging is enabled | ❌ No |
| `childLock` | Whether child lock is on | ❌ No |
| `deploymentState` | Deployment state flag | ❌ No |
| `lastCommand` | Last command sent to robot | ⚠️ Informational |
| `lastDisconnect` | Last disconnect reason code | ⚠️ Informational |
| `dock.known` | Whether dock position is known | ❌ No |
| `featureFlags` | Feature flag overrides | ❌ No |
| `secureBoot` | Secure boot configuration | ❌ No |
| `tls` | TLS security configuration | ❌ No |
| `sceneRecog` | Scene recognition (null on M6) | ❌ No |
| `behaviorFwk` | Behavior framework (null on M6) | ❌ No |
| `openOnly` | Open-area only mode | ❌ No |

---

## Fields Used in collect_state.py

| Test | Fields |
|------|--------|
| TEST-002 | `phase`, `cycle`, `batPct`, `signal` |
| TEST-003 | `phase`, `cycle`, `error`, `mssnM`, `batPct`, `nStuck`, `nPanics` |
| TEST-004 | `phase`, `error`, `nCliffsF`, `nCliffsR`, `nPanics` |
| TEST-005 | `phase`, `error`, `nCBump`, `nPanics`, `nStuck` |
