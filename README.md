# Braava M6 Behavioral Evaluation

A QA evaluation framework for the iRobot Braava Jet M6 (6110) robot mop.
Connects directly to the robot over local MQTT, polls state in real time during
cleaning missions, and logs structured data for systematic behavioral analysis.

## Why This Project

Physical AI systems need the same rigorous evaluation as software. This project
treats the M6 as a system under test — defining expected behavior, logging real
data, and analyzing results across repeated runs using standard QA methodology.

## How It Works

The M6 exposes its state locally over MQTT. This project uses `roombapy` to
connect directly over WiFi and poll the robot's full state
every 5 seconds during live missions.

## In Action

**On dock, awaiting mission:**
![Robot on dock](images/doc-station.jpg)

**Mapping freely during first run:**
![Robot mapping](images/free-map.jpg)

**Wall interaction during navigation:**
![Wall collision](images/wall-collision.jpg)

## Test Cases

See [docs/test_plan.md](docs/test_plan.md) for full documentation.

| ID | Test | Priority |
|----|------|----------|
| TEST-001 | Dock Return Reliability | High |
| TEST-002 | Coverage Consistency | High |
| TEST-003 | Obstacle Handling | Medium |
| TEST-004 | Cliff Sensor Validation | High |
| TEST-005 | Bumper Collision Detection | Medium |

## Project Structure
```
braava-m6-eval/
├── scripts/
│   ├── connect.py            # verify connection and credentials
│   ├── collect_state.py      # poll and log state during live run
│   ├── snapshot_profile.py   # capture robot baseline stats
│   └── analyze_results.py    # parse logs and generate summary
├── docs/
│   ├── test_plan.md
│   ├── initial_robot_profile.md
│   └── robot_profile.md
├── data/runs/                # JSON logs per run (gitignored)
├── results/                  # aggregated CSVs (gitignored)
├── requirements.txt
└── .env                      # credentials — never committed
```

## Setup
```bash
git clone https://github.com/MichaelNguyenz229/braava-m6-eval.git
cd braava-m6-eval
python -m venv venv
source venv/Scripts/activate  # Windows
# source venv/bin/activate    # Mac/Linux
pip install -r requirements.txt
```

Create `.env` with your robot credentials:
```
ROBOT_IP=192.168.X.X
BLID=your_blid
PASSWORD=your_password
```
```bash
python scripts/connect.py
```

## Status

 Active — data collection in progress

## Author

Michael Nguyen