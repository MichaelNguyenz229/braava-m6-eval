# Braava M6 Behavioral Evaluation

A systematic QA evaluation framework for the iRobot Braava Jet M6 (6110) robot mop.
Applies structured testing methodology to a physical robot — defining expected behavior,
logging real data via the robot's local MQTT API, and analyzing results across repeated runs.

## Why This Project

Physical AI systems require the same rigorous behavioral evaluation as software. This
project treats the M6 as a system under test — not just a consumer device — and builds
tooling to evaluate it systematically using the same QA principles applied to software:
expected vs actual behavior, pass/fail criteria, and failure mode analysis.

## Test Environment

- Dead-end hallway (~25ft) with dock in adjacent living room
- Kitchen with real-world obstacles — chair legs, bins, boxes
- Mixed hardwood and tile surfaces
- No pre-existing map — robot builds from scratch on first run

## Test Cases

See [test_plan.md](test_plan.md) for full test case documentation.

| ID | Test | Type | Priority |
|----|------|------|----------|
| TEST-001 | Dock Return Reliability | Automated + Observation | High |
| TEST-002 | Coverage Consistency | Automated | High |
| TEST-003 | Obstacle Handling | Manual Observation | Medium |

## How It Works

The M6 exposes its state locally over MQTT via a protocol reverse engineered by the
community. This project uses `roombapy` to connect directly over WiFi, poll robot
state in real time during cleaning missions, and log structured JSON data for analysis.

No cloud connection required — everything runs locally on your home network.

## Project Structure
```
braava-m6-eval/
├── connect.py           # connection test — verify credentials work
├── collect_state.py     # logs robot state during a live cleaning run
├── analyze_results.py   # parses logs and generates summary report
├── test_plan.md         # formal test cases with pass/fail criteria
├── push.sh              # git workflow automation
├── data/runs/           # timestamped JSON logs per run (gitignored)
├── results/             # aggregated CSV results (gitignored)
└── requirements.txt
```

## Setup
```bash
git clone https://github.com/MichaelNguyenz229/braava-m6-eval.git
cd braava-m6-eval

python3 -m venv venv            # If on Mac/Linux
source venv/bin/activate      

# python -m venv venv           # If on Windows
# source venv/Scripts/activate  

pip install -r requirements.txt
```

Create a `.env` file with your robot credentials:
```
ROBOT_IP=192.168.X.X
BLID=your_blid
PASSWORD=your_password
```

Run the connection test:
```bash
python connect.py
```

## Status

🔄 In progress — robot arriving soon, active data collection pending

## Author

Michael Nguyen